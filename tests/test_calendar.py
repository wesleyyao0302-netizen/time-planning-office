from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from build_calendar import build  # noqa: E402


class CalendarTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.payload = json.loads((ROOT / "data" / "schedule.json").read_text(encoding="utf-8"))
        cls.calendar = build(cls.payload)

    def test_calendar_markers(self) -> None:
        self.assertTrue(self.calendar.startswith("BEGIN:VCALENDAR\r\n"))
        self.assertTrue(self.calendar.endswith("END:VCALENDAR\r\n"))

    def test_unique_uids(self) -> None:
        uids = [line for line in self.calendar.splitlines() if line.startswith("UID:")]
        self.assertEqual(len(uids), len(set(uids)))
        self.assertEqual(len(uids), len(self.payload["events"]))

    def test_required_recurring_events(self) -> None:
        self.assertIn("weekly-group-meeting@skun-research-time-workstation", self.calendar)
        self.assertIn("RRULE:FREQ=WEEKLY;BYDAY=WE", self.calendar)
        self.assertIn("RRULE:FREQ=WEEKLY;BYDAY=MO;COUNT=9", self.calendar)

    def test_course_locations(self) -> None:
        self.assertIn("JMS Learning Hub\\, Room 743", self.calendar)
        self.assertIn("Boyd Orr Building\\, Room 407 (Lecture Theatre A)", self.calendar)


if __name__ == "__main__":
    unittest.main()
