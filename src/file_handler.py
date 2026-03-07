import csv
import os

class FileHandler:
    def __init__(self, filepath):
        self.filepath = filepath
        
        
    # load the data from our csv file which is stored in the data folder
    def load_csv(self):
        records = []
        
        try:
            if not os.path.exists(self.filepath):  # check before opening a file, if existed, if not raise an error instead of crashing
                raise FileNotFoundError(f"File not found: {self.filepath}")
        
            with open(self.filepath, 'r') as file:
                reader = csv.DictReader(file)  # 
                for row in reader:
                    records.append(row)
            print(f"Loaded {len(records)} records from {self.filepath}")
            return records
        
        
        except FileNotFoundError as error:
            print(f"Error: {error}")
        except csv.Error as error:
            print(f"CSV parsing Error: {error}")
        except Exception as error:
            print(f"Unexpected Error: {error}")
        
        return records
    

    def export_report(self, content, filename):
        try:
            output_path = f"data/reports/{filename}"
            os.makedirs("data/reports", exist_ok = True)
            
            with open(output_path, "w") as file:
                file.write(content)
                
            print(f"Report exported to {output_path}")
        except PermissionError:
            print("Permission denied when  writing report.")
        except Exception as error:
            print(f"Failed to export report: {error}")