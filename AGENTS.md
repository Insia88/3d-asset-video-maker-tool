# Repository workflow

This repository holds reusable 3D visual research, channel-format analysis, source metadata, foundation prompts, and tools for turning audited research into portable project snapshots.

- Read `README.md`, `docs/workflow.md`, and `manifests/snapshot.json` before adding or updating a project. Use the existing project slug and registered paths when continuing the same research.
- Direct visual observation, source provenance, generation-model evidence, and editable mesh verification are separate claims. Preserve their actual verification level.
- Count only directly observed, selected, unique units. A whole still image or model sheet is one unit. Search results, prepared previews, objects in a scene, panels, and repeated frames do not add completed units.
- Apply the project's current selection scope. The beauty ETF project is pure 3D only, with beauty subjects or attractive/cute stylized objects and miniature spaces. Preserve exclusion and representative decisions in the source research.
- Export completed audits through `tools/import_research.py` and run `tools/validate_library.py --root .` before committing a snapshot. Keep shard counts, hashes, source-document links, and project totals consistent.
- Store source URLs, original hashes, analysis, prompts, and verified rights claims. Keep credentials, local account paths, conversation identifiers, downloaded research media, and private tool responses out of committed files.
- Use source-specific rights and creator claims. A gallery preview or a platform-wide AI label does not prove an individual generation model or grant rights to an asset.
- Honor the project's generation prerequisite and dependency order. In the beauty ETF project, generate foundation masters with Higgsfield MCP after the 25,000-unit reference-collection gate is fulfilled. Record actual returned job, media, and Element identifiers only after success.
- Use a single clear mascot identity master before deriving model sheets. Lock product geometry, environment coordinates, material roles, and lighting when creating related images or I2V shots.
- Verify ETF holdings, weights, fees, and dates against issuer or disclosure originals before filling financial labels. Example tokens, palette choices, and visual height are production proposals rather than financial evidence.
- Tools use Python's standard library. Keep paths configurable and avoid workstation-specific executable paths in repository instructions.
- Preserve unrelated projects and existing Git history when adding new snapshots. Describe material changes in the commit message and update `docs/decisions.md` when the project's scope or counting unit changes.
