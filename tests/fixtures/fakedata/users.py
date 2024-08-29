import pytest

from schemas import post
from schemas import user
from schemas import vote
from db.orm import models

@pytest.fixture
def fake_emails_dict() -> list[dict[str, str]]:
    return [ 
                {'email': 'testuser@gmail.com',},
                {'email': 'cat@gmail.com',},
                {'email': 'dog@gmail.com',},
    ]

@pytest.fixture
def fake_usernames_dict() -> list[dict[str, str]]:
    return [ 
                {'username': 'testuser@gmail.com',},
                {'username': 'cat@gmail.com',},
                {'username': 'dog@gmail.com',},
    ]

@pytest.fixture
def fake_passwords_dict() -> list[dict[str, str]]:
    return [ 
                {'password': 'password',},
                {'password': 'meow',},
                {'password': 'wof',},
    ]

@pytest.fixture
def fake_users_creation_dict(
            fake_emails_dict,
            fake_passwords_dict
) -> list[dict[str, str]]:
    return [email | password for email, password in zip(fake_emails_dict, fake_passwords_dict)]

@pytest.fixture
def fake_users_login_dict(
            fake_usernames_dict,
            fake_passwords_dict
) -> list[dict[str, str]]:
    return [email | password for email, password in zip(fake_usernames_dict, fake_passwords_dict)]
