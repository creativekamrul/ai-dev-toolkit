# Architecture

The toolkit has a passive central library and a focused active project installation.
`library/skills` holds original core workflows, `library/community` holds pinned upstream packages,
and `library/local` holds reusable local snapshots. Cloning brings bundled package files to the
new computer. The library is not copied wholesale into `.agents/skills`.

`presets/` chooses technology guidance. `styles/` chooses visual guidance independently.
`library/agents` defines the four portable roles. The one active toolkit skill is project-kickoff,
which routes a new project request to START-HERE.md.

The Python standard-library initializer builds a complete plan in memory, checks source hashes
and destination conflicts, then exclusively creates approved files. PowerShell is a thin argument
wrapper. No catalog strings are evaluated as shell commands. It rejects path traversal, linked
paths and file-as-directory parents. Unexpected IO failure can leave new files behind, but cannot
overwrite an existing file. This is not an atomic multi-file transaction or a defense against a
malicious concurrent process swapping directories.

Generated projects contain AGENTS.md, a Goose hint, chosen skill packages, a project brief,
design contract, four role definitions, a task ledger, compact selected-skill catalog, bounded offline search index and installation
receipt. A JSON answer file reproduces selection without adding machine paths to project config.

Catalog schema version 2 records identity, description, path, category, technologies, project
types, compatibility, dependencies, source, license, revision, review state, file allowlist and
SHA-256 hashes. The validator uses real YAML and JSON Schema parsers. Installations do not need
either dependency. Imported metadata is preserved except documented discovery-name/path changes.

Reviewed defaults are distinct from screened optional packages. Screening covers evidence and
static checks; it does not imply full behavioral compatibility. Local import revisions use content
hashes when no trustworthy upstream commit exists. Pinned upstream imports retain full commits.

The team uses real host delegation where available, otherwise sequential roles. No unsupported
native agent adapter is installed. Tool integrations and application scaffolding are separate
from selecting the AI resources.

## v0.3 project lifecycle

The root `toolkit.py` delegates to standard-library helpers. Preferences live only in ignored
`.local/preferences.json`; a project name resolves under the chosen projects root. Initialization
rejects every destination inside the checkout, not only its root. `manifests/curation.json` adds
explicit capabilities and compatibility rules on top of stack/style selections. Recommendations
explain why each default is selected; unknown optional packages are not assumed compatible.

The installed catalog contains selected metadata only. `tools.py search` reads a separate compact
index and returns a bounded shortlist (default 8, maximum 50). Detailed package bodies remain
passive until selected. `tools.py checkpoint/resume` saves brief state separately from the task
ledger; its claims must be checked against the current code. `doctor` probes tool availability only.

Skill changes compare baseline/current/incoming hashes before writes. AGENTS.md has one managed
skill-list block; its saved baseline permits preserving customized surrounding instructions.
Arbitrary skill conflicts require a manual merge. A transaction records prior bytes and expected
post-update hashes. Each file replacement is atomic; the whole multi-file update is recoverable,
not atomic. Partial updates retain a prepared journal. Rollback refuses to overwrite later edits.
