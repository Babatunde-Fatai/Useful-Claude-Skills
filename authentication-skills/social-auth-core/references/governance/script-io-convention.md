# Deterministic Script I/O Convention (Local)

## Input

- Accept optional JSON file path.
- If missing, read JSON from stdin.

## Output envelope

```json
{
  "ok": true,
  "tool": "script-name",
  "errors": [],
  "warnings": [],
  "result": {}
}
```

## Exit codes

- `0` pass
- `1` fail
