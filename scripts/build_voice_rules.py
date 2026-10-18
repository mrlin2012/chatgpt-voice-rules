#!/usr/bin/env python3
"""Extract CIDR networks from OpenAI's official ChatGPT Voice JSON."""
import ipaddress
import json
import re
import sys
from pathlib import Path

SOURCE = Path("chatgpt-voice.json")
OUTPUT = Path("voice.txt")
CIDR_CANDIDATE = re.compile(r"^[0-9a-fA-F:.]+/\d{1,3}$")


def walk(value, result):
    if isinstance(value, dict):
        for child in value.values():
            walk(child, result)
    elif isinstance(value, list):
        for child in value:
            walk(child, result)
    elif isinstance(value, str):
        candidate = value.strip()
        if not CIDR_CANDIDATE.fullmatch(candidate):
            return
        try:
            result.add(str(ipaddress.ip_network(candidate, strict=False)))
        except ValueError:
            pass


def main():
    if not SOURCE.is_file() or SOURCE.stat().st_size == 0:
        sys.exit("ERROR: official JSON is missing or empty")
    try:
        data = json.loads(SOURCE.read_text(encoding="utf-8"))
    except Exception as exc:
        sys.exit(f"ERROR: could not parse official JSON: {exc}")

    networks = set()
    walk(data, networks)
    if not networks:
        sys.exit("ERROR: no valid CIDR networks found; refusing to publish")

    if OUTPUT.exists():
        old_count = sum(1 for line in OUTPUT.read_text(encoding="utf-8").splitlines() if line.strip())
        if old_count and len(networks) < max(1, old_count // 2):
            sys.exit(f"ERROR: new count ({len(networks)}) is suspiciously below half of previous count ({old_count})")

    ordered = sorted(
        networks,
        key=lambda item: (
            ipaddress.ip_network(item).version,
            int(ipaddress.ip_network(item).network_address),
            ipaddress.ip_network(item).prefixlen,
        ),
    )
    OUTPUT.write_text("\n".join(ordered) + "\n", encoding="utf-8")
    print(f"Extracted {len(ordered)} unique CIDR networks.")


if __name__ == "__main__":
    main()
