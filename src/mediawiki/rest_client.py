"""REST API client for MediaWiki."""

import time
from typing import List, Dict, Any, Optional
from datetime import datetime
from urllib.parse import quote

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from src.core import get_logger, RateLimitError, APIError
from .models import SearchResult, PageMetadata


logger = get_logger(__name__)


class RESTClient:
    """Client for MediaWiki REST API v1."""

    def __init__(self, url: str, timeout: int = 30, verify_ssl: bool = True):
        """
        Initialize REST client.
        
        Args:
            url: MediaWiki base URL (e.g., https://en.wikipedia.org/wiki)
            timeout: Request timeout in seconds
            verify_ssl: Whether to verify SSL certificates
        """
        self.base_url = url.rstrip("/")
        self.api_url = self.base_url.replace("/wiki", "") + "/api/rest_v1"
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        self.session = self._create_session()
        
        # Rate limiting
        self.last_request_time = 0
        self.min_request_interval = 1.0  # seconds
        
        logger.info(f"Initialized REST client for {self.api_url}")

    def _create_session(self) -> requests.Session:
        """Create a requests session with retry strategy."""
        session = requests.Session()
        
        # Retry strategy
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS"]
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        # User agent
        session.headers.update({
            "User-Agent": "MediaWikiAgent/0.1.0"
        })
        
        return session

    def _rate_limit(self) -> None:
        """Apply rate limiting."""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.min_request_interval:
            time.sleep(self.min_request_interval - elapsed)
        self.last_request_time = time.time()

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """
        Make an API request.
        
        Args:
            method: HTTP method
            endpoint: API endpoint (relative to api_url)
            **kwargs: Additional request arguments
            
        Returns:
            Response JSON
            
        Raises:
            APIError: If request fails
            RateLimitError: If rate limited
        """
        self._rate_limit()
        
        url = f"{self.api_url}{endpoint}"
        kwargs.setdefault("timeout", self.timeout)
        kwargs.setdefault("verify", self.verify_ssl)
        
        try:
            response = self.session.request(method, url, **kwargs)
            
            if response.status_code == 429:
                raise RateLimitError("Rate limited by MediaWiki")
            
            response.raise_for_status()
            return response.json() if response.text else {}
            
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            raise APIError(f"Failed to fetch {endpoint}: {str(e)}")

    def get_page(self, title: str) -> Dict[str, Any]:
        """Get page content as HTML."""
        encoded_title = quote(title, safe="")
        return self._request("GET", f"/page/html/{encoded_title}")

    def get_page_history(self, title: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Get page revision history."""
        encoded_title = quote(title, safe="")
        return self._request(
            "GET", 
            f"/page/{encoded_title}/history",
            params={"limit": limit}
        ).get("revisions", [])

    def get_page_links(self, title: str) -> List[str]:
        """Get all links on a page."""
        encoded_title = quote(title, safe="")
        data = self._request("GET", f"/page/{encoded_title}/links/all")
        return [link.get("title") for link in data.get("links", []) if link.get("title")]

    def search(self, query: str, limit: int = 20) -> List[SearchResult]:
        """
        Search for pages.
        
        Args:
            query: Search query
            limit: Number of results
            
        Returns:
            List of search results
        """
        data = self._request(
            "GET",
            "/search/page",
            params={"q": query, "limit": limit}
        )
        
        results = []
        for hit in data.get("pages", []):
            results.append(SearchResult(
                pageid=hit.get("id", 0),
                title=hit.get("title", ""),
                namespace=0,
                relevance=0.8,  # REST API doesn't provide relevance scores
                snippet=hit.get("excerpt", ""),
                categories=[]
            ))
        
        return results

    def get_page_metadata(self, title: str) -> PageMetadata:
        """Get basic page metadata."""
        # This is a basic implementation
        # In practice, you'd use the Action API for more complete metadata
        encoded_title = quote(title, safe="")
        
        try:
            data = self._request("GET", f"/page/summary/{encoded_title}")
            return PageMetadata(
                title=data.get("title", title),
                pageid=data.get("pageid", 0),
                namespace=0,
                revision_id=data.get("last_edits", [{}])[0].get("id", 0),
                timestamp=datetime.now(),
                length_bytes=data.get("content_urls", {}).get("mobile", {}).get("page", "").count(""),
            )
        except Exception as e:
            logger.error(f"Failed to get metadata for {title}: {e}")
            raise APIError(f"Failed to get metadata for {title}")
