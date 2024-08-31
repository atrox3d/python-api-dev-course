import pytest
import logging

logger = logging.getLogger(__name__)

@pytest.fixture
def fake_emails_dict() -> list[dict[str, str]]:
    logger.debug('returning emails')
    return [ 
                {'email': 'testuser@gmail.com',},
                {'email': 'cat@gmail.com',},
                {'email': 'dog@gmail.com',},
    ]

@pytest.fixture
def fake_usernames_dict() -> list[dict[str, str]]:
    logger.debug('returning usernames')
    return [ 
                {'username': 'testuser@gmail.com',},
                {'username': 'cat@gmail.com',},
                {'username': 'dog@gmail.com',},
    ]

@pytest.fixture
def fake_passwords_dict() -> list[dict[str, str]]:
    logger.debug('returning passwords')
    return [ 
                {'password': 'password',},
                {'password': 'meow',},
                {'password': 'wof',},
    ]

@pytest.fixture
def fake_users_creation_dict(
            fake_emails_dict:list[dict[str, str]],
            fake_passwords_dict:list[dict[str, str]],
) -> list[dict[str, str]]:
    logger.debug('merging email and passwords')
    return [email | password for email, password in zip(fake_emails_dict, fake_passwords_dict)]

@pytest.fixture
def fake_users_login_dict(
            fake_usernames_dict:list[dict[str, str]],
            fake_passwords_dict:list[dict[str, str]]
) -> list[dict[str, str]]:
    logger.debug('merging usernames and passwords')
    return [email | password for email, password in zip(fake_usernames_dict, fake_passwords_dict)]
