"""
timetable_system.py
Main system to coordinate everything
"""

from typing import List, Dict, Optional
from models import ClassSession, Clash
from parser import TimetableParser
from detector import ClashDetector
from resolver import ClashResolver
from exporter import TimetableExporter


class TimetableSystem:
    """Main system to coordinate everything"""
    
    def __init__(self):
        self.sessions: List[ClassSession] = []
        self.detector: Optional[ClashDetector] = None
        self.resolver: Optional[ClashResolver] = None
        self.clashes: List[Clash] = []
        self.resolved_sessions: List[ClassSession] = []
        self.report: Dict = {}
    
    def load_timetable(self, filepath: str, file_type: str = 'csv') -> Dict:
        """Load timetable from file"""
        try:
            if file_type.lower() == 'csv':
                self.sessions = TimetableParser.load_from_csv(filepath)
            elif file_type.lower() in ['xlsx', 'xls', 'excel']:
                self.sessions = TimetableParser.load_from_excel(filepath)
            else:
                raise ValueError(f"Unsupported file type: {file_type}")
            
            return {
                'success': True,
                'message': f'Loaded {len(self.sessions)} sessions',
                'session_count': len(self.sessions)
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e),
                'session_count': 0
            }
    
    def detect_clashes(self) -> Dict:
        """Detect all clashes in the loaded timetable"""
        if not self.sessions:
            return {'success': False, 'message': 'No timetable loaded'}
        
        self.detector = ClashDetector(self.sessions)
        self.clashes = self.detector.detect_all_clashes()
        
        return {
            'success': True,
            'total_clashes': len(self.clashes),
            'clash_summary': self.detector.get_clash_summary(),
            'clashes': [clash.to_dict() for clash in self.clashes]
        }
    
    def resolve_clashes(self) -> Dict:
        """Resolve all detected clashes"""
        if not self.clashes:
            return {'success': False, 'message': 'No clashes detected'}
        
        self.resolver = ClashResolver(self.sessions, self.clashes)
        self.resolved_sessions, self.report = self.resolver.resolve_all_clashes()
        
        return {
            'success': True,
            'report': self.report
        }
    
    def export_resolved_timetable(self, output_filepath: str, format: str = 'csv') -> Dict:
        """Export the resolved timetable"""
        if not self.resolved_sessions:
            return {'success': False, 'message': 'No resolved timetable available'}
        
        try:
            if format.lower() == 'csv':
                TimetableExporter.export_to_csv(self.resolved_sessions, output_filepath)
            elif format.lower() in ['xlsx', 'excel']:
                TimetableExporter.export_to_excel(self.resolved_sessions, output_filepath)
            else:
                raise ValueError(f"Unsupported export format: {format}")
            
            return {
                'success': True,
                'message': f'Resolved timetable exported to {output_filepath}'
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
    
    def run_complete_process(self, input_file: str, output_file: str, file_type: str = 'csv') -> Dict:
        """Run the complete process: load, detect, resolve, export"""
        results = {
            'load': {},
            'detect': {},
            'resolve': {},
            'export': {}
        }
        
        # Load
        print("\n[1/4] Loading timetable...")
        results['load'] = self.load_timetable(input_file, file_type)
        if not results['load']['success']:
            return results
        print(f"✓ {results['load']['message']}")
        
        # Detect
        print("\n[2/4] Detecting clashes...")
        results['detect'] = self.detect_clashes()
        print(f"✓ Found {results['detect']['total_clashes']} clashes")
        
        # If no clashes, just export the original
        if results['detect']['total_clashes'] == 0:
            print("\n✓ No clashes found! Timetable is already clash-free.")
            results['resolve'] = {'success': True, 'message': 'No clashes to resolve'}
            self.resolved_sessions = self.sessions
        else:
            # Resolve
            print("\n[3/4] Resolving clashes...")
            results['resolve'] = self.resolve_clashes()
            print(f"✓ Resolved {self.report.get('resolved', 0)} out of {self.report.get('total_clashes', 0)} clashes")
        
        # Export
        print("\n[4/4] Exporting resolved timetable...")
        results['export'] = self.export_resolved_timetable(output_file)
        
        return results