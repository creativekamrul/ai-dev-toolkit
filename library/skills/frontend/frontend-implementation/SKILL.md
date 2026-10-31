---
name: frontend-implementation
description: "Implement or repair frontend behavior in an existing React or Next.js project, using its installed versions, component conventions and validation commands."
---

# Frontend implementation

Read the package manifest, lockfile, route structure and nearby components before editing.
Find the existing component library and shared data/state conventions. Reuse them and keep the
scope tied to the requested behavior. Use the project's installed framework version when
consulting official documentation; do not assume the newest API or add a framework by default.

Trace user input through state, data access and rendering. Keep secrets and privileged logic
on the server. In Next.js, inspect the router in use and place client boundaries only where
browser APIs or interaction require them. Make loading, retry and failure states usable.

Use semantic elements and typed component contracts. Preserve existing keyboard behavior and
focus after dialogs, navigation and validation. Avoid introducing state libraries for a local
interaction, duplicating derived state, or coupling unrelated page logic into a shared component.

For visual decisions follow the project's chosen design standards; this workflow does not
prescribe an aesthetic. Verify the changed behavior with the project's available build, lint,
type-check and relevant tests. Read script definitions before running them. Do not invent a
successful command or install tooling merely because a common script is missing.

Report the implemented behavior, checks performed and any setup or integration still required.

