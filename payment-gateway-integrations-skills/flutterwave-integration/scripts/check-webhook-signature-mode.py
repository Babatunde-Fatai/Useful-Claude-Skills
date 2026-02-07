#!/usr/bin/env python3
import json
import sys
from typing import Any, Dict, List


VALID_MODES = {"verif-hash", "hmac-sha256"}


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

    mode = data.get("signature_mode")
    if mode not in VALID_MODES:
        errors.append(err("INVALID_SIGNATURE_MODE", f"signature_mode must be one of {sorted(VALID_MODES)}", "signature_mode", "Set signature mode to `verif-hash` or `hmac-sha256`."))

    headers = data.get("headers")
    if not isinstance(headers, dict):
        errors.append(err("INVALID_HEADERS", "headers must be an object", "headers", "Provide webhook request headers object."))
        headers = {}

    if mode == "verif-hash" and not headers.get("verif-hash"):
        errors.append(err("MISSING_VERIF_HASH", "Missing verif-hash header", "headers.verif-hash", "Configure FLW_SECRET_HASH and require verif-hash header."))

    if mode == "hmac-sha256":
        if data.get("raw_body_enabled") is not True:
            errors.append(err("RAW_BODY_REQUIRED", "raw_body_enabled must be true for hmac-sha256 mode", "raw_body_enabled", "Enable raw body capture before parsing JSON payload."))
        if not headers.get("x-flutterwave-signature"):
            errors.append(err("MISSING_HMAC_HEADER", "Missing x-flutterwave-signature header", "headers.x-flutterwave-signature", "Require x-flutterwave-signature for HMAC mode."))

    if errors:
        print(json.dumps({"ok": False, "tool": "check-webhook-signature-mode", "errors": errors, "warnings": [], "result": {"action": "reject"}}, indent=2))
        return 1

    print(json.dumps({
        "ok": True,
        "tool": "check-webhook-signature-mode",
        "errors": [],
        "warnings": [],
        "result": {"action": "process-webhook", "signature_mode": mode}
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
