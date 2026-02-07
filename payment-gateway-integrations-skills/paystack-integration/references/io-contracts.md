# Paystack I/O Contracts

## Script Input Contract: `validate-payment-contract.py`

Required fields:
- `expected_reference` (string)
- `expected_amount_kobo` (integer)
- `verify_payload` (object)
  - `verify_payload.status` (string)
  - `verify_payload.reference` (string)
  - `verify_payload.amount` (integer)

Optional fields:
- `order_status` (string; if `paid`, script returns idempotent no-op)

## Script Input Contract: `check-webhook-contract.py`

Required fields:
- `raw_body_enabled` (boolean)
- `headers` (object)
- `signature_header_name` (string, expected `x-paystack-signature`)

Optional fields:
- `order_status`
- `event_reference`
- `event_amount_kobo`
- `expected_reference`
- `expected_amount_kobo`

## Script Output Envelope

```json
{
  "ok": true,
  "tool": "validate-payment-contract",
  "errors": [],
  "warnings": [],
  "result": {}
}
```

On failure, `ok=false`, `errors` contains deterministic codes and remediations, and exit code is `1`.
