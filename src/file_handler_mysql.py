import mysql.connector
import os

class FileHandlerMySQL:
    def __init__(self, host,port, user, password, database):
        self.host = host
        self.user = user
        self.port = port
        self.password = password
        self.database = database
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                port=self.port,       
                user=self.user,
                password=self.password,
                database=self.database
            )
            print(" Connected to MySQL database.")
        except mysql.connector.Error as e:
            print(f"Connection failed: {e}")

    def load_csv(self):           
        records = []
        try:
            if self.connection is None:
                raise ConnectionError("No active database connection.")

            cursor = self.connection.cursor(dictionary=True)  
            cursor.execute("SELECT * FROM students")
            records = cursor.fetchall()

            # Convert all values to strings to match CSV behavior
            records = [{k: str(v) if v is not None else "" for k, v in row.items()} for row in records]

            print(f" Loaded {len(records)} records from MySQL.")
        except mysql.connector.Error as e:
            print(f" Query failed: {e}")
        except ConnectionError as e:
            print(f" Connection error: {e}")
        return records


    # export the student info 
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


    def disconnect(self):
        if self.connection:
            self.connection.close()
            print(" Disconnected from MySQL.")