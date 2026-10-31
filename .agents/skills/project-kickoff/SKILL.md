---
name: project-kickoff
description: "Start a project from this toolkit by interviewing the user about goals, stack, design style and team setup, then installing a focused set of resources."
---

# Project kickoff

Read `START-HERE.md` from the toolkit repository root and follow its interview and setup flow.
Reuse answers already supplied in the conversation. Offer the actual available presets and
styles; do not assume Next.js or business styling. Keep the destination separate from the toolkit.

Use the shared catalog to select a small relevant skill set. Preserve existing files, preview the
installation and use the user's existing authorization. After setup, read the destination's
AGENTS.md and coordinate its Planner, Designer, Builder and Reviewer roles using supported host
capabilities. Do not pretend role files launch subagents on their own.

Use the standard-library `toolkit.py` helpers for preferences, recommendations, preview, installation
and environment checks. Start a new chat in a generated project with its resume helper. The project
search helper returns a bounded shortlist; do not read the entire passive library or search index.
