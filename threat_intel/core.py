"""Safe, offline threat-intelligence processing for authorized log review."""

import ipaddress
import re
from collections.abc import Iterable
from dataclasses import dataclass

HASH_RE = re.compile(r"^[a-fA-F0-9]{32,128}$")


@dataclass(frozen=True)
class Indicator:
    value: str
    kind: str
    confidence: str = "medium"


def classify(value: str) -> str:
    value = value.strip()
    try:
        ipaddress.ip_address(value)
        return "ipv4" if "." in value else "ipv6"
    except ValueError:
        if HASH_RE.fullmatch(value):
            return "hash"
        if value.startswith(("http://", "https://")):
            return "url"
        return "domain"


def normalize(values: Iterable[str]) -> list[Indicator]:
    unique = {}
    for raw in values:
        value = raw.strip().lower()
        if value and not value.startswith("#"):
            unique[value] = Indicator(value=value, kind=classify(value))
    return sorted(unique.values(), key=lambda item: (item.kind, item.value))


def find_matches(text: str, indicators: Iterable[Indicator]) -> list[Indicator]:
    lowered = text.lower()
    return [indicator for indicator in indicators if indicator.value in lowered]
