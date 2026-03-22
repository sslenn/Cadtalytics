# grade_manager.py
# This file is responsible for loading all student data from the CSV file
# and turning each row into a proper Student object that the rest of the
# program can use.

from .student_types import UndergraduateStudent, GraduateStudent


class GradeManager:

    def __init__(self):
        # This list will hold all the Student objects after loading
        self.student_list = []


    def load_from_records(self, records):
        # records is a list of dictionaries — each dictionary is one row
        # from the CSV file, where the keys are the column names.
        # Example of one record (one row):
        # {
        #   "student_id": "114592",
        #   "age": "22",
        #   "gender": "Other",
        #   "major": "Biology",
        #   "semester": "2",
        #   "exam_score": "91",
        #   ... and so on for all 31 columns
        # }

        # Reset the list every time we load fresh data
        self.student_list = []

        for row in records:
            try:
                # Read the semester number so we know which type of
                # student to create — undergraduate or graduate
                semester = int(float(row.get("semester", 1)))

                # Build a dictionary of all the arguments we need to
                # pass into the Student constructor.
                # We use row.get("column_name", default_value) so that
                # if a column is missing we use a safe default instead
                # of crashing.
                student_data = {
                    "student_id"                    : str(row["student_id"]),
                    "age"                           : int(float(row.get("age", 18))),
                    "gender"                        : str(row.get("gender", "Other")),
                    "major"                         : str(row.get("major", "Unknown")),
                    "semester"                      : semester,
                    "study_hours_per_day"           : float(row.get("study_hours_per_day", 5)),
                    "social_media_hours"            : float(row.get("social_media_hours", 2)),
                    "netflix_hours"                 : float(row.get("netflix_hours", 1)),
                    "part_time_job"                 : str(row.get("part_time_job", "No")),
                    "attendance_percentage"         : float(row.get("attendance_percentage", 80)),
                    "sleep_hours"                   : float(row.get("sleep_hours", 7)),
                    "diet_quality"                  : str(row.get("diet_quality", "Fair")),
                    "exercise_frequency"            : float(row.get("exercise_frequency", 3)),
                    "parental_education_level"      : str(row.get("parental_education_level", "High School")),
                    "internet_quality"              : str(row.get("internet_quality", "Medium")),
                    "mental_health_rating"          : float(row.get("mental_health_rating", 5)),
                    "extracurricular_participation" : str(row.get("extracurricular_participation", "No")),
                    "previous_gpa"                  : float(row.get("previous_gpa", 2.0)),
                    "stress_level"                  : float(row.get("stress_level", 5)),
                    "dropout_risk"                  : str(row.get("dropout_risk", "No")),
                    "social_activity"               : float(row.get("social_activity", 3)),
                    "screen_time"                   : float(row.get("screen_time", 5)),
                    "study_environment"             : str(row.get("study_environment", "Home")),
                    "access_to_tutoring"            : str(row.get("access_to_tutoring", "No")),
                    "family_income_range"           : str(row.get("family_income_range", "Medium")),
                    "parental_support_level"        : int(float(row.get("parental_support_level", 5))),
                    "motivation_level"              : float(row.get("motivation_level", 5)),
                    "exam_anxiety_score"            : float(row.get("exam_anxiety_score", 5)),
                    "learning_style"                : str(row.get("learning_style", "Reading")),
                    "time_management_score"         : float(row.get("time_management_score", 5)),
                    "exam_score"                    : float(row.get("exam_score", 0)),
                }

                # Semester 1 to 4 = undergraduate student
                # Semester 5 to 8 = graduate student
                if semester <= 4:
                    student = UndergraduateStudent(**student_data)
                else:
                    student = GraduateStudent(**student_data)

                self.student_list.append(student)

            except (KeyError, ValueError) as error:
                print("Skipping one invalid record:", error)

        print("GradeManager: loaded", len(self.student_list), "students.")
        return self.student_list


    def get_all_students(self):
        # Returns the full list of all student objects
        return self.student_list


    def get_student_by_id(self, student_id):
        # Search through the list and return the student whose ID matches.
        # Returns None if no match is found.
        for student in self.student_list:
            if student.student_id == str(student_id):
                return student
        return None


    def get_total_count(self):
        # Returns how many students are loaded
        return len(self.student_list)


    def get_top_students(self, number_of_students=10):
        # Sort all students by exam score from highest to lowest,
        # then return only the top N students.
        # The Student class has __lt__ defined so sorted() works on it.
        sorted_students = sorted(self.student_list, reverse=True)
        return sorted_students[:number_of_students]


    def get_at_risk_students(self, passing_threshold=60):
        # Return all students whose exam score is below the threshold.
        at_risk = []
        for student in self.student_list:
            if student.exam_score < passing_threshold:
                at_risk.append(student)
        return at_risk


    def get_dropout_risk_students(self):
        # Return all students who are flagged as dropout risk in the dataset
        result = []
        for student in self.student_list:
            if student.dropout_risk == "Yes":
                result.append(student)
        return result


    def get_students_by_type(self, student_type):
        # Return only undergraduate students or only graduate students
        # depending on what student_type string is passed in
        result = []
        for student in self.student_list:
            if student.type.lower() == student_type.lower():
                result.append(student)
        return result


    def search_by_name(self, keyword):
        # The new dataset does not have a name column so we search by ID
        return self.search_by_id(keyword)


    def search_by_id(self, keyword):
        # Return all students whose student_id contains the keyword
        result = []
        for student in self.student_list:
            if keyword.lower() in student.student_id.lower():
                result.append(student)
        return result


    def __str__(self):
        return "GradeManager: " + str(len(self.student_list)) + " students loaded"