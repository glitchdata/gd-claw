"""Main MediaWiki client combining REST and Action APIs."""

from typing import List

from src.core import get_logger
from .models import PageMetadata, PageContent, SearchResult, RecentChange, EditResult
from .rest_client import RESTClient
from .action_client import ActionClient


logger = get_logger(__name__)


class MediaWikiClient:
    """High-level MediaWiki client."""

    def __init__(
        self,
        url: str,
        bot_user: str,
        bot_password: str,
        timeout: int = 30,
    ):
        """
        Initialize MediaWiki client.
        
        Args:
            url: MediaWiki base URL
            bot_user: Bot username
            bot_password: Bot password or token
            timeout: Request timeout in seconds
        """
        self.rest_client = RESTClient(url, timeout=timeout)
        self.action_client = ActionClient(url, bot_user, bot_password, timeout=timeout)
        logger.info("MediaWiki client initialized")

    def search(self, query: str, limit: int = 20) -> List[SearchResult]:
        """Search for pages."""
        return self.rest_client.search(query, limit=limit)

    def get_page_metadata(self, title: str) -> PageMetadata:
        """Get page metadata."""
        return self.action_client.get_page_info(title)

    def get_page_text(self, title: str) -> str:
        """Get raw wiki markup."""
        return self.action_client.get_page_text(title)

    def get_recent_changes(self, limit: int = 100) -> List[RecentChange]:
        """Get recently modified pages."""
        return self.action_client.get_recent_changes(limit=limit)

    def get_category_members(self, category: str, limit: int = 100) -> List[str]:
        """Get pages in a category."""
        return self.action_client.get_category_members(category, limit=limit)

    def edit_page(self, title: str, content: str, summary: str) -> EditResult:
        """Edit a page."""
        return self.action_client.edit_page(title, content, summary)
