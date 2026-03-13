"""Action API client for MediaWiki."""

import time
from typing import List, Dict, Any, Optional
from datetime import datetime

import requests

from src.core import get_logger, AuthenticationError, APIError, RateLimitError
from .models import PageMetadata, RecentChange, EditResult


logger = get_logger(__name__)


class ActionClient:
    """Client for MediaWiki Action API."""

    def __init__(
        self,
        url: str,
        bot_user: str,
        bot_password: str,
        timeout: int = 30,
    ):
        """
        Initialize Action API client.
        
        Args:
            url: MediaWiki base URL
            bot_user: Bot username
            bot_password: Bot password or OAuth2 token
            timeout: Request timeout in seconds
        """
        self.base_url = url.rstrip("/")
        self.api_url = self.base_url.replace("/wiki", "") + "/w/api.php"
        self.bot_user = bot_user
        self.bot_password = bot_password
        self.timeout = timeout
        self.session = requests.Session()
        
        # Rate limiting
        self.last_request_time = 0
        self.min_request_interval = 1.0
        
        # Auth token
        self.token = None
        
        logger.info(f"Initialized Action client for {self.api_url}")

    def _rate_limit(self) -> None:
        """Apply rate limiting."""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.min_request_interval:
            time.sleep(self.min_request_interval - elapsed)
        self.last_request_time = time.time()

    def _request(self, method: str = "POST", **params) -> Dict[str, Any]:
        """
        Make an Action API request.
        
        Args:
            method: HTTP method
            **params: API parameters
            
        Returns:
            Response data
            
        Raises:
            APIError: If request fails
        """
        self._rate_limit()
        
        params.setdefault("format", "json")
        
        try:
            if method == "GET":
                response = self.session.get(
                    self.api_url,
                    params=params,
                    timeout=self.timeout,
                    headers={"User-Agent": "MediaWikiAgent/0.1.0"}
                )
            else:
                response = self.session.post(
                    self.api_url,
                    data=params,
                    timeout=self.timeout,
                    headers={"User-Agent": "MediaWikiAgent/0.1.0"}
                )
            
            if response.status_code == 429:
                raise RateLimitError("Rate limited by MediaWiki")
            
            response.raise_for_status()
            data = response.json()
            
            # Check for API errors
            if "error" in data:
                raise APIError(f"API error: {data['error'].get('info', 'Unknown error')}")
            
            return data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            raise APIError(f"Request failed: {str(e)}")

    def get_login_token(self) -> str:
        """Get CSRF token for editing."""
        data = self._request(
            action="query",
            meta="tokens",
            type="csrf"
        )
        return data.get("query", {}).get("tokens", {}).get("csrftoken", "")

    def get_page_info(self, title: str) -> PageMetadata:
        """Get page metadata and info."""
        data = self._request(
            action="query",
            titles=title,
            prop="info|revisions|categories|templates|links",
            rvprop="timestamp|user",
            rvlimit=1,
            redirects=True,
            format="json"
        )
        
        pages = data.get("query", {}).get("pages", {})
        page_data = list(pages.values())[0] if pages else {}
        
        revisions = page_data.get("revisions", [])
        last_revision = revisions[0] if revisions else {}
        
        return PageMetadata(
            title=page_data.get("title", title),
            pageid=page_data.get("pageid", 0),
            namespace=page_data.get("ns", 0),
            revision_id=last_revision.get("revid", 0),
            timestamp=datetime.fromisoformat(
                last_revision.get("timestamp", "").replace("Z", "+00:00")
            ) if last_revision.get("timestamp") else datetime.now(),
            contributors=[rev.get("user", "") for rev in revisions],
            categories=[cat.get("*", "") for cat in page_data.get("categories", [])],
            templates=[tpl.get("*", "") for tpl in page_data.get("templates", [])],
            links=[link.get("*", "") for link in page_data.get("links", [])[:20]],
            length_bytes=page_data.get("length", 0),
            is_redirect="redirect" in page_data,
        )

    def get_recent_changes(self, limit: int = 100) -> List[RecentChange]:
        """Get recently modified pages."""
        data = self._request(
            action="query",
            list="recentchanges",
            rclimit=limit,
            rcprop="title|timestamp|user|comment|type|ids",
            format="json"
        )
        
        changes = []
        for item in data.get("query", {}).get("recentchanges", []):
            changes.append(RecentChange(
                pageid=item.get("pageid", 0),
                title=item.get("title", ""),
                type=item.get("type", "edit"),
                timestamp=datetime.fromisoformat(
                    item.get("timestamp", "").replace("Z", "+00:00")
                ) if item.get("timestamp") else datetime.now(),
                user=item.get("user", ""),
                comment=item.get("comment", ""),
                revision_id=item.get("revid", None),
            ))
        
        return changes

    def get_category_members(self, category: str, limit: int = 100) -> List[str]:
        """Get pages in a category."""
        data = self._request(
            action="query",
            list="categorymembers",
            cmtitle=f"Category:{category}",
            cmlimit=limit,
            format="json"
        )
        
        members = []
        for item in data.get("query", {}).get("categorymembers", []):
            members.append(item.get("title", ""))
        
        return members

    def edit_page(self, title: str, content: str, summary: str) -> EditResult:
        """
        Edit a page.
        
        Args:
            title: Page title
            content: New page content
            summary: Edit summary
            
        Returns:
            EditResult with operation details
        """
        # Get token
        token = self.get_login_token()
        
        # Edit
        data = self._request(
            action="edit",
            title=title,
            text=content,
            summary=summary,
            bot=True,
            minor=False,
            token=token,
            format="json"
        )
        
        edit_info = data.get("edit", {})
        
        if edit_info.get("result") == "Success":
            return EditResult(
                success=True,
                pageid=edit_info.get("pageid", 0),
                title=title,
                revision_id=edit_info.get("pageid", 0),
                timestamp=datetime.now(),
                summary=summary,
            )
        else:
            return EditResult(
                success=False,
                pageid=edit_info.get("pageid", 0),
                title=title,
                revision_id=0,
                timestamp=datetime.now(),
                summary=summary,
                error=edit_info.get("result", "Unknown error"),
            )

    def get_page_text(self, title: str) -> str:
        """Get raw wiki markup of a page."""
        data = self._request(
            action="query",
            titles=title,
            prop="revisions",
            rvprop="content",
            format="json"
        )
        
        pages = data.get("query", {}).get("pages", {})
        page_data = list(pages.values())[0] if pages else {}
        revisions = page_data.get("revisions", [])
        
        if revisions:
            return revisions[0].get("*", "")
        return ""
