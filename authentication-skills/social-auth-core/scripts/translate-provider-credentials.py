#!/usr/bin/env python3
import json
import sys
from typing import Any, Dict, List

PROVIDER_REQUIREMENTS = {
    "google": {
        "required": ["client_id", "client_secret"],
        "env": {"client_id": "GOOGLE_CLIENT_ID", "client_secret": "GOOGLE_CLIENT_SECRET"},
    },
    "github": {
        "required": ["client_id", "client_secret"],
        "env": {"client_id": "GITHUB_CLIENT_ID", "client_secret": "GITHUB_CLIENT_SECRET"},
    },
    "linkedin": {
        "required": ["client_id", "client_secret"],
        "env": {"client_id": "LINKEDIN_CLIENT_ID", "client_secret": "LINKEDIN_CLIENT_SECRET"},
    },
    "apple": {
        "required": ["client_id", "team_id", "key_id", "private_key"],
        "env": {
            "client_id": "APPLE_CLIENT_ID",
            "team_id": "APPLE_TEAM_ID",
            "key_id": "APPLE_KEY_ID",
            "private_key": "APPLE_PRIVATE_KEY",
        },
    },
    "twitter": {
        "required": ["client_id", "client_secret"],
        "env": {"client_id": "TWITTER_CLIENT_ID", "client_secret": "TWITTER_CLIENT_SECRET"},
    },
}


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

    provider = str(data.get("provider", "")).strip().lower()
    creds = data.get("credentials")

    if provider not in PROVIDER_REQUIREMENTS:
        errors.append(err("UNSUPPORTED_PROVIDER", f"Unsupported provider: {provider}", "provider", "Use one of: google, github, linkedin, apple, twitter."))

    if not isinstance(creds, dict):
        errors.append(err("INVALID_CREDENTIALS", "credentials must be an object", "credentials", "Provide provider credentials as a JSON object."))
        creds = {}

    if errors:
        print(json.dumps({"ok": False, "tool": "translate-provider-credentials", "errors": errors, "warnings": [], "result": {}}, indent=2))
        return 1

    req = PROVIDER_REQUIREMENTS[provider]
    mapped: Dict[str, str] = {}

    for key in req["required"]:
        if not creds.get(key):
            errors.append(err("MISSING_CREDENTIAL", f"Missing required credential: {key}", f"credentials.{key}", f"Provide `{key}` for provider `{provider}`."))
        else:
            mapped[req["env"][key]] = str(creds[key])

    if errors:
        print(json.dumps({"ok": False, "tool": "translate-provider-credentials", "errors": errors, "warnings": [], "result": {"provider": provider}}, indent=2))
        return 1

    print(json.dumps({
        "ok": True,
        "tool": "translate-provider-credentials",
        "errors": [],
        "warnings": [],
        "result": {"provider": provider, "env_mapping": mapped}
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
