# Payment Router Template (Local)

Use this sequence for Paystack integration tasks:

1. Read `references/AGENT_EXECUTION_SPEC.md`.
2. Load only one scenario reference set (checkout, verify, webhook, subscriptions).
3. Run deterministic scripts for reference/amount/signature checks.
4. Enforce idempotency and amount/reference matching before fulfillment.
5. Return output using this skill's local output contract.
