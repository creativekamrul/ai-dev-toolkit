---
name: penpot-workflow
description: "Inspect or edit a Penpot design through an available Penpot MCP connection, preserving editable layers and verifying the resulting design."
---

# Penpot MCP workflow

Discover the available Penpot tools and read their high-level overview before executing code.
Consult the exposed API documentation for the specific types and methods needed; do not assume
Figma APIs or remembered Penpot methods are supported. If the connection is missing, report
the missing capability and provide a concrete design plan without claiming a file was edited.

Inspect the selected file, page, boards, component library and existing tokens. Resolve the
requested target from observed IDs and names. Preserve unrelated boards and user work.

Use native editable text, shapes, layout and components whenever practical. Keep layers named
by purpose and grouped into understandable boards or sections. Reuse existing components and
tokens. Use raster assets for imagery rather than flattening an entire interface into an image.

Make changes in bounded batches. Read each tool result and inspect the target after changes.
Distinguish a failed operation, a partial change and a confirmed success; do not blindly repeat
a mutation that may already have succeeded. Export or preview the affected board when available
and inspect spacing, clipping, type, alignment and responsive variants.

Report changed boards or nodes, visual verification performed, and unresolved tool errors.
Do not report a design as saved or edited solely because code was submitted to a tool.

