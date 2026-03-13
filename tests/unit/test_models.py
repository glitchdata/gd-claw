"""Tests for core configuration and models."""

import pytest
from datetime import datetime

from src.core import Settings, get_settings
from src.mediawiki import PageMetadata, PageContent, SearchResult, EditResult


class TestConfiguration:
    """Tests for configuration management."""

    def test_default_settings(self):
        """Test default settings."""
        settings = Settings()
        assert settings.mediawiki.timeout == 30
        assert settings.llm.provider == "openai"
        assert settings.vector_store.type == "faiss"
        assert settings.cache.backend == "memory"

    def test_log_level_validation(self):
        """Test log level validation."""
        # Valid levels
        for level in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            settings = Settings(log_level=level)
            assert settings.log_level == level

        # Invalid level
        with pytest.raises(ValueError):
            Settings(log_level="INVALID")

    def test_get_settings(self):
        """Test getting settings singleton."""
        settings1 = get_settings()
        settings2 = get_settings()
        assert settings1 is settings2


class TestPageMetadata:
    """Tests for PageMetadata model."""

    def test_page_metadata_creation(self):
        """Test creating page metadata."""
        metadata = PageMetadata(
            title="Test Page",
            pageid=123,
            namespace=0,
            revision_id=456,
            timestamp=datetime.now(),
        )
        assert metadata.title == "Test Page"
        assert metadata.pageid == 123
        assert metadata.is_redirect is False

    def test_page_metadata_with_categories(self):
        """Test page metadata with categories."""
        metadata = PageMetadata(
            title="Test",
            pageid=1,
            namespace=0,
            revision_id=2,
            timestamp=datetime.now(),
            categories=["Category1", "Category2"],
        )
        assert len(metadata.categories) == 2
        assert "Category1" in metadata.categories

    def test_page_metadata_json_serialization(self):
        """Test page metadata JSON serialization."""
        metadata = PageMetadata(
            title="Test",
            pageid=1,
            namespace=0,
            revision_id=2,
            timestamp=datetime.now(),
        )
        # Should serialize without errors
        json_str = metadata.json()
        assert "Test" in json_str


class TestPageContent:
    """Tests for PageContent model."""

    def test_page_content_creation(self):
        """Test creating page content."""
        content = PageContent(
            pageid=123,
            title="Test",
            wiki_text="== Section ==\nContent here",
        )
        assert content.pageid == 123
        assert content.title == "Test"
        assert "Section" in content.wiki_text

    def test_page_content_with_sections(self):
        """Test page content with sections."""
        from src.mediawiki.models import Section
        
        content = PageContent(
            pageid=1,
            title="Test",
            wiki_text="",
            sections=[
                Section(level=2, title="Section 1", content="Content 1")
            ],
        )
        assert len(content.sections) == 1
        assert content.sections[0].title == "Section 1"


class TestSearchResult:
    """Tests for SearchResult model."""

    def test_search_result_creation(self):
        """Test creating search result."""
        result = SearchResult(
            pageid=123,
            title="Test Page",
            namespace=0,
            relevance=0.95,
            snippet="Test snippet...",
        )
        assert result.title == "Test Page"
        assert result.relevance == 0.95

    def test_search_result_with_categories(self):
        """Test search result with categories."""
        result = SearchResult(
            pageid=1,
            title="Test",
            namespace=0,
            relevance=0.8,
            snippet="Snippet",
            categories=["Cat1", "Cat2"],
        )
        assert len(result.categories) == 2


class TestEditResult:
    """Tests for EditResult model."""

    def test_edit_result_success(self):
        """Test successful edit result."""
        result = EditResult(
            success=True,
            pageid=123,
            title="Test",
            revision_id=456,
            timestamp=datetime.now(),
            summary="Updated",
        )
        assert result.success is True
        assert result.error is None

    def test_edit_result_failure(self):
        """Test failed edit result."""
        result = EditResult(
            success=False,
            pageid=123,
            title="Test",
            revision_id=0,
            timestamp=datetime.now(),
            summary="Attempted",
            error="Conflict detected",
        )
        assert result.success is False
        assert result.error == "Conflict detected"
