import sqlite3
import random

DAYS = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
SLOTS = ["9-10","10-11","11-12","12-1","2-3","3-4"]

def generate_timetable():

    conn = sqlite3.connect("database/timetable.db")
    cursor = conn.cursor()

    # Clear old timetable
    cursor.execute("DELETE FROM timetable")

    # Get subjects
    cursor.execute("SELECT subject, faculty FROM subjects")
    subjects = cursor.fetchall()

    # Get rooms
    cursor.execute("SELECT room FROM rooms")
    rooms = cursor.fetchall()

    if not subjects or not rooms:
        return

    for day in DAYS:
        for slot in SLOTS:

            subject = random.choice(subjects)
            room = random.choice(rooms)

            cursor.execute("""
                INSERT INTO timetable(day,time,subject,faculty,room)
                VALUES (?,?,?,?,?)
            """,(day,slot,subject[0],subject[1],room[0]))

    conn.commit()
    conn.close()