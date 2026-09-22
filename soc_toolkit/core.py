"""Small, dependency-free log triage components for authorized defensive use."""

from __future__ import annotations

import re
from collections import Counter
from collections.abc import Iterable
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

FAILED_LOGIN_RE = re.compile(
    r"Failed password for (?:invalid user |user )?(?P<user>\S+) from (?P<ip>\S+)"
)


@dataclass(frozen=True)
class Event:
    timestamp: str
    source: str
    message: str
    username: str | None = None
    source_ip: str | None = None


@dataclass(frozen=True)
class Alert:
    alert_type: str
    severity: str
    title: str
    evidence: dict[str, object]


def parse_auth_log(lines: Iterable[str], source: str = "auth.log") -> list[Event]:
    """Parse SSH failed-login lines from a safe, local sample or log export."""
    events: list[Event] = []
    for raw_line in lines:
        line = raw_line.strip()
        match = FAILED_LOGIN_RE.search(line)
        if not match:
            continue
        timestamp = line[:15].strip() or "unknown"
        events.append(
            Event(
                timestamp=timestamp,
                source=source,
                message=line,
                username=match.group("user"),
                source_ip=match.group("ip"),
            )
        )
    return events


def detect_brute_force(events: Iterable[Event], threshold: int = 3) -> list[Alert]:
    """Raise one alert for each source IP meeting the failed-login threshold."""
    if threshold < 1:
        raise ValueError("threshold must be at least 1")
    grouped: dict[str, list[Event]] = {}
    for event in events:
        if event.source_ip:
            grouped.setdefault(event.source_ip, []).append(event)

    alerts: list[Alert] = []
    for source_ip, matches in sorted(grouped.items()):
        if len(matches) < threshold:
            continue
        users = sorted({event.username for event in matches if event.username})
        alerts.append(
            Alert(
                alert_type="brute_force",
                severity="high",
                title=f"Repeated failed logins from {source_ip}",
                evidence={
                    "source_ip": source_ip,
                    "attempts": len(matches),
                    "target_users": users,
                    "first_seen": matches[0].timestamp,
                    "last_seen": matches[-1].timestamp,
                },
            )
        )
    return alerts


def match_iocs(events: Iterable[Event], iocs: Iterable[str]) -> list[Alert]:
    """Match IOC tokens against parsed event text.

    Matching is delimiter-aware: the indicator ``10.0.0.1`` does not match
    ``10.0.0.11`` or ``210.0.0.1``, which a naive substring search would.
    """
    indicators = {ioc.strip() for ioc in iocs if ioc.strip()}
    patterns = {
        indicator: re.compile(rf"(?<![\w.-]){re.escape(indicator)}(?![\w.-])")
        for indicator in indicators
    }
    alerts: list[Alert] = []
    for event in events:
        matched = sorted(
            indicator
            for indicator, pattern in patterns.items()
            if pattern.search(event.message)
        )
        if matched:
            alerts.append(
                Alert(
                    alert_type="ioc_match",
                    severity="critical",
                    title="Known indicator found in authentication event",
                    evidence={
                        "indicators": matched,
                        "timestamp": event.timestamp,
                        "source_ip": event.source_ip,
                        "username": event.username,
                    },
                )
            )
    return alerts


def build_report(
    events: list[Event], alerts: list[Alert], source: str
) -> dict[str, object]:
    """Create a stable JSON-serializable triage report."""
    return {
        "report": {
            "tool": "Fernando Tafurt SOC Toolkit",
            "version": "0.1.0",
            "source": source,
            "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        },
        "summary": {
            "events_analyzed": len(events),
            "alerts": len(alerts),
            "severity_counts": dict(Counter(alert.severity for alert in alerts)),
        },
        "events": [asdict(event) for event in events],
        "alerts": [asdict(alert) for alert in alerts],
    }


def load_lines(path: Path) -> list[str]:
    """Read a UTF-8 log export without modifying it."""
    return path.read_text(encoding="utf-8").splitlines()
