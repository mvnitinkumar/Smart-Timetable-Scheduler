from flask import Flask, render_template, request, redirect
from scheduler import generate_timetable
import sqlite3
app = Flask(__name__)
DATABASE = "database/timetable.db"


# ---------------- DATABASE CONNECTION ----------------
def get_db():
    conn = sqlite3.connect(DATABASE)
    return conn


# ---------------- DATABASE INITIALIZATION ----------------
def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # FACULTY TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS faculty(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        department TEXT
    )
    """)

    # ROOMS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS rooms(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        room TEXT,
        capacity INTEGER
    )
    """)

    # SUBJECTS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS subjects(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject TEXT,
        faculty TEXT,
        hours INTEGER
    )
    """)

    # TIMETABLE TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS timetable(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        day TEXT,
        time TEXT,
        subject TEXT,
        faculty TEXT,
        room TEXT
    )
    """)

    conn.commit()
    conn.close()


init_db()


# ---------------- DASHBOARD ----------------
@app.route("/")
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


# ---------------- ADD FACULTY ----------------
@app.route("/add_faculty", methods=["GET", "POST"])
def add_faculty():
    conn = get_db()
    cursor = conn.cursor()

    if request.method == "POST":
        name = request.form.get("name")
        department = request.form.get("department")

        cursor.execute(
            "INSERT INTO faculty(name, department) VALUES (?, ?)",
            (name, department)
        )

        conn.commit()

    conn.close()
    return render_template("add_faculty.html")


# ---------------- ADD ROOM ----------------
@app.route("/add_room", methods=["GET", "POST"])
def add_room():
    conn = get_db()
    cursor = conn.cursor()

    if request.method == "POST":
        room = request.form.get("room")
        capacity = request.form.get("capacity")

        cursor.execute(
            "INSERT INTO rooms(room, capacity) VALUES (?, ?)",
            (room, capacity)
        )

        conn.commit()

    conn.close()
    return render_template("add_room.html")


# ---------------- ADD SUBJECT ----------------
@app.route("/add_subject", methods=["GET", "POST"])
def add_subject():
    conn = get_db()
    cursor = conn.cursor()

    # Fetch faculty list
    cursor.execute("SELECT name FROM faculty")
    faculty_list = cursor.fetchall()

    if request.method == "POST":
        subject = request.form.get("subject")
        faculty = request.form.get("faculty")
        hours = request.form.get("hours")

        cursor.execute(
            "INSERT INTO subjects(subject, faculty, hours) VALUES (?, ?, ?)",
            (subject, faculty, hours)
        )

        conn.commit()
        conn.close()

        return redirect("/add_subject")

    conn.close()
    return render_template("add_subject.html", faculty_list=faculty_list)


# ---------------- GENERATE TIMETABLE ----------------
@app.route("/generate")
def generate():
    generate_timetable()
    return redirect("/timetable")

# ---------------- VIEW TIMETABLE ----------------
@app.route("/timetable")
def timetable():

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT day,time,subject FROM timetable")
    rows = cursor.fetchall()

    conn.close()

    timetable = {}

    for day, time, subject in rows:
        if time not in timetable:
            timetable[time] = {}
        timetable[time][day] = subject

    days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]

    return render_template("timetable.html", timetable=timetable, days=days)
# ---------------- RUN SERVER ----------------
if __name__ == "__main__":
    app.run(debug=True)