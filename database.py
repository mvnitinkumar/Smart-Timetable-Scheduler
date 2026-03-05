import sqlite3
import os


def connect_db():

    # ensure database folder exists
    if not os.path.exists("database"):
        os.makedirs("database")

    conn = sqlite3.connect("database/timetable.db")

    return conn


def create_tables():

    conn = connect_db()
    cursor = conn.cursor()

    # ---------- FACULTY ----------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS faculty(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        department TEXT,
        max_hours INTEGER
    )
    """)

    # ---------- SUBJECTS ----------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS subjects(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject_name TEXT NOT NULL,
        hours_per_week INTEGER
    )
    """)

    # ---------- ROOMS ----------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS rooms(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        room_number TEXT NOT NULL,
        capacity INTEGER
    )
    """)

    conn.commit()
    conn.close()
    