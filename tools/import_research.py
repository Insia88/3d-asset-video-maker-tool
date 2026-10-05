#!/usr/bin/env python3
"""Export an audited local 3D research library without copying original media."""
from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
import tempfile
from collections import Counter
from datetime import date, datetime, timezone
from pathlib import Path
from urllib.parse import quote, urlsplit

from validate_library import (
    LOCAL_EVIDENCE, LOCAL_PATH_RE, MAX_SHARD_BYTES, MAX_SHARD_ROWS, PRIVATE_CONTEXT_RE, PRIVATE_KEY_RE,
    SCHEMA_VERSION, SHA256_RE, SLUG_RE, WITHHELD, decode_reference,
    digest_bytes, inline_links, markdown_destinations, privacy_findings, safe_public_url,
    split_destination, validate_library,
)

NUMBERED_MD_RE = re.compile(r"^\d+[A-Za-z]*[_-].+\.md$", re.I)
ARTIFACT_KEY_RE = re.compile(
    r"^(?:local_.+|canonical_evidence|evidence_board|evidence_path|"
    r"evidence_file|evidence_contact_sheets?|evidence_original_still|"
    r"contact_sheet(?:s|_paths)?|source_path|metadata_evidence_path|"
    r"model_evidence_file|individual_asset_sheet)$", re.I
)
ARTIFACT_VALUE_RE = re.compile(r"^(?:evidence[/\\]|(?:\.?\.?[/\\])?(?:frames|boundary_pairs|motion_sheets)[/\\])", re.I)
MODEL_KEYS = {"model", "verified_generation_model", "model_evidence", "model_evidence_url", "model_observation", "model_observation_basis", "model_source", "model_source_url", "model_provenance", "model_association_precision", "model_gallery_label", "model_dimensions_display", "verified_native_tools", "actual_mesh_verified"}
PROVENANCE_KEYS = {"ai_provenance", "generative_provenance", "generative_provenance_sources", "generative_status", "source_ai_provenance", "source_native_cg_provenance", "source_production_claim", "primary_provenance_evidence", "primary_creator_sources", "provenance_verification_level", "provenance_observation", "provenance_url", "source_provenance_band", "public_process_claim", "official_ai_generated", "source_license", "license_claim", "rights_note", "source_use"}


class ExportError(ValueError):
    pass


class Sanitizer:
    """Preserve research statements while replacing private/local artifacts."""
    def __init__(self):
        self.stats = Counter()

    def string(self, value: str) -> str:
        decoded = decode_reference(value)
        if value.startswith(("http://", "https://")) and not re.search(r"\s", value) and not safe_public_url(value):
            self.stats["private_links_withheld"] += 1
            return WITHHELD
        if value.startswith(("data:", "plugin://", "codex://")):
            self.stats["private_payloads_withheld"] += 1
            return WITHHELD
        if ARTIFACT_VALUE_RE.match(decoded):
            self.stats["local_artifacts_replaced"] += 1
            return LOCAL_EVIDENCE
        if LOCAL_PATH_RE.search(decoded):
            self.stats["local_artifacts_replaced"] += 1
            value = LOCAL_PATH_RE.sub(LOCAL_EVIDENCE, decoded)
        if PRIVATE_CONTEXT_RE.search(value):
            self.stats["private_contexts_replaced"] += 1
            value = PRIVATE_CONTEXT_RE.sub(WITHHELD, value)
        def public_link(match):
            url = match.group(0)
            trimmed = url.rstrip(").,;")
            suffix = url[len(trimmed):]
            if safe_public_url(trimmed):
                return url
            self.stats["private_links_withheld"] += 1
            return WITHHELD + suffix
        value = re.sub(r"https?://[^\s<>\"']+", public_link, value)
        if re.search(r"(?:data:[^\s,]*;base64,|codex-remote-attachments|\.cache[/\\]codex)", value, re.I):
            self.stats["private_payloads_withheld"] += 1
            return WITHHELD
        return value

    def value(self, value, key: str = ""):
        if isinstance(value, dict):
            result = {}
            for child_key, child in value.items():
                child_key = str(child_key)
                if PRIVATE_KEY_RE.fullmatch(child_key):
                    self.stats["private_fields_removed"] += 1
                    continue
                safe_key = self.string(child_key)
                if safe_key in result:
                    raise ExportError("Sanitized keys collide; inspect the source record.")
                result[safe_key] = self.value(child, child_key)
            return result
        if isinstance(value, list):
            return [self.value(item, key) for item in value]
        if isinstance(value, str):
            if ARTIFACT_KEY_RE.fullmatch(key) and value and not safe_public_url(value):
                self.stats["local_artifacts_replaced"] += 1
                return LOCAL_EVIDENCE
            return self.string(value)
        if isinstance(value, float) and not math.isfinite(value):
            raise ExportError("Nonfinite numbers cannot be exported as portable JSON.")
        if value is None or isinstance(value, (bool, int, float)):
            return value
        raise ExportError("Unsupported source value type.")


def first_value(record: dict, keys: tuple[str, ...], default=None):
    for key in keys:
        value = record.get(key)
        if value is not None and value != "" and value != [] and value != {}:
            return value
    return default


def select_fields(record: dict, keys) -> dict:
    return {key: record[key] for key in sorted(keys) if key in record}


def collect_urls(value, trail: str = "") -> list[dict]:
    found = []
    if isinstance(value, dict):
        for key, item in value.items():
            found.extend(collect_urls(item, f"{trail}.{key}" if trail else str(key)))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            found.extend(collect_urls(item, f"{trail}[{index}]"))
    elif isinstance(value, str) and safe_public_url(value):
        found.append({"field": trail, "url": value})
    return found


def collect_hashes(value, trail: str = "") -> list[dict]:
    hashes = []
    if isinstance(value, dict):
        for key, item in value.items():
            child_trail = f"{trail}.{key}" if trail else str(key)
            if "sha256" in str(key).lower() and isinstance(item, str) and SHA256_RE.fullmatch(item):
                hashes.append({"field": child_trail, "value": item})
            else:
                hashes.extend(collect_hashes(item, child_trail))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            hashes.extend(collect_hashes(item, f"{trail}[{index}]"))
    return hashes


def has_recorded_evidence(record: dict) -> bool:
    return any(record.get(key) for key in (
        "canonical_evidence", "evidence", "evidence_contact_sheet", "evidence_contact_sheets",
        "evidence_board", "contact_sheet", "contact_sheets", "contact_sheet_paths",
        "evidence_path", "evidence_original_still", "observed_frames", "observed_samples",
        "local_image", "local_asset", "local_detail_image", "individual_asset_sheet",
    ))


def normalize_record(record: dict, sanitizer: Sanitizer) -> dict:
    identifier = record.get("canonical_shot_id")
    if not isinstance(identifier, str) or not identifier.strip():
        raise ExportError("An eligible row has no canonical_shot_id.")
    if record.get("canonical_class") != "core3D":
        raise ExportError(f"Eligible row {identifier} is not classified as pure core3D.")
    if any(record.get(k) for k in ("duplicate_of", "exact_clip_duplicate_of")):
        raise ExportError(f"Eligible row {identifier} still points to a duplicate representative.")
    if not has_recorded_evidence(record):
        raise ExportError(f"Eligible row {identifier} has no recorded observation evidence.")
    if record.get("reviewed") is False or record.get("observation_complete") is False:
        raise ExportError(f"Eligible row {identifier} contradicts its observation completion flag.")
    for key in ("observation_status", "observation_level", "analysis_status"):
        status = str(record.get(key, "")).lower()
        if "metadata_only" in status or status in {"unobserved", "pending", "not_reviewed", "downloaded_only"}:
            raise ExportError(f"Eligible row {identifier} is marked as unobserved metadata.")
    clean = sanitizer.value(record)
    start = first_value(clean, ("start_seconds", "time_start"))
    end = first_value(clean, ("end_seconds", "time_end"))
    original_unit = first_value(clean, ("unit_type", "media_kind", "reference_unit", "unit"), "")
    if isinstance(start, (int, float)) and not isinstance(start, bool) and isinstance(end, (int, float)) and not isinstance(end, bool):
        if start < 0 or end < start:
            raise ExportError(f"Invalid time range in {identifier}.")
        unit_type = "video_scene"
    elif re.search(r"still|image|design|sheet|render", str(original_unit), re.I) or any(clean.get(k) for k in ("image_url", "source_image_url", "original_image_url", "public_image_url", "preview_url", "local_image", "local_asset")):
        unit_type = "still_image"
    else:
        unit_type = "reference_unit_unspecified"
    urls = collect_urls(clean)
    source_note = str(first_value(clean, ("generative_provenance", "ai_provenance", "source_ai_provenance"), ""))
    url_status = "public_urls_recorded" if urls else (
        "user_provided_local_reference" if re.search(r"user local reference|사용자 제공", source_note, re.I)
        else "no_public_source_url_in_record"
    )
    description = first_value(clean, ("visual_description", "composition", "visual_observation", "visual_family", "detail_observation"))
    if not description:
        raise ExportError(f"Eligible row {identifier} has no actual visual description.")
    cross_keys = {key for key in clean if "cross" in key.lower() or key in {"variant_comparison", "variant_observation_status", "variant_peer", "variant_relation", "same_model_variation_rule", "curation_representative_rule", "design_family_note"}}
    return {
        "schema_version": SCHEMA_VERSION,
        "reference_id": identifier,
        "source_id": first_value(clean, ("canonical_source_id", "source_id", "video_id")),
        "class": "core3D",
        "count_eligible": True,
        "unit_type": unit_type,
        "source": {
            "title": first_value(clean, ("source_title", "title", "source_name", "name", "original_title")),
            "creator": clean.get("creator"), "urls": urls, "public_url_status": url_status,
            "dates": select_fields(clean, {key for key in clean if "date" in key.lower()}),
        },
        "observation": {
            "status": first_value(clean, ("observation_status", "analysis_status", "detail_observation_status")),
            "level": clean.get("observation_level"),
            "basis": first_value(clean, ("observation_basis", "basis", "sampling_method", "scope_3d_review_basis")),
            "has_recorded_evidence": True,
            "local_evidence_label": LOCAL_EVIDENCE,
            "original_media_redistributed": False,
            "timing": {"start_seconds": start, "end_seconds": end,
                       "boundary_basis": first_value(clean, ("boundary_basis", "boundary_precision", "boundary_type")),
                       "time_range_kind": clean.get("time_range_kind")},
            "details": select_fields(clean, {key for key in clean if key.startswith("observed_") or key in {"audio_observed", "motion_observed", "motion_observation", "fast_intermediate_cuts_verified", "full_timeline_sample_coverage", "observation_complete", "observation_status", "observation_level", "observation_basis", "detail_observation", "detail_observation_status", "additional_direct_UI_observation"}}),
        },
        "visual": {
            "description": description,
            "composition": clean.get("composition"),
            "materials": first_value(clean, ("materials", "material", "material_lighting", "materials_composition_change")),
            "palette": clean.get("palette"),
            "aesthetic_reason": first_value(clean, ("aesthetic_reason", "aesthetic")),
            "cute_reason": clean.get("cute_reason"),
            "camera_or_change": first_value(clean, ("camera_or_change", "camera_assessment", "motion")),
        },
        "application": select_fields(clean, {"beauty_relevance", "beauty_etf_application", "ETF_application", "etf_translation", "narrative_role", "role", "higgsfield_application", "higgsfield_proposal", "higgsfield_difficulty", "suggested_motion", "beauty_application_basis"}),
        "provenance": {
            "claims": select_fields(clean, PROVENANCE_KEYS),
            "model_and_native_tool_evidence": select_fields(clean, MODEL_KEYS),
            "cross_review": select_fields(clean, cross_keys),
            "verification_policy": "Original individual verification claims are preserved. The importer does not infer a model, editable mesh, AI origin or motion from appearance.",
        },
        "hashes": collect_hashes(clean),
        "lineage": {"ledger_file": str(clean.get("ledger_file", "unknown")), "ledger_line": clean.get("ledger_line")},
        "source_record": clean,
    }


def path_key(path: Path) -> str:
    return str(path.resolve()).replace("\\", "/").casefold()


def portable_link(origin: Path, target: Path) -> str:
    relative = os.path.relpath(target, origin.parent).replace("\\", "/")
    return quote(relative, safe="/._-~")


def normalize_markdown_lines(text: str) -> str:
    """Use LF and one EOF newline; keep meaningful two-space hard breaks."""
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    normalized, fence = [], None
    for line in lines:
        stripped = line.rstrip(" \t")
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        in_code = fence is not None or line.startswith(("    ", "\t"))
        if marker:
            chars, suffix = marker.groups()
            if fence is None:
                fence = (chars[0], len(chars))
            elif chars[0] == fence[0] and len(chars) >= fence[1] and not suffix.strip():
                fence = None
            in_code = True
        if stripped and not in_code and re.search(r" {2,}$", line) and not re.search(r"<br\s*/?>$", stripped, re.I):
            stripped += "<br>"
        normalized.append(stripped)
    return "\n".join(normalized).rstrip("\n") + "\n"


def select_reference_index_documents(source: Path):
    """Use the live integrated index, never silently import old partial indices."""
    directory = source / "reference-index"
    if not directory.is_dir():
        return [], {"method": "no_reference_index_directory", "selected_documents": [], "unlinked_markdown_omitted": 0}
    all_documents = sorted(path for path in directory.rglob("*.md") if path.is_file())
    driver = source / "36_3D_고유참고_통합색인.md"
    if not driver.is_file():
        for path in all_documents:
            if not path.resolve().is_relative_to(directory.resolve()):
                raise ExportError("A fallback reference-index document resolves outside its source directory.")
        return all_documents, {
            "method": "all_reference_index_markdown_fallback", "driver": None,
            "fallback_reason": "The project has no current 36 integrated-index document.",
            "selected_documents": [path.relative_to(source).as_posix() for path in all_documents],
            "unlinked_markdown_omitted": 0,
        }
    driver_bytes = driver.read_bytes()
    selected, seen = [], set()
    for raw in markdown_destinations(driver_bytes.decode("utf-8-sig")):
        decoded = decode_reference(raw).strip()
        if decoded.startswith(("http:", "https:", "#", "mailto:", "plugin:", "codex:")):
            continue
        if decoded.startswith("file://"):
            decoded = decoded[7:]
        decoded = re.sub(r"(\.md):\d+$", r"\1", decoded.split("#", 1)[0].split("?", 1)[0], flags=re.I)
        candidate = Path(decoded.replace("\\", "/"))
        if not candidate.is_absolute():
            candidate = driver.parent / candidate
        resolved = candidate.resolve()
        if not resolved.is_relative_to(directory.resolve()):
            if "reference-index" in decoded.replace("\\", "/").split("/"):
                raise ExportError("The current integrated index links outside the source reference-index directory.")
            continue
        if resolved.suffix.lower() != ".md":
            continue
        if not resolved.is_file():
            raise ExportError("The current integrated index links a missing reference-index Markdown document.")
        identity = path_key(resolved)
        if identity not in seen:
            seen.add(identity)
            selected.append(resolved)
    if not selected:
        raise ExportError("The current integrated index has no linked reference-index Markdown documents; refresh it before exporting.")
    return selected, {
        "method": "linked_from_current_integrated_index", "driver": driver.name,
        "driver_sha256": digest_bytes(driver_bytes),
        "selected_documents": [path.relative_to(source).as_posix() for path in selected],
        "unlinked_markdown_omitted": len(all_documents) - len(selected),
    }


def stale_managed_file_report(root: Path, snapshot: dict, project: str, new_paths: set[str], docs_directory: str) -> dict:
    """Report cleanup candidates only; never delete a managed or shared file."""
    projects = snapshot.get("projects", {})
    previous = projects.get(project, {})
    other_owned = {item.get("path") for name, entry in projects.items() if name != project and isinstance(entry, dict)
                   for item in entry.get("files", []) if isinstance(item, dict)}
    stale, shared, historical, unsafe = [], [], [], 0
    for item in previous.get("files", []) if isinstance(previous, dict) else []:
        if not isinstance(item, dict) or not isinstance(item.get("path"), str):
            continue
        rel = item["path"]
        if rel in new_paths:
            continue
        if "\\" in rel or rel.startswith("/") or ".." in rel.split("/"):
            unsafe += 1
            continue
        if rel in other_owned:
            shared.append(rel)
            continue
        owned_data = rel.startswith(f"data/projects/{project}/")
        owned_current_doc = rel.startswith(docs_directory + "/") and rel.endswith(".md")
        if not owned_data and not owned_current_doc:
            historical.append(rel)
            continue
        candidate = (root / rel).resolve()
        if not candidate.is_relative_to(root):
            unsafe += 1
            continue
        if not candidate.is_file():
            state = "already_missing"
        elif digest_bytes(candidate.read_bytes()) == item.get("sha256"):
            state = "unchanged_since_previous_snapshot"
        else:
            state = "modified_since_previous_snapshot_preserve_for_review"
        stale.append({"path": rel, "previous_sha256": item.get("sha256"), "status": state,
                      "removal_candidate": state == "unchanged_since_previous_snapshot"})
    return {"mode": "report_only_no_deletion", "stale_files": stale,
            "shared_files_preserved": sorted(shared), "historical_files_preserved": sorted(historical),
            "unsafe_previous_paths_ignored": unsafe}


def rewrite_markdown(text: str, source_file: Path, output_file: Path, document_map: dict[str, Path], references_file: Path, sanitizer: Sanitizer, *, audit_file: Path, snapshot_file: Path) -> str:
    def destination(raw: str) -> str | None:
        decoded = decode_reference(raw).strip()
        if decoded.startswith("#"):
            return decoded
        if safe_public_url(decoded):
            return decoded
        if decoded.startswith(("http:", "https:", "data:", "plugin:", "codex:", "mailto:")):
            return None
        if decoded.startswith("file://"):
            decoded = decoded[7:]
        # Local file links sometimes include an editor line suffix.
        decoded = re.sub(r"(\.md):\d+$", r"\1", decoded, flags=re.I)
        base, separator, fragment = decoded.partition("#")
        base = base.split("?", 1)[0].replace("\\", "/")
        local = Path(base)
        if not local.is_absolute():
            local = source_file.parent / local
        mapped = document_map.get(path_key(local))
        if mapped is not None:
            result = portable_link(output_file, mapped)
            return result + ("#" + fragment if separator else "")
        if local.suffix.lower() == ".jsonl" and (local.name.startswith(("shots_", "references_")) or local.name == "references.jsonl"):
            return portable_link(output_file, references_file)
        return None

    result, previous = [], 0
    for start, end, image, label, raw, title in inline_links(text):
        result.append(text[previous:start])
        target = destination(raw)
        if target is None:
            sanitizer.stats["markdown_local_or_unpublished_links_replaced"] += 1
            result.append(LOCAL_EVIDENCE)
        else:
            # Remote media remain source links, never an embedded/repackaged original.
            safe_label = sanitizer.string(label) or ("원본 공개 이미지" if image else "출처")
            safe_title = sanitizer.string(title)
            result.append(f"[{safe_label}](<{target}>" + (f" {safe_title}" if safe_title else "") + ")")
        previous = end
    result.append(text[previous:])
    document = "".join(result)

    def reference_definition(match):
        raw, title = split_destination(match.group(2))
        target = destination(raw)
        if target is None:
            sanitizer.stats["markdown_local_or_unpublished_links_replaced"] += 1
            # Preserve the reference label as a readable local-evidence anchor.
            return f"[{match.group(1)}]: #local-observation-evidence"
        return f"[{match.group(1)}]: <{target}>" + (" " + sanitizer.string(title) if title else "")

    document = re.sub(r"(?m)^\s{0,3}\[(?!\^)([^\]\n]+)\]:\s*(.+)$", reference_definition, document)

    def html_media(match):
        tag = match.group(0)
        src = re.search(r"\bsrc\s*=\s*([\"'])(.*?)\1", tag, re.I | re.S)
        target = destination(src.group(2)) if src else None
        return f"[원본 공개 미디어](<{target}>)" if target and target.startswith(("http://", "https://")) else LOCAL_EVIDENCE

    document = re.sub(r"<(?:video|audio)\b[^>]*>.*?</(?:video|audio)>", html_media, document, flags=re.I | re.S)
    document = re.sub(r"<img\b[^>]*>", html_media, document, flags=re.I | re.S)

    def html_link(match):
        target = destination(match.group(2))
        return "href=" + match.group(1) + (target or "#local-observation-evidence") + match.group(1)

    document = re.sub(r"\bhref\s*=\s*([\"'])(.*?)\1", html_link, document, flags=re.I | re.S)
    document = sanitizer.string(document)
    if privacy_findings(document):
        raise ExportError(f"Privacy redaction is incomplete in document {source_file.name}.")
    audit_link = portable_link(output_file, audit_file)
    manifest_link = portable_link(output_file, snapshot_file)
    notice = (
        "> 공개본에는 원본 이미지·영상과 로컬 관찰판을 포함하지 않는다. ‘로컬 관찰 근거’는 저장소에 재배포하지 않는 로컬 관찰 자료를 가리킨다. "
        "공개 출처 링크와 관찰·제작 제안은 보존하며, 문서별 과거 수량보다 "
        f"[프로젝트 감사 집계](<{audit_link}>)와 [스냅샷 매니페스트](<{manifest_link}>)의 집계가 최신 기준이다.\n\n"
    )
    return normalize_markdown_lines(notice + document)


def json_bytes(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode("utf-8")


def shard_references(rows: list[dict], project: str, index_relative: Path):
    """Bound each JSONL part by both row count and byte size, preserving order."""
    payloads, shards, chunk = {}, [], []
    chunk_bytes = 0

    def finish_chunk():
        nonlocal chunk, chunk_bytes
        if not chunk:
            return
        filename = f"part-{len(shards) + 1:05d}.jsonl"
        content = b"".join(chunk)
        relative = (index_relative.parent / filename).as_posix()
        payloads[relative] = content
        shards.append({"path": filename, "rows": len(chunk), "sha256": digest_bytes(content), "bytes": len(content)})
        chunk, chunk_bytes = [], 0

    for row in rows:
        line = (json.dumps(row, ensure_ascii=False, allow_nan=False) + "\n").encode("utf-8")
        if len(line) > MAX_SHARD_BYTES:
            raise ExportError("One reference exceeds the 16MiB shard limit; reduce nonresearch payloads in the local ledger first.")
        if chunk and (len(chunk) >= MAX_SHARD_ROWS or chunk_bytes + len(line) > MAX_SHARD_BYTES):
            finish_chunk()
        chunk.append(line)
        chunk_bytes += len(line)
    finish_chunk()
    index = {"schema_version": SCHEMA_VERSION, "project": project,
             "reference_format": "sharded_jsonl", "total_references": len(rows),
             "shard_count": len(shards), "max_rows_per_shard": MAX_SHARD_ROWS,
             "max_bytes_per_shard": MAX_SHARD_BYTES, "shards": shards}
    payloads[index_relative.as_posix()] = json_bytes(index)
    return payloads, index


def atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, temporary = tempfile.mkstemp(prefix=".research-", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(handle, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def document_links(document_sources: list[Path], source: Path, root: Path,
                   docs_rel: Path, aliases: tuple[Path, ...] = ()) -> dict[str, Path]:
    """Map only exported documents, including explicitly named prior checkpoints."""
    mapping = {path_key(path): root / docs_rel / path.relative_to(source)
               for path in document_sources}
    for alias in aliases:
        alias = alias.resolve()
        if not alias.is_dir():
            raise ExportError("A document-source alias must be an existing checkpoint directory.")
        for path in document_sources:
            prior = alias / path.relative_to(source)
            if not prior.is_file() or not prior.resolve().is_relative_to(alias):
                continue
            key, target = path_key(prior), mapping[path_key(path)]
            if key in mapping and mapping[key] != target:
                raise ExportError("Document-source aliases map one path to different public documents.")
            mapping[key] = target
    return mapping


def export_research(source: Path, destination: Path, project: str, snapshot_date: str,
                    document_source_aliases: tuple[Path, ...] = ()) -> dict:
    if not SLUG_RE.fullmatch(project):
        raise ExportError("Project must be a lowercase hyphen-separated slug.")
    try:
        if date.fromisoformat(snapshot_date).isoformat() != snapshot_date:
            raise ValueError
    except ValueError as exc:
        raise ExportError("Date must be YYYY-MM-DD.") from exc
    source, root = source.resolve(), destination.resolve()
    if source == root or source in root.parents or root in source.parents:
        raise ExportError("Source and destination must be separate, non-nested directories.")
    audit_path, master_path = source / "shot_audit.json", source / "shots_master.jsonl"
    try:
        source_audit_bytes, master_bytes = audit_path.read_bytes(), master_path.read_bytes()
        source_audit = json.loads(source_audit_bytes.decode("utf-8-sig"))
        rows = [json.loads(line) for line in master_bytes.decode("utf-8-sig").splitlines() if line.strip()]
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ExportError("Read a completed shot_audit.json and matching shots_master.jsonl first.") from exc
    if not isinstance(source_audit, dict) or any(not isinstance(row, dict) for row in rows):
        raise ExportError("Audit must be an object and master rows must be objects.")
    eligible = [row for row in rows if row.get("count_eligible") is True]
    if source_audit.get("eligible_observed_units") != len(eligible) or source_audit.get("raw_rows") != len(rows):
        raise ExportError("Audit/master counts disagree. Refresh the local audit before exporting.")
    if source_audit.get("classes") != {"core3D": len(eligible)}:
        raise ExportError("The completed audit must count only pure core3D units.")
    if source_audit.get("data_quality_notes"):
        raise ExportError("Resolve the source audit's data_quality_notes before exporting.")
    target = source_audit.get("target")
    if isinstance(target, bool) or not isinstance(target, int) or target <= 0:
        raise ExportError("Source audit has no valid positive project target.")
    sanitizer = Sanitizer()
    normalized = [normalize_record(row, sanitizer) for row in eligible]
    identifiers = [row["reference_id"] for row in normalized]
    if len(identifiers) != len(set(identifiers)):
        raise ExportError("Eligible canonical reference IDs are not unique.")
    per_ledger = dict(sorted(Counter(row["lineage"]["ledger_file"] for row in normalized).items()))
    source_per_ledger = {row["file"]: row["eligible"] for row in source_audit.get("per_file", []) if row.get("eligible")}
    if source_per_ledger != per_ledger:
        raise ExportError("Per-ledger audit totals disagree with the selected master rows.")
    reference_rel = Path("data/projects") / project / "references/index.json"
    audit_rel = Path("data/projects") / project / "audit.json"
    docs_rel = Path("docs/research") / snapshot_date
    document_sources = sorted(path for path in source.iterdir() if path.is_file() and NUMBERED_MD_RE.fullmatch(path.name))
    for public_supporting_document in ("shot-counting.md", "analysis-schema.md"):
        methodology = source / public_supporting_document
        if methodology.is_file():
            document_sources.append(methodology)
    reference_documents, reference_selection = select_reference_index_documents(source)
    document_sources.extend(reference_documents)
    if not document_sources:
        raise ExportError("No numbered Markdown research documents were found.")
    document_map = document_links(document_sources, source, root, docs_rel, document_source_aliases)
    payloads, reference_index = shard_references(normalized, project, reference_rel)
    document_inputs = []
    for path in document_sources:
        data = path.read_bytes()
        exported_path = document_map[path_key(path)]
        text = rewrite_markdown(data.decode("utf-8-sig"), path, exported_path, document_map, root / reference_rel, sanitizer, audit_file=root / audit_rel, snapshot_file=root / "manifests/snapshot.json")
        rel = exported_path.relative_to(root).as_posix()
        payloads[rel] = text.encode("utf-8")
        document_inputs.append({"name": path.relative_to(source).as_posix(), "sha256": digest_bytes(data)})
    input_hashes = {"shot_audit.json": digest_bytes(source_audit_bytes), "shots_master.jsonl": digest_bytes(master_bytes)}
    # A snapshot must describe one consistent completed audit, not a moving collection.
    if digest_bytes(audit_path.read_bytes()) != input_hashes["shot_audit.json"] or digest_bytes(master_path.read_bytes()) != input_hashes["shots_master.jsonl"]:
        raise ExportError("Source audit/master changed during export. Retry after the audit completes.")
    for item, path in zip(document_inputs, document_sources):
        if digest_bytes(path.read_bytes()) != item["sha256"]:
            raise ExportError("A source Markdown document changed during export. Retry after its update completes.")
    if reference_selection.get("driver"):
        driver_input = next(item for item in document_inputs if item["name"] == reference_selection["driver"])
        if driver_input["sha256"] != reference_selection["driver_sha256"]:
            raise ExportError("The integrated reference index changed during document selection. Retry after its update completes.")
    exported_audit = {
        "schema_version": SCHEMA_VERSION, "project": project, "snapshot_date": snapshot_date,
        "target": target, "eligible_observed_units": len(normalized), "exported_references": len(normalized),
        "remaining": max(0, target - len(normalized)), "classes": {"core3D": len(normalized)},
        "project_completion_claim": len(normalized) >= target,
        "reference_format": "sharded_jsonl", "reference_index": reference_rel.as_posix(),
        "shard_count": reference_index["shard_count"],
        "reference_index_selection": reference_selection,
        "exported_per_ledger": per_ledger, "original_media_redistributed": False,
        "selection_rule": "Completed master count_eligible=true and canonical_class=core3D only. Near variants, hybrid, 2D and unobserved metadata are excluded.",
        "input_sha256": input_hashes, "privacy_redactions": dict(sorted(sanitizer.stats.items())),
        "source_audit": sanitizer.value(source_audit),
    }
    payloads[audit_rel.as_posix()] = json_bytes(exported_audit)
    for rel, data in payloads.items():
        if privacy_findings(data.decode("utf-8")):
            raise ExportError(f"Output {rel} contains a forbidden private/local value.")
    snapshot_path = root / "manifests/snapshot.json"
    if snapshot_path.exists():
        snapshot = json.loads(snapshot_path.read_text(encoding="utf-8"))
        if not isinstance(snapshot, dict) or snapshot.get("schema_version") != SCHEMA_VERSION or not isinstance(snapshot.get("projects"), dict):
            raise ExportError("Existing snapshot manifest uses an incompatible schema.")
    else:
        snapshot = {"schema_version": SCHEMA_VERSION, "projects": {}}
    for other_project, other_entry in snapshot["projects"].items():
        if other_project == project or not isinstance(other_entry, dict):
            continue
        for other_file in other_entry.get("files", []):
            if isinstance(other_file, dict) and other_file.get("path") in payloads:
                if digest_bytes(payloads[other_file["path"]]) != other_file.get("sha256"):
                    raise ExportError("Another project owns different content at this research date/path. Choose a separate snapshot date before exporting.")
    cleanup_report = stale_managed_file_report(root, snapshot, project, set(payloads), docs_rel.as_posix())
    entry = {
        "project": project, "snapshot_date": snapshot_date,
        "exported_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "references": reference_rel.as_posix(), "audit": audit_rel.as_posix(),
        "reference_format": "sharded_jsonl", "shard_count": reference_index["shard_count"],
        "reference_index_selection": reference_selection, "managed_file_cleanup": cleanup_report,
        "research_directory": docs_rel.as_posix(), "research_document_count": len(document_sources),
        "eligible_observed_units": len(normalized), "input_sha256": input_hashes,
        "source_documents": document_inputs,
        "files": [{"path": rel, "sha256": digest_bytes(data), "bytes": len(data)} for rel, data in sorted(payloads.items())],
        "original_media_redistributed": False,
        "validation_scope": "Portable data integrity; original visual observation remains the source research's responsibility.",
    }
    snapshot["projects"][project] = entry
    snapshot_bytes = json_bytes(snapshot)
    if privacy_findings(snapshot_bytes.decode("utf-8")):
        raise ExportError("The existing or updated snapshot contains a private value.")
    # Validate prepared outputs before touching the destination. No source media are copied.
    with tempfile.TemporaryDirectory(prefix="portable-research-") as stage:
        stage_root = Path(stage)
        for rel, data in payloads.items():
            staged = stage_root / rel
            staged.parent.mkdir(parents=True, exist_ok=True)
            staged.write_bytes(data)
        staged_snapshot = stage_root / "manifests/snapshot.json"
        staged_snapshot.parent.mkdir(parents=True, exist_ok=True)
        staged_snapshot.write_bytes(snapshot_bytes)
        validation = validate_library(stage_root, project)
        if not validation["ok"]:
            # Errors contain relative paths and field names, not private input values.
            raise ExportError("Prepared snapshot failed validation: " + "; ".join(validation["errors"][:20]))
    for rel, data in sorted(payloads.items()):
        atomic_write(root / rel, data)
    # Commit marker last: readers must validate its digests before trusting a snapshot.
    atomic_write(snapshot_path, snapshot_bytes)
    validation = validate_library(root, project)
    if not validation["ok"]:
        raise ExportError("Written snapshot failed validation: " + "; ".join(validation["errors"][:20]))
    return {"ok": True, "project": project, "snapshot_date": snapshot_date,
            "exported_references": len(normalized), "research_documents": len(document_sources),
            "shard_count": reference_index["shard_count"], "reference_index": reference_rel.as_posix(),
            "reference_index_selection": reference_selection,
            "managed_file_cleanup": cleanup_report,
            "remaining": max(0, target - len(normalized)), "original_media_redistributed": False,
            "manifest": "manifests/snapshot.json"}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True, help="Completed local research directory.")
    parser.add_argument("--destination", type=Path, required=True, help="Separate destination repository directory.")
    parser.add_argument("--project", required=True, help="Lowercase hyphen-separated project slug.")
    parser.add_argument("--date", required=True, help="Research snapshot date, YYYY-MM-DD.")
    parser.add_argument("--document-source-alias", type=Path, action="append", default=[],
                        help="Explicit prior checkpoint of this project, for exported document links only. Repeat as needed.")
    args = parser.parse_args(argv)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    try:
        result = export_research(args.source, args.destination, args.project, args.date,
                                 tuple(args.document_source_alias))
    except (ExportError, OSError, UnicodeError, json.JSONDecodeError) as exc:
        # Path-bearing OSError text is deliberately not printed into portable logs.
        message = str(exc) if isinstance(exc, ExportError) else type(exc).__name__
        print(json.dumps({"ok": False, "error": message}, ensure_ascii=False), file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
