# mandatory backend & Styling : "CustomtkinterGUI"
import matplotlib
matplotlib.use('TkAgg')  # Mandatory for Tkinter integration 
import matplotlib.pyplot as plt
import numpy as np

# Set a dark theme to match your main.py CustomTkinter UI 
plt.style.use('dark_background')

def _setup_ax(ax, title):
    """Helper to maintain consistent styling across all charts."""
    ax.clear()
    ax.set_title(title, fontsize=12, pad=15)
    ax.set_facecolor('#2b2b2b')  # Dark grey to match GUI panels 
    for spine in ax.spines.values():
        spine.set_color('#444444')

# Embedded Methods

def plot_grade_distribution_embedded(ax, distribution): #imported
    """Visualizes counts of A, B, C, D, and F grades."""
    _setup_ax(ax, "Class Grade Distribution")
    grades = list(distribution.keys())
    counts = list(distribution.values())
    
    bars = ax.bar(grades, counts, color='#5dade2')
    ax.bar_label(bars, padding=3)
    
    plt.savefig("data/reports/grade_distribution.png") # Required save 


# Student GPA Trend 

def plot_student_trend_embedded(ax, student, trend):
    """Line chart with fill_between shading for a specific student."""
    _setup_ax(ax, f"GPA Trend: {student.name}") # Uses Sreylenn's Student object
    periods = [f"P{i+1}" for i in range(len(trend))]
    
    ax.plot(periods, trend, marker='o', linewidth=2, color='#f39c12')
    ax.fill_between(periods, trend, alpha=0.2, color='#f39c12')
    ax.set_ylim(0, 100)
    
    plt.savefig(f"data/reports/trend_{student.id}.png") 


# Harizonal Bar 
# and The Features

def plot_feature_importance_embedded(ax, feature_names, importances):
    """Shows which factors most influenced Sambath's ML model."""
    _setup_ax(ax, "Prediction Model: Feature Importance")
    
    # Sort features by importance for a cleaner look 
    indices = np.argsort(importances)
    
    ax.barh(range(len(indices)), [importances[i] for i in indices], color='#2ecc71')
    ax.set_yticks(range(len(indices)))
    ax.set_yticklabels([feature_names[i] for i in indices])
    
    plt.savefig("data/reports/feature_importance.png")

# Top Student Performance 

def plot_top_students_embedded(ax, top_students):
    """
    Horizontal bars for top 5 students.
    - top_students: List of Student objects sorted by GPA.
    """
    _setup_ax(ax, "Top 5 Student Performers")
    
    names = [s.name for s in top_students]
    gpas = [s.get_gpa() for s in top_students] # I'm calling Sreylenn's method
    
    # Conditional Coloring: 
    # Green if GPA >= 90, otherwise Blue (Sreylenn based)
    colors = ['#27ae60' if gpa >= 90 else '#2980b9' for gpa in gpas]
    
    bars = ax.barh(names, gpas, color=colors)
    ax.invert_yaxis()  # Highest GPA at the top
    ax.set_xlim(0, 100)
    
    # Add GPA labels on the bars for clarity
    ax.bar_label(bars, fmt='%.1f%%', padding=5, color='white')
    
    plt.savefig("data/reports/top_students.png") # Required Save

# Subject Average (Embedded Method)

def plot_class_average_by_subject_embedded(ax, averages_by_period):
    """
    Draws grouped bars for subjects across 3 periods.
    - averages_by_period: { 'Math': [80, 85, 90], 'Science': [70, 75, 72] ... }
    """
    _setup_ax(ax, "Class Average by Subject & Period")
    
    subjects = list(averages_by_period.keys())
    x = np.arange(len(subjects))  # Label locations
    width = 0.25  # Width of the bars
    
    # Extract period data (Assuming 3 periods)
    p1 = [averages_by_period[s][0] for s in subjects]
    p2 = [averages_by_period[s][1] for s in subjects]
    p3 = [averages_by_period[s][2] for s in subjects]

    # Plotting with 3 distinct colors 
    ax.bar(x - width, p1, width, label='Period 1', color='#3498db')
    ax.bar(x, p2, width, label='Period 2', color='#9b59b6')
    ax.bar(x + width, p3, width, label='Period 3', color='#2ecc71')

    ax.set_xticks(x)
    ax.set_xticklabels(subjects, rotation=15)
    ax.legend()
    
    plt.savefig("data/reports/subject_averages.png") # Required Save