from .student import Student


class UndergraduateStudent(Student):
    """
    Semester 1-4 students.
    Standard exam scoring, no GPA bonus.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = "Undergraduate"

    def get_gpa(self):
        return super().get_gpa()      # Standard 0–100 conversion

    def generate_report(self):        # Polymorphism
        return (
            f"{'─' * 46}\n"
            f"  UNDERGRADUATE STUDENT REPORT\n"
            f"{'─' * 46}\n"
            f"  ID               : {self.student_id}\n"
            f"  Major            : {self.major}\n"
            f"  Semester         : {self.semester}\n"
            f"  Age / Gender     : {self.age}  /  {self.gender}\n"
            f"\n  ── Academic ───────────────────────────────\n"
            f"  Previous GPA     : {self.previous_gpa:.2f}  (out of 4.0)\n"
            f"  Exam Score       : {self.exam_score:.1f} / 100\n"
            f"  Dropout Risk     : {self.dropout_risk}\n"
            f"\n  ── Study Habits ───────────────────────────\n"
            f"  Study Hrs/Day    : {self.study_hours_per_day:.1f}\n"
            f"  Attendance       : {self.attendance_percentage:.1f}%\n"
            f"  Study Environ.   : {self.study_environment}\n"
            f"  Tutoring         : {self.access_to_tutoring}\n"
            f"  Time Management  : {self.time_management_score:.1f} / 10\n"
            f"\n  ── Screen & Leisure ───────────────────────\n"
            f"  Social Media     : {self.social_media_hours:.1f} hrs/day\n"
            f"  Netflix          : {self.netflix_hours:.1f} hrs/day\n"
            f"  Total Screen     : {self.screen_time:.1f} hrs/day\n"
            f"\n  ── Health & Wellbeing ─────────────────────\n"
            f"  Sleep Hours      : {self.sleep_hours:.1f}\n"
            f"  Diet Quality     : {self.diet_quality}\n"
            f"  Exercise         : {self.exercise_frequency:.0f} days/week\n"
            f"  Mental Health    : {self.mental_health_rating:.1f} / 10\n"
            f"  Stress Level     : {self.stress_level:.1f} / 10\n"
            f"  Exam Anxiety     : {self.exam_anxiety_score:.1f} / 10\n"
            f"\n  ── Socio-economic ─────────────────────────\n"
            f"  Part-time Job    : {self.part_time_job}\n"
            f"  Family Income    : {self.family_income_range}\n"
            f"  Parent Education : {self.parental_education_level}\n"
            f"  Parent Support   : {self.parental_support_level} / 10\n"
            f"  Internet Quality : {self.internet_quality}\n"
            f"\n  ── Engagement ──────────────────────────────\n"
            f"  Extracurricular  : {self.extracurricular_participation}\n"
            f"  Motivation       : {self.motivation_level:.1f} / 10\n"
            f"  Learning Style   : {self.learning_style}\n"
            f"{'─' * 46}\n"
        )


class GraduateStudent(Student):
    """
    Semester 5–8 students.
    +3 bonus added to exam score to reflect advanced coursework difficulty.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = "Graduate"

    def get_gpa(self):
        # Graduate students get a +5 GPA point bonus for difficulty
        return round(min(super().get_gpa() + 5, 100), 2)

    def generate_report(self):        # Polymorphism
        return (
            f"{'─' * 46}\n"
            f"  GRADUATE STUDENT REPORT\n"
            f"{'─' * 46}\n"
            f"  ID               : {self.student_id}\n"
            f"  Field of Study   : {self.major}\n"
            f"  Semester         : {self.semester}\n"
            f"  Age / Gender     : {self.age}  /  {self.gender}\n"
            f"\n  ── Academic ───────────────────────────────\n"
            f"  Previous GPA     : {self.previous_gpa:.2f}  (out of 4.0)\n"
            f"  Exam Score       : {self.exam_score:.1f} / 100\n"
            f"  Weighted Score   : {min(self.exam_score + 3, 100):.1f} / 100  (+3 grad bonus)\n"
            f"  Dropout Risk     : {self.dropout_risk}\n"
            f"\n  ── Study Habits ───────────────────────────\n"
            f"  Study Hrs/Day    : {self.study_hours_per_day:.1f}\n"
            f"  Attendance       : {self.attendance_percentage:.1f}%\n"
            f"  Study Environ.   : {self.study_environment}\n"
            f"  Tutoring         : {self.access_to_tutoring}\n"
            f"  Time Management  : {self.time_management_score:.1f} / 10\n"
            f"\n  ── Screen & Leisure ───────────────────────\n"
            f"  Social Media     : {self.social_media_hours:.1f} hrs/day\n"
            f"  Netflix          : {self.netflix_hours:.1f} hrs/day\n"
            f"  Total Screen     : {self.screen_time:.1f} hrs/day\n"
            f"\n  ── Health & Wellbeing ─────────────────────\n"
            f"  Sleep Hours      : {self.sleep_hours:.1f}\n"
            f"  Diet Quality     : {self.diet_quality}\n"
            f"  Exercise         : {self.exercise_frequency:.0f} days/week\n"
            f"  Mental Health    : {self.mental_health_rating:.1f} / 10\n"
            f"  Stress Level     : {self.stress_level:.1f} / 10\n"
            f"  Exam Anxiety     : {self.exam_anxiety_score:.1f} / 10\n"
            f"\n  ── Socio-economic ─────────────────────────\n"
            f"  Part-time Job    : {self.part_time_job}\n"
            f"  Family Income    : {self.family_income_range}\n"
            f"  Parent Education : {self.parental_education_level}\n"
            f"  Parent Support   : {self.parental_support_level} / 10\n"
            f"  Internet Quality : {self.internet_quality}\n"
            f"\n  ── Engagement ──────────────────────────────\n"
            f"  Extracurricular  : {self.extracurricular_participation}\n"
            f"  Motivation       : {self.motivation_level:.1f} / 10\n"
            f"  Learning Style   : {self.learning_style}\n"
            f"{'─' * 46}\n"
        )
