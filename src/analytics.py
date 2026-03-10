class Analytics:

    def __init__(self, students):
        self.students = students


    # ── Class Averages ────────────────────────────────────────────────────────

    def class_average_per_subject(self, period="G1"):
        totals = {}
        counts = {}

        for student in self.students:
            for subject in student.grades:
                if period in student.grades[subject]:
                    score = student.grades[subject][period]

                    if subject not in totals:
                        totals[subject] = 0
                        counts[subject] = 0

                    totals[subject] = totals[subject] + score
                    counts[subject] = counts[subject] + 1

        averages = {}
        for subject in totals:
            averages[subject] = round(totals[subject] / counts[subject], 2)

        return averages


    def overall_class_average(self, period="G3"):
        all_scores = []

        for student in self.students:
            for subject in student.grades:
                if period in student.grades[subject]:
                    all_scores.append(student.grades[subject][period])

        if len(all_scores) == 0:
            return 0.0

        return round(sum(all_scores) / len(all_scores), 2)


    def subject_averages_by_period(self):
        result = {}

        for period in ["G1", "G2", "G3"]:
            period_averages = self.class_average_per_subject(period)
            for subject in period_averages:
                if subject not in result:
                    result[subject] = []
                result[subject].append(period_averages[subject])

        return result


    # ── Grade Distribution ────────────────────────────────────────────────────

    def grade_distribution(self, period="G3"):
        distribution = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}

        for student in self.students:
            for subject in student.grades:
                if period in student.grades[subject]:
                    score = student.grades[subject][period]

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


    def grade_distribution_by_subject(self, subject, period="G3"):
        distribution = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}

        for student in self.students:
            if subject in student.grades:
                if period in student.grades[subject]:
                    score = student.grades[subject][period]

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


    # ── Student Trend ─────────────────────────────────────────────────────────

    def student_trend(self, student):
        trend = {}

        for period in ["G1", "G2", "G3"]:
            scores = []
            for subject in student.grades:
                if period in student.grades[subject]:
                    scores.append(student.grades[subject][period])

            if len(scores) > 0:
                trend[period] = round(sum(scores) / len(scores), 2)
            else:
                trend[period] = 0.0

        return trend


    def student_trend_values(self, student):
        # Returns [G1_avg, G2_avg, G3_avg] as a plain list
        # This format is what the visualizer needs for the trend line chart
        trend = self.student_trend(student)
        return [trend["G1"], trend["G2"], trend["G3"]]


    def trend_direction(self, student):
        trend = self.student_trend(student)
        g1_average = trend["G1"]
        g3_average = trend["G3"]

        if g3_average > g1_average + 2:
            return "Improving"
        elif g3_average < g1_average - 2:
            return "Declining"
        else:
            return "Stable"


    # ── Subject Difficulty Ranking ────────────────────────────────────────────

    def subject_difficulty_ranking(self):
        subject_scores = {}

        for period in ["G1", "G2", "G3"]:
            period_averages = self.class_average_per_subject(period)
            for subject in period_averages:
                if subject not in subject_scores:
                    subject_scores[subject] = []
                subject_scores[subject].append(period_averages[subject])

        overall_averages = {}
        for subject in subject_scores:
            scores = subject_scores[subject]
            overall_averages[subject] = round(sum(scores) / len(scores), 2)

        sorted_subjects = dict(sorted(overall_averages.items(), key=lambda item: item[1]))
        return sorted_subjects


    # ── Class Statistics ──────────────────────────────────────────────────────

    def class_gpa_stats(self):
        if len(self.students) == 0:
            return {"average": 0, "highest": 0, "lowest": 0, "total": 0}

        all_gpas = []
        for student in self.students:
            all_gpas.append(student.get_gpa())

        stats = {
            "average": round(sum(all_gpas) / len(all_gpas), 2),
            "highest": round(max(all_gpas), 2),
            "lowest": round(min(all_gpas), 2),
            "total": len(all_gpas)
        }

        return stats


    def passing_rate(self, passing_threshold=60):
        if len(self.students) == 0:
            return 0.0

        passing_count = 0
        for student in self.students:
            if student.get_gpa() >= passing_threshold:
                passing_count = passing_count + 1

        return round((passing_count / len(self.students)) * 100, 2)