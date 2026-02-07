# Flutterwave Core Implementation

## Minimal Backend Flow

1. Generate unique `tx_ref`.
2. Persist order as pending with expected amount and currency.
3. Call `/v3/payments` with `tx_ref`.
4. On callback/webhook, verify transaction via backend API.
5. Match `tx_ref` and amount to DB values.
6. Treat `success-pending-validation` as pending.
7. Mark paid only on valid settled status.

## Required Safety Checks

- Do not fulfill from redirect query params.
- Validate status transitions explicitly (`successful`, `pending`, `success-pending-validation`, `failed`).
- Record verification evidence for auditability.
