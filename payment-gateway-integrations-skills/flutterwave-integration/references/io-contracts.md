# Flutterwave I/O Contracts

## Script Input Contract: `validate-verify-response.py`

Required fields:
- `expected_tx_ref` (string)
- `expected_amount` (integer)
- `verify_payload` (object)
  - `verify_payload.status` (string)
  - `verify_payload.tx_ref` (string)
  - `verify_payload.amount` (integer)

Optional fields:
- `order_status` (string)

## Script Input Contract: `check-webhook-signature-mode.py`

Required fields:
- `signature_mode` (`verif-hash` or `hmac-sha256`)
- `headers` (object)
- `raw_body_enabled` (boolean, required for `hmac-sha256`)

## Script Output Envelope

```json
{
  "ok": true,
  "tool": "validate-verify-response",
  "errors": [],
  "warnings": [],
  "result": {}
}
```

Failures return `ok=false`, deterministic error codes, and exit code `1`.
