# Security Policy

## Supported Versions
Only the latest main branch is supported for security updates.

## Reporting a Vulnerability
Please open a private security advisory or contact the maintainer directly. Do not open public issues for vulnerabilities.

## Security Architecture Highlights
- No hardcoded secrets; use environment variables or secure vaults
- All API keys encrypted at rest
- Audit logging for all trading signals and data access
- Rate limiting and anomaly detection on data ingestion
- Dependency scanning via Dependabot and CI
- gitleaks for secret detection

See docs/security-architecture.md for full details.
