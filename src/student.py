class Student:
    """
    Base student class built around the Enhanced Student Habits & Performance dataset.

    Attributes cover demographics, 20+ behavioral habits, and academic outcome.
    Target prediction: exam_score (0–100)
    """

    def __init__(self, student_id, age, gender, major, semester,
                 study_hours_per_day, social_media_hours, netflix_hours,
                 part_time_job, attendance_percentage, sleep_hours,
                 diet_quality, exercise_frequency, parental_education_level,
                 internet_quality, mental_health_rating,
                 extracurricular_participation, previous_gpa,
                 stress_level, dropout_risk, social_activity, screen_time,
                 study_environment, access_to_tutoring, family_income_range,
                 parental_support_level, motivation_level, exam_anxiety_score,
                 learning_style, time_management_score, exam_score):

        # ── Identifiers ───────────────────────────────────────────────────────
        self.__student_id = str(student_id)
        self.__age        = int(age)
        self.__gender     = str(gender)
        self.__major      = str(major)
        self.__semester   = int(semester)       # 1–4 undergrad  |  5–8 grad

        # ── Academic ──────────────────────────────────────────────────────────
        self.__previous_gpa = float(previous_gpa)   # 0.0–4.0 scale
        self.__exam_score   = float(exam_score)      # 0–100 (prediction target)
        self.__dropout_risk = str(dropout_risk)      # "Yes" / "No"

        # ── Study Habits ──────────────────────────────────────────────────────
        self.__study_hours_per_day  = float(study_hours_per_day)
        self.__attendance_percentage = float(attendance_percentage)
        self.__study_environment    = str(study_environment)
        self.__access_to_tutoring   = str(access_to_tutoring)
        self.__time_management_score = float(time_management_score)

        # ── Screen / Leisure ──────────────────────────────────────────────────
        self.__social_media_hours = float(social_media_hours)
        self.__netflix_hours      = float(netflix_hours)
        self.__screen_time        = float(screen_time)
        self.__social_activity    = float(social_activity)

        # ── Health & Lifestyle ────────────────────────────────────────────────
        self.__sleep_hours          = float(sleep_hours)
        self.__diet_quality         = str(diet_quality)         # Poor/Fair/Good
        self.__exercise_frequency   = float(exercise_frequency) # days/week
        self.__mental_health_rating = float(mental_health_rating)
        self.__stress_level         = float(stress_level)
        self.__exam_anxiety_score   = float(exam_anxiety_score)

        # ── Socio-economic ────────────────────────────────────────────────────
        self.__part_time_job           = str(part_time_job)
        self.__parental_education_level = str(parental_education_level)
        self.__parental_support_level   = int(parental_support_level)
        self.__family_income_range      = str(family_income_range)
        self.__internet_quality         = str(internet_quality)

        # ── Engagement ────────────────────────────────────────────────────────
        self.__extracurricular_participation = str(extracurricular_participation)
        self.__motivation_level   = float(motivation_level)
        self.__learning_style     = str(learning_style)

    # ── Getters ───────────────────────────────────────────────────────────────
    @property
    def student_id(self):               return self.__student_id
    @property
    def age(self):                      return self.__age
    @property
    def gender(self):                   return self.__gender
    @property
    def major(self):                    return self.__major
    @property
    def semester(self):                 return self.__semester
    @property
    def previous_gpa(self):             return self.__previous_gpa
    @property
    def exam_score(self):               return self.__exam_score
    @property
    def dropout_risk(self):             return self.__dropout_risk
    @property
    def study_hours_per_day(self):      return self.__study_hours_per_day
    @property
    def attendance_percentage(self):    return self.__attendance_percentage
    @property
    def study_environment(self):        return self.__study_environment
    @property
    def access_to_tutoring(self):       return self.__access_to_tutoring
    @property
    def time_management_score(self):    return self.__time_management_score
    @property
    def social_media_hours(self):       return self.__social_media_hours
    @property
    def netflix_hours(self):            return self.__netflix_hours
    @property
    def screen_time(self):              return self.__screen_time
    @property
    def social_activity(self):          return self.__social_activity
    @property
    def sleep_hours(self):              return self.__sleep_hours
    @property
    def diet_quality(self):             return self.__diet_quality
    @property
    def exercise_frequency(self):       return self.__exercise_frequency
    @property
    def mental_health_rating(self):     return self.__mental_health_rating
    @property
    def stress_level(self):             return self.__stress_level
    @property
    def exam_anxiety_score(self):       return self.__exam_anxiety_score
    @property
    def part_time_job(self):            return self.__part_time_job
    @property
    def parental_education_level(self): return self.__parental_education_level
    @property
    def parental_support_level(self):   return self.__parental_support_level
    @property
    def family_income_range(self):      return self.__family_income_range
    @property
    def internet_quality(self):         return self.__internet_quality
    @property
    def extracurricular_participation(self): return self.__extracurricular_participation
    @property
    def motivation_level(self):         return self.__motivation_level
    @property
    def learning_style(self):           return self.__learning_style

    # ── Academic helpers ──────────────────────────────────────────────────────
    def get_gpa(self):
        """Return previous_gpa on 0–100 scale (converted from 4.0 scale)."""
        return round(self.__previous_gpa / 4.0 * 100, 2)

    def get_exam_score(self):
        return self.__exam_score

    # ── Magic methods ─────────────────────────────────────────────────────────
    def __str__(self):
        return (f"[{self.__student_id}] {self.__major} | "
                f"Sem {self.__semester} | "
                f"Exam: {self.__exam_score:.1f} | "
                f"GPA: {self.__previous_gpa:.2f}")

    def __repr__(self):
        return f"Student(id={self.__student_id}, major={self.__major})"

    def __eq__(self, other):
        return self.__student_id == other.student_id

    def __lt__(self, other):
        return self.__exam_score < other.exam_score    # Sort by exam score

    def __len__(self):
        return self.__semester                          # Semesters completed

    # ── Abstraction ───────────────────────────────────────────────────────────
    def generate_report(self):
        raise NotImplementedError("Subclasses must implement generate_report()")
