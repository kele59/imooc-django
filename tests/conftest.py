"""
Shared pytest fixtures and configuration for the test suite.
"""

import os
import sys
import tempfile
from pathlib import Path

import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import Client


# Add project root to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Configure Django settings for tests
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'imooc.settings')

import django
django.setup()

User = get_user_model()


@pytest.fixture
def temp_dir():
    """
    Provides a temporary directory that's automatically cleaned up after tests.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def mock_config():
    """
    Provides a mock configuration dictionary for testing.
    """
    return {
        'debug': True,
        'test_mode': True,
        'database': {
            'engine': 'django.db.backends.sqlite3',
            'name': ':memory:',
        },
        'cache': {
            'backend': 'django.core.cache.backends.dummy.DummyCache',
        },
        'email': {
            'backend': 'django.core.mail.backends.locmem.EmailBackend',
        },
    }


@pytest.fixture
def client():
    """
    Provides a Django test client for making HTTP requests.
    """
    return Client()


@pytest.fixture
def authenticated_client(client, test_user):
    """
    Provides a Django test client with an authenticated user.
    """
    client.force_login(test_user)
    return client


@pytest.fixture
def test_user(db):
    """
    Creates a test user for authentication tests.
    """
    user = User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )
    return user


@pytest.fixture
def test_superuser(db):
    """
    Creates a test superuser for admin tests.
    """
    user = User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='adminpass123'
    )
    return user


@pytest.fixture
def mock_request(client):
    """
    Provides a mock request object for view testing.
    """
    from django.http import HttpRequest
    from django.contrib.sessions.middleware import SessionMiddleware
    from django.contrib.messages.middleware import MessageMiddleware
    
    request = HttpRequest()
    request.META = {
        'HTTP_HOST': 'testserver',
        'HTTP_USER_AGENT': 'Mozilla/5.0',
    }
    
    # Add session support
    middleware = SessionMiddleware()
    middleware.process_request(request)
    request.session.save()
    
    # Add message support
    messages = MessageMiddleware()
    messages.process_request(request)
    
    return request


@pytest.fixture
def sample_file():
    """
    Creates a temporary file for testing file uploads.
    """
    import io
    from django.core.files.uploadedfile import SimpleUploadedFile
    
    content = b"This is a test file content"
    file = SimpleUploadedFile(
        name="test_file.txt",
        content=content,
        content_type="text/plain"
    )
    return file


@pytest.fixture
def sample_image():
    """
    Creates a temporary image file for testing image uploads.
    """
    import io
    from PIL import Image
    from django.core.files.uploadedfile import SimpleUploadedFile
    
    # Create a simple 100x100 red image
    image = Image.new('RGB', (100, 100), color='red')
    file_io = io.BytesIO()
    image.save(file_io, 'PNG')
    file_io.seek(0)
    
    file = SimpleUploadedFile(
        name="test_image.png",
        content=file_io.getvalue(),
        content_type="image/png"
    )
    return file


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    """
    Automatically enables database access for all tests.
    This avoids having to mark every test with @pytest.mark.django_db
    """
    pass


@pytest.fixture
def mock_cache():
    """
    Provides a mock cache backend for testing cache operations.
    """
    from django.core.cache import cache
    cache.clear()
    return cache


@pytest.fixture
def captured_emails():
    """
    Captures emails sent during tests.
    """
    from django.core import mail
    mail.outbox = []
    return mail.outbox


@pytest.fixture
def mock_datetime(monkeypatch):
    """
    Allows mocking of datetime.now() for time-sensitive tests.
    """
    import datetime
    
    class MockDatetime:
        def __init__(self, target_datetime):
            self.target = target_datetime
        
        def now(self, tz=None):
            return self.target
        
        def utcnow(self):
            return self.target
    
    def _mock_datetime(target_datetime):
        mock = MockDatetime(target_datetime)
        monkeypatch.setattr(datetime, 'datetime', mock)
        return mock
    
    return _mock_datetime


# Pytest hooks and configuration

def pytest_configure(config):
    """
    Configure pytest with custom markers.
    """
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )


def pytest_collection_modifyitems(config, items):
    """
    Automatically add markers based on test location.
    """
    for item in items:
        # Add unit marker for tests in tests/unit/
        if "unit" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        
        # Add integration marker for tests in tests/integration/
        elif "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)