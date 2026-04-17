"""
exporter.py
Export timetable to various formats
"""

import pandas as pd
import json
from typing import List, Dict
from models import ClassSession


class TimetableExporter:
    """Export timetable to various formats"""
    
    @staticmethod
    def export_to_csv(sessions: List[ClassSession], filepath: str) -> None:
        """Export resolved timetable to CSV"""
        data = []
        for session in sessions:
            data.append({
                'Session ID': session.session_id,
                'Course Name': session.course_name,
                'Course Code': session.course_code,
                'Teacher': session.teacher,
                'Room': session.room,
                'Student Group': session.student_group,
                'Day': session.day,
                'Start Time': session.start_time,
                'End Time': session.end_time
            })
        
        df = pd.DataFrame(data)
        df.to_csv(filepath, index=False)
        print(f"✓ Timetable exported to: {filepath}")
    
    @staticmethod
    def export_report_to_json(report: Dict, filepath: str) -> None:
        """Export resolution report to JSON"""
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"✓ Report exported to: {filepath}")
    
    @staticmethod
    def export_to_excel(sessions: List[ClassSession], filepath: str) -> None:
        """Export resolved timetable to Excel"""
        data = []
        for session in sessions:
            data.append({
                'Session ID': session.session_id,
                'Course Name': session.course_name,
                'Course Code': session.course_code,
                'Teacher': session.teacher,
                'Room': session.room,
                'Student Group': session.student_group,
                'Day': session.day,
                'Start Time': session.start_time,
                'End Time': session.end_time
            })
        
        df = pd.DataFrame(data)
        df.to_excel(filepath, index=False)
        print(f"✓ Timetable exported to: {filepath}")