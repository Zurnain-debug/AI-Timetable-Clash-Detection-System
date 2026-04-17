# 🧠 AI Timetable Clash Detection & Resolution System

## 📌 Overview
This project is an AI-based system that automatically detects and resolves timetable clashes in educational institutions.

## 🚀 Features
- Detects Teacher, Room, and Student Group clashes
- AI-based resolution using Constraint Satisfaction Problem (CSP)
- Supports CSV and Excel input
- Web-based interface using Flask
- Generates resolved timetable automatically

## 🧠 AI Techniques Used
- Rule-Based System (for clash detection)
- Constraint Satisfaction Problem (CSP)
- Greedy Search Algorithm

## 🛠️ Tech Stack
- Python
- Flask
- Pandas
- OpenPyXL

## 📂 Input Format
CSV/Excel file with:
- Course Name
- Teacher
- Room
- Student Group
- Day & Time

## 📊 Output
- Clash-free timetable (CSV)
- Resolution report (JSON)

## ▶️ How to Run
```bash
pip install -r requirements.txt
python app.py
