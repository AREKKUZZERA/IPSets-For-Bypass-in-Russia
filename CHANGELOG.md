# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project follows a semver-friendly tag strategy (`vMAJOR.MINOR.PATCH`).

## [Unreleased]

## [0.4.0] - 2026-03-10
### Added
- CI/CD stage for release readiness with dedicated workflows:
  - validation + deterministic smoke check;
  - build artifact publication;
  - tag-driven release workflow;
  - scheduled update workflow that opens PRs.
- SHA256 checksum generation in `dist/checksums/` and checksum references in manifest.
- Release tag validation helper and deterministic build check script.
- Developer docs: `CONTRIBUTING.md`, `SECURITY.md`, release notes template.

### Changed
- Build manifest now includes deterministic metadata controls and checksum entries.

[Unreleased]: https://github.com/V3nilla/IPSets-For-Bypass-in-Russia/compare/v0.4.0...HEAD
[0.4.0]: https://github.com/V3nilla/IPSets-For-Bypass-in-Russia/releases/tag/v0.4.0
