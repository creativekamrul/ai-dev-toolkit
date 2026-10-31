# Progress and verification

Updated 2026-11-01 (Asia/Dhaka), toolkit v0.3.0.

## Delivered

- Conversational startup through START-HERE, a Python-only launcher, private projects-root
  preference, and rejection of all destinations inside the toolkit checkout.
- 18 stack presets, 9 independent styles, explained recommendations, known compatibility checks,
  and reviewed database/testing capabilities.
- 779 actual packages: 638 reusable local snapshots, 132 community packages and 9 original skills.
  14 are reviewed; 765 remain screened optional packages. Originals and global settings unchanged.
- Compact selected-skill catalog plus bounded offline search of the full passive library.
- Concrete design preview/contract handoff, environment checks, checkpoints and resume.
- Skill add/check/update, preservation of custom instructions and working documents, conflict
  detection, recoverable per-file transactions and guarded rollback. Legacy projects gain missing
  resume resources without resetting their brief.
- Clear task transitions and a documented review handoff, refined through an independent forward test.

## Verified locally

- 42 behavior tests cover all stack/style defaults, interactive setup, capabilities, preferences,
  containment, PowerShell arguments, no-overwrite rules, update conflicts, later edits, interrupted
  transactions, rollback, legacy migration, search, checkpoint/resume and WordPress detectors.
- Catalog validation passes real YAML/JSON Schema parsing, hashes, allowlists, license evidence,
  curated defaults and compatibility combinations, and common secret-pattern checks.
- Skill Creator validator accepts the updated kickoff, design, delivery and database skills.
- Actual Codex CLI 0.148.0 app-server loader checks pass for current generated projects:

| Preset | Style | Database | Enabled skills | Selected catalog |
|---|---|---|---:|---:|
| HTML/CSS | Funky | None | 5 | 3,434 bytes |
| PHP | Glassmorphism | SQLite | 7 | 4,725 bytes |
| WordPress plugin | Funky | None | 7 | 5,205 bytes |
| Next.js | Editorial | None | 5 | 3,478 bytes |

All four use the testing capability. Loader errors: zero. These isolated loader checks make no
model call and do not establish arbitrary imported skill behavior. The former project catalog was
1,204,034 bytes; the new selected catalog is under 0.5% of that size in these cases. A separate
search index stays on disk and is queried for a bounded shortlist instead of loaded into context.

## Application evidence

An independent agent used the actual kickoff workflow to build a funky HTML event directory and
a business PHP member directory in separate project folders. It filled design contracts, tested
real runtime behavior, saved checkpoints, and resumed successfully. Its 20 browser evidence groups
cover keyboard controls, empty states, no-JS operation, PHP escaping and malformed input, narrow
and desktop layouts, and selected color contrast pairs. The portable checked-in harness repeats them.

A Next.js 16.4.3 / React 19.3.1 fixture passes a production build and Chromium checks for filtering,
empty/reset behavior, keyboard operation, layout overflow and browser exceptions. A WordPress
7.1.4 fixture activates the plugin in a disposable SQLite-backed site, verifies shortcode output
and escaping, and passes desktop/mobile Chromium rendering checks. Screenshots were inspected.
The pinned WordPress setup script was also rerun in a second empty directory successfully.

See evaluation/README.md for reproduction, versions and limits. These are small useful applications,
not proof of all 18 stacks, all 9 styles or every imported skill. Chromium-only checks are not a
complete accessibility/security audit. No real data, external application service or deployment was used.

CI runs helper validation/tests on Windows and Ubuntu, plus repeatable application checks on Ubuntu.
The GitHub Actions result is the authoritative status for the published revision.

## Review boundaries

Screened packages need task-specific path/tool/executable review and explicit selection. Some
require a connected service or original host tooling. Of 1,147 distinct original local definitions,
638 have bundled local packages; the remaining 509 stay references because of licensing, scope,
fixtures or content review. Private inventory paths and credentials remain excluded.

## Local audit results



All five drive traversals completed. Permission errors mean coverage is limited to accessible
paths. The scan included hidden and ignored directories; symlinks, archive contents, offline
cloud content and WSL/container filesystems were not followed or unpacked.

| Drive | Recognized resource files | Access/error lines |
|---|---:|---:|
| C: | 1,675 | 848 |
| E: | 0 | 4 |
| H: | 4 | 2 |
| I: | 0 | 4 |
| K: | 161 | 3 |

The original E: scan ran before creating the toolkit. These counts describe original resources.
The audit read 1,651 SKILL.md files and 185 other instruction/MCP documents, plus four lockfiles
and selected configuration metadata. It found 1,147 distinct skill entrypoint contents, 369
duplicate-content groups, 91 differing same-name groups, 279 folders with executables, 14 naming
flags and 166 folders with sensitivity-review flags. None of those flags alone proves a leak.

