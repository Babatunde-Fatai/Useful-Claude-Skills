---
name: social-auth
description: Implement OAuth2/OIDC social login provider integrations (Google/GitHub/Apple/LinkedIn/Twitter), including provider setup, callback handling, token exchange, session strategy, and account linking across common frameworks. Use for social-auth flows only; not for password-only auth or generic JWT debugging.
---

## Quick Navigation

1. Read `references/AGENT_EXECUTION_SPEC.md` first.
2. Mandatory governance reads:
- `references/governance/env-contract.md`
- `references/governance/error-edge-cases.md`
- `references/governance/account-linking.md`
- `references/governance/testing-validation.md`
- `references/governance/output-template.md`
3. Provider docs:
- `references/providers/{provider}/CREDENTIALS.md`
- `references/providers/{provider}.md`
4. Pattern baseline:
- `references/patterns/oauth-flow-core.md`

## Mandatory Start (No Code)

1. Produce Discovery Report before code changes.
2. Confirm provider(s), framework, deployment domain(s), callback URL(s), and session strategy.
3. Run deterministic checks before implementation:
- `scripts/translate-provider-credentials.py`
- `scripts/validate-redirect-uri.py`
4. If required discovery fields are unknown, stop and ask.

## Minimal Required Reads By Scenario

- Frontend-only scope:
1. `references/AGENT_EXECUTION_SPEC.md`
2. `references/patterns/session-handling.md`
3. Matching adapter reference for frontend framework

- Backend-only social callback scope:
1. `references/AGENT_EXECUTION_SPEC.md`
2. Provider credential docs
3. `references/patterns/oauth-flow-core.md`
4. Matching backend adapter reference
5. Governance references

- Existing auth stack with account linking:
1. `references/AGENT_EXECUTION_SPEC.md`
2. `references/patterns/existing-auth-integration.md`
3. `references/governance/account-linking.md`
4. `references/patterns/data-models.md`

## Routing Logic

Provider routing:
- Google: `references/providers/google/CREDENTIALS.md`, `references/providers/google.md`
- GitHub: `references/providers/github/CREDENTIALS.md`, `references/providers/github.md`
- LinkedIn: `references/providers/linkedin/CREDENTIALS.md`, `references/providers/linkedin.md`
- Apple: `references/providers/apple/CREDENTIALS.md`, `references/providers/apple.md`
- Twitter/X: `references/providers/twitter/CREDENTIALS.md`, `references/providers/twitter.md`

Adapter routing:
- Express: `references/adapters/express-patterns.md`
- Next.js: `references/adapters/nextjs-patterns.md`
- Node custom server: `references/adapters/vanilla-node-patterns.md`
- Laravel: `references/adapters/laravel-patterns.md`
- Django: `references/adapters/django-patterns.md`
- Flask: `references/adapters/flask-patterns.md`
- Rails: `references/adapters/rails-patterns.md`
- Vue frontend + backend adapter pairing: `references/adapters/vue-patterns.md`
- Unknown stack: `references/adapters/pseudocode-patterns.md`

## Forbidden Practices

- Do not use implicit flow.
- Do not skip `state`/`nonce` checks.
- Do not use wildcard redirect URIs.
- Do not store provider tokens in localStorage.
- Do not log auth codes/tokens/secrets.
- Do not trust unverified email claims as identity proof.

## Stop Conditions

Stop and ask if any of these are missing:
- Provider client credentials.
- Allowed redirect URIs.
- App framework/runtime.
- Session strategy.
- Account-linking policy.
- Secret rotation strategy.

## Required Output Contract

- Narrative output must follow `references/governance/output-contract.md`.
- Machine-readable output must validate against `references/governance/output-schema.json`.
- Use `references/governance/output-template.md`.
- Validate generated JSON with `scripts/validate-output-schema.py`.

## Deterministic Script Interface

All scripts follow `references/governance/script-io-convention.md`:
- Input: JSON via file path or stdin.
- Output: `ok`, `tool`, `errors`, `warnings`, `result`.
- Exit code: `0` pass, `1` fail.

## Multi-Provider Invariant

Design routes and account-linking data so adding providers does not break existing providers.

## Documentation Freshness

Provider reference files are guidance. Verify current provider docs before coding if uncertainty exists.
