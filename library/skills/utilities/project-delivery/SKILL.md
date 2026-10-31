---
name: project-delivery
description: "Coordinate a small project team from requirements through a verified delivery, with explicit task ownership and handoffs."
---

# Project delivery

Read the project brief and selected stack before choosing work. The Planner translates the user
goal into observable acceptance criteria and a small first deliverable. Separate unresolved
questions from reasonable assumptions. Inspect existing code and dependencies before planning.

Use `.ai-team/tasks.json` as the shared task ledger. A task has id, title, owner (planner,
designer, builder or reviewer), status (todo, doing, blocked, review or done), dependencies,
ownedPaths, acceptanceCriteria, and evidence. Only the coordinator edits the ledger to avoid
simultaneous writes. Do not mark a blocked task complete or fabricate reviewer approval.

The Designer records visual tokens, component states, layout and responsive behavior in the
design contract. The Builder delivers a small functional slice using that contract. The Reviewer
compares behavior to acceptance criteria and reports reproducible findings with file references.
The Builder fixes actionable findings; the Reviewer checks the changed behavior again.

Delegate only when the host exposes a real agent mechanism and team execution is requested.
At most four active roles are needed. Give each delegated task its goal, relevant files, skill
paths, constraints, owned paths and expected evidence. Do not assign overlapping writes.
With one agent, explicitly switch roles and describe that review as a self-review.

Keep handoffs short: decisions, changed files, tests, unresolved issues, next owner. Ask the user
only for choices that materially affect the outcome. Preserve existing authorization; no repeated
approval for routine reversible work. Deployment, publication or messaging follow the user's scope.

Tasks move `todo -> doing -> review -> done`; completion needs evidence and an explicit reviewer
label. Review the Builder's existing task, then complete it; a separate review task depending on
that task being done would block its own prerequisite. Record a checkpoint at handoff with
`python .ai-toolkit/tools.py checkpoint`; resume via `python .ai-toolkit/tools.py resume` and
verify the current files before trusting saved notes. See `.ai-team/TEAM.md` for command examples.
