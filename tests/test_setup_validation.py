"""
Validation tests to ensure the testing infrastructure is properly configured.
"""

import pytest
from pathlib import Path


class TestInfrastructureSetup:
    """Test class to validate the testing infrastructure setup."""
    
    def test_pytest_is_working(self):
        """Verify that pytest can run basic tests."""
        assert True
        assert 1 + 1 == 2
    
    def test_project_structure_exists(self):
        """Verify that the test directory structure is properly created."""
        test_root = Path(__file__).parent
        
        assert test_root.exists()
        assert test_root.is_dir()
        assert (test_root / "__init__.py").exists()
        assert (test_root / "conftest.py").exists()
        assert (test_root / "unit").exists()
        assert (test_root / "unit" / "__init__.py").exists()
        assert (test_root / "integration").exists()
        assert (test_root / "integration" / "__init__.py").exists()
    
    def test_pyproject_toml_exists(self):
        """Verify that pyproject.toml is properly configured."""
        project_root = Path(__file__).parent.parent
        pyproject_path = project_root / "pyproject.toml"
        
        assert pyproject_path.exists()
        
        # Check that it contains Poetry configuration
        content = pyproject_path.read_text()
        assert "[tool.poetry]" in content
        assert "[tool.pytest.ini_options]" in content
        assert "[tool.coverage.run]" in content
    
    @pytest.mark.unit
    def test_unit_marker_works(self):
        """Verify that the unit test marker is functional."""
        assert True
    
    @pytest.mark.integration
    def test_integration_marker_works(self):
        """Verify that the integration test marker is functional."""
        assert True
    
    @pytest.mark.slow
    def test_slow_marker_works(self):
        """Verify that the slow test marker is functional."""
        import time
        start = time.time()
        time.sleep(0.1)  # Simulate a slow test
        end = time.time()
        assert end - start >= 0.1
    
    def test_fixtures_are_available(self, temp_dir, mock_config):
        """Verify that conftest fixtures are accessible."""
        assert temp_dir.exists()
        assert temp_dir.is_dir()
        
        assert isinstance(mock_config, dict)
        assert 'debug' in mock_config
        assert mock_config['test_mode'] is True
    
    def test_django_is_configured(self):
        """Verify that Django is properly configured for testing."""
        from django.conf import settings
        assert settings.configured
    
    def test_database_fixture_works(self, db, test_user):
        """Verify that database fixtures are functional."""
        assert test_user is not None
        assert test_user.username == 'testuser'
        assert test_user.email == 'test@example.com'
    
    def test_client_fixture_works(self, client):
        """Verify that the Django test client is available."""
        response = client.get('/')
        assert response is not None
        # Status code might be 200, 302, 404 etc. depending on your URL configuration
        assert hasattr(response, 'status_code')
    
    def test_mock_fixture_works(self, mocker):
        """Verify that pytest-mock is properly installed and working."""
        mock_func = mocker.Mock(return_value=42)
        result = mock_func()
        assert result == 42
        mock_func.assert_called_once()
    
    def test_coverage_is_configured(self):
        """Verify that coverage is properly configured."""
        import coverage
        assert coverage.__version__  # Just check that coverage is importable


class TestSampleUnit:
    """Sample unit test class to demonstrate test organization."""
    
    @pytest.mark.unit
    def test_sample_unit_calculation(self):
        """Example unit test for a simple calculation."""
        def add(a, b):
            return a + b
        
        assert add(2, 3) == 5
        assert add(-1, 1) == 0
        assert add(0, 0) == 0


class TestSampleIntegration:
    """Sample integration test class to demonstrate test organization."""
    
    @pytest.mark.integration
    def test_sample_database_integration(self, db, test_user):
        """Example integration test with database."""
        from django.contrib.auth import get_user_model
        
        User = get_user_model()
        user_count = User.objects.count()
        assert user_count >= 1  # At least our test user exists
        
        found_user = User.objects.get(username='testuser')
        assert found_user.email == 'test@example.com'