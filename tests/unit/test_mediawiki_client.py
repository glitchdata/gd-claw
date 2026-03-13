"""Tests for MediaWiki API clients."""

import pytest
from unittest.mock import Mock, patch, MagicMock

from src.mediawiki.rest_client import RESTClient
from src.mediawiki.action_client import ActionClient
from src.core import APIError, RateLimitError


class TestRESTClient:
    """Tests for REST API client."""

    def test_client_initialization(self):
        """Test REST client initialization."""
        client = RESTClient("https://en.wikipedia.org/wiki")
        assert client.api_url == "https://en.wikipedia.org/api/rest_v1"
        assert client.timeout == 30

    def test_client_with_custom_timeout(self):
        """Test REST client with custom timeout."""
        client = RESTClient("https://en.wikipedia.org/wiki", timeout=60)
        assert client.timeout == 60

    @patch('requests.Session.request')
    def test_search_success(self, mock_request):
        """Test successful search."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "pages": [
                {
                    "id": 123,
                    "title": "Test Article",
                    "excerpt": "Test excerpt"
                }
            ]
        }
        mock_request.return_value = mock_response

        client = RESTClient("https://en.wikipedia.org/wiki")
        results = client.search("test", limit=10)

        assert len(results) == 1
        assert results[0].title == "Test Article"
        assert results[0].pageid == 123

    @patch('requests.Session.request')
    def test_rate_limit_error(self, mock_request):
        """Test rate limit handling."""
        mock_response = Mock()
        mock_response.status_code = 429
        mock_request.return_value = mock_response

        client = RESTClient("https://en.wikipedia.org/wiki")

        with pytest.raises(RateLimitError):
            client._request("GET", "/test")

    @patch('requests.Session.request')
    def test_request_error_handling(self, mock_request):
        """Test error handling."""
        mock_request.side_effect = Exception("Network error")

        client = RESTClient("https://en.wikipedia.org/wiki")

        with pytest.raises(APIError):
            client._request("GET", "/test")


class TestActionClient:
    """Tests for Action API client."""

    def test_client_initialization(self):
        """Test Action client initialization."""
        client = ActionClient(
            "https://en.wikipedia.org/wiki",
            "TestBot",
            "password123"
        )
        assert client.api_url == "https://en.wikipedia.org/w/api.php"
        assert client.bot_user == "TestBot"

    @patch('requests.Session.post')
    def test_get_page_info(self, mock_post):
        """Test getting page info."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "query": {
                "pages": {
                    "123": {
                        "pageid": 123,
                        "title": "Test Page",
                        "ns": 0,
                        "length": 5000,
                        "revisions": [
                            {
                                "revid": 456,
                                "timestamp": "2026-03-13T10:00:00Z",
                                "user": "TestUser"
                            }
                        ],
                        "categories": [
                            {"*": "Category:Test"}
                        ]
                    }
                }
            }
        }
        mock_post.return_value = mock_response

        client = ActionClient(
            "https://en.wikipedia.org/wiki",
            "TestBot",
            "password"
        )
        metadata = client.get_page_info("Test Page")

        assert metadata.title == "Test Page"
        assert metadata.pageid == 123
        assert metadata.length_bytes == 5000

    @patch('requests.Session.post')
    def test_recent_changes(self, mock_post):
        """Test get recent changes."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "query": {
                "recentchanges": [
                    {
                        "pageid": 123,
                        "title": "Test Page",
                        "type": "edit",
                        "timestamp": "2026-03-13T10:00:00Z",
                        "user": "TestUser",
                        "comment": "Test edit"
                    }
                ]
            }
        }
        mock_post.return_value = mock_response

        client = ActionClient(
            "https://en.wikipedia.org/wiki",
            "TestBot",
            "password"
        )
        changes = client.get_recent_changes(limit=10)

        assert len(changes) == 1
        assert changes[0].title == "Test Page"
        assert changes[0].type == "edit"
