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

Skill access is shared. `.ai-toolkit/catalog.json` describes installed skills and selection reasons.
Search the full passive index with `python .ai-toolkit/tools.py search <topic> --limit 8`;
do not load the index into chat context. Installed skill bodies are in `.agents/skills/`. Propose additional relevant skills
to the coordinator; do not copy the entire catalog into active context. Reference-only resources
require review/installation before use. The team's project files should not contain local machine
paths or credentials. Hosting and deployment remain separate authorized actions.

The task state sequence is `todo -> doing -> review -> done`. A blocked task resumes through
`blocked -> todo -> doing`; the Reviewer can send `review -> doing` for corrections.
Use `python .ai-team/team.py --help` and its subcommand help for the actual options.

The Reviewer normally reviews the Builder's existing task, then the coordinator marks that
same task done with evidence and `--reviewer reviewer` (or `--reviewer self-review` for sequential
roles). Do not create a review task depending on the Builder task being done: dependencies must
be done before a dependent task starts, so that would block the review needed for completion.
Ownership paths are write ownership; read-only review does not claim the Builder's paths.

Example handoff:

```text
python .ai-team/team.py transition --id build --status review --evidence "Build passed; preview inspected"
python .ai-team/team.py transition --id build --status done --evidence "Requirements checked; no remaining findings" --reviewer self-review
```

At a milestone or handoff, save a concise checkpoint with `.ai-toolkit/tools.py checkpoint`.
A new chat starts with `.ai-toolkit/tools.py resume`, then verifies current files and evidence.
