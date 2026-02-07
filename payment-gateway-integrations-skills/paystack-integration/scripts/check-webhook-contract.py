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

    raw_body_enabled = data.get("raw_body_enabled")
    if raw_body_enabled is not True:
        errors.append(err("RAW_BODY_REQUIRED", "raw_body_enabled must be true for signature verification", "raw_body_enabled", "Enable raw body parsing on webhook route before JSON parse."))

    header_name = data.get("signature_header_name")
    if header_name != "x-paystack-signature":
        errors.append(err("WRONG_SIGNATURE_HEADER", "signature_header_name must be x-paystack-signature", "signature_header_name", "Read signature from `x-paystack-signature` header."))

    headers = data.get("headers")
    if not isinstance(headers, dict):
        errors.append(err("INVALID_HEADERS", "headers must be an object", "headers", "Provide request headers object."))
        headers = {}

    signature = headers.get("x-paystack-signature")
    if not signature:
        errors.append(err("MISSING_SIGNATURE", "Missing x-paystack-signature header", "headers.x-paystack-signature", "Require raw body and reject unsigned webhook payloads."))

    if data.get("order_status") == "paid":
        print(json.dumps({
            "ok": True,
            "tool": "check-webhook-contract",
            "errors": [],
            "warnings": [],
            "result": {"action": "no-op", "reason": "order already paid", "idempotent": True}
        }, indent=2))
        return 0

    expected_reference = data.get("expected_reference")
    event_reference = data.get("event_reference")
    if expected_reference and event_reference and expected_reference != event_reference:
        errors.append(err("REFERENCE_MISMATCH", "Webhook reference does not match expected reference", "event_reference", "Lookup order by Paystack reference and reject mismatches."))

    expected_amount = data.get("expected_amount_kobo")
    event_amount = data.get("event_amount_kobo")
    if isinstance(expected_amount, int) and isinstance(event_amount, int) and expected_amount != event_amount:
        errors.append(err("AMOUNT_MISMATCH", "Webhook amount does not match expected amount", "event_amount_kobo", "Compare smallest-unit integers before fulfillment."))

    if errors:
        print(json.dumps({"ok": False, "tool": "check-webhook-contract", "errors": errors, "warnings": [], "result": {"action": "reject"}}, indent=2))
        return 1

    print(json.dumps({
        "ok": True,
        "tool": "check-webhook-contract",
        "errors": [],
        "warnings": [],
        "result": {"action": "process-webhook", "signature_header": "x-paystack-signature"}
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
