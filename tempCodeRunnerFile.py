"""
main.py
Main entry point for the Timetable Clash Detection & Resolution System
"""

from timetable_system import TimetableSystem
import os


def print_banner():
    """Print application banner"""
    print("=" * 70)
    print(" " * 10 + "TIMETABLE CLASH DETECTION & RESOLUTION SYSTEM")
    print(" " * 20 + "Powered by AI")
    print("=" * 70)


def print_results(results):
    """Print detailed results"""
    print("\n" + "=" * 70)
    print("PROCESS SUMMARY")
    print("=" * 70)
    
    # Load Results
    if results['load'].get('success'):
        print(f"\n✓ LOAD SUCCESSFUL")
        print(f"  Sessions loaded: {results['load'].get('session_count', 0)}")
    else:
        print(f"\n✗ LOAD FAILED")
        print(f"  Error: {results['load'].get('message', 'Unknown error')}")
        return
    
    # Detect Results
    if results['detect'].get('success'):
        print(f"\n✓ CLASH DETECTION COMPLETE")
        print(f"  Total clashes found: {results['detect']['total_clashes']}")
        
        clash_summary = results['detect'].get('clash_summary', {})
        if clash_summary:
            print(f"\n  Clash Breakdown:")
            for clash_type, count in clash_summary.items():
                if count > 0:
                    print(f"    - {clash_type.replace('_', ' ')}: {count}")
    
    # Resolve Results
    if results['resolve'].get('success'):
        report = results['resolve'].get('report', {})
        print(f"\n✓ CLASH RESOLUTION COMPLETE")
        print(f"  Total clashes: {report.get('total_clashes', 0)}")
        print(f"  Successfully resolved: {report.get('resolved', 0)}")
        print(f"  Unresolved: {report.get('unresolved', 0)}")
        
        resolution_log = report.get('resolution_log', [])
        if resolution_log:
            print(f"\n  Resolution Details:")
            for log in resolution_log:
                print(f"    {log}")
    
    # Export Results
    if results['export'].get('success'):
        print(f"\n✓ EXPORT SUCCESSFUL")
        print(f"  {results['export']['message']}")
    else:
        print(f"\n✗ EXPORT FAILED")
        print(f"  Error: {results['export'].get('message', 'Unknown error')}")
    
    print("\n" + "=" * 70)


def main():
    """Main function"""
    print_banner()
    
    # Configuration
    input_file = 'input_timetable.csv'  # Change this to your input file
    output_file = 'resolved_timetable.csv'  # Output file name
    file_type = 'csv'  # 'csv' or 'excel'
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"\n✗ Error: Input file '{input_file}' not found!")
        print(f"\nPlease ensure the file exists in the current directory.")
        print(f"Current directory: {os.getcwd()}")
        
        # Create a sample CSV template
        create_sample = input("\nWould you like to create a sample template? (yes/no): ").strip().lower()
        if create_sample in ['yes', 'y']:
            create_sample_csv()
            print("\n✓ Sample CSV created! Please fill it with your data and run again.")
        return
    
    # Initialize system
    system = TimetableSystem()
    
    # Run complete process
    print(f"\nProcessing file: {input_file}")
    print(f"Output will be saved to: {output_file}\n")
    
    results = system.run_complete_process(
        input_file=input_file,
        output_file=output_file,
        file_type=file_type
    )
    
    # Print detailed results
    print_results(results)
    
    # Calculate success rate
    if results['resolve'].get('success'):
        report = results['resolve'].get('report', {})
        total = report.get('total_clashes', 0)
        resolved = report.get('resolved', 0)
        
        if total > 0:
            success_rate = (resolved / total) * 100
            print(f"\n🎯 Overall Success Rate: {success_rate:.1f}%")
            
            if success_rate == 100:
                print("🎉 Perfect! All clashes resolved successfully!")
            elif success_rate >= 80:
                print("👍 Great! Most clashes resolved.")
            elif success_rate >= 50:
                print("⚠️  Some clashes remain unresolved.")
            else:
                print("❌ Many clashes could not be resolved automatically.")
    
    print("\n✓ Process completed!")


def create_sample_csv():
    """Create a sample CSV template"""
    import csv
    
    sample_data = [
        ['Course Name', 'Course Code', 'Teacher', 'Room', 'Student Group', 'Day', 'Start Time', 'End Time'],
        ['Data Structures', 'CS301', 'Dr. Smith', '101', 'CS-2024', 'Monday', '09:00', '10:30'],
        ['Algorithms', 'CS302', 'Dr. Smith', '102', 'CS-2023', 'Monday', '09:00', '10:30'],  # Teacher clash
        ['Database Systems', 'CS303', 'Dr. Johnson', '101', 'CS-2024', 'Tuesday', '14:00', '15:30'],
        ['Web Development', 'CS304', 'Dr. Lee', '101', 'CS-2023', 'Tuesday', '14:00', '15:30'],  # Room clash
        ['Operating Systems', 'CS305', 'Dr. Brown', '103', 'CS-2024', 'Wednesday', '11:00', '12:30'],
        ['Networks', 'CS306', 'Dr. Davis', '104', 'CS-2024', 'Wednesday', '11:00', '12:30'],  # Group clash
        ['AI/ML', 'CS401', 'Dr. Wilson', '105', 'CS-2022', 'Thursday', '09:00', '10:30'],
        ['Software Engineering', 'CS402', 'Dr. Taylor', '106', 'CS-2022', 'Thursday', '11:00', '12:30'],
    ]
    
    filename = 'sample_timetable.csv'
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(sample_data)
    
    print(f"✓ Sample template created: {filename}")


if __name__ == "__main__":
    main()