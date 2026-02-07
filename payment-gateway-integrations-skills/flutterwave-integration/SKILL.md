---
name: flutterwave-integration
description: Implement Flutterwave payment flows (card, transfer, USSD, mobile money), backend verification, webhooks, and subscriptions in Node/Next/Express for African-market payments. Use only for Flutterwave integrations; not for Paystack/Stripe or generic payment debugging.
---

# Flutterwave Integration

## Start Here

1. Read `references/AGENT_EXECUTION_SPEC.md` first.
2. Reuse local payment router baseline: `references/payment-router-template.md`.
3. Select only the scenario files required:
- One-time checkout: `references/one-time-payments.md`
- Backend routes/handlers: `references/express-implementation.md` or `references/nextjs-implementation.md`
- Webhooks and confirmation lifecycle: `references/webhooks.md`
- Mobile money: `references/mobile-money.md`
- Subscriptions: `references/subscriptions.md`
- Bank transfer/payout flows: `references/bank-transfers.md`
4. Run script checks before finalizing:
- Verify payload and status contract: `scripts/validate-verify-response.py`
- Webhook signature mode contract: `scripts/check-webhook-signature-mode.py`

## Minimal Required Reads By Task

- Mobile-money-only task:
1. `references/AGENT_EXECUTION_SPEC.md`
2. `references/mobile-money.md`
3. `references/io-contracts.md`

- Backend verification task:
1. `references/AGENT_EXECUTION_SPEC.md`
2. `references/core-implementation.md`
3. `references/io-contracts.md`
4. Run `scripts/validate-verify-response.py`

- Webhook task:
1. `references/AGENT_EXECUTION_SPEC.md`
2. `references/webhook-playbook.md`
3. `references/io-contracts.md`
4. Run `scripts/check-webhook-signature-mode.py`

## Reliability Invariants

- Generate and persist `tx_ref` before initiating payment.
- Verify transactions on backend; never fulfill on frontend callback alone.
- Treat `success-pending-validation` as pending, not settled.
- Verify exact amount/reference match before fulfillment.
- Verify webhook signature using configured mode (`verif-hash` or HMAC-SHA256) with raw body handling.
- Enforce idempotency if order is already paid.

## I/O Contracts

- Read `references/io-contracts.md` for input/output requirements.
- Validate response structure with `references/output-schema.json`.

## Deterministic Script Interface

All scripts follow `references/script-io-convention.md`:
- Input: JSON file path or stdin JSON.
- Output: JSON envelope with `ok`, `tool`, `errors`, `warnings`, `result`.
- Exit code: `0` pass, `1` failure.

## Standard Response Contract

Use `references/output-contract.md`:
1. Summary
2. Artifacts
3. Next actions
4. Machine-readable JSON (`decisions`, `risks`, `required_inputs`, `validation_results`)

## Reference Index

- Quick setup and channel checks: `references/quick-reference.md`
- Verify/status flow: `references/core-implementation.md`
- Webhook signature handling: `references/webhook-playbook.md`
- Existing deep guides:
- `references/flutterwave-specific.md`
- `references/implementation-patterns.md`
- `references/one-time-payments.md`
- `references/express-implementation.md`
- `references/nextjs-implementation.md`
- `references/mobile-money.md`
- `references/webhooks.md`
- `references/subscriptions.md`
- `references/bank-transfers.md`
- `references/troubleshooting.md`
