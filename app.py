from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
from dateutil import parser


app = Flask(__name__)

# Configure the database URI. For SQLite, the URI is in the format: 'sqlite:///path/to/database.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'

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


# Create database tables
with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def index():
    # Render the HTML template located in the templates folder
    return render_template('index.html')

# @app.route('/create')
# def create_task_page():
#     return render_template('create.html')

@app.route('/create', methods=['GET', 'POST'])
def create_task_page():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        due_date_str = request.form['due_date']

        # Split the date string into year, month, and day components
        year, month, day = map(int, due_date_str.split('-'))
        due_date = date(year, month, day)

        new_task = Task(title=title, description=description, due_date=due_date)
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('create.html')

@app.route('/create-task', methods=['POST'])
def create_task():
    title = request.form['title']
    description = request.form['description']
    due_date = request.form['due_date']
    new_task = Task(title=title, description=description, due_date=due_date)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    output = []
    for task in tasks:
        task_data = {'id': task.id, 'title': task.title, 'description': task.description, 'due_date': task.due_date}
        output.append(task_data)
    return jsonify({'tasks': output})

@app.route('/tasks', methods=['POST'])
def handle_task_creation():
    # Handle task creation logic here
    return 'Task created successfully!'


# @app.route('/tasks', methods=['POST'])
# def create_task():
#     data = request.get_json()
#     new_task = Task(title=data['title'], description=data['description'])
#     db.session.add(new_task)
#     db.session.commit()
#     return jsonify({'message': 'Task created successfully'}), 201



@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.get_json()
    task.title = data['title']
    task.description = data['description']
    task.status = data['status']
    db.session.commit()
    return jsonify({'message': 'Task updated successfully'})

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted successfully'})



# Run the application
if __name__ == '__main__':
    # db.create_all()
    app.run(debug=True)


