import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(160), nullable=False)
    description = db.Column(db.Text, nullable=False, default="")
    priority = db.Column(db.String(16), nullable=False, default="medium")
    completed = db.Column(db.Boolean, nullable=False, default=False)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "completed": self.completed,
        }

def create_app(config=None):
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL", "sqlite:///tasks.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    if config:
        app.config.update(config)
    db.init_app(app)

    with app.app_context():
        db.create_all()

    @app.get("/healthz")
    def health():
        return jsonify(status="healthy")

    @app.get("/api/tasks")
    def list_tasks():
        tasks = db.session.execute(db.select(Task).order_by(Task.id.desc())).scalars()
        return jsonify([task.to_dict() for task in tasks])

    @app.post("/api/tasks")
    def create_task():
        data = request.get_json(silent=True) or {}
        title = str(data.get("title", "")).strip()
        priority = str(data.get("priority", "medium")).lower()
        if not title:
            return jsonify(error="title is required"), 400
        if priority not in {"low", "medium", "high"}:
            return jsonify(error="priority must be low, medium, or high"), 400
        task = Task(
            title=title,
            description=str(data.get("description", "")).strip(),
            priority=priority,
        )
        db.session.add(task)
        db.session.commit()
        return jsonify(task.to_dict()), 201

    @app.get("/api/tasks/<int:task_id>")
    def get_task(task_id):
        task = db.session.get(Task, task_id)
        if not task:
            return jsonify(error="task not found"), 404
        return jsonify(task.to_dict())

    @app.patch("/api/tasks/<int:task_id>")
    def update_task(task_id):
        task = db.session.get(Task, task_id)
        if not task:
            return jsonify(error="task not found"), 404
        data = request.get_json(silent=True) or {}
        if "title" in data:
            title = str(data["title"]).strip()
            if not title:
                return jsonify(error="title cannot be empty"), 400
            task.title = title
        if "description" in data:
            task.description = str(data["description"]).strip()
        if "priority" in data:
            priority = str(data["priority"]).lower()
            if priority not in {"low", "medium", "high"}:
                return jsonify(error="priority must be low, medium, or high"), 400
            task.priority = priority
        if "completed" in data:
            if not isinstance(data["completed"], bool):
                return jsonify(error="completed must be boolean"), 400
            task.completed = data["completed"]
        db.session.commit()
        return jsonify(task.to_dict())

    @app.delete("/api/tasks/<int:task_id>")
    def delete_task(task_id):
        task = db.session.get(Task, task_id)
        if not task:
            return jsonify(error="task not found"), 404
        db.session.delete(task)
        db.session.commit()
        return "", 204

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
