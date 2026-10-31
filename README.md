# Universal AI Development Toolkit

Clone once. Tell your coding agent what you want to build. Choose a stack and visual style.
A small **Planner, Designer, Builder and Reviewer** team then works from one project brief,
design contract and shared skill catalog.

## Start here

```bash
git clone https://github.com/creativekamrul/ai-dev-toolkit.git
cd ai-dev-toolkit
```

Open the folder in your coding agent and say:

> Read START-HERE.md. Help me start a project. Ask me to choose the stack, visual style and
> useful skills, then set up the Planner, Designer, Builder and Reviewer team.

Or use the terminal wizard:

```powershell
python scripts/init-project.py
# Windows PowerShell entry point:
.\scripts\init-project.ps1
```

Python 3.10+ is required. The initializer uses only its standard library. Your coding agent
provides AI execution; this repo does not require its own API key or run a separate AI service.

## Choose the project, then the design

**18 presets:** WordPress site, WordPress plugin, WordPress theme, headless WordPress,
HTML/CSS/JavaScript, PHP, Laravel, Next.js, React/Vite, MERN, Express, NestJS, SaaS,
landing page, API service, n8n, Python, or another existing stack.

**9 visual directions:** business, funky, glassmorphism, minimal, editorial, brutalist,
match existing design, custom references, or no visual interface.

These choices are independent. A PHP app can use glassmorphism; a WordPress plugin can be funky;
a plain HTML site can be professional. Selecting a preset installs development resources,
not an entire application or its dependencies.

```powershell
.\scripts\init-project.ps1 -Destination ..\my-site -Preset html-css -Style glassmorphism -NonInteractive -DryRun
.\scripts\init-project.ps1 -Destination ..\my-plugin -Preset wordpress-plugin -Style funky -Brief "An event registration plugin" -NonInteractive -Yes
```

## A small team, with shared skills

| Role | Owns | Handoff |
|---|---|---|
| Planner | Goal, acceptance criteria, tasks and ownership | Bounded implementation plan |
| Designer | Chosen style, layout, tokens and component states | Design contract and visual expectations |
| Builder | Working code and relevant tests | Changed files and verification evidence |
| Reviewer | Requirement checks, regressions and actionable findings | Corrections or a scoped review result |

The generated `.ai-team/` contains roles and a task ledger. Real native subagents can perform
these roles when the host supports them. Otherwise one agent performs them sequentially and
reports a self-review. Role files do not themselves launch four AI processes.

Every role can search the central catalog. Only a focused selection is installed into the
project's `.agents/skills/`; the rest of the library stays out of active context.

## Real files, available after cloning

**778 bundled packages:** 638 reusable local snapshots, 132 community imports and 8 original
toolkit skills. Of the original 1,147 distinct local definitions, 509 remain references because
they need licensing/content review or belong to project, dependency or test-fixture contexts.

- `library/skills/`: original toolkit skills used by the setup flow.
- `library/community/`: pinned public community packages, with supporting files and licenses.
- `library/local/`: reusable licensed local skill snapshots, with supporting files and attribution.
- `manifests/catalog.json`: searchable bundled packages, review status and file hashes.
- `manifests/discovered-skills.json`: disposition of the original local discoveries.

The repository includes skill bodies, scripts, references and assets for bundled packages.
It does not merely link to the original computer. Project-specific configs, credentials and
packages with unresolved/restricted redistribution terms are excluded. Some plugin skills still
need their original service connection or runtime on another computer.

Default selections are **reviewed**. Other bundled packages are **screened**: license, metadata,
files and common secret patterns were checked, but their behavior and scripts are not certified.
Inspect these before use. `--allow-screened` explicitly permits installing a selected screened
package with a recorded review requirement. Nothing in the importer executes upstream scripts.

```bash
python scripts/search-catalog.py wordpress
python scripts/search-catalog.py design --status reviewed
python scripts/search-catalog.py --references
```

## Preservation and reproducibility

The installer previews every file. Conflicts stop it before writes, identical files are kept,
and there is no overwrite flag. It records selections in `.ai-toolkit/project.json` and hashes
in `.ai-toolkit/installed.json`. Reproduce a setup with `--config <project.json>` and a new destination.
No global Codex/Goose settings, credentials or MCP configuration are copied.

## Documentation

[Startup interview](START-HERE.md) · [Catalog](docs/CATALOG.md) · [Architecture](docs/ARCHITECTURE.md) ·
[Team workflow](docs/TEAM.md) · [Imports and updates](docs/MAINTENANCE.md) ·
[Licensing and exclusions](docs/SECURITY-AND-LICENSING.md) · [Validation results](PROGRESS.md)

For development checks, install `requirements-dev.txt`, then run:

```bash
python scripts/validate.py
python -m unittest discover -s tests -v
```

Toolkit code is MIT licensed. Third-party packages retain their own licenses, including GPL
for the WordPress collection. See each package's license and provenance files.
