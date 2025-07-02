import sys, os, sqlite3
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils import hash_password, is_valid_email, is_valid_name, is_valid_password, generate_db_data, check_user_credentials
from database import initialize_database


def test_valid_emails():
    assert is_valid_email("user@example.com")
    assert is_valid_email("john.doe123@sub.domain.org")
    assert is_valid_email("user.name+tag@company.co.uk")


def test_invalid_emails():
    assert not is_valid_email("invalid-email")
    assert not is_valid_email("user@com")
    assert not is_valid_email("user@.com")
    assert not is_valid_email("@missingusername.com")
    assert not is_valid_email("user@domain.c")


def test_valid_names():
    assert is_valid_name("John") == True
    assert is_valid_name("Mary Jane") == True
    assert is_valid_name("Anne-Marie") == True
    assert is_valid_name("O'Connor") == True


def test_invalid_names():
    assert is_valid_name("John123") == False
    assert is_valid_name("Mary@") == False
    assert is_valid_name("123Anne") == False
    assert is_valid_name("") == False
    assert is_valid_name(" ") == False


def test_valid_passwords():
    assert is_valid_password("Password1!") == True
    assert is_valid_password("StrongPass@2023") == True
    assert is_valid_password("Valid123$") == True
    assert is_valid_password("AnotherValid1!") == True


def test_invalid_passwords():
    assert is_valid_password("short") == False
    assert is_valid_password("NoSpecialChar1") == False
    assert is_valid_password("nouppercase1!") == False
    assert is_valid_password("NOLOWERCASE1!") == False
    assert is_valid_password("NoDigit!") == False
    assert is_valid_password("12345678") == False
    assert is_valid_password("") == False


def test_generate_db_data():
    test_db = 'test_edutrakr.db'

    if os.path.exists(test_db):
        os.remove(test_db)

    initialize_database(test_db)

    counts = generate_db_data(db_name='test_edutrakr.db', num_students=5, num_instructors=3, num_courses=15, min_sessions=1, max_sessions=2)

    assert counts['students'] == 5
    assert counts['instructors'] == 3
    assert counts['courses'] == 15
    assert counts["users"] == 8
    assert counts['study_sessions'] > 0


def test_user_authentication():
    test_db = 'test_edutrakr.db'

    if os.path.exists(test_db):
        os.remove(test_db)

    initialize_database(test_db)

    conn = sqlite3.connect(test_db)
    cursor = conn.cursor()
    name = 'Test User'
    password = 'testpass'
    hashed = hash_password(password)
    email = 'test@test.com'
    role = 'student'

    cursor.execute('INSERT INTO users (name, email, password, role) VALUES (?,?,?,?)', (name, email, hashed, role))

    conn.commit()
    conn.close()

    user = check_user_credentials(email, password, db_name=test_db)

    assert user is not None
    assert user[1] == name
    assert user[2] == email
    assert user[3] == hashed
    assert user[4] == role

