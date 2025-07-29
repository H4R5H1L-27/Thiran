# Step-by-step Setup to Build Web Version of "Thiran" (Flask + MySQL)

from flask import Flask, render_template, request, redirect, session
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)
app.secret_key = 'supersecretkey'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'  # Your MySQL password
app.config['MYSQL_DB'] = 'thiran_db'

mysql = MySQL(app)

# ---------- CREATE DATABASE AND TABLES IF NOT EXISTS ----------
def init_db():
    import mysql.connector as mysql_connector
    con = mysql_connector.connect(host='localhost', user='root', password='1234')
    cursor = con.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS thiran_db")
    con.close()

    from flask import current_app
    with app.app_context():
        cur = mysql.connection.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS skills (
                skill_id INT AUTO_INCREMENT PRIMARY KEY,
                skill_name VARCHAR(50)
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS workers (
                worker_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100),
                password VARCHAR(100)
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS worker_skills (
                worker_id INT,
                skill_id INT
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(100),
                password VARCHAR(100),
                phone VARCHAR(20)
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                job_id INT AUTO_INCREMENT PRIMARY KEY,
                employer_id INT,
                title VARCHAR(100),
                skill_required INT,
                description TEXT,
                address TEXT,
                status VARCHAR(20) DEFAULT 'Open',
                assigned_worker_id INT DEFAULT NULL
            )
        """)
        cur.execute("SELECT COUNT(*) FROM skills")
        if cur.fetchone()[0] == 0:
            cur.executemany("INSERT INTO skills (skill_name) VALUES (%s)",
                [('Electrician',), ('Plumber',), ('Tailor',), ('Data Entry',)])
        mysql.connection.commit()
        cur.close()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/register_worker', methods=['GET', 'POST'])
def register_worker():
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        name = request.form['name']
        pwd = request.form['password']
        skills = request.form.getlist('skills')
        cur.execute("INSERT INTO workers (name, password) VALUES (%s, %s)", (name, pwd))
        mysql.connection.commit()
        wid = cur.lastrowid
        for sid in skills:
            cur.execute("INSERT INTO worker_skills (worker_id, skill_id) VALUES (%s, %s)", (wid, sid))
        mysql.connection.commit()
        cur.close()
        return redirect('/')
    else:
        cur.execute("SELECT skill_id, skill_name FROM skills")
        skills = cur.fetchall()
        return render_template("register_worker.html", skills=skills)

@app.route('/login_worker', methods=['POST'])
def login_worker():
    name = request.form['name']
    pwd = request.form['password']
    cur = mysql.connection.cursor()
    cur.execute("SELECT worker_id FROM workers WHERE name=%s AND password=%s", (name, pwd))
    user = cur.fetchone()
    cur.close()
    if user:
        session['worker_id'] = user[0]
        return redirect('/dashboard_worker')
    else:
        return "Login Failed"

@app.route('/dashboard_worker', methods=['GET', 'POST'])
def dashboard_worker():
    wid = session.get('worker_id')
    if not wid:
        return redirect('/')
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        job_id = request.form['job_id']
        cur.execute("UPDATE jobs SET status='Assigned', assigned_worker_id=%s WHERE job_id=%s", (wid, job_id))
        mysql.connection.commit()

    cur.execute("""
        SELECT j.job_id, j.title, s.skill_name, j.description, j.address, j.status
        FROM jobs j
        JOIN skills s ON j.skill_required = s.skill_id
        WHERE j.skill_required IN (
            SELECT skill_id FROM worker_skills WHERE worker_id = %s
        ) AND j.status = 'Open'
    """, (wid,))
    jobs = cur.fetchall()
    cur.close()
    return render_template("dashboard_worker.html", jobs=jobs)

@app.route('/register_user', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        phone = request.form['phone']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (username, password, phone) VALUES (%s, %s, %s)", (username, password, phone))
        mysql.connection.commit()
        return redirect('/')
    return render_template("register_user.html")

@app.route('/login_user', methods=['POST'])
def login_user():
    username = request.form['username']
    password = request.form['password']
    cur = mysql.connection.cursor()
    cur.execute("SELECT user_id FROM users WHERE username=%s AND password=%s", (username, password))
    user = cur.fetchone()
    cur.close()
    if user:
        session['user_id'] = user[0]
        return redirect('/dashboard_user')
    else:
        return "Login Failed"

@app.route('/dashboard_user', methods=['GET', 'POST'])
def dashboard_user():
    uid = session.get('user_id')
    if not uid:
        return redirect('/')
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        title = request.form['title']
        skill = request.form['skill']
        desc = request.form['description']
        addr = request.form['address']
        cur.execute("INSERT INTO jobs (employer_id, title, skill_required, description, address) VALUES (%s, %s, %s, %s, %s)",
                    (uid, title, skill, desc, addr))
        mysql.connection.commit()

    cur.execute("SELECT skill_id, skill_name FROM skills")
    skills = cur.fetchall()
    cur.execute("""
        SELECT j.title, s.skill_name, j.description, j.status
        FROM jobs j
        JOIN skills s ON j.skill_required = s.skill_id
        WHERE j.employer_id = %s
    """, (uid,))
    jobs = cur.fetchall()
    cur.close()
    return render_template("dashboard_user.html", jobs=jobs, skills=skills)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)