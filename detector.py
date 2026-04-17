"""
detector.py
Detects clashes in the timetable
"""

from typing import List, Dict
from collections import defaultdict
from models import ClassSession, Clash, ClashType


class ClashDetector:
    """Detects clashes in the timetable"""
    
    def __init__(self, sessions: List[ClassSession]):
        self.sessions = sessions
        self.detected_clashes: List[Clash] = []
    
    def detect_all_clashes(self) -> List[Clash]:
        """Run all clash detection methods"""
        self.detected_clashes = []
        self.detected_clashes.extend(self.detect_teacher_clashes())
        self.detected_clashes.extend(self.detect_room_clashes())
        self.detected_clashes.extend(self.detect_student_group_clashes())
        return self.detected_clashes
    
    def detect_teacher_clashes(self) -> List[Clash]:
        """Detect when a teacher is assigned to multiple classes at the same time"""
        clashes = []
        teacher_sessions = defaultdict(list)
        
        # Group sessions by teacher
        for session in self.sessions:
            teacher_sessions[session.teacher].append(session)
        
        # Check for overlaps
        for teacher, sessions in teacher_sessions.items():
            for i in range(len(sessions)):
                for j in range(i + 1, len(sessions)):
                    if sessions[i].time_slot.overlaps_with(sessions[j].time_slot):
                        clash = Clash(
                            clash_type=ClashType.TEACHER_CLASH,
                            sessions=[sessions[i], sessions[j]],
                            description=f"{teacher} is assigned to {sessions[i].course_name} and {sessions[j].course_name} at the same time",
                            severity=5
                        )
                        clashes.append(clash)
        
        return clashes
    
    def detect_room_clashes(self) -> List[Clash]:
        """Detect when a room is booked for multiple classes at the same time"""
        clashes = []
        room_sessions = defaultdict(list)
        
        # Group sessions by room
        for session in self.sessions:
            room_sessions[session.room].append(session)
        
        # Check for overlaps
        for room, sessions in room_sessions.items():
            for i in range(len(sessions)):
                for j in range(i + 1, len(sessions)):
                    if sessions[i].time_slot.overlaps_with(sessions[j].time_slot):
                        clash = Clash(
                            clash_type=ClashType.ROOM_CLASH,
                            sessions=[sessions[i], sessions[j]],
                            description=f"Room {room} is booked for {sessions[i].course_name} and {sessions[j].course_name} at the same time",
                            severity=4
                        )
                        clashes.append(clash)
        
        return clashes
    
    def detect_student_group_clashes(self) -> List[Clash]:
        """Detect when a student group has multiple classes at the same time"""
        clashes = []
        group_sessions = defaultdict(list)
        
        # Group sessions by student group
        for session in self.sessions:
            group_sessions[session.student_group].append(session)
        
        # Check for overlaps
        for group, sessions in group_sessions.items():
            for i in range(len(sessions)):
                for j in range(i + 1, len(sessions)):
                    if sessions[i].time_slot.overlaps_with(sessions[j].time_slot):
                        clash = Clash(
                            clash_type=ClashType.STUDENT_GROUP_CLASH,
                            sessions=[sessions[i], sessions[j]],
                            description=f"Student group {group} has {sessions[i].course_name} and {sessions[j].course_name} at the same time",
                            severity=5
                        )
                        clashes.append(clash)
        
        return clashes
    
    def get_clash_summary(self) -> Dict[str, int]:
        """Get a summary of clashes by type"""
        summary = {clash_type.name: 0 for clash_type in ClashType}
        for clash in self.detected_clashes:
            summary[clash.clash_type.name] += 1
        return summary