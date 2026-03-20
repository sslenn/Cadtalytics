import csv
import os

class FileHandler:
    def __init__(self, filepath):
        self.filepath = filepath

    def load_csv(self):
        records = []
        try:
            if not os.path.exists(self.filepath):
                raise FileNotFoundError(f"File not found: {self.filepath}")

            with open(self.filepath, "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    records.append(row)

            print(f" Loaded {len(records)} records from {self.filepath}")
            return records

        except FileNotFoundError as e:
            print(f" Error: {e}")
        except csv.Error as e:
            print(f" CSV Parsing Error: {e}")
        except Exception as e:
            print(f" Unexpected Error: {e}")

        return []

    def export_report(self, content, filename):
        try:
            output_path = f"data/reports/{filename}"
            os.makedirs("data/reports", exist_ok=True)

            with open(output_path, "w") as file:
                file.write(content)

            print(f" Report exported to {output_path}")

        except PermissionError:
            print(" Permission denied when writing report.")
        except Exception as e:
            print(f" Failed to export report: {e}")