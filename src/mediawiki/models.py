"""Data models for MediaWiki API responses and page content."""

from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class PageMetadata(BaseModel):
    """Metadata about a wiki page."""
    title: str
    pageid: int
    namespace: int = 0  # 0=Article, 1=Talk, 10=Template, etc.
    revision_id: int
    timestamp: datetime
    contributors: List[str] = Field(default_factory=list)
    categories: List[str] = Field(default_factory=list)
    templates: List[str] = Field(default_factory=list)
    links: List[str] = Field(default_factory=list)
    references: int = 0
    length_bytes: int = 0
    is_redirect: bool = False
    is_disambiguation: bool = False
    language: str = "en"

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class Section(BaseModel):
    """A section within a page."""
    level: int
    title: str
    content: str
    subsections: List["Section"] = Field(default_factory=list)


class Table(BaseModel):
    """A table in a page."""
    headers: List[str]
    rows: List[List[str]]


class Reference(BaseModel):
    """A citation/reference in a page."""
    id: str
    title: Optional[str] = None
    url: Optional[str] = None
    authors: List[str] = Field(default_factory=list)
    date: Optional[str] = None


class Media(BaseModel):
    """Media file reference."""
    title: str
    url: str
    media_type: str  # image, video, audio, etc.


class PageContent(BaseModel):
    """Complete content of a wiki page."""
    pageid: int
    title: str
    namespace: int = 0
    wiki_text: str  # raw wiki markup
    html: Optional[str] = None
    sections: List[Section] = Field(default_factory=list)
    tables: List[Table] = Field(default_factory=list)
    templates: Dict[str, Any] = Field(default_factory=dict)
    infobox: Optional[Dict[str, Any]] = None
    references: List[Reference] = Field(default_factory=list)
    media: List[Media] = Field(default_factory=list)
    last_modified: datetime = Field(default_factory=datetime.now)


class EditResult(BaseModel):
    """Result of an edit operation."""
    success: bool
    pageid: int
    title: str
    revision_id: int
    timestamp: datetime
    summary: str
    error: Optional[str] = None


class SearchResult(BaseModel):
    """Result from a search operation."""
    pageid: int
    title: str
    namespace: int
    relevance: float  # 0-1 score
    snippet: str
    categories: List[str] = Field(default_factory=list)


class RecentChange(BaseModel):
    """A recent change to a page."""
    pageid: int
    title: str
    type: str  # new, edit, delete, move
    timestamp: datetime
    user: str
    comment: str
    revision_id: Optional[int] = None


class BotEdit(BaseModel):
    """A queued bot edit operation."""
    action: str  # 'create', 'update', 'delete'
    page_title: str
    content: str
    summary: str
    minor: bool = False
    bot: bool = True
    timestamp: Optional[datetime] = None
    status: str = "pending"  # pending, executing, completed, failed
    error: Optional[str] = None


# Resolve forward references
Section.update_forward_refs()
