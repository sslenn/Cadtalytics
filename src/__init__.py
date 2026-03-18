# main.py stays clean
# Add all Class exports
from .student import Student 
from .student_types import UndergraduateStudent, GraduateStudent
from .file_handler import FileHandler
from .file_handler_mysql import FileHandlerMySQL

# Error handling when sombath's path not valid to import
try:
    from .grade_manager import GradeManager
    from .analytics import grade_distribution
    from .predictor import GradePredictor

except ImportError as e:
    
    print(f"Skipping missing team components: {e}")
    
    class GradeManager: pass
    class GradePredictor: pass
    class grade_distribution: pass

"""from .grade_manager import GradeManager
from .analytics import Analytics
from .predictor import GradePredictor"""

from .visualizer import (plot_grade_distribution_embedded, plot_top_students_embedded,
                          plot_class_average_by_subject_embedded, plot_feature_importance_embedded, 
                          plot_student_trend_embedded)