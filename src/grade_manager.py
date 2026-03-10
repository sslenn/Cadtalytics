from .student_types import UndergraduateStudent, GraduateStudent


class GradeManager:

    def __init__(self):
        self.student_list = []


    def load_from_records(self, records):
        for row in records:
            try:
                study_time = int(float(row.get("study_time", 2)))
                absences = int(float(row.get("absences", 5)))
                internet_usage = float(row.get("internet_usage", 4.0))
                extra_classes = int(float(row.get("extra_classes", 0)))
                sleep_hours = float(row.get("sleep_hours", 7.0))
                parent_education = int(float(row.get("parent_education", 2)))

                if row["type"] == "undergraduate":
                    student = UndergraduateStudent(
                        row["student_id"],
                        row["name"],
                        int(row["age"]),
                        int(row["year_level"]),
                        row["major"],
                        study_time,
                        absences,
                        internet_usage,
                        extra_classes,
                        sleep_hours,
                        parent_education
                    )
                else:
                    student = GraduateStudent(
                        row["student_id"],
                        row["name"],
                        int(row["age"]),
                        int(row["year_level"]),
                        row["thesis_topic"],
                        study_time,
                        absences,
                        internet_usage,
                        extra_classes,
                        sleep_hours,
                        parent_education
                    )

                for period in ["G1", "G2", "G3"]:
                    for subject in ["math", "science", "english", "programming"]:
                        key = subject + "_" + period
                        if key in row and row[key] != "":
                            student.add_grade(subject, period, float(row[key]))

                self.student_list.append(student)

            except (KeyError, ValueError) as error:
                print("Skipping invalid record:", error)


    def get_all_students(self):
        return self.student_list


    def get_student_by_id(self, student_id):
        for student in self.student_list:
            if student.student_id == student_id:
                return student
        return None


    def get_total_count(self):
        return len(self.student_list)


    def get_top_students(self, number_of_students=5):
        sorted_students = sorted(self.student_list, reverse=True)
        return sorted_students[:number_of_students]


    def get_at_risk_students(self, passing_threshold=60):
        at_risk = []
        for student in self.student_list:
            if student.get_gpa() < passing_threshold:
                at_risk.append(student)
        return at_risk


    def get_students_by_type(self, student_type):
        result = []
        for student in self.student_list:
            if student.type.lower() == student_type.lower():
                result.append(student)
        return result


    def search_by_name(self, keyword):
        result = []
        for student in self.student_list:
            if keyword.lower() in student.name.lower():
                result.append(student)
        return result