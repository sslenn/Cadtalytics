# prevent the GUI from crashing when rendering charts

import matplotlib
matplotlib.use('TkAgg') 
import matplotlib.pyplot as plt

import seaborn as sn
import os 

# Top Students Chart 
# Conditional Coloring 

def plot_top_students_embedded(ax, top_students):
    """
    Draws horizontal bars for top students on the provided axis.
    Saves the result to data/reports/top_students.png.
    """
    # 1. Clear the axis for a fresh draw
    ax.clear()
    
    # 2. Extract data (Assuming top_students is a list of objects or dicts)
    names = [s.name for s in top_students]
    gpas = [s.get_gpa() for s in top_students]
    
    # 3. Apply conditional logic: Green if GPA >= 90, else Blue 
    colors = ['#2ecc71' if gpa >= 90 else '#3498db' for gpa in gpas]
    
    # 4. Create Horizontal Bar Chart
    bars = ax.barh(names, gpas, color=colors)
    ax.set_title("Top 5 Students by GPA", color='white', fontsize=12)
    ax.set_xlabel("GPA (%)", color='white')
    ax.invert_yaxis()  # Put the top student at the top
    
    # 5. Styling for Dark Theme 
    ax.tick_params(colors='white')
    ax.set_facecolor('#2b2b2b') # Matches CustomTkinter dark theme
    
    # 6. Save to report directory 
    if not os.path.exists('data/reports'):
        os.makedirs('data/reports')
    plt.savefig('data/reports/top_students.png', facecolor='#1a1a1a')



# Four more remaining embedded methods required for layers  



# Grade Distribution (uniform color palette) 

def plot_grade_distribution_embedded(ax, distribution):
    """Bar chart of A/B/C/D/F counts with dark styling[cite: 22]."""
    ax.clear()
    grades = list(distribution.keys())
    counts = list(distribution.values())
    ax.bar(grades, counts, color='#9b59b6') # Consistent purple theme
    ax.set_title("Grade Distribution", color='white')
    plt.savefig('data/reports/grade_distribution.png', facecolor='#1a1a1a')



# Student Trend 

def plot_student_trend_embedded(ax, student, trend):
    """Line chart with fill_between shading for GPA progress[cite: 22]."""
    ax.clear()
    periods = [f"P{i+1}" for i in range(len(trend))]
    ax.plot(periods, trend, marker='o', color='#f1c40f', linewidth=2)
    ax.fill_between(periods, trend, alpha=0.2, color='#f1c40f')
    ax.set_title(f"GPA Trend: {student.name}", color='white')
    ax.set_ylim(0, 100)
    plt.savefig(f'data/reports/trend_{student.id}.png', facecolor='#1a1a1a')



# Class Averages 

def plot_class_average_by_subject_embedded(ax, averages_by_period):
    """Grouped bars with 3 colors per period[cite: 22]."""
    ax.clear()
    subjects = list(averages_by_period.keys())
    # Assuming data structure: {Subject: [Avg1, Avg2, Avg3]}
    x = range(len(subjects))
    width = 0.2
    
    colors = ['#e74c3c', '#3498db', '#2ecc71'] # Period 1, 2, 3
    for i in range(3):
        vals = [averages_by_period[s][i] for s in subjects]
        ax.bar([p + width*i for p in x], vals, width, label=f'Period {i+1}', color=colors[i])
    
    ax.set_xticks([p + width for p in x])
    ax.set_xticklabels(subjects, color='white')
    ax.legend()
    plt.savefig('data/reports/subject_averages.png', facecolor='#1a1a1a')



# & Feature Importance

def plot_feature_importance_embedded(ax, feature_names, importances):
    """Horizontal bars sorted ascending with % labels[cite: 22]."""
    ax.clear()
    # Sort data for better visualization
    data = sorted(zip(feature_names, importances), key=lambda x: x[1])
    names, values = zip(*data)
    
    bars = ax.barh(names, values, color=plt.cm.viridis(values))
    ax.bar_label(bars, fmt='%.1f%%', padding=3, color='white')
    ax.set_title("Model Feature Importance", color='white')
    plt.savefig('data/reports/feature_importance.png', facecolor='#1a1a1a')


# Test My Script

if __name__ == "__main__":
    # Create a temporary figure and axis for testing
    fig, ax = plt.subplots()
    
    # Mock data for testing (since analytics.py might not be ready)
    mock_dist = {'A': 5, 'B': 10, 'C': 8, 'D': 2, 'F': 1}
    
    # Run your method
    plot_grade_distribution_embedded(ax, mock_dist)
    
    # Show the result
    plt.show()