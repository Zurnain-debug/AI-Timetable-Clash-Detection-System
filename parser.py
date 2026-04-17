"""
parser.py
Parses CSV/Excel files into timetable structure
"""

import pandas as pd
from datetime import datetime
from typing import List
from models import ClassSession


class TimetableParser:
    """Parses CSV/Excel files into timetable structure"""
    
    @staticmethod
    def parse_time(time_str: str) -> str:
        """Parse various time formats to HH:MM"""
        time_str = str(time_str).strip()
        
        # Try different formats
        formats = ["%H:%M", "%I:%M %p", "%H:%M:%S", "%I:%M:%S %p"]
        
        for fmt in formats:
            try:
                parsed = datetime.strptime(time_str, fmt)
                return parsed.strftime("%H:%M")
            except:
                continue
        
        # If all fails, return as is
        return time_str
    
    @staticmethod
    def load_from_csv(filepath: str) -> List[ClassSession]:
        """Load timetable from CSV file"""
        try:
            df = pd.read_csv(filepath)
            return TimetableParser._parse_dataframe(df)
        except Exception as e:
            raise Exception(f"Error loading CSV: {str(e)}")
    
    @staticmethod
    def load_from_excel(filepath: str, sheet_name: str = 0) -> List[ClassSession]:
        """Load timetable from Excel file"""
        try:
            df = pd.read_excel(filepath, sheet_name=sheet_name)
            return TimetableParser._parse_dataframe(df)
        except Exception as e:
            raise Exception(f"Error loading Excel: {str(e)}")
    
    @staticmethod
    def _parse_dataframe(df: pd.DataFrame) -> List[ClassSession]:
        """Parse DataFrame into ClassSession objects"""
        sessions = []
        
        # Normalize column names (remove spaces, lowercase)
        df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
        
        # Required columns mapping
        column_mapping = {
            'course_name': ['course_name', 'course', 'subject', 'subject_name'],
            'course_code': ['course_code', 'code', 'subject_code'],
            'teacher': ['teacher', 'instructor', 'faculty', 'teacher_name'],
            'room': ['room', 'classroom', 'room_no', 'room_number'],
            'student_group': ['student_group', 'group', 'class', 'section', 'batch'],
            'day': ['day', 'day_of_week', 'weekday'],
            'start_time': ['start_time', 'start', 'time_start', 'from'],
            'end_time': ['end_time', 'end', 'time_end', 'to']
        }
        
        # Find actual column names
        actual_columns = {}
        for key, possible_names in column_mapping.items():
            for col in df.columns:
                if col in possible_names:
                    actual_columns[key] = col
                    break
        
        # Check if all required columns are present
        missing = set(column_mapping.keys()) - set(actual_columns.keys())
        if missing:
            raise Exception(f"Missing required columns: {missing}")
        
        # Parse each row
        for idx, row in df.iterrows():
            try:
                session = ClassSession(
                    session_id=f"S{idx+1:04d}",
                    course_name=str(row[actual_columns['course_name']]).strip(),
                    course_code=str(row[actual_columns['course_code']]).strip(),
                    teacher=str(row[actual_columns['teacher']]).strip(),
                    room=str(row[actual_columns['room']]).strip(),
                    student_group=str(row[actual_columns['student_group']]).strip(),
                    day=str(row[actual_columns['day']]).strip(),
                    start_time=TimetableParser.parse_time(row[actual_columns['start_time']]),
                    end_time=TimetableParser.parse_time(row[actual_columns['end_time']])
                )
                sessions.append(session)
            except Exception as e:
                print(f"Warning: Could not parse row {idx+1}: {str(e)}")
                continue
        
        return sessions