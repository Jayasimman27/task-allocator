from tinydb import TinyDB

db = TinyDB("tasks.json")

def save_tasks(result):
    for t in result["tasks"]:
        db.insert(t)
