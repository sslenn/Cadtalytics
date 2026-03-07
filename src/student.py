
class Student:
    def __init__(self, student_id, name, age, year_level, study_time = 2, absences = 5,
                internet_usage = 4.0, extra_classes = 0, sleep_hours = 7.0, parent_education = 2):
        
        # core info
        self.__student_id = student_id
        self.__name = name
        self.__age = age
        self.__year_level = year_level
        self.__grades = {}
        
        # Behavioral
        self.__study_time = int(study_time)    
        self.__absences    = int(absences)    
        self.__internet_usage = float(internet_usage)
        self.__extra_classes = int(extra_classes)
        self.__sleep_hours = float(sleep_hours)
        self.__parent_education = int(parent_education)
        
    # core and behavioral getters
        
    @property   # this protect our data from outside class to modify and represent Encapsulation Pillar
    def student_id(self):  return self.__student_id
        
    @property
    def name(self): return self.__name
        
    @property
    def age(self):  return self.__age
        
    @property
    def grades(self):  return self.__grades
        
    @property
    def year_level(self):  return self.__year_level
        
    @property
    def study_time(self):  return self.__study_time
        
    @property
    def absences(self):  return self.__absences
        
    @property
    def internet_usage(self):   return self.__internet_usage
        
    @property
    def extra_classes(self):  return self.__extra_classes
        
    @property
    def sleep_hours(self):  return self.__sleep_hours
        
    @property
    def parent_education(self):  return self.__parent_education
    
    

    # add grade
    def add_grade(self, subject, period, score):
        if subject not in self.__grades:
            self.__grades[subject] = {}
        self.__grades[subject][period] = score
        
    # get gpa
    def get_gpa(self):
        all_scores = []
        
        for subject in self.__grades.values():
            for score in subject.values():
                all_scores.append(score)
        
        if all_scores:
            return round(sum(all_scores) / len(all_scores), 2)
        else:
            return 0.0
        
        
    # get period average
    def get_period_avg(self, period):
        scores = []
        
        for subject in self.__grades.values():
            if period in subject:
                scores.append(subject[period])
        
        if scores:
            return round(sum(scores) / len(scores), 2)
        else:
            return 0.0
        


    def __str__(self):
        return f"[{self.__student_id}] {self.__name} | Year {self.__year_level} | GPA: {self.get_gpa()}"
    
    def __repr__(self):
        return f"Student(id = {self.__student_id}, name = {self.__name})"

    def __eq__(self, other):
        return self.student_id == other.student_id
    
    def __lt__(self, other):
        return self.get_gpa() < other.get_gpa()
    
    def __len__(self):
        return len(self.__grades)
        
    
    def generate_report(self):
        # raise an error here to ensure that the subclass(student_type.py) must override it 
        raise NotImplementedError("Subclasses must implement generate_report()")