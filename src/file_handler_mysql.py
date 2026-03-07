import mysql.connector
import os

class FileHandlerMySQL:
    def __init__(self, host, port, user, password, database):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host = self.host,
                port = self.port,
                user = self.user,
                password = self.password,
                database = self.database
            )
            print("Connected to MySQL database")
        except mysql.connector.Error as error:
            print(f"Connection failed: {error}")
        
        
    def load_csv(self):
        records = []
        
        try:
            if self.connection is None:
                raise ConnectionError("Noo active database connection.")
            cursor = self.connection.cursor(dictionary = True)
            cursor.execute("SELECT * FROM students")
            records = cursor.fetchall()
            
            records = [{k: str(v) if v is not None else "" for k, v in row.items()} for row in records]
            print(f"Loaded {len(records)} records from mySQL.")
            
        except mysql.connector.Error as error:
            print(f"Query failed: {error}")
        except ConnectionError as error:
            print(f"Connection error: {error}")
            
        return records
    
    
    # export thereport and store in the data folder inside report folder
    def export_report(self, content, filename):
        try:
            output_path = f"data/reports/{filename}"
            os.makedirs("data/reports", exist_ok = True)
            
            with open(output_path, "w") as file:
                file.write(content)
            print(f"Report exported to {output_path}")
        except PermissionError:
            print("Permission denied when writing report.")
        except Exception as error:
            print(f"Failed to export report: {error}")
            

    # disconnect from MySQL
    def disconnect(self):
        if self.connection:
            self.connection.close()
            print("Disconnect from MySQL.")