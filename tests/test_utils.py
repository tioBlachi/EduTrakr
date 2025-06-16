from utils import is_valid_email

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