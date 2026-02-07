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
    warnings: List[str] = []

    required_root = ["expected_reference", "expected_amount_kobo", "verify_payload"]
    for key in required_root:
        if key not in data:
            errors.append(err("MISSING_FIELD", f"Missing required field: {key}", key, f"Provide `{key}` in input JSON."))

    verify_payload = data.get("verify_payload", {})
    if not isinstance(verify_payload, dict):
        errors.append(err("INVALID_TYPE", "verify_payload must be an object", "verify_payload", "Set `verify_payload` to a JSON object."))
        verify_payload = {}

    for key in ["status", "reference", "amount"]:
        if key not in verify_payload:
            errors.append(err("MISSING_FIELD", f"verify_payload missing: {key}", f"verify_payload.{key}", f"Populate `verify_payload.{key}` from Paystack verify response."))

    order_status = data.get("order_status")
    if order_status == "paid":
        result = {
            "action": "no-op",
            "reason": "order already paid",
            "idempotent": True,
        }
        print(json.dumps({"ok": True, "tool": "validate-payment-contract", "errors": [], "warnings": warnings, "result": result}, indent=2))
        return 0

    expected_reference = data.get("expected_reference")
    expected_amount = data.get("expected_amount_kobo")
    status = verify_payload.get("status")
    actual_reference = verify_payload.get("reference")
    actual_amount = verify_payload.get("amount")

    if isinstance(expected_reference, str) and isinstance(actual_reference, str) and actual_reference != expected_reference:
        errors.append(err("REFERENCE_MISMATCH", "Verified reference does not match expected reference", "verify_payload.reference", "Use Paystack returned reference from initialization and verify against DB."))

    if isinstance(expected_amount, int) and isinstance(actual_amount, int) and actual_amount != expected_amount:
        errors.append(err("AMOUNT_MISMATCH", "Verified amount does not match expected amount", "verify_payload.amount", "Store expected amount in kobo and compare exact integer values."))

    if status != "success":
        errors.append(err("INVALID_STATUS", f"Verified status must be success, got: {status}", "verify_payload.status", "Do not fulfill order unless verify status is `success`."))

    if errors:
        print(json.dumps({"ok": False, "tool": "validate-payment-contract", "errors": errors, "warnings": warnings, "result": {"action": "reject"}}, indent=2))
        return 1

    result = {
        "action": "mark-paid",
        "idempotent": False,
        "reference": actual_reference,
        "amount_kobo": actual_amount,
    }
    print(json.dumps({"ok": True, "tool": "validate-payment-contract", "errors": [], "warnings": warnings, "result": result}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
