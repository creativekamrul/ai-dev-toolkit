# Start a project with the small team

Tell your coding agent:

> Read START-HERE.md. Help me set up a project with the Planner, Designer, Builder and Reviewer.
> Ask me to choose the stack, visual style and useful capabilities, then prepare the project
> instructions and start the first useful milestone.

## Instructions for the agent

This is a toolkit checkout, not the application to build. Inspect the available choices in
`presets/`, `styles/` and `manifests/catalog.json`. Ask a few useful questions at a time:

1. What are we building, who will use it, and is there an existing codebase?
2. Where should the project live? Prefer a separate project directory; do not replace this
   toolkit's AGENTS.md or generate an application inside its library.
3. Which stack? Include WordPress site/plugin/theme, HTML/CSS, PHP/Laravel, React/Next.js,
   backend and automation choices. Recommend based on the actual project; do not default to Next.js.
4. Which visual direction? Offer business, funky, glassmorphism, minimal, editorial, brutalist,
   existing design, custom references, or no UI. The user's choice controls the design.
5. Which database or integrations, if needed? Ask about Penpot only when useful. Skills do not
   provision those services or grant credentials.
6. Use the four-role team, or perform the same roles sequentially in solo mode?

Summarize the chosen stack, style and first milestone. Use the existing conversation's answers;
do not ask them again. Propose only relevant skills. Most of the central library remains inactive.

Save the answers as a local JSON configuration, then call `scripts/init-project.py --config
<answers.json> --destination <project-directory> --noninteractive --dry-run`. Inspect conflicts.
Install the agreed setup with `--yes`. The PowerShell wrapper supports the same options.
Use arguments or a JSON file, not interpolated shell code containing the user's project brief.

Default selections are reviewed. For an optional `screened` community/local package, inspect its
provenance, required tools, cross-skill links and executable files first. Explain unresolved
requirements. `--allow-screened` is an explicit opt-in, not a claim that the package is reviewed.
Never execute unreviewed scripts. Do not copy project-specific configs or credentials.

Open the destination and read its AGENTS.md. Run the Planner -> Designer -> Builder -> Reviewer
workflow. Use real native subagents only when supported; otherwise perform the roles sequentially
and label review as self-review. The central skills catalog is shared by all roles. Keep file
ownership clear and use `.ai-team/tasks.json` for task state. Deliver working behavior and evidence.

## Terminal alternative

```powershell
python scripts/init-project.py
# or
.\scripts\init-project.ps1
```

Python 3.10+ is the only initializer dependency. No API key or third-party Python package is
required to select and install project resources. Your coding agent provides the AI execution.
