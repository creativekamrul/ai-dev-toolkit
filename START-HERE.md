# Start by talking to your AI

Open this toolkit checkout in your coding agent and say what you want to build. For example:

> Create a restaurant website called Olive. Help me choose the stack and design, put it in
> a separate project folder, and start the first useful milestone.

Only Python 3.10+ is required for the toolkit. Your coding agent provides AI execution.
You do not need to install the library globally, create API keys or learn terminal commands.
The agent uses the helpers below on your behalf.

## Instructions for the agent

1. Read the user's request and reuse existing answers. Ask a few useful questions about the
   goal/audience, project name or existing code, stack, style and destination. Offer choices from
   `presets/` and `styles/`. Do not assume Next.js or business styling. Ask about a database,
   capabilities and integrations only when the project needs them. Default to the small four-role
   workflow, using sequential roles unless native delegation is supported and requested.
2. Inspect `python toolkit.py preferences` for an optional private projects directory. Without one,
   suggest a `projects` directory beside the toolkit checkout. The user may choose any separate
   destination. Never create a project inside the toolkit. Save a projects directory only when
   requested: `python toolkit.py preferences --projects-root <directory>`; this stays in `.local/`.
3. Use `python toolkit.py recommend --preset <id> --style <id> --database <id>` to get a small
   selection with reasons. Optional `--capabilities testing,database` adds reviewed workflows.
   Search additional candidates with `python toolkit.py search <topic> --limit 8`. Inspect a
   screened package's tools, paths and scripts before opting into it. Do not activate the library
   wholesale. User choices override generic skill preferences.
4. Save the agreed answers as an ignored `.local/answers-<name>.json` using the fields shown below.
   Preview with `python toolkit.py new --config <file> --name <name> --projects-root <directory>
   --noninteractive --dry-run`. An explicit `--destination <path>` also works. Inspect conflicts,
   then install the already agreed setup with `--yes`. Do not ask again for an action already
   authorized. Pass arguments as data; do not interpolate the user's brief into shell code.
5. Run `python toolkit.py doctor --project <destination>`. It reports missing executables without
   installing anything or changing credentials. Resolve project runtime requirements within the
   user's scope. Read the destination's AGENTS.md, brief, team instructions and design contract.
   Use the destination as the working directory for application work. If this host cannot switch
   its workspace, tell the user exactly which folder to open and give the continuation prompt.
6. Planner: define the first observable milestone and task ownership. Designer: record concrete
   tokens, layout and states, then show a representative preview in the chosen stack before
   expanding the UI. Reuse a clear existing direction; do not require extra choices for a small
   fix or an already specified design. Builder and Reviewer implement and check the milestone
   using docs/QUALITY-CHECKS.md. Keep the team small and label sequential review as self-review.
7. At a handoff or milestone, run `python .ai-toolkit/tools.py checkpoint --summary <what changed>
   --next <next task> --decision <decision> --evidence <actual result>` in the project. A new chat
   starts with `python .ai-toolkit/tools.py resume`, checks the current files and continues.

## Answer-file example

```json
{
  "preset": "php",
  "style": "glassmorphism",
  "team": "small",
  "brief": "A member directory for a local club",
  "audience": "Club members",
  "database": "sqlite",
  "capabilities": ["testing"],
  "integrations": [],
  "add_skills": [],
  "remove_skills": []
}
```

## Continuing in the new project

> Read AGENTS.md, run the project resume helper, and continue the next milestone. Preserve the
> selected stack and design direction. Use the small-team workflow and report actual checks.

For more skills or updates, use the central checkout's `toolkit.py skills` commands. Preview first;
customized skills are preserved or reported as conflicts. See docs/MAINTENANCE.md for rollback.
The terminal wizard remains available with `python toolkit.py new` or `scripts/init-project.ps1`.
