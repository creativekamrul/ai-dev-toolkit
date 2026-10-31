# Selecting, updating and recovering project skills

Use `python toolkit.py search <topic> --limit 8` in the toolkit, or the generated project's
`python .ai-toolkit/tools.py search <topic> --limit 8`. The advanced `scripts/search-catalog.py`
retains category/status/reference filters. Search loads metadata, never skill bodies or scripts.

## Existing project changes

```bash
python toolkit.py skills add --project <folder> --skill block-testing-strategy --dry-run
python toolkit.py skills update --project <folder> --dry-run
python toolkit.py skills check --project <folder>
python toolkit.py skills rollback --project <folder> --dry-run
```

Replace `--dry-run` with `--yes` to apply an agreed change. Repeated `--skill` options add several
skills. Screened packages require inspection and `--allow-screened`. Updated source files must
match the central catalog's hashes; use a trusted checkout/revision before updating.

The updater compares current, installed-baseline and incoming hashes. Unchanged installed files
can update; customized skills remain when upstream is unchanged. Conflicting upstream/custom
changes stop the entire preview before writes. Skill-list markers let AGENTS.md keep custom text
outside that block. Legacy AGENTS.md without a baseline must be unchanged to update automatically.
Briefs, design contracts, checkpoints and tasks remain project-owned. Unchanged generated role
instructions and helpers can update; customized versions require a manual merge. Older projects
receive missing resume state and quality-check instructions without resetting existing work.

Applied changes create `.ai-toolkit/history/<transaction>/` with prior bytes and before/after hashes.
`skills rollback --transaction <id>` selects a particular backup; omitting it selects the latest
restorable transaction. Rollback checks every current hash before restoring anything and refuses
to overwrite edits made after the update. Rollback itself is recorded and reversible.

History may contain private project instructions: keep `.ai-toolkit/history/` out of your project's
Git repository. Every transaction also has its own ignore-all file, including in legacy projects.
New projects receive the top-level ignore rule. For older repositories, add it to your
existing .gitignore without replacing its contents. Backups never leave the project automatically.

An unexpected IO error can leave a partial transaction marked `prepared`. After resolving the
underlying problem, inspect its journal and preview rollback. A crash may leave operation.lock;
confirm no writer is active before removing that lock. Checks protect ordinary concurrent changes,
but are not a defense against a malicious process replacing directories during the write window.

## Updating the central library

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
Preserve local changes. The project updater below compares hashes and manages its skill-list block.
Conflicting skill contents need a manual merge; it does not guess how to merge arbitrary skill code.

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
