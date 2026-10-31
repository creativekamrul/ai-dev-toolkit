# Small project team

Four roles, one project: Planner -> Designer -> Builder -> Reviewer -> Builder fixes -> delivery.
The Planner is the coordinator and single writer of `.ai-team/tasks.json`. The user can combine
or skip stages for a small change; do not create ceremony for a typo fix.

Read the matching role file in `.ai-team/roles/` before performing a role. Share decisions through
the brief, design contract, task ledger and handoff evidence. Every task has one owner and clear
owned paths. Independent research/review can run concurrently; overlapping edits cannot.

In small-team mode, use real native subagents if the host supports them and team execution is
requested. Keep at most four active roles; the main agent can be the Planner. Each task packet
contains goal, acceptance criteria, relevant files/skills, owned paths, dependencies and expected
evidence. In solo mode, or when delegation is unavailable, perform the roles sequentially and
call the final check a self-review. Never claim four agents ran merely because these files exist.

Skill access is shared. `.ai-toolkit/catalog.json` is the searchable snapshot of the central
repository. Installed skill bodies are in `.agents/skills/`. Propose additional relevant skills
to the coordinator; do not copy the entire catalog into active context. Reference-only resources
require review/installation before use. The team's project files should not contain local machine
paths or credentials. Hosting and deployment remain separate authorized actions.
