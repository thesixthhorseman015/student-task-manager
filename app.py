from flask import Flask, render_template, request, redirect, url_for
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)  # Exposes the /metrics endpoint automatically

tasks = []
next_id = 1

@app.route("/")
def index():
    status = request.args.get("status", "all")
    visible_tasks = [
        task for task in tasks
        if status == "all" or task["status"] == status
    ]
    return render_template("index.html", tasks=visible_tasks, status=status)

@app.route("/add", methods=["POST"])
def add_task():
    global next_id
    title = request.form.get("title", "").strip()
    deadline = request.form.get("deadline", "").strip()
    if not title:
        return "Task title is required", 400
    tasks.append({
        "id": next_id,
        "title": title,
        "deadline": deadline,
        "status": "pending"
    })
    next_id += 1
    return redirect(url_for("index"))

@app.route("/complete/<int:task_id>", methods=["POST"])
def complete_task(task_id):
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = "completed"
            break
    return redirect(url_for("index"))

@app.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task["id"] != task_id]
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True, port=5000)