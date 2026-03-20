import matplotlib.pyplot as plt
import os

class Visualizer:
    def __init__(self):
        os.makedirs("data/reports", exist_ok=True)

    def plot_grade_distribution(self, distribution):
        """Bar chart of exam score letter grade distribution."""
        colors = ["#2ecc71", "#3498db", "#f39c12", "#e74c3c", "#2c3e50"]
        plt.figure(figsize=(8, 5))
        bars = plt.bar(distribution.keys(), distribution.values(), color=colors)
        for bar, val in zip(bars, distribution.values()):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                     str(val), ha="center", fontweight="bold")
        plt.title("Exam Score Distribution — All Students")
        plt.xlabel("Grade Band")
        plt.ylabel("Number of Students")
        plt.tight_layout()
        plt.savefig("data/reports/grade_distribution.png")
        plt.show()

    def plot_student_trend(self, student, trend):
        """
        Horizontal bar chart of a single student's behavioral profile.
        'trend' is a dict of {metric: value} from analytics.student_trend().
        """
        labels = list(trend.keys())
        values = list(trend.values())

        plt.figure(figsize=(7, 4))
        bars = plt.barh(labels, values, color="steelblue")
        for bar, val in zip(bars, values):
            plt.text(bar.get_width() + 0.1,
                     bar.get_y() + bar.get_height()/2,
                     f"{val:.1f}", va="center")
        plt.title(f"Behavioral Profile — {student.student_id}  "
                  f"({student.major}, Sem {student.semester})")
        plt.xlabel("Score / Value (0–10 scale)")
        plt.xlim(0, 13)
        plt.tight_layout()
        plt.savefig(f"data/reports/trend_{student.student_id}.png")
        plt.show()

    def plot_class_average_by_subject(self, averages_by_group):
        """
        Bar chart of average exam score per semester (1–8).
        averages_by_group = {"1": avg, "2": avg, ...}
        """
        labels = list(averages_by_group.keys())
        values = list(averages_by_group.values())

        plt.figure(figsize=(9, 5))
        bars = plt.bar(labels, values,
                       color=["#3498db" if int(l) <= 4 else "#e67e22"
                              for l in labels])
        for bar, val in zip(bars, values):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
                     f"{val:.1f}", ha="center", fontsize=9)
        plt.title("Average Exam Score by Semester\n"
                  "(Blue = Undergraduate   Orange = Graduate)")
        plt.xlabel("Semester")
        plt.ylabel("Average Exam Score")
        plt.ylim(0, 105)
        plt.tight_layout()
        plt.savefig("data/reports/subject_averages.png")
        plt.show()

    def plot_top_students(self, top_students):
        """Horizontal bar chart of top 5 students by exam score."""
        ids    = [s.student_id for s in top_students]
        scores = [s.exam_score for s in top_students]

        plt.figure(figsize=(7, 4))
        bars = plt.barh(ids, scores, color="teal")
        for bar, val in zip(bars, scores):
            plt.text(bar.get_width() + 0.2,
                     bar.get_y() + bar.get_height()/2,
                     f"{val:.1f}", va="center", fontweight="bold")
        plt.title("Top 5 Students by Exam Score")
        plt.xlabel("Exam Score")
        plt.xlim(0, 110)
        plt.tight_layout()
        plt.savefig("data/reports/top_students.png")
        plt.show()
