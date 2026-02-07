#!/usr/bin/env python3
import json
import sys
from typing import Any, Dict, List


def load_payload() -> Dict[str, Any]:
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            return json.load(f)
    return json.load(sys.stdin)


def err(code: str, message: str, path: str, remediation: str) -> Dict[str, str]:
    return {
        "code": code,
        "message": message,
        "path": path,
        "remediation": remediation,
    }


def main() -> int:
    data = load_payload()
    errors: List[Dict[str, str]] = []

    for key in ["expected_tx_ref", "expected_amount", "verify_payload"]:
        if key not in data:
            errors.append(err("MISSING_FIELD", f"Missing required field: {key}", key, f"Provide `{key}` in input JSON."))

    payload = data.get("verify_payload", {})
    if not isinstance(payload, dict):
        errors.append(err("INVALID_TYPE", "verify_payload must be an object", "verify_payload", "Set verify_payload to a JSON object."))
        payload = {}

    for key in ["status", "tx_ref", "amount"]:
        if key not in payload:
            errors.append(err("MISSING_FIELD", f"verify_payload missing: {key}", f"verify_payload.{key}", f"Populate `verify_payload.{key}` from verify API response."))

    if data.get("order_status") == "paid":
        print(json.dumps({"ok": True, "tool": "validate-verify-response", "errors": [], "warnings": [], "result": {"action": "no-op", "reason": "order already paid", "idempotent": True}}, indent=2))
        return 0

    expected_tx_ref = data.get("expected_tx_ref")
    expected_amount = data.get("expected_amount")
    status = payload.get("status")
    tx_ref = payload.get("tx_ref")
    amount = payload.get("amount")

    if isinstance(expected_tx_ref, str) and isinstance(tx_ref, str) and tx_ref != expected_tx_ref:
        errors.append(err("TX_REF_MISMATCH", "verify tx_ref does not match expected tx_ref", "verify_payload.tx_ref", "Use stored tx_ref and reject mismatches."))

    if isinstance(expected_amount, int) and isinstance(amount, int) and amount != expected_amount:
        errors.append(err("AMOUNT_MISMATCH", "verify amount does not match expected amount", "verify_payload.amount", "Compare integer smallest-unit amounts from DB and verify payload."))

    if status == "success-pending-validation":
        print(json.dumps({
            "ok": True,
            "tool": "validate-verify-response",
            "errors": [],
            "warnings": ["await webhook confirmation before fulfillment"],
            "result": {"action": "await-webhook", "settled": False}
        }, indent=2))
        return 0

    if status != "successful":
        errors.append(err("INVALID_STATUS", f"status must be successful for immediate fulfillment, got: {status}", "verify_payload.status", "Treat pending/failed statuses as non-settled."))

    if errors:
        print(json.dumps({"ok": False, "tool": "validate-verify-response", "errors": errors, "warnings": [], "result": {"action": "reject"}}, indent=2))
        return 1

    print(json.dumps({
        "ok": True,
        "tool": "validate-verify-response",
        "errors": [],
        "warnings": [],
        "result": {"action": "mark-paid", "tx_ref": tx_ref, "amount": amount, "settled": True}
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
