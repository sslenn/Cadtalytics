# analytics.py
# This file computes all the statistics and analysis results
# that the GUI needs to display — averages, distributions,
# rankings, trends, and so on.
# It works on a list of Student objects provided by GradeManager.


class Analytics:

    def __init__(self, students):
        # students is the list of Student objects from GradeManager
        self.students = students


    # -------------------------------------------------------------------------
    # AVERAGES
    # -------------------------------------------------------------------------

    def class_average_per_subject(self, period="semester"):
        # This method is called by main.py view_semester_avg() to draw the
        # "Average Score by Semester" bar chart.
        # It groups students by their semester number and calculates the
        # average exam_score for each semester.
        # Returns a dictionary like: {"1": 85.2, "2": 87.4, "3": 83.1, ...}

        totals = {}
        counts = {}

        for student in self.students:
            # Use the semester number as the key (as a string)
            key = str(student.semester)

            if key not in totals:
                totals[key] = 0
                counts[key] = 0

            totals[key] = totals[key] + student.exam_score
            counts[key] = counts[key] + 1

        # Build the result dict sorted by semester number
        averages = {}
        for key in sorted(totals.keys(), key=int):
            averages[key] = round(totals[key] / counts[key], 2)

        return averages


    def overall_class_average(self):
        # Returns the average exam_score across all students combined
        if len(self.students) == 0:
            return 0.0

        total = 0
        for student in self.students:
            total = total + student.exam_score

        return round(total / len(self.students), 2)


    def subject_averages_by_period(self):
        # Returns average exam score and average previous GPA (scaled to 100)
        # as two data points — used by visualizer trend charts
        if len(self.students) == 0:
            return {}

        total_exam = 0
        total_gpa  = 0

        for student in self.students:
            total_exam = total_exam + student.exam_score
            # Convert GPA from 0-4.0 scale to 0-100 scale for comparison
            total_gpa  = total_gpa + (student.previous_gpa / 4.0 * 100)

        avg_exam = round(total_exam / len(self.students), 2)
        avg_gpa  = round(total_gpa  / len(self.students), 2)

        return {
            "exam_score":   [avg_exam],
            "previous_gpa": [avg_gpa],
        }


    # -------------------------------------------------------------------------
    # GRADE DISTRIBUTION
    # -------------------------------------------------------------------------

    def grade_distribution(self):
        # Called by main.py view_distribution() to draw the pie and bar charts.
        # Counts how many students fall into each letter grade band
        # based on their exam_score (0 to 100).
        # A = 90 and above
        # B = 80 to 89
        # C = 70 to 79
        # D = 60 to 69
        # F = below 60

        distribution = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}

        for student in self.students:
            score = student.exam_score

            if score >= 90:
                distribution["A"] = distribution["A"] + 1
            elif score >= 80:
                distribution["B"] = distribution["B"] + 1
            elif score >= 70:
                distribution["C"] = distribution["C"] + 1
            elif score >= 60:
                distribution["D"] = distribution["D"] + 1
            else:
                distribution["F"] = distribution["F"] + 1

        return distribution


    def grade_distribution_by_subject(self, major):
        # Same as grade_distribution but filtered to only one major.
        # The new dataset does not have subjects like math/science,
        # so we use major as the grouping instead.

        distribution = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}

        for student in self.students:
            if student.major.lower() != major.lower():
                continue

            score = student.exam_score

            if score >= 90:
                distribution["A"] = distribution["A"] + 1
            elif score >= 80:
                distribution["B"] = distribution["B"] + 1
            elif score >= 70:
                distribution["C"] = distribution["C"] + 1
            elif score >= 60:
                distribution["D"] = distribution["D"] + 1
            else:
                distribution["F"] = distribution["F"] + 1

        return distribution


    # -------------------------------------------------------------------------
    # STUDENT TREND
    # -------------------------------------------------------------------------

    def student_trend(self, student):
        # Called by visualizer.plot_student_trend() to draw a single
        # student's behavioral profile as a horizontal bar chart.
        # Returns a dictionary where each key is a label and each value
        # is a number — all on roughly the same 0-10 scale so they
        # look good side by side in a chart.

        return {
            "Study hrs/day"  : student.study_hours_per_day,
            "Sleep hrs"      : student.sleep_hours,
            "Motivation"     : student.motivation_level,
            "Mental health"  : student.mental_health_rating,
            "Time management": student.time_management_score,
            "Stress level"   : student.stress_level,
            "Exam anxiety"   : student.exam_anxiety_score,
        }


    def student_trend_values(self, student):
        # Returns just the values from student_trend as a plain list.
        # Some visualizer functions need a list instead of a dict.
        trend = self.student_trend(student)
        return list(trend.values())


    def trend_direction(self, student):
        # Compares the student's previous GPA (converted to 100 scale)
        # against their exam score to figure out if they are improving,
        # declining, or staying stable.

        gpa_on_100_scale = student.previous_gpa / 4.0 * 100
        exam             = student.exam_score

        if exam > gpa_on_100_scale + 2:
            return "Improving"
        elif exam < gpa_on_100_scale - 2:
            return "Declining"
        else:
            return "Stable"


    # -------------------------------------------------------------------------
    # MAJOR RANKING
    # -------------------------------------------------------------------------

    def subject_difficulty_ranking(self):
        # Called by main.py view_major_ranking() to draw the major ranking chart.
        # Groups students by major and calculates the average exam score
        # for each major. Returns them sorted from lowest to highest average
        # (lowest average = hardest major).
        # Returns a dict like: {"Biology": 82.1, "Engineering": 85.4, ...}

        totals = {}
        counts = {}

        for student in self.students:
            major = student.major

            if major not in totals:
                totals[major] = 0
                counts[major] = 0

            totals[major] = totals[major] + student.exam_score
            counts[major] = counts[major] + 1

        averages = {}
        for major in totals:
            averages[major] = round(totals[major] / counts[major], 2)

        # Sort from lowest average to highest average
        sorted_averages = dict(sorted(averages.items(), key=lambda item: item[1]))
        return sorted_averages


    # -------------------------------------------------------------------------
    # CLASS STATISTICS
    # -------------------------------------------------------------------------

    def class_gpa_stats(self):
        # Returns a summary of exam score statistics across all students.
        # Used for the stat cards at the top of various views.

        if len(self.students) == 0:
            return {"average": 0, "highest": 0, "lowest": 0, "total": 0}

        all_scores = []
        for student in self.students:
            all_scores.append(student.exam_score)

        stats = {
            "average": round(sum(all_scores) / len(all_scores), 2),
            "highest": round(max(all_scores), 2),
            "lowest":  round(min(all_scores), 2),
            "total":   len(all_scores),
        }

        return stats


    def passing_rate(self, passing_threshold=60):
        # Returns the percentage of students who scored above the threshold

        if len(self.students) == 0:
            return 0.0

        passing_count = 0
        for student in self.students:
            if student.exam_score >= passing_threshold:
                passing_count = passing_count + 1

        return round((passing_count / len(self.students)) * 100, 2)


    def dropout_risk_count(self):
        # Returns how many students are flagged as dropout risk

        count = 0
        for student in self.students:
            if student.dropout_risk == "Yes":
                count = count + 1
        return count


    # -------------------------------------------------------------------------
    # BEHAVIORAL AVERAGES
    # -------------------------------------------------------------------------

    def avg_study_hours(self):
        if len(self.students) == 0:
            return 0.0
        total = 0
        for student in self.students:
            total = total + student.study_hours_per_day
        return round(total / len(self.students), 2)


    def avg_sleep_hours(self):
        if len(self.students) == 0:
            return 0.0
        total = 0
        for student in self.students:
            total = total + student.sleep_hours
        return round(total / len(self.students), 2)


    def avg_stress_level(self):
        if len(self.students) == 0:
            return 0.0
        total = 0
        for student in self.students:
            total = total + student.stress_level
        return round(total / len(self.students), 2)


    def avg_mental_health(self):
        if len(self.students) == 0:
            return 0.0
        total = 0
        for student in self.students:
            total = total + student.mental_health_rating
        return round(total / len(self.students), 2)