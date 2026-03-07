# Cadtalytics — Student Grade Analytics System

A desktop GUI application built with **Python & CustomTkinter** that loads student data, performs grade analytics, and predicts future academic performance using a **Random Forest machine learning model**.

---

## Project Overview

Cadtalytics is a data-driven student performance analytics system designed to help educators track, analyze, and predict student outcomes. The system supports two data sources (CSV and MySQL), provides interactive visualizations, and uses machine learning to forecast Grade 4 (G4) performance based on behavioral habits and historical grades.

**Key Features:**
- View all students, top performers, and at-risk students
- Visualize grade distributions and subject averages
- Track individual student GPA trends across periods
- Predict future grades using a Random Forest model (8 behavioral + academic features)
- Export individual student reports to text files
- Dark-themed modern GUI with sidebar navigation

**OOP Concepts Applied:**
- **Encapsulation** : private attributes with `@property` getters in `Student` class
- **Inheritance** : `UndergraduateStudent` and `GraduateStudent` extend `Student`
- **Polymorphism**: `generate_report()` behaves differently per student type
- **Abstraction** : `Student.generate_report()` raises `NotImplementedError` forcing subclasses to implement it

---

## Team Members

| Seat Sreylenn   | Data Models & Persistence Layer |
| Chim SokSambath | Analytics & ML Prediction Layer |
| Yin Sousdey     | GUI, Visualization & Application Layer |

---

## Project Structure

```
cadtalytics/
├── main.py                   # GUI application entry point
├── requirements.txt          # Required libraries
├── README.md
├── data/
│   ├── students.csv          # Hybrid dataset (400 records)
│   └── reports/              # Auto-generated charts & exported reports
└── src/
    ├── __init__.py
    ├── student.py            # Base Student class
    ├── student_types.py      # UndergraduateStudent & GraduateStudent
    ├── file_handler.py       # CSV file loading & report export
    ├── file_handler_mysql.py # MySQL database connector
    ├── grade_manager.py      # Student list management
    ├── analytics.py          # Grade statistics & computations
    ├── predictor.py          # Random Forest ML predictor
    └── visualizer.py         # Matplotlib chart methods
```

---

## Dependencies & Installation

### Requirements
- Python 3.10 or higher
- pip (Python package manager)

### Step 1:  Clone the repository
```bash
git clone < https://github.com/sslenn/Cadtalytics >
cd cadtalytics
```

### Step 2: Install required libraries
```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install customtkinter
pip install mysql-connector-python
pip install scikit-learn
pip install matplotlib
pip install numpy
```

### Required Libraries

| `customtkinter`          | Modern dark-themed GUI framework |
| `mysql-connector-python` | MySQL database connection |
| `scikit-learn`           | Random Forest ML model |
| `matplotlib`             | Charts and data visualizations |
| `numpy`                  | Numerical computations |

---

##  Steps to Run the Code

### Step 1 — Make sure the dataset is in place
Ensure `data/students.csv` exists in the project folder.

### Step 2 — Run the application
```bash
python main.py
```

### Step 3 — Using the application
- The app loads automatically on startup
- Use the **left sidebar** to navigate between features
- **Analytics section**  : view students, charts, rankings, export reports
- **Prediction section** : predict G4 grades manually or by student ID

### Step 4:  MySQL (Optional)
If using MySQL instead of CSV, update the connection settings in `main.py`:
```python
host     = "127.0.0.1"
port     = 8889
user     = "root"
password = "root"
database = "student_analytics"
```

---

##  Dataset

The dataset used in this project is a **hybrid dataset**. The behavioral and academic feature structure was inspired by the UCI Student Performance Dataset (Cortez & Silva, 2008). Additional features including student demographics, academic type, subject grades across 4 disciplines, and extended behavioral attributes were synthetically generated to suit the system's prediction model requirements.

**Dataset details:**
- 400 student records
- 2 student types: Undergraduate & Graduate
- 4 subjects: Math, Science, English, Programming
- 3 grade periods: G1, G2, G3
- 6 behavioral features: study time, absences, internet usage, extra classes, sleep hours, parent education

**Reference:**
> Cortez, P. & Silva, A. (2008). *Student Performance Dataset*. UCI Machine Learning Repository. Available at: https://www.kaggle.com/datasets/larsen0966/student-performance-data-set

---

## GitHub Repository

[https://github.com/sslenn/Cadtalytics](https://github.com/sslenn/Cadtalytics)
