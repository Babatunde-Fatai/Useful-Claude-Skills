# Paystack Webhook Playbook

## Required Preconditions

- Raw request body available before JSON parsing.
- `x-paystack-signature` header present.
- Signature verified against raw body using backend secret.

## Processing Rules

1. Verify signature.
2. Parse event.
3. Extract provider reference and amount.
4. Lookup order by stored reference.
5. If already paid, return no-op success.
6. Compare verified amount/reference against expected DB values.
7. Mark paid and emit downstream fulfillment once.

## Event Handling Notes

- Ignore unknown events safely.
- Reject malformed payloads with structured errors.
- Log minimal metadata; do not log secrets.
