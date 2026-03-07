from .student import Student

# we have 2 type of student such as Undergraduate and Graduate

class UndergraduateStudent(Student):
    def __init__(self, student_id, name, age, year_level, study_time = 2, absences = 5,
                internet_usage = 4.0, extra_classes = 0, sleep_hours = 7.0, parent_education = 2, major = ""):
        
        # inheritance from parent(Student)
        super().__init__(student_id, name, age, year_level, study_time, absences,
                internet_usage, extra_classes, sleep_hours, parent_education)
        self.major = major
        self.type = "Undergraduate"
        
        
    def get_gpa(self):
        return super().get_gpa()
    
    def generate_report(self):
        return (
            f"------------- Undergraduate Report --------------\n"
            f"Name:                               {self.name}\n"
            f"Major:                              {self.major}\n"
            f"GPA:                                {self.get_gpa()}\n"
            f"Subjects Enrolled:                  {len(self)}\n"
            f"Study time:                         {self.study_time} (1=<2h 2=2-5h 3=5-10h 4=>10h)\n"
            f"Absences:                           {self.absences}\n"
            f"Internet Usage:                     {self.internet_usage} hrs/day\n\n"
            f"Extra class:                        {'yes' if self.extra_class else 'No'}\n"
            f"Sleep hours:                        {self.sleep_hours} hrs/night\n"
            f"Parent Education:                   {self.parent_education}(0 = none .... 4 = degree)\n"  
        )
        
        
class GraduateStudent(Student):
    def __init__(self, student_id, name, age, year_level, thesis_topic, study_time = 2, 
                absences = 5, internet_usage = 4.0, extra_classes = 0, sleep_hours = 7.0, parent_education = 4.0):
        
        # inheritance from parent(Student)
        super().__init__(student_id, name, age, year_level, study_time, absences,
                internet_usage, extra_classes, sleep_hours, parent_education)
        self.thesis_topic = thesis_topic
        self.type = "GraduateStudent"
        
    def get_gpa(self):
        base = super().get_gpa()
        
        # +2 bonusfor grad difficulty as graduate student take harder course
        return round(min(base + 2, 100), 2)  # making sure it never exceed 100
    
    def generate_report(self):
        return (
            f"------------- Undergraduate Report --------------\n"
            f"Name:                               {self.name}\n"
            f"Major:                              {self.major}\n"
            f"GPA:                                {self.get_gpa()}\n"
            f"Subjects Enrolled:                  {len(self)}\n"
            f"Study time:                         {self.study_time}\n"
            f"Absences:                           {self.absences}\n"
            f"Internet Usage:                     {self.internet_usage} hrs/day\n\n"
            f"Extra class:                        {'yes' if self.extra_class else 'No'}\n"
            f"Sleep hours:                        {self.sleep_hours} hrs/night\n"
            f"Parent Education:                   {self.parent_education}(0 = none .... 4 = degree)\n"  
        )