from __future__ import annotations

import json
import sys
import unittest
from datetime import datetime, timedelta
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
        self.assertIn("english-course-wednesday-2026@skun-research-time-workstation", self.calendar)
        self.assertIn("RRULE:FREQ=WEEKLY;BYDAY=WE;COUNT=12", self.calendar)
        self.assertIn("english-course-friday-2026@skun-research-time-workstation", self.calendar)
        self.assertIn("RRULE:FREQ=WEEKLY;BYDAY=FR;COUNT=12", self.calendar)

    def test_eng5292_is_removed(self) -> None:
        self.assertNotIn("ENG 5292", self.calendar)
        self.assertFalse(
            any(event["id"].startswith("eng5292-") for event in self.payload["events"])
        )

    def test_phase_reminders_are_included(self) -> None:
        reminders = [
            event
            for event in self.payload["events"]
            if event["id"].startswith("phase-reminder-")
        ]
        self.assertEqual(4, len(reminders))
        self.assertTrue(all(event["start"].endswith("T18:00:00") for event in reminders))
        self.assertTrue(all(event["alarm_minutes_before"] == 1 for event in reminders))
        self.assertEqual(4, self.calendar.count("BEGIN:VALARM"))
        self.assertEqual(4, self.calendar.count("TRIGGER:-PT1M"))
        self.assertGreaterEqual(self.calendar.count("TRANSP:TRANSPARENT"), 4)

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

    def test_graduate_course_and_annual_review_outputs(self) -> None:
        graduate = [
            event
            for event in self.payload["events"]
            if event["id"].startswith("power-electronics-graduate-")
        ]
        freezes = [
            event
            for event in self.payload["events"]
            if event["id"].startswith("load-forecast-freeze-")
        ]
        self.assertEqual(16, len(graduate))
        self.assertEqual("2026-11-23T18:30:00", min(event["start"] for event in graduate))
        self.assertEqual("2026-12-19T10:00:00", max(event["start"] for event in graduate))
        self.assertTrue(all("输出" in event["description"] for event in graduate))
        self.assertEqual(5, len(freezes))
        self.assertTrue((ROOT / "LOAD_FORECAST_SPRINT.md").is_file())
        self.assertTrue((ROOT / "ANNUAL_REVIEW_EVIDENCE.md").is_file())

    def test_all_self_study_courses_finish_before_winter_break(self) -> None:
        prefixes = (
            "python-",
            "power-electronics-undergrad-",
            "simulink-",
            "ml-load-forecasting-",
            "power-electronics-graduate-",
        )
        self_study = [
            event
            for event in self.payload["events"]
            if event["id"].startswith(prefixes)
        ]
        self.assertEqual(11, sum(event["id"].startswith("python-") for event in self_study))
        self.assertLessEqual(
            max(datetime.fromisoformat(event["end"]) for event in self_study),
            datetime(2026, 12, 19, 12, 30),
        )

    def test_research_blocks_pause_for_winter_break(self) -> None:
        self.assertIn("research-core-monday-2026-27@skun-research-time-workstation", self.calendar)
        self.assertIn(
            "EXDATE;TZID=Europe/London:20261221T090000,20261228T090000",
            self.calendar.replace("\r\n ", ""),
        )

    def test_second_research_stage_continues_without_exam_break(self) -> None:
        event = next(
            item
            for item in self.payload["events"]
            if item["id"] == "research-core-thursday-2027-spring-summer"
        )
        self.assertEqual("FREQ=WEEKLY;BYDAY=TH;COUNT=24", event["rrule"])
        self.assertNotIn("exdate", event)

    def test_expanded_schedule_has_no_time_conflicts(self) -> None:
        end_of_check = datetime(2027, 7, 10)
        instances: list[tuple[datetime, datetime, str]] = []
        for event in self.payload["events"]:
            start = datetime.fromisoformat(event["start"])
            end = datetime.fromisoformat(event["end"])
            starts = [start]
            if event.get("rrule", "").startswith("FREQ=WEEKLY"):
                count = next(
                    (
                        int(part.split("=", 1)[1])
                        for part in event["rrule"].split(";")
                        if part.startswith("COUNT=")
                    ),
                    ((end_of_check - start).days // 7) + 1,
                )
                starts = [start + timedelta(days=7 * index) for index in range(count)]
            excluded = {
                datetime.fromisoformat(value) for value in event.get("exdate", [])
            }
            for occurrence in starts:
                if occurrence in excluded or occurrence >= end_of_check:
                    continue
                instances.append(
                    (occurrence, occurrence + (end - start), event["id"])
                )

        instances.sort()
        conflicts: list[tuple[str, str, datetime]] = []
        for index, first in enumerate(instances):
            for second in instances[index + 1 :]:
                if second[0] >= first[1]:
                    break
                if first[0] < second[1]:
                    conflicts.append((first[2], second[2], first[0]))
        self.assertEqual([], conflicts)


if __name__ == "__main__":
    unittest.main()
