# domain-suite Documentation

This directory contains comprehensive documentation for all five packages in the domain-suite distribution.

## Packages

### [domain-errors](domain_errors/)

Typed domain error hierarchy with wrapping and chaining for Python services.

- **Key concepts**: DomainError base class, error classification, error chaining, exception wrapping
- **Use when**: Building typed exception hierarchies, wrapping third-party library exceptions
- **Documentation**: [domain_errors/README.md](domain_errors/README.md)

### [domain-security](domain_security/)

Cross-cutting security concerns: authorization, tenancy, secrets, and context management.

- **Key concepts**: Security context, authorization checks, tenant isolation, secret management
- **Use when**: Enforcing access control, managing multi-tenant boundaries, handling API credentials
- **Documentation**: [domain_security/README.md](domain_security/README.md)

### [domain-api-limiter](domain_api_limiter/)

Request rate limiting and quota enforcement for Python services.

- **Key concepts**: Throttle policies, rate limits per tier, quota tracking
- **Use when**: Protecting APIs from abuse, enforcing tier-based rate limits
- **Documentation**: [domain_api_limiter/README.md](domain_api_limiter/README.md)

### [domain-monitoring](domain_monitoring/)

Event monitoring and telemetry for cross-cutting concerns.

- **Key concepts**: Event sinks, metric collection, monitoring registry
- **Use when**: Tracking performance metrics, collecting domain events, integrating with observability systems
- **Documentation**: [domain_monitoring/README.md](domain_monitoring/README.md)

### [domain-aspects](domain_aspects/)

Composable decorators for logging, auth, throttling, error wrapping, and sensitivity masking.

- **Key concepts**: Aspect composition, cross-cutting concerns, decorator stacking
- **Use when**: Applying multiple concerns to a function (logging + auth + throttling), reducing boilerplate
- **Documentation**: [domain_aspects/README.md](domain_aspects/README.md)

## Documentation Structure

Each package directory contains:

- **`README.md`**: Quick-start guide and API overview
- **`apps/`**: Feature-level documentation for each service or component
- **`audits/`**: Security audit reports for each feature
- **`reviews/`**: Code review summaries for each feature
- **`CHANGELOG-history.md`**: Version history before consolidation into domain-suite

## Getting Started

1. Install domain-suite: `pip install domain-suite` or `uv add domain-suite`
2. Read the [main README](../README.md) for installation options and examples
3. Choose a package based on your use case (above)
4. Refer to the feature docs in the package's `apps/` directory

## Consolidation Notes

All five packages were consolidated into a single distribution in v0.1.0 (July 2026). Each package retains its original public API and namespace.

For version history prior to consolidation, see the `CHANGELOG-history.md` file in each package directory.
