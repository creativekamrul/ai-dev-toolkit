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
design contract, four role definitions, a task ledger, shared catalog snapshot and installation
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
