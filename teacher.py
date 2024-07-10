from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'abcd21234455'

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''  # Enter your MySQL password here
app.config['MYSQL_DB'] = 'teacher_part'

mysql = MySQL(app)

class User:
    def __init__(self, id, username):
        self.id = id
        self.username = username

# Global variable to track user authentication
current_user = None

@app.route('/login', methods=['GET', 'POST'])
def login():
    global current_user  # Use global variable
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, username, password FROM teachers WHERE username = %s", (username,))
        teacher = cur.fetchone()
        cur.close()
        if teacher and teacher[2] == password:
            user = User(id=teacher[0], username=teacher[1])
            current_user = user  # Set current user
            flash('Login successful', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'error')
    return render_template('login.html')

@app.route('/logout')
def logout():
    global current_user  # Use global variable
    current_user = None  # Reset current user
    return redirect(url_for('login'))# Route to display all tests
@app.route('/')
def index():
    user = getattr(User, 'current_user', None)
    if user and user.is_authenticated:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM tests WHERE teacher_id = %s", (user.id,))
        tests = cur.fetchall()
        cur.close()
        return render_template('index.html', tests=tests)
    else:
        return redirect(url_for('login'))

# Route to add a new test
@app.route('/add_test', methods=['POST'])
def add_test():
    user = getattr(User, 'current_user', None)
    if user and user.is_authenticated:
        test_name = request.form['test_name']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO tests (test_name, teacher_id) VALUES (%s, %s)", (test_name, user.id))
        mysql.connection.commit()
        cur.close()
    return redirect(url_for('index'))

# Route to update a test
@app.route('/update_test/<int:test_id>', methods=['POST'])
def update_test(test_id):
    user = getattr(User, 'current_user', None)
    if user and user.is_authenticated:
        new_test_name = request.form['new_test_name']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE tests SET test_name = %s WHERE id = %s AND teacher_id = %s",
                    (new_test_name, test_id, user.id))
        mysql.connection.commit()
        cur.close()
    return redirect(url_for('index'))

# Route to delete a test
@app.route('/delete_test/<int:test_id>', methods=['POST'])
def delete_test(test_id):
    user = getattr(User, 'current_user', None)
    if user and user.is_authenticated:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM tests WHERE id = %s AND teacher_id = %s", (test_id, user.id))
        mysql.connection.commit()
        cur.close()
    return redirect(url_for('index'))

# Route to display questions for a specific test
@app.route('/questions/<int:test_id>')
def questions(test_id):
    user = getattr(User, 'current_user', None)
    if user and user.is_authenticated:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM questions WHERE test_id = %s", (test_id,))
        questions = cur.fetchall()
        cur.close()
        return render_template('questions.html', test_id=test_id, questions=questions)
    else:
        return redirect(url_for('login'))

# Route to add a new question to a test
@app.route('/add_question/<int:test_id>', methods=['POST'])
def add_question(test_id):
    user = getattr(User, 'current_user', None)
    if user and user.is_authenticated:
        question_text = request.form['question_text']
        answer_text = request.form['answer_text']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO questions (test_id, question_text, answer_text) VALUES (%s, %s, %s)",
                    (test_id, question_text, answer_text))
        mysql.connection.commit()
        cur.close()
    return redirect(url_for('questions', test_id=test_id))

# Route to update a question
@app.route('/update_question/<int:question_id>', methods=['POST'])
def update_question(question_id):
    user = getattr(User, 'current_user', None)
    if user and user.is_authenticated:
        new_question_text = request.form['new_question_text']
        new_answer_text = request.form['new_answer_text']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE questions SET question_text = %s, answer_text = %s WHERE id = %s",
                    (new_question_text, new_answer_text, question_id))
        mysql.connection.commit()
        cur.close()
        test_id = request.form['test_id']
        return redirect(url_for('questions', test_id=test_id))
    else:
        return redirect(url_for('login'))

# Route to delete a question
@app.route('/delete_question/<int:question_id>', methods=['POST'])
def delete_question(question_id):
    user = getattr(User, 'current_user', None)
    if user and user.is_authenticated:
        cur = mysql.connection.cursor()
        cur.execute("SELECT test_id FROM questions WHERE id = %s", (question_id,))
        test_id = cur.fetchone()[0]
        cur.execute("DELETE FROM questions WHERE id = %s", (question_id,))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('questions', test_id=test_id))
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
