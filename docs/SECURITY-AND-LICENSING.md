# Security, licensing and exclusions

The public tree contains actual reusable skill packages where license evidence supports copying.
Original sources remain untouched. Private filesystem inventories, staging checkouts, machine
paths, authentication files and credentials are excluded from Git. Review every intended public
file before publishing; ignore rules alone are not a security boundary.

Original toolkit code and authored resources are MIT licensed. Third-party resources keep their
original license text, notices and provenance. WordPress resources retain GPL-2.0-or-later terms
and a full GPL copy. Do not apply the toolkit's MIT license to third-party material. Some sources
publish a permissive SPDX declaration without a license file; those local imports retain the
attribution and corresponding standard license terms. Unknown or explicitly restricted terms
are recorded as exclusions rather than silently treated as public domain.

Local packages are content-addressed snapshots. Their original discovery names are namespaced
for installation; any additional adaptation is documented. Current upstream packages and local
snapshots may represent different versions and supporting resources. Keep that history rather
than deleting the user's copies based only on matching names.

Reviewed default packages have an explicit review record. Other packages are screened and
inactive by default. They may assume tools, paths, runtimes or agent frameworks not present on
a new computer. Inspect the package and executable files before use; do not treat static scanning
as a security certificate. Installing a skill is not permission to deploy, delete user data,
rewrite Git history or contact external people.

The scanners detect common token formats, private-key markers, known local-machine paths and
some private endpoint patterns. They can miss sensitive information and can flag harmless
examples. Runtime integrations must be configured on the new computer through the host's own
mechanism. Never move service credentials into this central repository.
