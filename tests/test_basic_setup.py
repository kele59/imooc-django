"""
Basic validation tests that don't require Django.
"""

import pytest
from pathlib import Path


def test_pytest_works():
    """Basic test to verify pytest is installed."""
    assert True
    assert 1 + 1 == 2


def test_directory_structure():
    """Verify test directory structure."""
    test_root = Path(__file__).parent
    assert (test_root / "__init__.py").exists()
    assert (test_root / "conftest.py").exists()
    assert (test_root / "unit").is_dir()
    assert (test_root / "integration").is_dir()


def test_pyproject_toml():
    """Verify pyproject.toml configuration."""
    pyproject = Path(__file__).parent.parent / "pyproject.toml"
    assert pyproject.exists()
    
    content = pyproject.read_text()
    assert "[tool.poetry]" in content
    assert "pytest" in content
    assert "[tool.coverage.run]" in content


@pytest.mark.unit
def test_unit_marker():
    """Test unit marker."""
    assert True


@pytest.mark.integration  
def test_integration_marker():
    """Test integration marker."""
    assert True


def test_mock_works(mocker):
    """Test pytest-mock functionality."""
    mock = mocker.Mock(return_value=42)
    assert mock() == 42