# Paystack Core Implementation

## Minimal Backend Flow

1. Receive checkout request (`email`, display amount, currency).
2. Convert amount to smallest unit.
3. Call initialize endpoint.
4. Persist returned `reference` with pending status.
5. On callback or polling, verify transaction by `reference`.
6. Compare expected amount/reference from DB to verified payload.
7. Mark paid only on exact match and `success` status.

## Required Safety Checks

- Never trust frontend callback without backend verify call.
- Treat missing reference or missing amount as hard failures.
- Enforce idempotency before fulfillment.
- Persist verification evidence (provider id, timestamps, status).
