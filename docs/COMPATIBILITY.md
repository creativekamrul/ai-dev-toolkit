# Compatibility evidence

Checked locally on 2026-11-01. The installer requires Python 3.10+ and no third-party Python
packages. Maintenance validation requires `requirements-dev.txt`. The PowerShell wrapper is
covered by tests on PowerShell 7. The reviewed WordPress detectors require Node.js.

Codex CLI 0.148.0 discovered every selected skill in four generated projects: HTML/CSS,
PHP, WordPress plugin and Next.js. The checks used the real app-server skills/list protocol,
with an isolated home and no model invocation. See PROGRESS.md for counts and scope.
Start the coding agent in the generated project. An existing chat may need a skill refresh.

AGENTS.md, `.agents/skills/`, portable role instructions and `.goosehints` are generated.
Goose and other hosts may require their skill extension or an explicit instruction to read these
files. Their runtime behavior has not been verified here. Where native subagents are unavailable,
the team workflow uses sequential roles and labels its review as self-review.

Only selected skill packages are copied to active discovery paths. The central catalog is shared
metadata; other skills are available from the toolkit checkout. Additional screened packages may
include nested platform entrypoints, old cross-skill paths or original-host tool dependencies.
Review those before activation. No connection credentials are included.

The defaults are workflow resources, not generated production applications. Your coding agent
uses the brief, selected stack and design contract to implement the application. WordPress/PHP,
Node, database and design-service runtimes must be available where the actual project runs.

Git attributes preserve exact package bytes so catalog hashes remain valid across operating
systems. CI runs validation and behavior tests on Windows and Ubuntu; a passing loader test on
Windows does not establish universal runtime compatibility or design quality.
