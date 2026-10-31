---
name: backend-implementation
description: "Implement backend and automation behavior in the chosen stack, focusing on contracts, authorization, failures, migrations and observable verification."
---

# Backend implementation

Inspect the selected language, framework, runtime versions, package scripts and existing service
boundaries. Keep the requested stack: Node, NestJS, Python, PHP and n8n have different conventions.
Define request/event inputs, validation, authorization, outputs and failure behavior before edits.

Keep secrets out of logs and repositories. Separate authentication from resource authorization.
Use bounded retries only where operations are safe to repeat, add idempotency for retryable writes,
and make timeouts and cancellation visible. Match database changes to the actual data lifecycle.
For automation inspect trigger, credentials, deduplication, retries and failure recovery; do not
enable live workflows or send real messages merely to demonstrate a setup.

Test the changed contract and failure paths using the available test infrastructure. Report
what was local, mocked or live. Record migration and operational prerequisites. Avoid replacing
existing architecture for an unrelated feature or assuming a provider integration is configured.
