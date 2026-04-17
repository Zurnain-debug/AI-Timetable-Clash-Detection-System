"""
app.py
Flask web application for Timetable Clash Detection & Resolution System
"""

from flask import Flask, render_template, request, jsonify, send_file, session
from werkzeug.utils import secure_filename
import os
import json
from datetime import datetime
from timetable_system import TimetableSystem

app = Flask(__name__)
app.secret_key = 'your-secret-key-here-change-this'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create necessary folders
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls'}

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and processing"""
    try:
        # Check if file was uploaded
        if 'file' not in request.files:
            return jsonify({'success': False, 'message': 'No file uploaded'})
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'success': False, 'message': 'No file selected'})
        
        if not allowed_file(file.filename):
            return jsonify({'success': False, 'message': 'Invalid file type. Please upload CSV or Excel file'})
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_filename = f"{timestamp}_{filename}"
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(input_path)
        
        # Determine file type
        file_extension = filename.rsplit('.', 1)[1].lower()
        file_type = 'csv' if file_extension == 'csv' else 'excel'
        
        # Process the file
        system = TimetableSystem()
        output_filename = f"{timestamp}_resolved.csv"
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
        
        results = system.run_complete_process(
            input_file=input_path,
            output_file=output_path,
            file_type=file_type
        )
        
        # Store results in session for later retrieval
        session['last_output_file'] = output_filename
        session['last_results'] = {
            'load': results.get('load', {}),
            'detect': results.get('detect', {}),
            'resolve': results.get('resolve', {}),
            'export': results.get('export', {})
        }
        
        # Prepare response
        response = {
            'success': True,
            'results': session['last_results'],
            'output_file': output_filename
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/download/<filename>')
def download_file(filename):
    """Download resolved timetable"""
    try:
        file_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True, download_name='resolved_timetable.csv')
        else:
            return jsonify({'success': False, 'message': 'File not found'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/sample')
def download_sample():
    """Download sample CSV template"""
    try:
        # Check if sample file exists
        sample_path = 'input_timetable.csv'
        if os.path.exists(sample_path):
            return send_file(sample_path, as_attachment=True, download_name='sample_timetable.csv')
        else:
            # Create sample file on the fly
            create_sample_csv()
            return send_file(sample_path, as_attachment=True, download_name='sample_timetable.csv')
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

def create_sample_csv():
    """Create a sample CSV file"""
    import csv
    sample_data = [
        ['Course Name', 'Course Code', 'Teacher', 'Room', 'Student Group', 'Day', 'Start Time', 'End Time'],
        ['Data Structures', 'CS301', 'Dr. Smith', '101', 'CS-2024', 'Monday', '09:00', '10:30'],
        ['Algorithms', 'CS302', 'Dr. Smith', '102', 'CS-2023', 'Monday', '09:00', '10:30'],
        ['Database Systems', 'CS303', 'Dr. Johnson', '101', 'CS-2024', 'Tuesday', '14:00', '15:30'],
        ['Web Development', 'CS304', 'Dr. Lee', '101', 'CS-2023', 'Tuesday', '14:00', '15:30'],
    ]
    
    with open('sample_timetable.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(sample_data)

if __name__ == '__main__':
    print("=" * 70)
    print(" " * 10 + "TIMETABLE CLASH DETECTION WEB APPLICATION")
    print(" " * 20 + "Starting Server...")
    print("=" * 70)
    print("\n🌐 Open your browser and go to: http://localhost:5000")
    print("📁 Upload folder: " + os.path.abspath(app.config['UPLOAD_FOLDER']))
    print("📁 Output folder: " + os.path.abspath(app.config['OUTPUT_FOLDER']))
    print("\nPress Ctrl+C to stop the server\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)