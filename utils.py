"""
This file will contain utility fucntions that are not
file specific

"""

import re
from faker import Faker
from datetime import timedelta
from database import initialize_database
import hashlib, random, sqlite3, os, datetime


fake = Faker()


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def is_valid_email(email: str) -> bool:
    """
    Validate an email using regex
    """
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.fullmatch(pattern, email) is not None


def is_valid_name(name: str) -> bool:
    """
    Returns True if the name contains only letters and spaces,
    and starts with a letter.
    """
    pattern = r"^[A-Za-z][A-Za-z\s'-]*$"
    return bool(re.fullmatch(pattern, name.strip()))


def is_valid_password(password: str) -> bool:
    """
    Returns True if the password is at least 8 characters long,
    contains at least one uppercase letter, one lowercase letter,
    one digit, and one special character.
    """
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
    return bool(re.fullmatch(pattern, password))



def generate_db_data(db_name='edutrakr.db', num_students=20, num_instructors=10, num_courses=15, min_sessions=30, max_sessions=40):
    fake.unique.clear()  # Clear unique data to avoid duplicates
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Create instructors
    instructor_ids = []
    for _ in range(num_instructors):
        name = fake.name()
        email = fake.unique.email()
        password = hash_password(fake.password())
        role = 'instructor'

        cursor.execute(
            "INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)",
            (name, email, password, role)
        )

        user_id = cursor.lastrowid
        cursor.execute(
            "INSERT INTO instructors (user_id) VALUES (?)",
            (user_id,)
        )
        instructor_ids.append(user_id)

    # create students
    student_ids = []
    for _ in range(num_students):
        name = fake.name()
        email = fake.unique.email()
        password = hash_password(fake.password())
        role = 'student'

        cursor.execute(
            "INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)",
            (name, email, password, role)
        )

        user_id = cursor.lastrowid
        private = random.choice([0, 0, 1, 0, 0, 0])
        cursor.execute(
            "INSERT INTO students (user_id, private) VALUES (?, ?)",
            (user_id, private)
        )
        student_ids.append(user_id)

    # Course names, 15 should be enough for generating data
    course_names = [
        "Introduction to Python",
        "Data Science Fundamentals",
        "Web Development Basics",
        "Machine Learning Essentials",
        "Database Management Systems",
        "Cloud Computing Concepts",
        "Cybersecurity Fundamentals",
        "Mobile App Development",
        "Software Engineering Principles",
        "Artificial Intelligence Overview", 
        "Game Development with Unity",
        "Digital Marketing Strategies",
        "Project Management Essentials",
        "UX Design",
        "Blockchain Technology Basics"  
    ]

    # Create courses
    course_ids = []
    for name in course_names[:num_courses]:
        instructor_id = random.choice(instructor_ids)
        cursor.execute(
            "INSERT INTO courses (name, instructor_id) VALUES (?, ?)",
            (name, instructor_id)
        )
        course_ids.append(cursor.lastrowid)

    # Generate study sessions for each student
    for student_id in student_ids:
        enrolled = random.sample(course_ids, random.randint(3, 5))
        for course_id in enrolled:
            for _ in range(random.randint(min_sessions, max_sessions)):
                start = fake.date_time_between(start_date='-356d', end_date='now')
                end = start + timedelta(minutes=random.randint(10, 90))
                cursor.execute(
                    "INSERT INTO study_sessions (user_id, course_id, start_time, end_time) VALUES (?, ?, ?, ?)",
                    (student_id, course_id, start.isoformat(), end.isoformat()))
                    
    
    conn.commit()

    # Everything below this line is for testing purposes
    cursor.execute("SELECT COUNT(*) FROM users")
    users = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM instructors")
    instructors = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM students")
    students = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM courses")
    courses = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM study_sessions")
    study_sessions = cursor.fetchone()[0]

    conn.close()

    return {
        "users": users,
        "instructors": instructors,
        "students": students,
        "courses": courses,
        "study_sessions": study_sessions
    }

def check_user_credentials(email: str, password: str, db_name='edutrakr.db'):
    """
    Verifies if a user exists with the given email and password.
    Returns user info if correct, else None.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    hashed_pw = hash_password(password)

    cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, hashed_pw))
    user = cursor.fetchone()

    conn.close()
    return user


def add_user(name: str, email: str, password: str, role: str, db_name='edutrakr.db') -> bool:
    """
    Adds a new user to the database and links them to the correct role table.
    Returns True if successful, False if the email already exists or error occurs.
    """
    
    hashed_pw = hash_password(password)

    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # Check for duplicate email
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        if cursor.fetchone():
            return False  # Email already exists

        # Insert into users table
        cursor.execute(
            "INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)",
            (name, email, hashed_pw, role)
        )
        user_id = cursor.lastrowid

        # Insert into role-specific table
        if role.lower() == 'student':
            cursor.execute("INSERT INTO students (user_id) VALUES (?, 0)", (user_id,))
        elif role.lower() == 'instructor':
            cursor.execute("INSERT INTO instructors (user_id) VALUES (?)", (user_id,))

        conn.commit()
        return True

    except Exception as e:
        print(f"Error adding user: {e}")
        return False

    finally:
        conn.close()


def get_study_sessions(user_id: int, db_name: str):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT study_sessions.id, study_sessions.user_id, courses.name, study_sessions.start_time, study_sessions.end_time
        FROM study_sessions
        JOIN courses ON study_sessions.course_id = courses.id
        WHERE study_sessions.user_id = ?
        ORDER BY study_sessions.id ASC               
    ''', (int(user_id),))

    sessions = cursor.fetchall()

    conn.close()

    return sessions


def get_random_student(db_name: str):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute('''
    SELECT id, name, role FROM users WHERE role = "student"
''')
    all_students = cursor.fetchall()
    
    conn.close()

    if not all_students:
        return None
    student = random.choice(all_students)
    
    return student

def get_random_instructor(db_name: str):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute('''
    SELECT id, name, role FROM users WHERE role = "instructor"
''')
    all_instructors = cursor.fetchall()
    
    conn.close()

    if not all_instructors:
        return None
    instructor = random.choice(all_instructors)
    
    return instructor

def get_courses(user_id, db_name: str):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM courses ORDER BY name ASC")
    courses = [row[0] for row in cursor.fetchall()]

    conn.close()
    return courses


# user insert new course
def insert_course(user_id, course_name, db_name: str):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # We'll attach a random instructor from the instructor table to this course
    cursor.execute("SELECT user_id FROM instructors")
    instructors = cursor.fetchall()

    if not instructors:
        conn.close()
        raise Exception("No instructors found in the database.")

    instructor_id = random.choice(instructors)[0]

    # Insert new course with random instructor
    cursor.execute(
        "INSERT INTO courses (name, instructor_id) VALUES (?, ?)",
        (course_name, instructor_id)
    )

    course_id = cursor.lastrowid
    now = datetime.datetime.now().isoformat()

    cursor.execute(
        "INSERT INTO study_sessions (user_id, course_id, start_time, end_time) VALUES (?, ?, ?, ?)",
        (user_id, course_id, now, now)
    )

    conn.commit()
    conn.close()


def insert_study_session(user_id, course_name, start_time, end_time, db_name: str):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # get the course ID from the course name
    cursor.execute("SELECT id FROM courses WHERE name = ?", (course_name,))
    result = cursor.fetchone()
    
    if result:
        course_id = result[0]

        # insert study session
        cursor.execute(
            "INSERT INTO study_sessions (user_id, course_id, start_time, end_time) VALUES (?, ?, ?, ?)",
            (user_id, course_id, start_time.isoformat(), end_time.isoformat())
        )

        conn.commit()
    else:
        print(f"[Error] Course '{course_name}' not found in the database.")

    conn.close()

def get_student_privacy(user_id: int, db_name='edutrakr.db') -> bool:
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT private FROM students WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result and result[0] == 1

def set_student_privacy(user_id: int, is_private: bool, db_name='edutrakr.db'):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("UPDATE students SET private = ? WHERE user_id = ?", (int(is_private), user_id))
    conn.commit()
    conn.close()
