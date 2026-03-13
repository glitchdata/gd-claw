"""MediaWiki API clients and models."""

from .client import MediaWikiClient
from .models import (
    PageMetadata,
    PageContent,
    SearchResult,
    RecentChange,
    EditResult,
    BotEdit,
)

__all__ = [
    "MediaWikiClient",
    "PageMetadata",
    "PageContent",
    "SearchResult",
    "RecentChange",
    "EditResult",
    "BotEdit",
]
