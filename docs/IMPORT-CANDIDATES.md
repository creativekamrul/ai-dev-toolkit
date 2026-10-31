# Migration and inclusion decisions

Reusable skills are bundled as actual files in library/local; additional pinned community packages
live in library/community. Consult manifests/local-imports.json for local inclusion/exclusion
reasons and manifests/imports for per-collection results. The catalog links every included package.

The original scan found 1,651 SKILL.md files with 1,147 distinct entrypoint contents. Duplicated
installations were grouped by content; differing versions and supporting resources remain
traceable. The public discovery index contains no original filesystem paths or credential values.

Excluded categories include project-specific and dependency installations, restricted or unresolved
license terms, and private/machine-specific content. A file being available on the original
computer does not itself permit public redistribution. Some explicitly proprietary plugin skills
must be installed through their provider on the next computer instead.

License and static screening is distinct from behavioral review. Most of the broad library is
screened and inactive by default. The installer uses reviewed selections and requires an explicit
opt-in for screened additions. Do not interpret a large catalog as a recommendation to load it all.
