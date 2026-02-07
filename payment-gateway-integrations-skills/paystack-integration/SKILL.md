---
name: paystack-integration
description: Implement Paystack payments safely in Node/Next/Express, including checkout initialization, backend verification, webhook handling, and subscriptions for NGN/African-market payments. Use only for Paystack integrations; not for Flutterwave/Stripe or generic payment questions.
---

# Paystack Integration

## Start Here

1. Read `references/AGENT_EXECUTION_SPEC.md` first.
2. Reuse local payment router baseline: `references/payment-router-template.md`.
3. Choose only the scenario files you need:
- Frontend checkout (redirect/popup): `references/one-time-payments.md`
- Backend initialize/verify handlers: `references/express-implementation.md` or `references/nextjs-implementation.md`
- Webhooks and event lifecycle: `references/webhooks.md`
- Recurring billing/subscriptions: `references/subscriptions.md`
- Troubleshooting production issues: `references/troubleshooting.md`
4. Use script checks before finalizing implementation:
- Payment/reference/amount checks: `scripts/validate-payment-contract.py`
- Webhook preconditions and signature handling: `scripts/check-webhook-contract.py`

## Minimal Required Reads By Task

- Frontend-only popup/redirect tasks:
1. `references/AGENT_EXECUTION_SPEC.md`
2. `references/one-time-payments.md`
3. `references/quick-reference.md`

- Backend verification tasks:
1. `references/AGENT_EXECUTION_SPEC.md`
2. `references/core-implementation.md`
3. `references/io-contracts.md`
4. Run `scripts/validate-payment-contract.py`

- Webhook tasks:
1. `references/AGENT_EXECUTION_SPEC.md`
2. `references/webhook-playbook.md`
3. `references/io-contracts.md`
4. Run `scripts/check-webhook-contract.py`

- Subscription tasks:
1. `references/AGENT_EXECUTION_SPEC.md`
2. `references/subscriptions.md`
3. `references/io-contracts.md`

## Reliability Invariants

- Initialize transaction first, then persist Paystack-generated `reference`.
- Store and compare amounts in smallest currency unit (kobo/pesewas/cents).
- Never fulfill from frontend callback alone; always verify on backend.
- Verify webhook signature using raw request body before parsing.
- Enforce idempotency: if order is already paid, return no-op.
- Fulfill only when verified status is success and amount/reference match expected DB values.

## I/O Contracts

- Read `references/io-contracts.md` for required inputs, outputs, and error envelope.
- Validate machine-readable output against `references/output-schema.json`.

## Deterministic Script Interface

All scripts in this skill follow `references/script-io-convention.md`:
- Input: JSON file path or JSON via stdin.
- Output: JSON object with `ok`, `tool`, `errors`, `warnings`, and `result`.
- Exit code: `0` for success, `1` for validation failure.

## Standard Response Contract

Respond using `references/output-contract.md`:
1. Summary
2. Artifacts
3. Next actions
4. Machine-readable JSON (`decisions`, `risks`, `required_inputs`, `validation_results`)

## Reference Index

- Quick config and currency rules: `references/quick-reference.md`
- Core backend flow: `references/core-implementation.md`
- Webhook flow and idempotency: `references/webhook-playbook.md`
- Existing deep implementation guides:
- `references/implementation-patterns.md`
- `references/one-time-payments.md`
- `references/express-implementation.md`
- `references/nextjs-implementation.md`
- `references/webhooks.md`
- `references/subscriptions.md`
- `references/troubleshooting.md`
