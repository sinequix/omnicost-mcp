"""Validate server.json against the official MCP registry schema."""

import json
import sys
import urllib.request

import jsonschema

SCHEMA_URL = "https://static.modelcontextprotocol.io/schemas/2025-12-11/server.schema.json"


def main() -> int:
    with urllib.request.urlopen(SCHEMA_URL, timeout=30) as resp:
        schema = json.load(resp)
    with open("server.json", encoding="utf-8") as fh:
        server = json.load(fh)

    if server.get("$schema") != SCHEMA_URL:
        print(f"server.json $schema must be {SCHEMA_URL}")
        return 1

    validator = jsonschema.Draft7Validator(schema, format_checker=jsonschema.FormatChecker())
    errors = sorted(validator.iter_errors(server), key=lambda e: list(e.path))
    for err in errors:
        where = "/".join(str(p) for p in err.path) or "(root)"
        print(f"{where}: {err.message}")
    if errors:
        return 1
    print("server.json is valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
