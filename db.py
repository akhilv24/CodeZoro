import sqlite3

DB_PATH = 'data/lab_programs.db'

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Access columns by name
    return conn

def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS programs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    subject TEXT,
                    lab_number INTEGER NOT NULL,
                    description TEXT,
                    code TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )''')
    conn.commit()
    conn.close()

def add_program(title, subject, lab_number, description, code):
    """Insert a new lab program into the database."""
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        "INSERT INTO programs (title, subject, lab_number, description, code) VALUES (?, ?, ?, ?, ?)",
        (title, subject, lab_number, description, code)
    )
    conn.commit()
    conn.close()

def get_programs_by_subject(subject):
    """Fetch all programs for a specific subject."""
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM programs WHERE subject = ? ORDER BY lab_number ASC", (subject,))
    data = c.fetchall()
    conn.close()
    return data

def get_all_programs():
    """Fetch all programs, sorted by most recent."""
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM programs ORDER BY created_at DESC")
    rows = c.fetchall()
    conn.close()
    return rows

def get_program_by_id(pid):
    """Fetch a single program by ID."""
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM programs WHERE id=?", (pid,))
    row = c.fetchone()
    conn.close()
    return row

def update_program(pid, title, subject, lab_number, description, code):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        UPDATE programs 
        SET title=?, subject=?, lab_number=?, description=?, code=?
        WHERE id=?
    """, (title, subject, lab_number, description, code, pid))
    conn.commit()
    conn.close()


def delete_program(pid):
    """Delete a program by ID."""
    conn = get_connection()
    c = conn.cursor()g
    c.execute("DELETE FROM programs WHERE id=?", (pid,))
    conn.commit()
    conn.close()
