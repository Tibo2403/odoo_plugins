# Security Policy

## Supported version

Security fixes target the current default branch and Odoo 16, which is the
version declared by the addon manifests. Other Odoo versions are not supported
unless documented explicitly.

## Reporting a vulnerability

Use GitHub's private vulnerability reporting or open a private security
advisory in this repository. Do not disclose customer databases, access
tokens, business records, or exploitable details in a public issue.

Include the affected addon, Odoo edition and version, impact, reproduction
steps, and a minimal redacted example when possible.

## Deployment safety

Test addons on a non-production database first. Review access-control rules,
record rules, scheduled jobs, migrations, backups, and rollback procedures
before production installation.
