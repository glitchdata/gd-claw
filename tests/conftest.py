"""Pytest configuration and fixtures."""

import pytest
from unittest.mock import Mock, MagicMock
from src.core import settings


@pytest.fixture
def mock_mediawiki_client():
    """Mock MediaWiki client for testing."""
    client = Mock()
    client.search = MagicMock(return_value=[])
    client.get_page_metadata = MagicMock()
    client.get_page_text = MagicMock(return_value="Test content")
    client.edit_page = MagicMock()
    return client


@pytest.fixture
def mock_settings():
    """Mock settings."""
    return settings


@pytest.fixture
def sample_page_metadata():
    """Sample page metadata."""
    from src.mediawiki import PageMetadata
    from datetime import datetime
    
    return PageMetadata(
        title="Test Page",
        pageid=123,
        namespace=0,
        revision_id=456,
        timestamp=datetime.now(),
        categories=["Test"],
        length_bytes=5000,
    )


@pytest.fixture
def sample_page_content():
    """Sample page content."""
    from src.mediawiki import PageContent
    from datetime import datetime
    
    return PageContent(
        pageid=123,
        title="Test Page",
        wiki_text="This is test content",
        sections=[],
        references=[],
    )
