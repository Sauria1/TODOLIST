import uuid
import json
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

def load_tasks():
    try:
        with open('tasks.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_tasks(tasks):
    with open('tasks.json', 'w') as file:
        json.dump(tasks, file)

tasks = load_tasks()

@app.route("/")
def index():
    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add():
    task_desc = request.form.get("description")
    task_date = request.form.get("date")
    if task_desc and task_date:
        task_id = str(uuid.uuid4())
        tasks.append({"id": task_id, "description": task_desc, "date": task_date})
        save_tasks(tasks)
    return redirect("/")

@app.route("/delete/<task_id>", methods=["POST"])
def delete(task_id):
    global tasks
    tasks = [task for task in tasks if task["id"] != task_id]
    save_tasks(tasks)
    return redirect("/")

@app.route("/edit/<task_id>", methods=["GET", "POST"])
def edit(task_id):
    task = next((task for task in tasks if task["id"] == task_id), None)
    if request.method == "POST" and task:
        task_desc = request.form.get("description")
        task_date = request.form.get("date")
        if task_desc and task_date:
            task["description"] = task_desc
            task["date"] = task_date
            save_tasks(tasks)
        return redirect("/")
    return render_template("edit.html", task=task, task_id=task_id)

if __name__ == "__main__":
    app.run(debug=True)
