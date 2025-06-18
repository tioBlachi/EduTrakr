from EduTrakr.utils import is_valid_email, is_valid_name, is_valid_password

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
