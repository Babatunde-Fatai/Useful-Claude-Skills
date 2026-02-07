#!/usr/bin/env python3
import json
import sys
from typing import Any, Dict, List

REQUIRED_ROOT = ["summary", "artifacts", "next_actions", "machine_json"]
REQUIRED_MACHINE = ["decisions", "risks", "required_inputs", "validation_results"]


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

    for key in REQUIRED_ROOT:
        if key not in data:
            errors.append(err("MISSING_FIELD", f"Missing root field: {key}", key, f"Add `{key}` to output."))

    machine = data.get("machine_json")
    if not isinstance(machine, dict):
        errors.append(err("INVALID_TYPE", "machine_json must be an object", "machine_json", "Set machine_json to an object."))
        machine = {}

    for key in REQUIRED_MACHINE:
        if key not in machine:
            errors.append(err("MISSING_FIELD", f"machine_json missing: {key}", f"machine_json.{key}", f"Add `machine_json.{key}` to output."))

    if isinstance(data.get("summary"), str) and not data["summary"].strip():
        errors.append(err("EMPTY_SUMMARY", "summary must be non-empty", "summary", "Provide a concise summary sentence."))

    for arr_key in ["artifacts", "next_actions"]:
        arr = data.get(arr_key)
        if arr is not None and not isinstance(arr, list):
            errors.append(err("INVALID_TYPE", f"{arr_key} must be an array", arr_key, f"Set `{arr_key}` to an array of strings."))

    results = machine.get("validation_results") if isinstance(machine, dict) else None
    if results is not None:
        if not isinstance(results, list):
            errors.append(err("INVALID_TYPE", "validation_results must be an array", "machine_json.validation_results", "Provide array of {name, ok, details?}."))
        else:
            for idx, item in enumerate(results):
                if not isinstance(item, dict):
                    errors.append(err("INVALID_ITEM", "validation_results item must be object", f"machine_json.validation_results[{idx}]", "Use object with name and ok fields."))
                    continue
                if "name" not in item or "ok" not in item:
                    errors.append(err("MISSING_FIELD", "validation_results item requires name and ok", f"machine_json.validation_results[{idx}]", "Add `name` and `ok` fields."))

    if errors:
        print(json.dumps({"ok": False, "tool": "validate-output-schema", "errors": errors, "warnings": [], "result": {"action": "fix-output"}}, indent=2))
        return 1

    print(json.dumps({"ok": True, "tool": "validate-output-schema", "errors": [], "warnings": [], "result": {"action": "schema-valid"}}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
