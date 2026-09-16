# Versioning and releases

The root `plugin.json` is the package identity and version authority. One SemVer
version covers this repository; other language packs release independently.
Skill names, paths, scope, invocation expectations and required environment form
the public contract. PATCH corrects behavior within that contract; MINOR adds
compatible capabilities; MAJOR changes or removes an existing contract.
A description change can affect activation and is not automatically cosmetic.

Update `plugin.json` and CHANGELOG.md, then run `python scripts/distribution.py sync`.
The native manifests are derived views; CI rejects version or metadata drift.
Skill files do not receive a package-version bump just to change their hashes.

Run `python scripts/distribution.py check` and the installation smoke command
in docs/distribution.md. CI validates the format and distributable; semantic
skill changes additionally need focused behavioral evaluation. An installation
pass is not proof of quality across all models. Use the focused
[comparison protocol](behavioral-evaluation.md) and record actual outcomes in
[results](evaluation-results.md) before publishing semantic instruction changes.

The 1.0.1 candidate corrects scope, routing, and completion within existing
skills; it changes no skill names, paths, installation independence, or required
environment. This is a PATCH correction under the contract above, not a claim
that descriptions are cosmetic. Keep installation examples on a published ref
until the candidate is released; a metadata bump does not publish a tag.

Release from a reviewed, green commit. Push `vX.Y.Z` matching plugin.json.
The release workflow validates that exact tag, builds one skills-only archive,
records file hashes and commit identity, and uploads all assets before publishing.
Enable GitHub release immutability in repository settings. Published versions
and their assets must never be replaced; corrections receive a new version.

The author marketplace pins each pack's release commit. After a release, update
that catalog's ref and SHA in a reviewed change. Claude versions affect cache
updates; always bump the native plugin version with the release. Do not put a
second version in the marketplace entry. Consumers use one manager per installed
copy and review instruction changes before updating a working project.
