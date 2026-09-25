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
        self.assertIn("english-course-wednesday-2026@skun-research-time-workstation", self.calendar)
        self.assertIn("RRULE:FREQ=WEEKLY;BYDAY=WE;COUNT=12", self.calendar)
        self.assertIn("english-course-friday-2026@skun-research-time-workstation", self.calendar)
        self.assertIn("RRULE:FREQ=WEEKLY;BYDAY=FR;COUNT=12", self.calendar)

    def test_course_locations(self) -> None:
        self.assertIn("JMS Learning Hub\\, Room 743", self.calendar)
        self.assertIn("Boyd Orr Building\\, Room 407 (Lecture Theatre A)", self.calendar)

    def test_balanced_course_roadmap_is_included(self) -> None:
        event_ids = {event["id"] for event in self.payload["events"]}
        theory_ids = {
            "power-electronics-undergrad-01",
            "power-electronics-undergrad-02",
            "power-electronics-undergrad-03",
            "power-electronics-undergrad-04",
            "power-electronics-undergrad-05-06",
            "power-electronics-undergrad-07-08",
            "power-electronics-undergrad-09-10",
            "power-electronics-undergrad-11-12",
            "power-electronics-undergrad-13-14",
            "power-electronics-undergrad-15-17",
            "power-electronics-undergrad-18-19",
            "power-electronics-undergrad-20-21",
            "power-electronics-undergrad-22",
            "power-electronics-undergrad-23",
            "power-electronics-undergrad-24",
        }
        simulator_ids = {
            "simulink-black-01-02",
            "simulink-black-03-04",
            "simulink-black-05-06",
            "simulink-black-07-08",
            "simulink-blue-01-02",
            "simulink-blue-03-04",
            "simulink-blue-05-06",
            "simulink-blue-07",
            "simulink-blue-08",
            "simulink-blue-09-10",
        }
        self.assertTrue(theory_ids <= event_ids)
        self.assertTrue(simulator_ids <= event_ids)
        self.assertEqual(
            14,
            sum(event_id.startswith("ml-load-forecasting-") for event_id in event_ids),
        )

    def test_research_blocks_pause_for_winter_break(self) -> None:
        self.assertIn("research-core-monday-2026-27@skun-research-time-workstation", self.calendar)
        self.assertIn(
            "EXDATE;TZID=Europe/London:20261221T090000,20261228T090000",
            self.calendar.replace("\r\n ", ""),
        )


if __name__ == "__main__":
    unittest.main()
