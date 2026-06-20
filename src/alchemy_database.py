import os
from pathlib import Path

class AlienDatabase:
    def __init__(self):
        self.data = {}

    def load(self, filename):
        path_data = f"src/{filename}"
        try:
            with open(path_data, "r") as f:
                data = json.load(f)
            self.data[data.name] = {i["key"]: i.get("value", 0) for i in data}
        except FileNotFoundError:
            pass

    def save(self):
        path_save = f"src/{self.data}" if self.data else None
        try:
            with open(path_save, "w") as f:
                json.dump((f.name,) + list(f.keys()), f)
            return True
        except IOError:
            pass

def run_aliens():
    db = AlienDatabase()
    # Create a sample data file
    import os
    with open("src/test_data.json", "w") as f:
        json.dump({"a": 1, "b": 2}, f)
    
    load_file = "./test" if os.path.exists("./test") else None
    db.load(load_file or os.path.join(os.getcwd(), ".aliens.db"))

if __name__ == "__main__":
    run_aliens()
