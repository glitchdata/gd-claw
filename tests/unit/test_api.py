"""Tests for FastAPI application."""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch

from src.api.app import app


@pytest.fixture
def client():
    """Test client for FastAPI app."""
    return TestClient(app)


class TestHealthEndpoints:
    """Tests for health check endpoints."""

    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "timestamp" in data
        assert data["version"] == "0.1.0"

    def test_status_endpoint(self, client):
        """Test status endpoint."""
        response = client.get("/status")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "running"
        assert "indexed_pages" in data
        assert "queue_size" in data


class TestSearchEndpoints:
    """Tests for search endpoints."""

    @patch('src.api.app.get_client')
    def test_search_success(self, mock_get_client, client):
        """Test successful search."""
        mock_client = Mock()
        mock_client.search.return_value = [
            Mock(
                pageid=123,
                title="Test Page",
                namespace=0,
                relevance=0.9,
                snippet="Test snippet",
                categories=[]
            )
        ]
        mock_get_client.return_value = mock_client

        response = client.get("/api/search?q=test&limit=10")
        assert response.status_code == 200
        data = response.json()
        assert data["query"] == "test"
        assert len(data["results"]) == 1
        assert data["results"][0]["title"] == "Test Page"

    @patch('src.api.app.get_client')
    def test_search_without_query(self, mock_get_client, client):
        """Test search without query parameter."""
        response = client.get("/api/search")
        assert response.status_code == 422  # Validation error

    @patch('src.api.app.get_client')
    def test_search_limit_validation(self, mock_get_client, client):
        """Test search limit validation."""
        response = client.get("/api/search?q=test&limit=1000")
        assert response.status_code == 422  # Limit too high


class TestPageEndpoints:
    """Tests for page endpoints."""

    @patch('src.api.app.get_client')
    def test_get_page(self, mock_get_client, client):
        """Test get page endpoint."""
        mock_client = Mock()
        
        from src.mediawiki import PageMetadata
        from datetime import datetime
        
        mock_client.get_page_metadata.return_value = PageMetadata(
            title="Test Page",
            pageid=123,
            namespace=0,
            revision_id=456,
            timestamp=datetime.now(),
        )
        mock_client.get_page_text.return_value = "Test content"
        mock_get_client.return_value = mock_client

        response = client.get("/api/page/Test%20Page")
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Test Page"
        assert data["pageid"] == 123
        assert data["content"] == "Test content"

    @patch('src.api.app.get_client')
    def test_get_page_summary(self, mock_get_client, client):
        """Test get page summary endpoint."""
        mock_client = Mock()
        
        from src.mediawiki import PageMetadata
        from datetime import datetime
        
        mock_client.get_page_metadata.return_value = PageMetadata(
            title="Test Page",
            pageid=123,
            namespace=0,
            revision_id=456,
            timestamp=datetime.now(),
            categories=["Test"],
            length_bytes=5000,
        )
        mock_get_client.return_value = mock_client

        response = client.get("/api/page/Test%20Page/summary")
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Test Page"
        assert data["length_bytes"] == 5000
        assert "Test" in data["categories"]


class TestSyncEndpoints:
    """Tests for sync endpoints."""

    def test_full_sync(self, client):
        """Test full sync endpoint."""
        response = client.post("/api/sync/full")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "pending"

    def test_incremental_sync(self, client):
        """Test incremental sync endpoint."""
        response = client.post("/api/sync/incremental")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "pending"
