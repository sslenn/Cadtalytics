# predictor.py
# This file handles all the Machine Learning for the project.
# It trains a Random Forest model on student behavioral data
# and uses it to predict a student's exam score (0 to 100).
#
# The main.py file uses this class like this:
#   predictor = GradePredictor()
#   predictor.train(students)
#   score = predictor.predict_exam_score(...)
#   score = predictor.predict_for_student(student)

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error
from sklearn.preprocessing import LabelEncoder


class GradePredictor:

    def __init__(self):
        # The Random Forest model — 200 trees for good accuracy
        self.model = RandomForestRegressor(n_estimators=200, random_state=42, n_jobs=-1)

        # We need to convert text columns (like "Male", "Poor", "Yes")
        # into numbers before the model can use them.
        # LabelEncoder does this — we store one encoder per column
        # so we can reuse them later when predicting.
        self.encoders = {}

        # These are all the text columns that need to be converted to numbers
        self.categorical_columns = [
            "gender",
            "diet_quality",
            "part_time_job",
            "parental_education_level",
            "internet_quality",
            "extracurricular_participation",
            "access_to_tutoring",
            "family_income_range",
            "learning_style",
            "study_environment",
        ]

        # These are the 25 input features the model uses to make predictions.
        # They must match exactly the column names in the CSV and the
        # property names on the Student class.
        self.feature_columns = [
            "study_hours_per_day",
            "attendance_percentage",
            "sleep_hours",
            "exercise_frequency",
            "mental_health_rating",
            "previous_gpa",
            "stress_level",
            "social_media_hours",
            "netflix_hours",
            "screen_time",
            "exam_anxiety_score",
            "time_management_score",
            "motivation_level",
            "parental_support_level",
            "social_activity",
            "gender",
            "diet_quality",
            "part_time_job",
            "parental_education_level",
            "internet_quality",
            "extracurricular_participation",
            "access_to_tutoring",
            "family_income_range",
            "learning_style",
            "study_environment",
        ]

        # These will be set after training and are used by main.py
        # to display results in the GUI views
        self.is_trained = False
        self.r2         = None   # R2 score — how accurate the model is (0 to 1)
        self.mae        = None   # MAE — average points the prediction is off by
        self.y_test     = None   # The actual exam scores from the test set
        self.y_pred     = None   # The predicted exam scores from the test set


    # -------------------------------------------------------------------------
    # TRAINING
    # -------------------------------------------------------------------------

    def train(self, students):
        # This is called by main.py after loading the CSV data.
        # It takes a list of Student objects and trains the Random Forest model.

        # Step 1: Convert each Student object into a flat dictionary
        # so we can put all students into a pandas DataFrame
        records = []
        for student in students:
            record = self._student_to_dict(student)
            records.append(record)

        df = pd.DataFrame(records)

        # Step 2: Convert text columns to numbers using LabelEncoder.
        # We pass fit=True so the encoders learn all possible values
        # from this training data.
        df = self._encode_text_columns(df, fit=True)

        # Step 3: Separate the input features (X) from the target (y)
        # X = all the behavioral columns the model learns from
        # y = exam_score — what the model is trying to predict
        X = df[self.feature_columns].apply(pd.to_numeric, errors="coerce").fillna(0)
        y = pd.to_numeric(df["exam_score"], errors="coerce").fillna(0)

        # Step 4: Split into training set (80%) and test set (20%)
        # The model trains on the training set and we measure accuracy
        # using the test set — which the model has never seen before
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # Step 5: Train the model
        self.model.fit(X_train, y_train)

        # Step 6: Make predictions on the test set to measure accuracy
        y_pred = self.model.predict(X_test)

        # Step 7: Calculate and store accuracy metrics
        # R2 — closer to 1.0 means the model predicts very well
        # MAE — the average number of points the prediction is off
        self.r2     = round(r2_score(y_test, y_pred), 4)
        self.mae    = round(mean_absolute_error(y_test, y_pred), 2)
        self.y_test = y_test
        self.y_pred = y_pred

        self.is_trained = True

        print("GradePredictor: training complete.")
        print("  R2 Score:", self.r2)
        print("  MAE     :", self.mae)


    # -------------------------------------------------------------------------
    # PREDICTION
    # -------------------------------------------------------------------------

    def predict_exam_score(
        self,
        study_hours_per_day,
        attendance_percentage,
        sleep_hours,
        exercise_frequency,
        mental_health_rating,
        previous_gpa,
        stress_level,
        social_media_hours,
        netflix_hours,
        screen_time,
        exam_anxiety_score,
        time_management_score,
        motivation_level,
        parental_support_level,
        gender,
        diet_quality,
        part_time_job,
        parental_education_level,
        internet_quality,
        extracurricular_participation,
        access_to_tutoring,
        family_income_range,
        learning_style,
        study_environment,
    ):
        # This method is called by main.py when the user fills in the
        # Manual Prediction form and clicks Predict.
        # Each parameter matches one field in the form exactly.

        if not self.is_trained:
            raise RuntimeError("The model has not been trained yet. Call train() first.")

        # Put all the input values into a dictionary
        data = {
            "study_hours_per_day"           : study_hours_per_day,
            "attendance_percentage"          : attendance_percentage,
            "sleep_hours"                    : sleep_hours,
            "exercise_frequency"             : exercise_frequency,
            "mental_health_rating"           : mental_health_rating,
            "previous_gpa"                   : previous_gpa,
            "stress_level"                   : stress_level,
            "social_media_hours"             : social_media_hours,
            "netflix_hours"                  : netflix_hours,
            "screen_time"                    : screen_time,
            "exam_anxiety_score"             : exam_anxiety_score,
            "time_management_score"          : time_management_score,
            "motivation_level"               : motivation_level,
            "parental_support_level"         : parental_support_level,
            "social_activity"                : 3.0,
            "gender"                         : gender,
            "diet_quality"                   : diet_quality,
            "part_time_job"                  : part_time_job,
            "parental_education_level"       : parental_education_level,
            "internet_quality"               : internet_quality,
            "extracurricular_participation"  : extracurricular_participation,
            "access_to_tutoring"             : access_to_tutoring,
            "family_income_range"            : family_income_range,
            "learning_style"                 : learning_style,
            "study_environment"              : study_environment,
        }

        return self._predict_from_dict(data)


    def predict_for_student(self, student):
        # This method is called by main.py when the user enters a student ID
        # and clicks Predict by ID.
        # It reads all the behavioral data directly from the Student object.

        if not self.is_trained:
            raise RuntimeError("The model has not been trained yet. Call train() first.")

        data = self._student_to_dict(student)
        return self._predict_from_dict(data)


    def _predict_from_dict(self, data):
        # Shared helper used by both predict methods above.
        # Takes a dictionary of input values and returns a predicted score.

        # Put the single data point into a DataFrame (model expects a table)
        input_df = pd.DataFrame([data])

        # Convert text columns using the encoders that were fitted during training
        input_df = self._encode_text_columns(input_df, fit=False)

        # Make sure all feature columns exist — fill with 0 if missing
        for column in self.feature_columns:
            if column not in input_df.columns:
                input_df[column] = 0

        # Select only the feature columns in the right order
        X = input_df[self.feature_columns].apply(pd.to_numeric, errors="coerce").fillna(0)

        # Ask the model to predict and round the result
        predicted_score = self.model.predict(X)[0]

        # Make sure the score stays between 0 and 100
        predicted_score = float(np.clip(predicted_score, 0, 100))

        return round(predicted_score, 2)


    # -------------------------------------------------------------------------
    # REPORTING — used by GUI views in main.py
    # -------------------------------------------------------------------------

    def get_feature_importances(self):
        # Called by main.py view_feature_importance() to draw the chart
        # that shows which behavioral habit matters the most for predicting
        # exam scores.
        # Returns a list of (feature_name, importance_value) pairs,
        # sorted from most important to least important.

        if not self.is_trained:
            return []

        # Random Forest gives us an importance score for each feature
        importances = self.model.feature_importances_

        # Combine feature names with their importance scores
        pairs = []
        for i in range(len(self.feature_columns)):
            pairs.append((self.feature_columns[i], importances[i]))

        # Sort from highest importance to lowest
        pairs.sort(key=lambda x: x[1], reverse=True)

        return pairs


    def get_model_summary(self):
        # Called by main.py view_model_summary() to display a text summary
        # of the model in the GUI textbox.

        if not self.is_trained:
            return "Model has not been trained yet."

        top_features = self.get_feature_importances()[:5]

        if self.r2 >= 0.9:
            accuracy_label = "Excellent"
        elif self.r2 >= 0.7:
            accuracy_label = "Good"
        else:
            accuracy_label = "Acceptable"

        lines = []
        lines.append("=" * 52)
        lines.append("   RANDOM FOREST MODEL SUMMARY — CADTALYTICS")
        lines.append("=" * 52)
        lines.append("  Algorithm      : Random Forest Regressor")
        lines.append("  Trees          : 200 estimators")
        lines.append("  Features used  : " + str(len(self.feature_columns)))
        lines.append("  Training split : 80% train  /  20% test")
        lines.append("  Test samples   : " + str(len(self.y_test)))
        lines.append("")
        lines.append("── PERFORMANCE ──────────────────────────────────")
        lines.append("  R2 Score       : " + str(self.r2))
        lines.append("  MAE            : ±" + str(self.mae) + " points")
        lines.append("  Accuracy label : " + accuracy_label)
        lines.append("")
        lines.append("── TOP 5 MOST IMPORTANT FEATURES ────────────────")

        for i in range(len(top_features)):
            feature_name  = top_features[i][0]
            feature_value = top_features[i][1]
            rank = str(i + 1) + "."
            lines.append("  " + rank + " " + feature_name.ljust(35) + str(round(feature_value * 100, 2)) + "%")

        lines.append("")
        lines.append("── WHAT THE NUMBERS MEAN ────────────────────────")
        lines.append("  R2 = 1.0  means the model predicts perfectly")
        lines.append("  R2 = 0.0  means no better than guessing")
        lines.append("  MAE = average exam points off per prediction")
        lines.append("=" * 52)

        return "\n".join(lines)


    # -------------------------------------------------------------------------
    # HELPER METHODS
    # -------------------------------------------------------------------------

    def _student_to_dict(self, student):
        # Converts a Student object into a flat dictionary
        # so it can be put into a pandas DataFrame.
        # Every key here must match one of the feature_columns above.

        return {
            "study_hours_per_day"           : student.study_hours_per_day,
            "attendance_percentage"          : student.attendance_percentage,
            "sleep_hours"                    : student.sleep_hours,
            "exercise_frequency"             : student.exercise_frequency,
            "mental_health_rating"           : student.mental_health_rating,
            "previous_gpa"                   : student.previous_gpa,
            "stress_level"                   : student.stress_level,
            "social_media_hours"             : student.social_media_hours,
            "netflix_hours"                  : student.netflix_hours,
            "screen_time"                    : student.screen_time,
            "exam_anxiety_score"             : student.exam_anxiety_score,
            "time_management_score"          : student.time_management_score,
            "motivation_level"               : student.motivation_level,
            "parental_support_level"         : student.parental_support_level,
            "social_activity"                : student.social_activity,
            "gender"                         : student.gender,
            "diet_quality"                   : student.diet_quality,
            "part_time_job"                  : student.part_time_job,
            "parental_education_level"       : student.parental_education_level,
            "internet_quality"               : student.internet_quality,
            "extracurricular_participation"  : student.extracurricular_participation,
            "access_to_tutoring"             : student.access_to_tutoring,
            "family_income_range"            : student.family_income_range,
            "learning_style"                 : student.learning_style,
            "study_environment"              : student.study_environment,
            "exam_score"                     : student.exam_score,
        }


    def _encode_text_columns(self, df, fit):
        # Converts text columns into numbers so the model can use them.
        # "Male" becomes 0, "Female" becomes 1, "Other" becomes 2 — for example.
        # If fit=True we are training, so the encoder learns all possible values.
        # If fit=False we are predicting, so we reuse the already trained encoders.

        df = df.copy()

        for column in self.categorical_columns:
            if column not in df.columns:
                continue

            if fit == True:
                # Create a new encoder and fit it on this column
                encoder = LabelEncoder()
                df[column] = encoder.fit_transform(df[column].astype(str))
                self.encoders[column] = encoder

            else:
                # Reuse the encoder that was fitted during training
                if column in self.encoders:
                    encoder = self.encoders[column]

                    # Convert each value — if it is an unknown value
                    # that was not seen during training, use -1 instead
                    new_values = []
                    for value in df[column].astype(str):
                        if value in encoder.classes_:
                            new_values.append(int(encoder.transform([value])[0]))
                        else:
                            new_values.append(-1)

                    df[column] = new_values

        return df