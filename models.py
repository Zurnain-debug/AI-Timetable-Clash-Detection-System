"""
models.py
Data models and classes for the Timetable System
"""

from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime, time
from enum import Enum


class DayOfWeek(Enum):
    """Enumeration for days of the week"""
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7
    
    @classmethod
    def from_string(cls, day_str: str):
        """Convert string to DayOfWeek enum"""
        day_map = {
            'monday': cls.MONDAY, 'mon': cls.MONDAY,
            'tuesday': cls.TUESDAY, 'tue': cls.TUESDAY, 'tues': cls.TUESDAY,
            'wednesday': cls.WEDNESDAY, 'wed': cls.WEDNESDAY,
            'thursday': cls.THURSDAY, 'thu': cls.THURSDAY, 'thur': cls.THURSDAY, 'thurs': cls.THURSDAY,
            'friday': cls.FRIDAY, 'fri': cls.FRIDAY,
            'saturday': cls.SATURDAY, 'sat': cls.SATURDAY,
            'sunday': cls.SUNDAY, 'sun': cls.SUNDAY
        }
        return day_map.get(day_str.lower().strip(), cls.MONDAY)


class ClashType(Enum):
    """Types of clashes that can occur"""
    TEACHER_CLASH = "Teacher assigned to multiple classes at same time"
    ROOM_CLASH = "Room booked for multiple classes at same time"
    STUDENT_GROUP_CLASH = "Student group has multiple classes at same time"


@dataclass
class TimeSlot:
    """Represents a time slot in the timetable"""
    day: DayOfWeek
    start_time: time
    end_time: time
    
    def overlaps_with(self, other: 'TimeSlot') -> bool:
        """Check if this time slot overlaps with another"""
        if self.day != other.day:
            return False
        return (self.start_time < other.end_time and 
                self.end_time > other.start_time)
    
    def __str__(self) -> str:
        return f"{self.day.name}: {self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')}"
    
    def __hash__(self):
        return hash((self.day, self.start_time, self.end_time))
    
    def __eq__(self, other):
        return (self.day == other.day and 
                self.start_time == other.start_time and 
                self.end_time == other.end_time)


@dataclass
class ClassSession:
    """Represents a single class session in the timetable"""
    session_id: str
    course_name: str
    course_code: str
    teacher: str
    room: str
    student_group: str
    day: str
    start_time: str
    end_time: str
    time_slot: Optional[TimeSlot] = None
    
    def __post_init__(self):
        """Initialize time slot from string times"""
        if self.time_slot is None:
            try:
                day_enum = DayOfWeek.from_string(self.day)
                start = datetime.strptime(self.start_time, "%H:%M").time()
                end = datetime.strptime(self.end_time, "%H:%M").time()
                self.time_slot = TimeSlot(day_enum, start, end)
            except Exception as e:
                print(f"Warning: Could not parse time slot for session {self.session_id}: {e}")
                self.time_slot = TimeSlot(DayOfWeek.MONDAY, time(9, 0), time(10, 0))
    
    def __hash__(self):
        return hash(self.session_id)


@dataclass
class Clash:
    """Represents a detected clash"""
    clash_type: ClashType
    sessions: list
    description: str
    severity: int
    
    def to_dict(self) -> dict:
        """Convert clash to dictionary for JSON export"""
        return {
            'type': self.clash_type.name,
            'severity': self.severity,
            'description': self.description,
            'sessions': [
                {
                    'session_id': s.session_id,
                    'course': s.course_name,
                    'teacher': s.teacher,
                    'room': s.room,
                    'group': s.student_group,
                    'time': f"{s.day} {s.start_time}-{s.end_time}"
                } for s in self.sessions
            ]
        }