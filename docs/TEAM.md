# Team workflow

The Planner is the coordinator and single writer of the task ledger. The Designer owns visual
specifications. The Builder owns production changes. The Reviewer checks acceptance criteria
and identifies actionable defects. Use fewer stages for trivial work; this is a small team,
not a company simulation.

## Real execution versus role instructions

When the agent host exposes native delegation, the coordinator can dispatch bounded role tasks
using that host's supported mechanism. Reuse agents, limit the team to four active roles and
avoid overlapping writes. On hosts without delegation, or in solo mode, perform roles sequentially.
Report self-review honestly. The toolkit does not invent a native subagent configuration format.

## Shared knowledge and ownership

All roles read the project brief, design contract and shared catalog snapshot. Only relevant
installed skill bodies are loaded. Other central packages can be inspected and selectively
installed later. A catalog entry is not proof that an MCP service or runtime is connected.

Each handoff includes task ID, goal, acceptance criteria, owned paths, dependencies, selected
skill paths and expected evidence. The coordinator records status and unresolved decisions.
The Builder should not implement a different visual style without a user decision.

## Task ledger commands

Every generated project includes `.ai-team/team.py` (standard-library Python):

```bash
python .ai-team/team.py status
python .ai-team/team.py add --id page --title "Build the contact page" --owner builder --paths src/contact --acceptance "Keyboard usable; validation errors are visible"
python .ai-team/team.py transition --id page --status doing
python .ai-team/team.py transition --id page --status review --evidence "Tests and narrow/desktop browser checks passed"
python .ai-team/team.py transition --id page --status done --reviewer reviewer --evidence "Acceptance criteria checked; no remaining findings"
```

Run these from the project root or pass `--project`. Use `--reviewer self-review` when the same
agent performed the review. Task state changes enforce dependencies, evidence, and overlapping
active path ownership. A ledger entry records reported evidence; it cannot prove a model really
performed the review. Native tools still provide actual execution.

A crash can leave a `tasks.lock` or `tasks.next.json` file. Confirm no other writer is running,
inspect the ledger and recover the leftover files manually. Do not delete an active writer's lock.
