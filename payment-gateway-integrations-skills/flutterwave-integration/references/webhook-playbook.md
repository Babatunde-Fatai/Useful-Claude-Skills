# Flutterwave Webhook Playbook

## Required Preconditions

- Configure one signature mode per environment:
- `verif-hash` header mode using dashboard secret hash.
- `hmac-sha256` mode using secret key and raw body.
- Ensure raw body support when HMAC mode is used.

## Processing Rules

1. Verify signature.
2. Parse webhook payload.
3. Extract `tx_ref`, provider status, amount.
4. Lookup pending order by `tx_ref`.
5. If already paid, return idempotent no-op.
6. Validate amount/reference.
7. Settle only on accepted final status.

## Settlement Notes

- `success-pending-validation`: do not fulfill yet.
- `successful`: eligible for fulfillment after amount/reference checks.
