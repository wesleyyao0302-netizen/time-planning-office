#!/usr/bin/env python3
"""Build a standards-friendly iCalendar file from data/schedule.json."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "schedule.json"
OUTPUTS = [
    ROOT / "docs" / "calendar.ics",
    ROOT / "time-planning-office.ics",
]


def escape_text(value: str) -> str:
    return (
        value.replace("\\", "\\\\")
        .replace("\n", "\\n")
        .replace(";", "\\;")
        .replace(",", "\\,")
    )


def fold_line(line: str, limit: int = 75) -> list[str]:
    """Fold a content line without splitting UTF-8 characters."""
    if len(line.encode("utf-8")) <= limit:
        return [line]

    result: list[str] = []
    remaining = line
    first = True
    while remaining:
        prefix = "" if first else " "
        allowance = limit - len(prefix.encode("utf-8"))
        chunk = ""
        for char in remaining:
            if len((chunk + char).encode("utf-8")) > allowance:
                break
            chunk += char
        if not chunk:
            raise ValueError("Unable to fold iCalendar line")
        result.append(prefix + chunk)
        remaining = remaining[len(chunk) :]
        first = False
    return result


def add(lines: list[str], name: str, value: str) -> None:
    lines.extend(fold_line(f"{name}:{value}"))


def compact_local(value: str) -> str:
    return datetime.fromisoformat(value).strftime("%Y%m%dT%H%M%S")


def validate_schedule(payload: dict) -> None:
    default_alarm_minutes = payload.get("calendar", {}).get(
        "default_alarm_minutes_before"
    )
    if default_alarm_minutes is not None and (
        not isinstance(default_alarm_minutes, int) or default_alarm_minutes < 0
    ):
        raise ValueError(
            "calendar.default_alarm_minutes_before must be a non-negative integer"
        )
    seen: set[str] = set()
    for event in payload.get("events", []):
        required = {"id", "title", "start", "end"}
        missing = required - event.keys()
        if missing:
            raise ValueError(f"Event is missing {sorted(missing)}: {event}")
        if event["id"] in seen:
            raise ValueError(f"Duplicate event id: {event['id']}")
        seen.add(event["id"])
        start = datetime.fromisoformat(event["start"])
        end = datetime.fromisoformat(event["end"])
        if end <= start:
            raise ValueError(f"Event end must be after start: {event['id']}")
        alarm_minutes = event.get(
            "alarm_minutes_before", default_alarm_minutes
        )
        if alarm_minutes is not None and (
            not isinstance(alarm_minutes, int) or alarm_minutes < 0
        ):
            raise ValueError(
                f"alarm_minutes_before must be a non-negative integer: {event['id']}"
            )
        for excluded in event.get("exdate", []):
            datetime.fromisoformat(excluded)


def build(payload: dict) -> str:
    validate_schedule(payload)
    cal = payload["calendar"]
    tzid = cal.get("timezone", "Europe/London")
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
    ]
    add(lines, "PRODID", cal.get("product_id", "-//Research Time Workstation//EN"))
    add(lines, "X-WR-CALNAME", escape_text(cal["name"]))
    add(lines, "X-WR-CALDESC", escape_text(cal.get("description", "")))
    add(lines, "X-WR-TIMEZONE", tzid)

    if tzid == "Europe/London":
        lines.extend(
            [
                "BEGIN:VTIMEZONE",
                "TZID:Europe/London",
                "X-LIC-LOCATION:Europe/London",
                "BEGIN:DAYLIGHT",
                "TZOFFSETFROM:+0000",
                "TZOFFSETTO:+0100",
                "TZNAME:BST",
                "DTSTART:19810329T010000",
                "RRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=-1SU",
                "END:DAYLIGHT",
                "BEGIN:STANDARD",
                "TZOFFSETFROM:+0100",
                "TZOFFSETTO:+0000",
                "TZNAME:GMT",
                "DTSTART:19961027T020000",
                "RRULE:FREQ=YEARLY;BYMONTH=10;BYDAY=-1SU",
                "END:STANDARD",
                "END:VTIMEZONE",
            ]
        )

    for event in payload["events"]:
        lines.append("BEGIN:VEVENT")
        add(lines, "UID", f"{event['id']}@skun-research-time-workstation")
        add(lines, "DTSTAMP", stamp)
        add(lines, f"DTSTART;TZID={tzid}", compact_local(event["start"]))
        add(lines, f"DTEND;TZID={tzid}", compact_local(event["end"]))
        add(lines, "SUMMARY", escape_text(event["title"]))
        if event.get("description"):
            add(lines, "DESCRIPTION", escape_text(event["description"]))
        if event.get("location"):
            add(lines, "LOCATION", escape_text(event["location"]))
        if event.get("url"):
            add(lines, "URL", event["url"])
        if event.get("categories"):
            add(lines, "CATEGORIES", ",".join(escape_text(x) for x in event["categories"]))
        if event.get("rrule"):
            add(lines, "RRULE", event["rrule"])
        if event.get("exdate"):
            excluded = ",".join(compact_local(value) for value in event["exdate"])
            add(lines, f"EXDATE;TZID={tzid}", excluded)
        lines.append("STATUS:CONFIRMED")
        lines.append(
            "TRANSP:TRANSPARENT" if event.get("transparent") else "TRANSP:OPAQUE"
        )
        alarm_minutes = event.get(
            "alarm_minutes_before", cal.get("default_alarm_minutes_before")
        )
        if alarm_minutes is not None:
            minutes = alarm_minutes
            lines.extend(["BEGIN:VALARM", "ACTION:DISPLAY"])
            add(lines, "DESCRIPTION", escape_text(event["title"]))
            add(lines, "TRIGGER", f"-PT{minutes}M")
            lines.append("END:VALARM")
        lines.append("END:VEVENT")

    lines.append("END:VCALENDAR")
    return "\r\n".join(lines) + "\r\n"


def main() -> None:
    payload = json.loads(SOURCE.read_text(encoding="utf-8"))
    calendar = build(payload)
    for output in OUTPUTS:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(calendar, encoding="utf-8", newline="")
    names = ", ".join(str(output.relative_to(ROOT)) for output in OUTPUTS)
    print(f"Built {names} with {len(payload['events'])} events")


if __name__ == "__main__":
    main()
