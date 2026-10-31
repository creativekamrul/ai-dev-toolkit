# Universal AI Development Toolkit

Keep one central skill library. Describe a project to your coding AI. It helps you choose a stack
and design, creates a separate project folder, and works through Planner, Designer, Builder and
Reviewer roles. Small changes can use fewer stages; hosts without delegation use sequential roles.

## What belongs here

Use this repository with an existing coding-agent harness. The harness reads and edits files,
searches code, runs commands, calls available tools and enforces permissions. The toolkit supplies
project instructions, design expertise, framework/database guidance, verification criteria and
small-team handoffs. Its helpers manage project resources and state; they are not a replacement harness.

Basic-operation wrappers are excluded. Specialist skills such as WordPress development, design
systems and database optimization remain useful because they guide decisions beyond tool execution.
The original discovery index is historical audit data, not the installable or recommended skill list.

## Clone, open, talk

```bash
git clone https://github.com/creativekamrul/ai-dev-toolkit.git
cd ai-dev-toolkit
```

Open this folder in your coding agent and say:

> Read START-HERE.md. Create a project called Olive. Help me choose the stack and design,
> put it in a separate project folder, and start the first useful milestone.

The AI asks only for missing choices, previews the setup, and creates the project elsewhere.
Python 3.10+ is the only toolkit requirement. No global skill installation, API key or separate
AI service is needed. Your coding agent provides AI execution and builds the application.

When continuing in the new folder, say:

> Read AGENTS.md, run the project resume helper, and continue the next milestone.

[START-HERE.md](START-HERE.md) contains the complete agent-facing flow. If your host cannot switch
workspaces, open the new project folder when instructed. Skill files do not launch agents by themselves.

## Your choices stay independent

**18 stack presets:** HTML/CSS/JavaScript, PHP, Laravel, WordPress site/plugin/theme/headless,
Next.js, React/Vite, MERN, Express, NestJS, SaaS, landing page, API service, n8n, Python and custom.

**9 design directions:** business, funky, glassmorphism, minimal, editorial, brutalist,
match existing, custom references and no UI. The Designer records concrete tokens and states,
prepares a representative preview, and checks narrow/desktop rendering before expanding the UI.

Database selections now add a reviewed database workflow. Optional testing capability adds a
reviewed test strategy. Explicit routing rules explain selections and reject known stack/style
mismatches. Arbitrary imported skills still need task-specific compatibility review.

## Included and portable

**776 actual packages:** 635 reusable local snapshots, 132 community imports and 9 toolkit skills,
with supporting files, licenses and provenance. Of these, 14 are reviewed; 762 are screened optional
packages. Project-specific/restricted material and private inventories remain excluded.

Only selected packages are copied into each project's `.agents/skills/`. A compact catalog lists
installed skills and why they were selected. A separate offline search index returns a short list;
the AI does not need to load the whole library. Some optional skills require their original tools.

The generated project also receives its brief, design contract, quality checks, team roles,
task ledger, checkpoint/resume helper and hashed installation receipt.

## Optional commands (the AI can run these for you)

```bash
# Remember a projects directory privately in this checkout:
python toolkit.py preferences --projects-root ../projects

# Preview an agreed project:
python toolkit.py new --name olive --preset php --style glassmorphism --database sqlite --capabilities testing --noninteractive --dry-run

# Inspect choices and tools:
python toolkit.py recommend --preset php --style glassmorphism --database sqlite
python toolkit.py doctor --project ../projects/olive

# Inside the generated project:
python .ai-toolkit/tools.py search "php escaping" --limit 5
python .ai-toolkit/tools.py resume
```

Use `--yes` instead of `--dry-run` to install the agreed setup. No project can be created inside
the toolkit checkout. Conflicts stop creation before writes. Preferences and original-machine
paths are not committed; choose a projects directory again on another computer if needed.

## Safe changes as projects grow

From the central checkout:

```bash
python toolkit.py skills add --project ../projects/olive --skill block-testing-strategy --dry-run
python toolkit.py skills update --project ../projects/olive --dry-run
python toolkit.py skills check --project ../projects/olive
python toolkit.py skills rollback --project ../projects/olive --dry-run
```

Apply with `--yes`. Updates preserve working briefs, designs and checkpoints. Conflicting edits
stop the update; local skill edits survive when upstream is unchanged. Managed skill-list updates
preserve surrounding AGENTS.md instructions. Every applied change has a restorable local backup.
Rollback refuses to overwrite edits made afterward. See [maintenance](docs/MAINTENANCE.md).

## Verification and documentation

[Validation results](PROGRESS.md) · [Outcome evaluation](evaluation/README.md) ·
[Catalog](docs/CATALOG.md) · [Team](docs/TEAM.md) · [Architecture](docs/ARCHITECTURE.md) ·
[Compatibility](docs/COMPATIBILITY.md) · [Licensing](docs/SECURITY-AND-LICENSING.md)

Development checks: install `requirements-dev.txt`, run `python scripts/validate.py`, then
`python -m unittest discover -s tests -v`. Optional browser/application fixtures are separate
from normal project setup. CI checks Windows/Ubuntu helpers and representative application outcomes.

Original toolkit code is MIT licensed. Third-party packages retain their own licenses; the
WordPress evaluation plugin is GPL-2.0-or-later. See package notices and THIRD-PARTY-NOTICES.md.
