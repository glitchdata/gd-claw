"""FastAPI application for MediaWiki AI Agent."""

from datetime import datetime
from typing import List, Optional

from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.core import get_settings, configure_logging, get_logger
from src.mediawiki import MediaWikiClient


# Configure logging
configure_logging()
logger = get_logger(__name__)
settings = get_settings()

# Initialize app
app = FastAPI(
    title="MediaWiki AI Agent",
    version="0.1.0",
    description="Intelligent knowledge base manager for MediaWiki",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global MediaWiki client
_mediawiki_client: MediaWikiClient = None


def get_client() -> MediaWikiClient:
    """Get or create MediaWiki client."""
    global _mediawiki_client
    if _mediawiki_client is None:
        try:
            _mediawiki_client = MediaWikiClient(
                url=settings.mediawiki.url,
                bot_user=settings.mediawiki.bot_user,
                bot_password=settings.mediawiki.bot_password,
                timeout=settings.mediawiki.timeout,
            )
        except Exception as e:
            logger.error(f"Failed to initialize MediaWiki client: {e}")
            raise
    return _mediawiki_client


# Response models
class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    timestamp: datetime
    version: str


class StatusResponse(BaseModel):
    """Status response."""
    status: str
    indexed_pages: int = 0
    last_sync: Optional[datetime] = None
    queue_size: int = 0


class SearchResultItem(BaseModel):
    """Search result item."""
    pageid: int
    title: str
    namespace: int
    relevance: float
    snippet: str


class SearchResponse(BaseModel):
    """Search response."""
    query: str
    results: List[SearchResultItem]
    total_results: int
    execution_time_ms: float


# ============================================================================
# Health & Status Endpoints
# ============================================================================

@app.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Health check endpoint."""
    return HealthResponse(
        status="ok",
        timestamp=datetime.now(),
        version="0.1.0",
    )


@app.get("/status", response_model=StatusResponse)
async def get_status() -> StatusResponse:
    """Get agent status."""
    return StatusResponse(
        status="running",
        indexed_pages=0,
        last_sync=None,
        queue_size=0,
    )


# ============================================================================
# Search Endpoints
# ============================================================================

@app.get("/api/search", response_model=SearchResponse)
async def search(
    q: str = Query(..., min_length=1, description="Search query"),
    limit: int = Query(10, ge=1, le=100, description="Number of results"),
    client: MediaWikiClient = Depends(get_client),
) -> SearchResponse:
    """Search wiki content."""
    import time
    start_time = time.time()
    
    try:
        results = client.search(query=q, limit=limit)
        
        execution_time = (time.time() - start_time) * 1000
        
        return SearchResponse(
            query=q,
            results=[
                SearchResultItem(
                    pageid=r.pageid,
                    title=r.title,
                    namespace=r.namespace,
                    relevance=r.relevance,
                    snippet=r.snippet,
                )
                for r in results
            ],
            total_results=len(results),
            execution_time_ms=execution_time,
        )
    except Exception as e:
        logger.error(f"Search failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Page Endpoints
# ============================================================================

class PageResponse(BaseModel):
    """Page response."""
    title: str
    pageid: int
    namespace: int
    content: str


@app.get("/api/page/{title}", response_model=PageResponse)
async def get_page(
    title: str,
    client: MediaWikiClient = Depends(get_client),
) -> PageResponse:
    """Get page content."""
    try:
        metadata = client.get_page_metadata(title)
        content = client.get_page_text(title)
        
        return PageResponse(
            title=metadata.title,
            pageid=metadata.pageid,
            namespace=metadata.namespace,
            content=content,
        )
    except Exception as e:
        logger.error(f"Failed to get page {title}: {e}")
        raise HTTPException(status_code=404, detail=f"Page not found: {title}")


class PageSummaryResponse(BaseModel):
    """Page summary response."""
    title: str
    pageid: int
    length_bytes: int
    categories: List[str]


@app.get("/api/page/{title}/summary", response_model=PageSummaryResponse)
async def get_page_summary(
    title: str,
    client: MediaWikiClient = Depends(get_client),
) -> PageSummaryResponse:
    """Get page summary."""
    try:
        metadata = client.get_page_metadata(title)
        
        return PageSummaryResponse(
            title=metadata.title,
            pageid=metadata.pageid,
            length_bytes=metadata.length_bytes,
            categories=metadata.categories,
        )
    except Exception as e:
        logger.error(f"Failed to get summary for {title}: {e}")
        raise HTTPException(status_code=404, detail=f"Page not found: {title}")


# ============================================================================
# Sync Endpoints (Stubs for Phase 1)
# ============================================================================

@app.post("/api/sync/full")
async def full_sync():
    """Start full wiki indexing."""
    return {
        "status": "pending",
        "message": "Full sync scheduled",
        "estimated_time": "TBD"
    }


@app.post("/api/sync/incremental")
async def incremental_sync():
    """Sync recent changes."""
    return {
        "status": "pending",
        "message": "Incremental sync scheduled",
        "changes_found": 0
    }


# Error handlers
@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions."""
    logger.error(f"Unhandled exception: {exc}")
    return {
        "error": str(exc),
        "status": 500
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
