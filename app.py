from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
from dateutil import parser
from flask import jsonify
import os

# from app import app, task
# import logging

# Configure logging
# logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# Configure the database URI. For SQLite, the URI is in the format: 'sqlite:///path/to/database.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'tasks.db')

# Suppress deprecation warnings
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the SQLAlchemy extension
db = SQLAlchemy(app)

# Define Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    due_date = db.Column(db.Date, nullable=False)


# Routes
@app.route('/')
def index():
    tasks = Task.query.all()
    print(" ")
    print(tasks)
    print("")
    # logging.debug(f"Retrieved {len(tasks)} tasks from the database")
    return render_template('index.html', tasks=tasks)


# Route for getting all tasks
@app.route('/api/tasks', methods=['GET'])
def get_tasks_api():
    tasks = Task.query.all()
    output = []
    for task in tasks:
        task_data = {
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'due_date': task.due_date.strftime('%Y-%m-%d')  # Convert date to string format
        }
        output.append(task_data)
    return jsonify({'tasks': output})


# Route for creating a new task
@app.route('/api/tasks', methods=['POST'])
def create_task():
    # Extract data from the request
    data = request.json
    title = data.get('title')
    description = data.get('description')
    due_date = data.get('due_date')

    # Create a new task object
    new_task = Task(title=title, description=description, due_date=due_date)

    # Add the task to the database session
    db.session.add(new_task)
    db.session.commit()

    # Return a JSON response indicating success
    return jsonify({'message': 'Task created successfully'}), 201


# Route for updating an existing task
@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    # Find the task by its ID
    task = Task.query.get_or_404(task_id)

    # Extract data from the request
    data = request.json
    title = data.get('title')
    description = data.get('description')
    due_date = data.get('due_date')

    # Update the task attributes
    task.title = title
    task.description = description
    task.due_date = due_date

    # Commit the changes to the database
    db.session.commit()

    # Return a JSON response indicating success
    return jsonify({'message': 'Task updated successfully'})


# Route for deleting a task
@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    # Find the task by its ID
    task = Task.query.get_or_404(task_id)

    # Delete the task from the database session
    db.session.delete(task)
    db.session.commit()

    # Return a JSON response indicating success
    return jsonify({'message': 'Task deleted successfully'})


# Connection confirmation
def test_database_connection():
    with app.app_context():  # Set up the application context
        try:
            task = Task.query.first()  # Fetch the first task from the database
            print("Database connection successful!")
            print("Sample task:", task)
        except Exception as e:
            print("Error:", e)



# Run the application
if __name__ == '__main__':
    # db.create_all()
    test_database_connection()
    app.run(debug=True)


