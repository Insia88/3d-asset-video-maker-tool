#!/usr/bin/env python3
"""Validate portable research snapshots. Standard library only; never fetch media."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import unquote, urlsplit

SCHEMA_VERSION = "1.0"
MAX_SHARD_ROWS = 1000
MAX_SHARD_BYTES = 16 * 1024 * 1024
LOCAL_EVIDENCE = "로컬 관찰 근거"
WITHHELD = "비공개 정보 생략"
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")
PRIVATE_KEY_RE = re.compile(
    r"^(?:access_token|refresh_token|auth_token|api_key|apikey|authorization|"
    r"password|passwd|secret|client_secret|cookie|cookies|request_headers|"
    r"response_headers|headers|raw_response|cached_response|cache_response|"
    r"raw_tool_response|tool_response|conversation_id|thread_id|session_id|"
    r"client_thread_id|codex_home|user_account|username|account_email)$", re.I
)
LOCAL_PATH_RE = re.compile(
    r"(?<![\w])(?:[A-Za-z]:[\\/]|file://|\\\\[^\s\\/]+[\\/]|"
    r"/(?:Users|home|mnt|tmp|private|var|root)/)[^\r\n<>`\"']*", re.I
)
PRIVATE_CONTEXT_RE = re.compile(
    r"(?:codex://(?:threads|tasks)/[^\s<>]+|"
    r"(?:conversation|thread|session)[ _-]?id\s*[:=]\s*[^\s,;<>]+|"
    r"Bearer\s+[A-Za-z0-9._~+/=-]+|"
    r"\bsk-(?:proj-|svcacct-)?[A-Za-z0-9_-]{16,}|"
    r"\beyJ[A-Za-z0-9_-]{15,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,})", re.I
)
PRIVATE_QUERY_RE = re.compile(
    r"^(?:token|access_token|auth|authorization|api[_-]?key|secret|password|"
    r"signature|sig|x-amz-signature|x-amz-credential|x-goog-signature|"
    r"conversation_id|thread_id|session_id)$", re.I
)
MEDIA_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg", ".mp4", ".mov", ".mkv", ".mp3", ".wav", ".glb", ".fbx"}


def digest_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def decode_reference(value: str) -> str:
    result = value
    for _ in range(3):
        decoded = unquote(result)
        if decoded == result:
            break
        result = decoded
    return result


def safe_public_url(value: str) -> bool:
    """Accept ordinary public HTTP(S) references, not signed/authenticated links."""
    if not isinstance(value, str) or value != value.strip() or re.search(r"[\s<>\"']", value):
        return False
    try:
        parsed = urlsplit(value)
    except ValueError:
        return False
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        return False
    if parsed.username is not None or parsed.password is not None:
        return False
    if parsed.hostname.lower() in {"localhost", "127.0.0.1", "::1"}:
        return False
    for pair in parsed.query.split("&"):
        if pair and PRIVATE_QUERY_RE.fullmatch(unquote(pair.split("=", 1)[0])):
            return False
    return not PRIVATE_CONTEXT_RE.search(decode_reference(value))


def privacy_findings(text: str) -> list[str]:
    decoded = decode_reference(text)
    findings = []
    if LOCAL_PATH_RE.search(decoded):
        findings.append("absolute_local_path")
    if PRIVATE_CONTEXT_RE.search(decoded):
        findings.append("private_context_or_credential")
    if re.search(r"(?:data:[^\s,]*;base64,|plugin://|codex-remote-attachments|\.cache[/\\]codex)", decoded, re.I):
        findings.append("embedded_payload_or_private_attachment")
    for match in re.finditer(r"https?://[^\s<>\"']+", text):
        if not safe_public_url(match.group(0).rstrip(").,;")):
            findings.append("nonpublic_or_authenticated_url")
    return sorted(set(findings))


def walk_strings(value, trail: tuple[str, ...] = ()):
    if isinstance(value, dict):
        for key, item in value.items():
            yield trail + (str(key), "<key>"), str(key)
            yield from walk_strings(item, trail + (str(key),))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            yield from walk_strings(item, trail + (str(index),))
    elif isinstance(value, str):
        yield trail, value


def split_destination(body: str) -> tuple[str, str]:
    """Split a Markdown destination and optional title without decoding its URL."""
    stripped = body.strip()
    if stripped.startswith("<"):
        end = stripped.find(">")
        if end >= 0:
            return stripped[1:end], stripped[end + 1:].strip()
    # Exported destinations use angle brackets; source destinations may have a title.
    match = re.match(r"^(.*?)(?:\s+([\"'].*[\"']|\(.*\)))$", stripped, re.S)
    if match:
        return match.group(1), match.group(2)
    return stripped, ""


def inline_links(text: str):
    """Yield balanced inline Markdown links, including angle-wrapped local paths."""
    index = 0
    while index < len(text):
        opening = text.find("[", index)
        if opening < 0:
            return
        if opening and text[opening - 1] == "\\":
            index = opening + 1
            continue
        depth, close = 1, opening + 1
        while close < len(text) and depth:
            char = text[close]
            if char == "\\":
                close += 2
                continue
            if char == "[":
                depth += 1
            elif char == "]":
                depth -= 1
            close += 1
        if depth or close >= len(text) or text[close] != "(":
            index = close
            continue
        cursor, parens, angle, quote = close + 1, 1, False, None
        while cursor < len(text) and parens:
            char = text[cursor]
            if char == "\\":
                cursor += 2
                continue
            if angle:
                if char == ">":
                    angle = False
            elif quote:
                if char == quote:
                    quote = None
            elif char == "<":
                angle = True
            elif char in {"\"", "'"} and cursor > close + 1 and text[cursor - 1].isspace():
                quote = char
            elif char == "(":
                parens += 1
            elif char == ")":
                parens -= 1
            cursor += 1
        if parens:
            index = close + 1
            continue
        image = opening > 0 and text[opening - 1] == "!" and (opening < 2 or text[opening - 2] != "\\")
        start = opening - 1 if image else opening
        destination, title = split_destination(text[close + 1:cursor - 1])
        yield start, cursor, image, text[opening + 1:close - 1], destination, title
        index = cursor


def markdown_destinations(text: str):
    for _, _, _, _, destination, _ in inline_links(text):
        yield destination
    for match in re.finditer(r"(?m)^\s{0,3}\[(?!\^)[^\]\n]+\]:\s*(.+)$", text):
        yield split_destination(match.group(1))[0]
    for match in re.finditer(r"\b(?:href|src)\s*=\s*([\"'])(.*?)\1", text, re.I | re.S):
        yield match.group(2)


def resolve_internal(root: Path, origin: Path, target: str) -> Path | None:
    decoded = decode_reference(target).replace("\\", "/")
    if decoded.startswith("#") or not decoded:
        return None
    parsed = urlsplit(decoded)
    if parsed.scheme in {"http", "https", "mailto"}:
        return None
    if parsed.scheme or parsed.netloc or decoded.startswith("/"):
        raise ValueError("absolute_or_unsupported_link")
    path = (origin.parent / parsed.path).resolve()
    try:
        path.relative_to(root.resolve())
    except ValueError as exc:
        raise ValueError("internal_link_escapes_repository") from exc
    return path


def read_reference_shards(root: Path, project: str, index_path: Path):
    errors, rows, paths = [], [], set()
    try:
        index = json.loads(index_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return [], {}, set(), [f"cannot_read_reference_index:{type(exc).__name__}"]
    if not isinstance(index, dict):
        return [], {}, set(), ["invalid_reference_index_shape"]
    if index.get("schema_version") != SCHEMA_VERSION or index.get("project") != project:
        errors.append("reference_index_schema_or_project_mismatch")
    if index.get("max_rows_per_shard") != MAX_SHARD_ROWS or index.get("max_bytes_per_shard") != MAX_SHARD_BYTES:
        errors.append("reference_index_limits_mismatch")
    shards = index.get("shards")
    if not isinstance(shards, list):
        return [], index, set(), errors + ["invalid_shard_table"]
    for number, shard in enumerate(shards, 1):
        if not isinstance(shard, dict) or shard.get("path") != f"part-{number:05d}.jsonl":
            errors.append(f"invalid_or_unordered_shard_path:{number}")
            continue
        relative_path = index_path.parent.relative_to(root).as_posix() + "/" + shard["path"]
        paths.add(relative_path)
        try:
            shard_path = resolve_internal(root, index_path, shard["path"])
            content = shard_path.read_bytes()
            shard_rows = [json.loads(line) for line in content.decode("utf-8").splitlines() if line.strip()]
        except (OSError, UnicodeError, json.JSONDecodeError, ValueError, AttributeError) as exc:
            errors.append(f"cannot_read_shard:{number}:{type(exc).__name__}")
            continue
        if not shard_rows or any(not isinstance(row, dict) for row in shard_rows):
            errors.append(f"invalid_shard_rows:{number}")
            continue
        if len(shard_rows) > MAX_SHARD_ROWS or len(content) > MAX_SHARD_BYTES:
            errors.append(f"shard_exceeds_limits:{number}")
        if shard.get("rows") != len(shard_rows) or isinstance(shard.get("rows"), bool):
            errors.append(f"shard_row_count_mismatch:{number}")
        if shard.get("bytes") != len(content) or digest_bytes(content) != shard.get("sha256"):
            errors.append(f"shard_digest_or_size_mismatch:{number}")
        rows.extend(shard_rows)
    if index.get("total_references") != len(rows) or isinstance(index.get("total_references"), bool):
        errors.append("reference_index_count_mismatch")
    if index.get("shard_count") != len(shards):
        errors.append("reference_index_shard_count_mismatch")
    for trail, value in walk_strings(index):
        if trail and trail[-1] == "<key>" and PRIVATE_KEY_RE.fullmatch(value):
            errors.append(f"reference_index:private_field:{'.'.join(trail[:-1])}")
        for finding in privacy_findings(value):
            errors.append(f"reference_index:{finding}:{'.'.join(trail)}")
    return rows, index, paths, errors


def check_project(root: Path, project: str, snapshot_entry: dict) -> list[str]:
    errors = []
    if not SLUG_RE.fullmatch(project):
        return ["invalid_project_slug"]
    expected_refs = f"data/projects/{project}/references/index.json"
    expected_audit = f"data/projects/{project}/audit.json"
    if snapshot_entry.get("references") != expected_refs or snapshot_entry.get("audit") != expected_audit:
        return ["unexpected_project_output_paths"]
    refs_path, audit_path = root / expected_refs, root / expected_audit
    try:
        audit_bytes = audit_path.read_bytes()
        audit = json.loads(audit_bytes)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return [f"cannot_read_project_data:{type(exc).__name__}"]
    rows, reference_index, shard_paths, shard_errors = read_reference_shards(root, project, refs_path)
    errors.extend(shard_errors)
    if not isinstance(audit, dict):
        return ["invalid_project_json_shape"]
    if snapshot_entry.get("reference_format") != "sharded_jsonl" or audit.get("reference_format") != "sharded_jsonl":
        errors.append("reference_format_mismatch")
    if audit.get("reference_index") != expected_refs:
        errors.append("audit_reference_index_path_mismatch")
    shard_count = reference_index.get("shard_count")
    if snapshot_entry.get("shard_count") != shard_count or audit.get("shard_count") != shard_count:
        errors.append("audit_snapshot_shard_count_mismatch")
    expected_count = snapshot_entry.get("eligible_observed_units")
    if isinstance(expected_count, bool) or not isinstance(expected_count, int) or expected_count < 0:
        errors.append("invalid_snapshot_count")
    for field in ("eligible_observed_units", "exported_references"):
        if audit.get(field) != len(rows):
            errors.append(f"audit_count_mismatch:{field}")
    if expected_count != len(rows):
        errors.append("snapshot_count_mismatch")
    if audit.get("classes") != {"core3D": len(rows)}:
        errors.append("audit_contains_non_core3D_count")
    if audit.get("project") != project or audit.get("schema_version") != SCHEMA_VERSION:
        errors.append("audit_schema_or_project_mismatch")
    target = audit.get("target")
    if isinstance(target, bool) or not isinstance(target, int) or target <= 0:
        errors.append("invalid_target")
    elif audit.get("remaining") != max(0, target - len(rows)):
        errors.append("remaining_count_mismatch")
    elif audit.get("project_completion_claim") is not (len(rows) >= target):
        errors.append("completion_claim_mismatch")
    source_audit = audit.get("source_audit", {})
    if source_audit.get("eligible_observed_units") != len(rows):
        errors.append("source_audit_count_mismatch")
    ids = []
    per_ledger = Counter()
    for number, row in enumerate(rows, 1):
        prefix = f"row_{number}"
        identifier = row.get("reference_id")
        if not isinstance(identifier, str) or not identifier.strip():
            errors.append(f"{prefix}:missing_id")
        else:
            ids.append(identifier)
        if row.get("schema_version") != SCHEMA_VERSION:
            errors.append(f"{prefix}:schema_version")
        if row.get("class") != "core3D" or row.get("count_eligible") is not True:
            errors.append(f"{prefix}:not_eligible_pure3D")
        original = row.get("source_record")
        if not isinstance(original, dict):
            errors.append(f"{prefix}:missing_source_record")
        elif original.get("count_eligible") is not True or original.get("canonical_class") != "core3D":
            errors.append(f"{prefix}:source_selection_mismatch")
        elif original.get("canonical_shot_id") != identifier:
            errors.append(f"{prefix}:source_id_mismatch")
        if isinstance(original, dict) and any(original.get(k) for k in ("duplicate_of", "exact_clip_duplicate_of")):
            errors.append(f"{prefix}:selected_duplicate")
        if not row.get("observation", {}).get("has_recorded_evidence"):
            errors.append(f"{prefix}:missing_observation_evidence")
        if row.get("unit_type") not in {"still_image", "video_scene", "reference_unit_unspecified"}:
            errors.append(f"{prefix}:unsupported_unit_type")
        if not row.get("visual", {}).get("description"):
            errors.append(f"{prefix}:missing_visual_description")
        for source in row.get("source", {}).get("urls", []):
            if not isinstance(source, dict) or not safe_public_url(str(source.get("url", ""))):
                errors.append(f"{prefix}:invalid_public_source_url")
        for item in row.get("hashes", []):
            if not isinstance(item, dict) or not SHA256_RE.fullmatch(str(item.get("value", ""))):
                errors.append(f"{prefix}:invalid_source_sha256")
        for trail, value in walk_strings(row):
            if trail and trail[-1] == "<key>" and PRIVATE_KEY_RE.fullmatch(value):
                errors.append(f"{prefix}:private_field:{'.'.join(trail[:-1])}")
            for finding in privacy_findings(value):
                errors.append(f"{prefix}:{finding}:{'.'.join(trail)}")
        per_ledger[row.get("lineage", {}).get("ledger_file", "unknown")] += 1
    if len(ids) != len(set(ids)):
        errors.append("duplicate_reference_ids")
    if dict(sorted(per_ledger.items())) != audit.get("exported_per_ledger"):
        errors.append("per_ledger_count_mismatch")
    for trail, value in walk_strings(audit):
        if trail and trail[-1] == "<key>" and PRIVATE_KEY_RE.fullmatch(value):
            errors.append(f"audit:private_field:{'.'.join(trail[:-1])}")
        for finding in privacy_findings(value):
            errors.append(f"audit:{finding}:{'.'.join(trail)}")
    files = snapshot_entry.get("files", [])
    if not isinstance(files, list) or not files:
        errors.append("missing_file_manifest")
        files = []
    seen_paths = set()
    for item in files:
        if not isinstance(item, dict) or not isinstance(item.get("path"), str):
            errors.append("invalid_manifest_file")
            continue
        rel = item["path"]
        if "\\" in rel or rel.startswith("/") or ".." in rel.split("/"):
            errors.append("unsafe_manifest_path")
            continue
        research_directory = snapshot_entry.get("research_directory", "")
        if rel not in {expected_refs, expected_audit} and rel not in shard_paths and not (isinstance(research_directory, str) and research_directory.startswith("docs/research/") and rel.startswith(research_directory + "/") and rel.endswith(".md")):
            errors.append(f"unexpected_export_file:{rel}")
            continue
        if rel in seen_paths:
            errors.append("duplicate_manifest_path")
        seen_paths.add(rel)
        try:
            path = resolve_internal(root, root / "__manifest__", rel)
            if path is None:
                raise ValueError("not_internal")
            content = path.read_bytes()
        except (OSError, ValueError):
            errors.append(f"missing_or_unsafe_manifest_file:{rel}")
            continue
        if digest_bytes(content) != item.get("sha256") or len(content) != item.get("bytes"):
            errors.append(f"file_digest_mismatch:{rel}")
        if path.suffix.lower() in MEDIA_SUFFIXES:
            errors.append(f"redistributed_media:{rel}")
        if path.suffix.lower() == ".md":
            try:
                document = content.decode("utf-8")
            except UnicodeError:
                errors.append(f"invalid_markdown_encoding:{rel}")
                continue
            for finding in privacy_findings(document):
                errors.append(f"markdown:{finding}:{rel}")
            for destination in markdown_destinations(document):
                try:
                    linked = resolve_internal(root, path, destination)
                    if linked is not None and not linked.is_file():
                        errors.append(f"broken_internal_link:{rel}:{destination}")
                except ValueError:
                    errors.append(f"unsafe_internal_link:{rel}")
    if expected_refs not in seen_paths or expected_audit not in seen_paths:
        errors.append("data_files_not_in_manifest")
    if not shard_paths.issubset(seen_paths):
        errors.append("shard_files_not_in_manifest")
    document_paths = {x for x in seen_paths if x.endswith(".md")}
    if len(document_paths) != snapshot_entry.get("research_document_count"):
        errors.append("research_document_count_mismatch")
    return errors


def validate_library(destination: Path, project: str | None = None) -> dict:
    root = destination.resolve()
    try:
        snapshot = json.loads((root / "manifests/snapshot.json").read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return {"ok": False, "errors": [f"cannot_read_snapshot:{type(exc).__name__}"]}
    if not isinstance(snapshot, dict):
        return {"ok": False, "errors": ["invalid_snapshot_json_shape"]}
    errors = []
    if snapshot.get("schema_version") != SCHEMA_VERSION:
        errors.append("snapshot_schema_version_mismatch")
    for trail, value in walk_strings(snapshot):
        if trail and trail[-1] == "<key>" and PRIVATE_KEY_RE.fullmatch(value):
            errors.append(f"snapshot:private_field:{'.'.join(trail[:-1])}")
        for finding in privacy_findings(value):
            errors.append(f"snapshot:{finding}:{'.'.join(trail)}")
    projects = snapshot.get("projects")
    if not isinstance(projects, dict) or not projects:
        return {"ok": False, "errors": errors + ["missing_projects"]}
    names = [project] if project else sorted(projects)
    checked = []
    for name in names:
        entry = projects.get(name)
        if not isinstance(entry, dict):
            errors.append(f"project_not_registered:{name}")
            continue
        project_errors = check_project(root, name, entry)
        errors.extend(f"{name}:{e}" for e in project_errors)
        checked.append({"project": name, "references": entry.get("eligible_observed_units"), "errors": len(project_errors)})
    return {"ok": not errors, "schema_version": SCHEMA_VERSION, "projects": checked, "errors": errors,
            "validation_scope": "Recorded classification, count, privacy, file integrity and internal links; no new visual observation or model verification."}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--destination", "--root", dest="destination", type=Path, default=Path(__file__).resolve().parents[1], help="Repository root; --root is an alias for --destination.")
    parser.add_argument("--project", help="Validate one registered project; omitted means all projects.")
    args = parser.parse_args(argv)
    result = validate_library(args.destination, args.project)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
