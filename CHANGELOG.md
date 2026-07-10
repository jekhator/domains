# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-07-09

### Added

- **Monorepo consolidation**: Consolidated five domain packages into a single distribution:
  - `domain-errors` 0.2.0: Typed domain error hierarchy with wrapping and chaining
  - `domain-security` 0.2.0: Security context management and authorization checks
  - `domain-api-limiter` 0.2.0: Request rate limiting and quota enforcement
  - `domain-monitoring` 0.1.0: Event monitoring and telemetry
  - `domain-aspects` 0.1.1: Composable decorators for cross-cutting concerns

- **Unified testing**: Consolidated pytest configuration, coverage tracking, and test discovery across all five packages. Merged root conftest fixtures for security context and monitoring registry reset.

- **Unified CI/CD**: Single `.github/workflows/` with six shared workflows:
  - `ci.yml`: Full test suite with coverage reporting
  - `cleanup-guard.yml`: Directory structure validation
  - `dto-strict.yml`: Per-package DTO validation and line-count gatekeeping
  - `no-ai-attribution.yml`: Attribution verification (zero Claude markers in commits/PRs)
  - `publish.yml`: PyPI publication via trusted publishers (gated by James)
  - `ruff.yml`: Linting and formatting checks

- **Dynamic versioning**: All five packages version-locked to `0.1.0` via `domain_errors/config/_version.py`, with hatch dynamic resolution in unified `pyproject.toml`.

- **Dissolved inter-package dependencies**: `domain-errors`, `domain-security`, `domain-api-limiter`, and `domain-monitoring` are no longer external dependencies within the distribution (imports resolve within the bundled `domain-suite` dist). `domain-aspects` optional extras re-scoped: `logging` (external `mixin-logging>=0.6.0`), `sensitivity` (external `mixin-sensitivity>=0.4.0`), `all` (both external packages).

- **Test consolidation**: Migrated all `domain-aspects` tests from top-level `tests/test_aspects/` into `domain_aspects/services/tests/test_aspects/` per concern-scoped layout. Single merged root `conftest.py` houses autouse fixtures for security context reset and monitoring registry reset.

- **Documentation structure**: Per-package documentation in `docs/<package>/` with historical changelogs preserved as `CHANGELOG-history.md`.

### Changed

- **Package structure**: No API changes to any package; purely organizational consolidation.

### Internal

- Single `pyproject.toml` with unified build configuration, test paths, coverage tracking, and tool settings.
- Shared `.github/workflows/` for CI/CD across all five packages.
- Root `uv.lock` coordinating dependencies for all packages.

---

For detailed changes to individual packages before consolidation, see:

- `docs/domain_errors/CHANGELOG-history.md`
- `docs/domain_security/CHANGELOG-history.md`
- `docs/domain_api_limiter/CHANGELOG-history.md`
- `docs/domain_monitoring/CHANGELOG-history.md`
- `docs/domain_aspects/CHANGELOG-history.md`
