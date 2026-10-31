# Importing, selecting and updating skills

## Search and select

Search `manifests/catalog.json` through `python scripts/search-catalog.py <query>`. It covers
actual bundled files. Filter by category or status. `--references` searches the original discovery
index, which records which local entries were copied and which remain excluded/reference-only.

Reviewed packages can be added with `--add-skills id1,id2`. Screened packages require inspection
and an explicit `--allow-screened` opt-in. The installer writes a review requirement into the
project. Skill instructions cannot grant permission for destructive or external actions.

## Import a public collection

Use a separate clean checkout at a specific Git revision. Inspect its license and relevant content.
The importer never downloads or executes scripts by itself:

```bash
python scripts/import-collection.py --checkout /path/to/checkout --source-id example --repo owner/repository
python scripts/import-collection.py --checkout /path/to/checkout --source-id example --repo owner/repository --apply
```

The first command previews eligibility. The second copies eligible packages into the passive
library, preserving licenses, files and a pinned revision. It rejects sensitive filenames,
common secret patterns, binaries, links, oversized packages and unrecognized license terms.
Imported packages start screened. Existing differing imports are not overwritten automatically.

## Import audited local packages

`python scripts/import-local.py --inventory .local/inventory.json` checks reusable locations and
license evidence. Add `--apply` to copy eligible actual packages into `library/local` and update
the catalog. It namespaces discovery names and retains content hashes, supporting files and
attribution. Local machine paths remain in the ignored audit records. Project-specific and
dependency directories are excluded. Original installations are never moved or edited.

## Review and maintain

Review the entrypoint, referenced instructions, scripts, dependencies, cross-skill paths and
host-specific tool assumptions. Record precise findings in TOOLKIT-PROVENANCE.json. A reviewed
package requires all executable files to have an explicit review, or no executables. Verify it in
an isolated project before promoting it into a default preset. Update all file hashes after an
intentional adaptation and keep upstream/local change history in provenance.

Stage an upstream update separately. Compare against the pinned revision and current hashes.
Preserve local changes. Existing projects receive conflicts instead of silent replacement; use a
separate installation to compare and merge. Automatic three-way merges are not implemented.

## Presets, styles and roles

Add a JSON preset in `presets/` and a matching instruction file. Styles live independently in
`styles/` and `library/design/`. Default selections must reference reviewed packages. All four
roles use the selected design contract, stack instructions and shared catalog snapshot.

## Validation and recovery

Install requirements-dev.txt for YAML/JSON Schema checks, then run the validator and unit tests.
The initializer itself needs only standard-library Python 3.10+. Regenerate docs with
`python scripts/build-catalog-docs.py` after catalog changes.

A conflict stops writes; use another destination or explicitly merge. Hash mismatches mean source
content and the manifest differ. Reparse points are refused. An unexpected IO error can leave
newly created files but does not overwrite existing ones. Resolve the cause, inspect output and
rerun. Missing MCP tools and external runtimes must be configured separately on each computer.
