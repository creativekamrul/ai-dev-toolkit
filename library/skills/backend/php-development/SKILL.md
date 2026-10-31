---
name: php-development
description: "Develop or repair PHP applications using the project framework and installed PHP version, safe input handling and reproducible validation."
---

# PHP development

Inspect PHP version, Composer manifest, entrypoints, routing and existing framework conventions.
For plain PHP keep includes and responsibilities clear. For Laravel or another framework use its
existing routing, validation, migrations and template facilities; do not build a competing stack.

Treat input, authorization and output encoding as separate boundaries. Use prepared queries or
the established query builder; escape output for its rendering context. Keep credentials outside
web roots and source control. Use established password hashing, session and CSRF facilities.
Never implement authorization solely in the browser. Avoid returning internal errors to users.

Choose database changes with reversibility and existing data in mind. Preserve the user's schema
and seed conventions; do not run destructive migrations without task authorization. Validate
syntax with the installed PHP and run the repository's tests/static checks when present. Do not
claim integration coverage when only syntax was checked. Follow the project design contract
for rendered templates, including non-business aesthetics.
