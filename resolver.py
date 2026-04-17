"""
resolver.py
AI-based clash resolution system
"""

from typing import List, Dict, Optional, Tuple
from collections import defaultdict
from datetime import time
from models import ClassSession, Clash, TimeSlot, DayOfWeek


class ClashResolver:
    """AI-based clash resolution system"""
    
    def __init__(self, sessions: List[ClassSession], clashes: List[Clash]):
        self.sessions = sessions
        self.clashes = clashes
        self.resolved_sessions: List[ClassSession] = []
        self.resolution_log: List[str] = []
    
    def resolve_all_clashes(self) -> Tuple[List[ClassSession], Dict]:
        """Attempt to resolve all clashes automatically"""
        self.resolved_sessions = self.sessions.copy()
        resolved_count = 0
        unresolved_count = 0
        
        # Sort clashes by severity (highest first)
        sorted_clashes = sorted(self.clashes, key=lambda c: c.severity, reverse=True)
        
        for clash in sorted_clashes:
            success = self._resolve_clash(clash)
            if success:
                resolved_count += 1
            else:
                unresolved_count += 1
        
        report = {
            'total_clashes': len(self.clashes),
            'resolved': resolved_count,
            'unresolved': unresolved_count,
            'resolution_log': self.resolution_log,
            'clash_summary': self._get_resolution_summary()
        }
        
        return self.resolved_sessions, report
    
    def _resolve_clash(self, clash: Clash) -> bool:
        """Resolve a single clash"""
        # Get the sessions involved in the clash
        session_to_move = clash.sessions[0]
        
        # Find alternative time slot
        alternative_slot = self._find_alternative_slot(session_to_move)
        
        if alternative_slot:
            # Update the session
            for session in self.resolved_sessions:
                if session.session_id == session_to_move.session_id:
                    session.day = alternative_slot.day.name.capitalize()
                    session.start_time = alternative_slot.start_time.strftime("%H:%M")
                    session.end_time = alternative_slot.end_time.strftime("%H:%M")
                    session.time_slot = alternative_slot
                    
                    self.resolution_log.append(
                        f"✓ Resolved {clash.clash_type.name}: Moved {session.course_name} "
                        f"({session.student_group}) to {alternative_slot}"
                    )
                    return True
        
        self.resolution_log.append(
            f"✗ Could not resolve {clash.clash_type.name} for {session_to_move.course_name}"
        )
        return False
    
    def _find_alternative_slot(self, session: ClassSession) -> Optional[TimeSlot]:
        """Find an alternative time slot for a session"""
        # Define possible time slots
        days = [DayOfWeek.MONDAY, DayOfWeek.TUESDAY, DayOfWeek.WEDNESDAY, 
                DayOfWeek.THURSDAY, DayOfWeek.FRIDAY]
        
        time_slots = [
            (time(8, 0), time(9, 30)),
            (time(9, 30), time(11, 0)),
            (time(11, 0), time(12, 30)),
            (time(13, 0), time(14, 30)),
            (time(14, 30), time(16, 0)),
            (time(16, 0), time(17, 30))
        ]
        
        # Try each combination
        for day in days:
            for start, end in time_slots:
                candidate_slot = TimeSlot(day, start, end)
                
                # Check if this slot is available for teacher, room, and student group
                if self._is_slot_available(session, candidate_slot):
                    return candidate_slot
        
        return None
    
    def _is_slot_available(self, session: ClassSession, candidate_slot: TimeSlot) -> bool:
        """Check if a time slot is available for a session"""
        for other_session in self.resolved_sessions:
            if other_session.session_id == session.session_id:
                continue
            
            # Check if slot overlaps with any existing session
            if candidate_slot.overlaps_with(other_session.time_slot):
                # Check if there's a conflict with teacher, room, or student group
                if (other_session.teacher == session.teacher or
                    other_session.room == session.room or
                    other_session.student_group == session.student_group):
                    return False
        
        return True
    
    def _get_resolution_summary(self) -> Dict[str, int]:
        """Get summary of resolution attempts by clash type"""
        summary = defaultdict(int)
        for log_entry in self.resolution_log:
            if "✓" in log_entry:
                summary["resolved"] += 1
            elif "✗" in log_entry:
                summary["unresolved"] += 1
        return dict(summary)