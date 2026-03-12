# Technical Implementation Guide - MediaWiki AI Agent

## Project Structure

```
mediawiki-agent/
├── README.md
├── setup.py
├── requirements.txt
├── .env.example
├── config.yaml.example
│
├── src/
│   ├── __init__.py
│   ├── main.py                 # Entry point
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── agent.py           # Main agent class
│   │   ├── config.py          # Configuration management
│   │   └── logger.py          # Logging setup
│   │
│   ├── mediawiki/
│   │   ├── __init__.py
│   │   ├── client.py          # MediaWiki API client
│   │   ├── rest_client.py     # REST API implementation
│   │   ├── action_client.py   # Action API implementation
│   │   ├── auth.py            # Authentication (OAuth2, bot password)
│   │   ├── models.py          # Data models
│   │   └── exceptions.py      # Custom exceptions
│   │
│   ├── indexing/
│   │   ├── __init__.py
│   │   ├── indexer.py         # Full and incremental indexing
│   │   ├── parser.py          # Wiki markup parser
│   │   ├── normalizer.py      # Text normalization
│   │   └── cache.py           # Cache management
│   │
│   ├── ai/
│   │   ├── __init__.py
│   │   ├── llm_client.py      # LLM interface (OpenAI, Anthropic, local)
│   │   ├── embeddings.py      # Embedding generation
│   │   ├── prompts.py         # LLM prompt templates
│   │   └── validators.py      # Output validation
│   │
│   ├── knowledge_graph/
│   │   ├── __init__.py
│   │   ├── graph.py           # Knowledge graph construction
│   │   ├── entities.py        # Entity extraction
│   │   ├── relationships.py   # Relationship extraction
│   │   └── storage.py         # Graph storage layer
│   │
│   ├── vector_store/
│   │   ├── __init__.py
│   │   ├── base.py            # Abstract vector store
│   │   ├── faiss_store.py    # FAISS implementation
│   │   ├── pinecone_store.py # Pinecone implementation
│   │   └── milvus_store.py   # Milvus implementation
│   │
│   ├── operations/
│   │   ├── __init__.py
│   │   ├── editor.py          # Page editing operations
│   │   ├── creator.py         # Page creation
│   │   ├── deleter.py         # Page deletion/archival
│   │   ├── merger.py          # Merge/conflict resolution
│   │   └── queue.py           # Operation queue/scheduler
│   │
│   ├── analysis/
│   │   ├── __init__.py
│   │   ├── quality.py         # Page quality assessment
│   │   ├── completeness.py    # Content completeness analysis
│   │   ├── relationships.py   # Cross-page relationships
│   │   └── suggestions.py     # Generate suggestions
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── app.py             # FastAPI application
│   │   ├── routes.py          # API endpoints
│   │   ├── models.py          # Request/response models
│   │   └── middleware.py      # Auth, logging middleware
│   │
│   └── utils/
│       ├── __init__.py
│       ├── text.py            # Text utilities
│       ├── time.py            # Time/timezone handling
│       ├── network.py         # Network utilities
│       └── validators.py      # Input validation
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py            # Pytest fixtures
│   ├── test_mediawiki_client.py
│   ├── test_indexer.py
│   ├── test_ai_extraction.py
│   ├── test_editor.py
│   ├── test_api.py
│   └── integration/
│       ├── test_e2e_workflows.py
│       └── fixtures/           # Test data, mock responses
│
├── scripts/
│   ├── init_wiki.py           # Initialize wikistance
│   ├── full_sync.py           # Full content synchronization
│   ├── benchmark.py           # Performance testing
│   └── generate_docs.py       # Generate API documentation
│
├── docker/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── .dockerignore
│
└── docs/
    ├── AGENT_SPECS.md
    ├── API.md
    ├── DEPLOYMENT.md
    ├── TROUBLESHOOTING.md
    └── examples/
```

---

## Core Module Descriptions

### mediawiki/client.py

```python
class MediaWikiClient:
    """Main client for MediaWiki interactions"""
    
    def __init__(self, url: str, bot_user: str, bot_password: str):
        self.url = url
        self.rest_client = RESTClient(url)
        self.action_client = ActionClient(url, bot_user, bot_password)
    
    # Read operations
    def get_page(self, title: str) -> PageContent:
        """Fetch full page content"""
    
    def get_page_html(self, title: str) -> str:
        """Fetch rendered HTML"""
    
    def search(self, query: str, limit: int = 20) -> List[PageMetadata]:
        """Full-text search"""
    
    def get_recentchanges(self, limit: int = 500) -> List[RecentChange]:
        """Get recently modified pages"""
    
    def get_category_members(self, category: str) -> List[PageMetadata]:
        """Get pages in category"""
    
    # Write operations
    def edit_page(self, title: str, content: str, summary: str) -> EditResult:
        """Edit existing page"""
    
    def create_page(self, title: str, content: str, summary: str) -> EditResult:
        """Create new page"""
    
    def delete_page(self, title: str, reason: str) -> bool:
        """Delete page (requires permissions)"""
```

### indexing/indexer.py

```python
class PageIndexer:
    """Manages page indexing and synchronization"""
    
    def __init__(self, client: MediaWikiClient, vector_store):
        self.client = client
        self.vector_store = vector_store
        self.local_db = LocalDatabase()
    
    async def full_sync(self):
        """Index all pages from scratch"""
        # Paginate through allpages
        # Parse and normalize content
        # Generate embeddings
        # Store in vector DB
    
    async def incremental_sync(self):
        """Process recent changes only"""
        # Get recentchanges since last sync
        # Update affected pages
        # Update vector embeddings
    
    def index_page(self, page: PageContent) -> IndexEntry:
        """Process single page into index entry"""
        # Extract metadata
        # Generate summary
        # Create embeddings
        # Detect relationships
        # Return structured entry
```

### ai/llm_client.py

```python
class LLMClient:
    """Interface for LLM operations"""
    
    def __init__(self, provider: str, model: str, api_key: str = None):
        self.provider = provider  # 'openai', 'anthropic', 'local'
        self.model = model
    
    def extract_entities(self, text: str, entity_types: List[str]) -> Dict:
        """Extract entities from text"""
    
    def summarize(self, text: str, length: str = 'medium') -> str:
        """Generate summary of text"""
    
    def analyze_quality(self, text: str, title: str) -> QualityReport:
        """Analyze content quality"""
    
    def answer_question(self, text: str, question: str) -> Answer:
        """Answer question about text"""
    
    def generate_suggestions(self, page: PageContent) -> List[Suggestion]:
        """Generate content improvement suggestions"""
```

### operations/editor.py

```python
class PageEditor:
    """Manages page editing operations"""
    
    def __init__(self, client: MediaWikiClient):
        self.client = client
        self.operation_queue = OperationQueue()
    
    async def edit_page(self, 
                       title: str, 
                       new_content: str,
                       dry_run: bool = False) -> EditResult:
        """Edit page with conflict detection"""
        # Fetch current page + revision ID
        # Check for concurrent edits
        # If conflict: resolve_conflict()
        # Submit edit
        # Update cache
        # Return result
    
    def resolve_conflict(self, 
                        current: str, 
                        new: str,
                        original: str) -> str:
        """Three-way merge for conflicts"""
    
    async def schedule_edit(self, operation: BotEdit) -> str:
        """Queue edit for later execution"""
        # Add to queue with UUID
        # Return operation ID
    
    async def execute_queued(self, operation_id: str) -> EditResult:
        """Execute queued operation"""
        # Fetch from queue
        # Execute edit
        # Update status
```

### api/app.py

```python
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(title="MediaWiki AI Agent", version="1.0")

# Health endpoints
@app.get("/health")
async def health():
    return {"status": "ok"}

# Search endpoints
@app.get("/api/search")
async def search(q: str, limit: int = 10, namespace: int = 0):
    """Search wiki content"""

# Page endpoints
@app.get("/api/page/{title}")
async def get_page(title: str):
    """Get page content"""

# Edit endpoints
@app.post("/api/edit")
async def edit_page(request: EditRequest):
    """Edit a page"""

# Analysis endpoints
@app.get("/api/analyze/page/{title}")
async def analyze_page(title: str):
    """Analyze page quality"""

# Admin endpoints
@app.post("/api/sync/full")
async def full_sync():
    """Start full synchronization"""
```

---

## Configuration Management

### config.py Example

```python
from pydantic import BaseSettings
from typing import Optional

class MediaWikiSettings(BaseSettings):
    url: str
    bot_user: str
    bot_password: str
    timeout: int = 30
    rate_limit: float = 1.0  # requests per second
    
class LLMSettings(BaseSettings):
    provider: str = "local"  # openai, anthropic, local
    model: str = "gpt-4"
    api_key: Optional[str] = None
    temperature: float = 0.7
    
class VectorStoreSettings(BaseSettings):
    type: str = "faiss"  # faiss, pinecone, milvus
    dimension: int = 1536
    
class Settings(BaseSettings):
    mediawiki: MediaWikiSettings
    llm: LLMSettings
    vector_store: VectorStoreSettings
    
    class Config:
        env_file = ".env"
        nested_delimiter = "__"
```

---

## Development Workflow

### 1. Setup Development Environment

```bash
git clone https://github.com/yourusername/mediawiki-agent.git
cd mediawiki-agent
python -m venv venv
source venv/bin/activate  # or: venv\Scripts\activate on Windows
pip install -r requirements-dev.txt
cp .env.example .env
# Edit .env with your MediaWiki URL and credentials
```

### 2. Run Tests

```bash
# Unit tests
pytest tests/unit -v

# Integration tests (requires test MediaWiki instance)
pytest tests/integration -v

# All tests
pytest tests/ -v --cov=src
```

### 3. Run Agent

```bash
# Start API server
python -m uvicorn src.api.app:app --reload

# Or run CLI
python src/main.py sync  # Full sync
python src/main.py search "query"
python src/main.py analyze "Page Title"
```

### 4. Docker Deployment

```bash
docker build -f docker/Dockerfile -t mediawiki-agent .
docker run -e MEDIAWIKI_URL=... -e MEDIAWIKI_BOT_USER=... mediawiki-agent
```

---

## API Response Examples

### Search Response

```json
{
  "query": "machine learning",
  "results": [
    {
      "pageid": 12345,
      "title": "Machine Learning",
      "namespace": 0,
      "relevance": 0.95,
      "snippet": "Machine learning is a branch of artificial intelligence...",
      "categories": ["Computer Science", "Artificial Intelligence"]
    }
  ],
  "total_results": 150,
  "execution_time_ms": 45
}
```

### Page Analysis Response

```json
{
  "title": "Climate Change",
  "quality_score": 0.78,
  "issues": [
    {
      "type": "missing_references",
      "severity": "high",
      "description": "Paragraphs 3-5 lack citations",
      "affected_section": "Causes and Effects"
    }
  ],
  "suggestions": [
    {
      "type": "add_link",
      "target_page": "Global Warming",
      "reason": "Related concept mentioned but not linked",
      "confidence": 0.82
    }
  ],
  "word_count": 5432,
  "references": 42,
  "last_updated": "2026-03-10T14:22:00Z"
}
```

---

## Common Implementation Patterns

### Rate Limiting

```python
from ratelimit import limits, sleep_and_retry
import time

@sleep_and_retry
@limits(calls=1, period=1)  # 1 request per second
def make_request(url):
    return requests.get(url)
```

### Retry Logic

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
def api_call():
    return requests.get(url)
```

### Async Operations

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

async def process_pages(pages):
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as executor:
        results = await asyncio.gather(*[
            loop.run_in_executor(executor, process_page, page)
            for page in pages
        ])
    return results
```

---

## Monitoring & Observability

### Logging Setup

```python
from loguru import logger
import sys

logger.remove()  # Remove default handler
logger.add(
    sys.stderr,
    format="<level>{level: <8}</level> | <cyan>{name}</cyan> - <level>{message}</level>",
    level="INFO"
)
logger.add(
    "logs/app.log",
    rotation="500 MB",
    retention="7 days",
    level="DEBUG"
)
```

### Metrics to Track

- API request latency (p50, p95, p99)
- Indexing progress (pages/second)
- Cache hit rate
- Edit success rate (failed edits)
- LLM API cost and latency
- Error rates by type
- Memory/disk usage

---

## Security Checklist

- [ ] Credentials stored in environment variables, not code
- [ ] HTTPS enforced for API calls
- [ ] Input validation on all endpoints
- [ ] Rate limiting enabled
- [ ] OAuth2 scopes limited to minimum necessary
- [ ] Audit logging for all write operations
- [ ] Regular dependency updates
- [ ] Secrets rotation implemented
- [ ] CORS properly configured

---

## Getting Help

- Check [MediaWiki API docs](https://www.mediawiki.org/wiki/API:Main_page)
- Review [pywikibot documentation](https://doc.wikimedia.org/pywikibot/)
- See [examples/](examples/) directory for code samples
- File issues on GitHub with reproducible examples

