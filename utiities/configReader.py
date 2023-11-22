import json


class BoundaryConditionsReader:
    def __init__(self, file_path: str) -> None:
        try:
            with open(file_path, "r") as file:
                self.json_content = json.load(file)
        except FileNotFoundError:
            print("File not found. Please provide a valid file path.")
        except KeyError:
            print("Invalid JSON format. Make sure your JSON file contains proper fields.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")


    def readFile(self, file_path: str):
        pass
