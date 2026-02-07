#!/usr/bin/env python3
import json
import sys
from typing import Any, Dict, List
from urllib.parse import urlparse


def load_payload() -> Dict[str, Any]:
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            return json.load(f)
    return json.load(sys.stdin)


def err(code: str, message: str, path: str, remediation: str) -> Dict[str, str]:
    return {"code": code, "message": message, "path": path, "remediation": remediation}


def main() -> int:
    data = load_payload()
    errors: List[Dict[str, str]] = []

    backend_base_url = data.get("backend_base_url")
    redirect_uri = data.get("redirect_uri")

    if not backend_base_url:
        errors.append(err("MISSING_FIELD", "Missing backend_base_url", "backend_base_url", "Provide backend_base_url (e.g., https://api.example.com)."))
    if not redirect_uri:
        errors.append(err("MISSING_FIELD", "Missing redirect_uri", "redirect_uri", "Provide redirect_uri exactly as configured with provider."))

    if errors:
        print(json.dumps({"ok": False, "tool": "validate-redirect-uri", "errors": errors, "warnings": [], "result": {}}, indent=2))
        return 1

    b = urlparse(str(backend_base_url))
    r = urlparse(str(redirect_uri))

    if b.scheme not in {"http", "https"}:
        errors.append(err("INVALID_URL", "backend_base_url must include http/https scheme", "backend_base_url", "Use a fully qualified URL."))
    if r.scheme not in {"http", "https"}:
        errors.append(err("INVALID_URL", "redirect_uri must include http/https scheme", "redirect_uri", "Use a fully qualified callback URL."))

    localhost_hosts = {"localhost", "127.0.0.1"}
    is_local = r.hostname in localhost_hosts

    if r.scheme != "https" and not is_local:
        errors.append(err("INSECURE_REDIRECT", "redirect_uri must use https outside localhost", "redirect_uri", "Use HTTPS callback URLs in non-local environments."))

    if b.hostname and r.hostname and b.hostname != r.hostname:
        errors.append(err("DOMAIN_MISMATCH", "redirect_uri host does not match backend host", "redirect_uri", "Point redirect_uri to backend callback domain, not frontend domain."))

    if "/callback" not in (r.path or ""):
        errors.append(err("UNEXPECTED_PATH", "redirect_uri path should include callback endpoint", "redirect_uri", "Use a provider callback path such as /auth/{provider}/callback."))

    if errors:
        print(json.dumps({"ok": False, "tool": "validate-redirect-uri", "errors": errors, "warnings": [], "result": {}}, indent=2))
        return 1

    print(json.dumps({
        "ok": True,
        "tool": "validate-redirect-uri",
        "errors": [],
        "warnings": [],
        "result": {
            "backend_host": b.hostname,
            "redirect_host": r.hostname,
            "redirect_path": r.path,
            "action": "redirect-uri-valid"
        }
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
