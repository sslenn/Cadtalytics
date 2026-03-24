# 📊 Student Habits & Performance Analytics System

> **Group 2 — Team 07** | CADT  IDT · Second Year · OOP (Python)  
> Lecturer: Han Leangsiv | Seat Sreylenn · Chhim SokSambath · Yin Sousdey  
> Academic Year 2024–2025

---

## 1. Project Overview

The **Student Habits & Performance Analytics System** is a Python-based desktop application that analyzes student behavioral data and predicts exam performance using Machine Learning. It is built with Object-Oriented Programming principles and presented through a modern dark-themed **CustomTkinter GUI**  no command-line interaction required.

The system loads data from a real-world dataset of **1,000 students** (sampled from 80,000) containing 30+ behavioral, health, socio-economic, and academic attributes per student. A **Random Forest Regressor** (scikit-learn) is trained on 24 behavioral features to predict each student's `exam_score` (0–100).

### Key Functionality

- **Analytics** — View all students, top performers, at-risk students, dropout-risk flags, score distribution charts, semester averages, and major rankings
- **Prediction** — Predict a student's exam score by entering a manual behavioral profile or by looking up an existing student ID
- **OOP Architecture** — Implements Encapsulation, Inheritance, Polymorphism, Abstraction, and 5 Magic Methods across the `Student`, `UndergraduateStudent`, and `GraduateStudent` class hierarchy
- **Dual Data Source** — Supports both CSV file loading and MySQL database connection
- **Report Export** — Generates and saves individual student `.txt` reports to `data/reports/`

---

## 2. Steps to Run the Code

### Step 1 — Clone or extract the project

```bash
# If using Git
git clone https://github.com/sslenn/Cadtalytics
cd Cadtalytics

# If using the ZIP file
# Extract the ZIP, then navigate into the proj2_out/ folder
```

### Step 2 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 3 — Run the application

```bash
python main.py
```

The app will:
1. Automatically load `data/students_habits.csv`
2. Build all student objects
3. Train the Random Forest model in the background (~2–5 seconds)
4. Display the GUI with all 13 views ready to use

> **Note:** The Prediction views will show a loading message until the RF model finishes training. All Analytics views are available immediately.

### Step 4 — (Optional) Load from MySQL instead of CSV

If you have MySQL running, first import the database:

```bash
mysql -u root -p < students_1000.sql
```

Then when the app starts, select **option 2** (Load from MySQL database). Update the connection settings in `main.py` if needed:

```python
FileHandlerMySQL(
    host="127.0.0.1",
    port=8889,
    user="root",
    password="root",
    database=students_1000"
)
```

---

## 3. Dependencies & Installation Instructions

### Requirements

| Library | Version | Purpose |
|---|---|---|
| `customtkinter` | >= 5.2.0 | Modern dark-themed GUI framework |
| `matplotlib` | >= 3.7.0 | Embedded charts and visualizations |
| `numpy` | >= 1.24.0 | Array operations for ML |
| `scikit-learn` | >= 1.3.0 | RandomForestRegressor, train_test_split, R², MAE |
| `mysql-connector-python` | >= 8.0.0 | Optional MySQL data source |

### Installation

All dependencies can be installed with a single command:

```bash
pip install customtkinter matplotlib numpy scikit-learn mysql-connector-python
```

Or using the provided requirements file:

```bash
pip install -r requirement.txt
```

### Python Version

- Python **3.10 or higher** is required
- Check your version: `python --version`
- Download from: https://www.python.org/downloads/

### Operating System

Compatible with **Windows**, **macOS**, and **Linux**.

---

## 4. GitHub Link
```
https://github.com/sslenn/Cadtalytics
```

---

## Project Structure

```
Cadtalytics/
│
├── main.py                     # GUI entry point
├── requirement.txt             # Python dependencies
├── README.md                   # This file
│
├── data/
│   ├── students_habits.csv     # 1,000-student dataset
│   └── reports/                # Exported .txt and .png reports
│
└── src/
    ├── student.py              # Base Student class
    ├── student_types.py        # UndergraduateStudent & GraduateStudent
    ├── grade_manager.py        # Manages Student objects
    ├── analytics.py            # Statistical analysis
    ├── visualizer.py           # Chart generation
    ├── predictor.py            # Random Forest model
    ├── file_handler.py         # CSV read/write/export
    └── file_handler_mysql.py   # MySQL connection
```

---

*Cambodia Academy of Digital Technology (CADT) — OOP (Python) Final Project*