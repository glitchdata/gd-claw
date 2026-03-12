# AI Agent Specifications: MediaWiki Knowledge Base Manager

**Version:** 1.0  
**Date:** March 2026  
**Status:** Draft

---

## 1. Executive Summary

This document specifies an AI Agent designed to function as an intelligent knowledge base manager for MediaWiki instances. The agent integrates with MediaWiki via REST and Action APIs, enabling automated knowledge discovery, content management, and intelligent information retrieval powered by language models.

**Key Capabilities:**
- Automated content indexing and semantic analysis
- Intelligent knowledge extraction from wiki pages
- Content quality assessment and suggestions
- Cross-page relationship discovery
- Multi-language support
- Bot-based edit operations with full audit trails

---

## 2. System Architecture

### 2.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     AI Agent Core                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   LLM/Embeddings         Knowledge Graph    Vector DB        │
│  │   Interface  │  │  Manager     │  │  Interface   │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                            ▲
                            │ (REST API)
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│              MediaWiki Instance                                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │  REST API│  │Action API│  │ Database │  │Extensions│       │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘       │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 Component Stack

- **Layer 1 - MediaWiki Integration:** API clients for MediaWiki REST and Action APIs
- **Layer 2 - Data Processing:** Parsing, normalization, and semantic analysis
- **Layer 3 - Knowledge Management:** Indexing, caching, and relationship mapping
- **Layer 4 - AI Interface:** LLM integration (OpenAI, Anthropic, local models)
- **Layer 5 - Output & Automation:** Content generation and bot operations

---

## 3. Core Features

### 3.1 Knowledge Discovery & Indexing

**Feature:** Automated discovery and indexing of all wiki content

- **Full-page indexing** with metadata extraction (title, namespace, categories, revision history)
- **Incremental indexing** for recent changes via RecentChanges API
- **Metadata extraction:**
  - Page structure (sections, templates, links, citations)
  - Categories and subcategories
  - Inbound and outbound links
  - Templates and parameters
  - File attachments and media

- **Search & Retrieval:**
  - Full-text search integration
  - Semantic/embedding-based search
  - Category-based filtering
  - Namespace filtering (articles, templates, talk pages)

### 3.2 Content Analysis

**Feature:** AI-powered analysis of wiki content quality and completeness

- **Page Quality Assessment:**
  - Completeness scoring (missing sections, references)
  - Readability metrics (sentence length, structure)
  - Coverage analysis (links to related topics)
  - Reference density and credibility

- **Relationship Discovery:**
  - Similar topic identification
  - Disambiguation detection
  - Cross-language content mapping
  - Orphaned articles identification

- **Bot Suggestions:**
  - Content gap recommendations
  - Link suggestions (add missing cross-references)
  - Redirect opportunities
  - Template standardization suggestions

### 3.3 Automated Content Management

**Feature:** Intelligent bot operations for wiki maintenance

- **Template Management:**
  - Template parameter standardization
  - Template migration support
  - Unused template identification

- **Category Operations:**
  - Batch category assignment
  - Category structure optimization
  - Category synonym consolidation

- **Maintenance Tasks:**
  - Dead link detection and removal
  - Orphaned page identification
  - Disambiguation page updates
  - Redirect creation and updates

- **Quality Improvements:**
  - Wiki-text syntax standardization
  - Reference formatting fixes
  - Duplicate content detection
  - Stub article identification

### 3.4 Knowledge Extraction

**Feature:** LLM-powered extraction of structured knowledge from unstructured wiki text

- **Entity Extraction:**
  - Named entity recognition (people, places, organizations)
  - Relationship extraction (A is related to B)
  - Fact extraction and validation

- **Summarization:**
  - Single-page summaries (variable lengths)
  - Multi-page topic summaries
  - Abstract/lead section generation
  - Diff summarization

- **Q&A Interface:**
  - Question answering over wiki content
  - Multi-hop reasoning (connecting concepts)
  - Explanation generation
  - Citation tracking

### 3.5 Bi-Directional Synchronization

**Feature:** Keep internal knowledge state synchronized with MediaWiki

- **Push Operations:**
  - Create new articles from structured data
  - Update articles with AI-generated content
  - Update templates and infoboxes
  - Create/update category pages

- **Pull Operations:**
  - Fetch all pages (initial sync)
  - Stream incremental changes via RecentChanges API
  - Monitor watchlists and notifications
  - Poll for updates on tracked pages

- **Conflict Resolution:**
  - Edit conflict detection and resolution
  - Version history analysis
  - Three-way merging for complex updates
  - Rollback capability

---

## 4. MediaWiki API Integration

### 4.1 REST API Usage

**Base Endpoints:**
```
https://{wiki-domain}/api/rest_v1/
```

**Core Endpoints:**

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/page/{title}` | GET | Fetch page content (HTML) |
| `/page/{title}/history` | GET | Get revision history |
| `/page/{title}/links/all` | GET | Get all links on a page |
| `/page_html_offline/{title}` | GET | Get offline page HTML |
| `/page/{title}/references/{reference-id}` | GET | Get citation details |
| `/search/page` | GET | Full-text search |

**Response Caching:** Implement HTTP caching headers (ETag, Cache-Control)

### 4.2 Action API Usage

**Base Endpoint:**
```
https://{wiki-domain}/w/api.php
```

**Core Actions:**

| Action | Parameters | Purpose |
|--------|-----------|---------|
| `query` | `titles`, `prop` | Fetch page metadata |
| `query` | `list=allpages` | List all pages |
| `query` | `list=recentchanges` | Get recent changes |
| `query` | `list=categorymembers` | Get category members |
| `edit` | `title`, `text`, `summary` | Edit a page |
| `parse` | `page`, `prop` | Parse wiki markup |

**Authentication:**
- **For read operations:** Public API (no auth)
- **For write operations:** OAuth2 or bot password with scopes:
  - `read:main` (read articles)
  - `edit:main` (edit articles)
  - `delete:main` (delete articles)

### 4.3 Rate Limiting & Throttling

- Respect `X-RateLimit-*` headers from MediaWiki
- Default: Max 1 request/sec for reads, 5 sec between edits
- Implement exponential backoff for 429 responses
- Queue edit operations for bot task scheduling

---

## 5. Data Models

### 5.1 Page Model

```python
class PageMetadata:
    title: str
    pageid: int
    namespace: int  # 0=Article, 1=Talk, 10=Template, etc.
    revision_id: int
    timestamp: datetime
    contributors: List[str]
    categories: List[str]
    templates: List[str]
    links: List[str]
    references: int  # count
    length_bytes: int
    is_redirect: bool
    is_disambiguation: bool
    language: str
```

### 5.2 Content Model

```python
class PageContent:
    pageid: int
    title: str
    wiki_text: str  # raw wiki markup
    html: str  # parsed HTML
    sections: List[Section]
    tables: List[Table]
    templates: List[Template]
    infobox: Optional[dict]  # structured data
    references: List[Reference]
    media: List[Media]
```

### 5.3 Edit Model

```python
class BotEdit:
    action: str  # 'create' | 'update' | 'delete' | 'revert'
    page_title: str
    content: str
    summary: str  # edit summary
    minor: bool
    bot: bool  # mark as bot edit
    timestamp: datetime
    status: str  # 'pending' | 'executed' | 'failed'
    error: Optional[str]
```

### 5.4 Index Entry Model

```python
class IndexEntry:
    pageid: int
    title: str
    namespace: int
    full_text: str
    embeddings: List[float]  # Vector embeddings
    summary: str
    keywords: List[str]
    quality_score: float  # 0-1
    last_updated: datetime
    related_pages: List[int]
```

---

## 6. Functional Specifications

### 6.1 Initialization Workflow

**Input:** MediaWiki instance URL, bot credentials

```
1. Authenticate with MediaWiki (OAuth2 or bot password)
2. Fetch site info (version, namespaces, restrictions)
3. Initialize database / vector store
4. Perform initial full-text sync of all pages
5. Build embeddings for vector search
6. Initialize cache
```

### 6.2 Page Updating Workflow

**Input:** Page title, new content

```
1. Fetch current page content and revision ID
2. Check for concurrent edits (compare revision ID)
3. If conflict: trigger conflict resolution
4. Generate edit summary from changes
5. Perform API edit with bot flag
6. Wait for confirmation
7. Update local index cache
8. Regenerate embeddings if needed
9. Log operation with audit trail
```

### 6.3 Knowledge Extraction Workflow

**Input:** Page title, query

```
1. Fetch page content
2. Parse wiki markup (sections, tables, infoboxes)
3. Send to LLM with extraction prompt
4. Validate extracted entities
5. Store in knowledge graph
6. Return structured results
```

### 6.4 Search & Retrieval Workflow

**Input:** Query string, filters (category, namespace)

```
1. Tokenize and normalize query
2. Execute semantic search (embeddings)
3. Execute keyword search (full-text)
4. Combine and rank results
5. Apply filters (namespace, category)
6. Fetch full page content for top-K results
7. Return results with relevance scores
```

### 6.5 Content Suggestion Workflow

**Input:** Page title

```
1. Fetch page and analyze structure
2. Identify gaps (missing sections, references)
3. Find similar/related pages via embeddings
4. Generate LLM-based suggestions
5. Validate suggestions against wiki policy
6. Return ranked suggestions with confidence
```

---

## 7. API Endpoints (Agent REST Interface)

### 7.1 Health & Status

```
GET /health
Response: { status: "ok", version: "1.0" }

GET /status
Response: { indexed_pages: int, last_sync: datetime, queue_size: int }
```

### 7.2 Search & Retrieval

```
GET /api/search?q={query}&limit=10&namespace=0
GET /api/page/{title}
GET /api/page/{title}/summary
GET /api/suggest-links?page={title}
```

### 7.3 Content Management

```
POST /api/edit
Body: { title, content, summary }

POST /api/create
Body: { title, content, namespace }

DELETE /api/page/{title}

GET /api/page/{title}/diff?from_rev={rev1}&to_rev={rev2}
```

### 7.4 Analysis & Insights

```
GET /api/analyze/page/{title}
Response: { quality_score, issues, suggestions[] }

GET /api/analyze/category/{name}
Response: { member_count, structure, gaps }

POST /api/extract
Body: { page, entity_types[] }
Response: { entities[], relationships[] }
```

### 7.5 Administration

```
POST /api/sync/full - Perform full indexing
POST /api/sync/incremental - Sync recent changes
POST /api/reindex - Rebuild vector index
POST /api/cache/clear - Clear local cache
GET /api/operations - List pending operations
POST /api/operations/{id}/execute - Execute queued operation
```

---

## 8. Configuration

### 8.1 Environment Variables

```bash
MEDIAWIKI_URL=https://example.com/wiki
MEDIAWIKI_BOT_USER=BotUser
MEDIAWIKI_BOT_PASSWORD=**** (OAuth token or bot password)
MEDIAWIKI_USER_AGENT=MediaWikiAgent/1.0

LLM_PROVIDER=openai|anthropic|local  # defaults to local if available
LLM_MODEL=gpt-4|claude-3|llama2
LLM_API_KEY=****

VECTOR_DB_TYPE=faiss|pinecone|milvus  # defaults to faiss
VECTOR_DB_URL=**** (if remote)

CACHE_BACKEND=redis|memory  # defaults to memory
CACHE_TTL=3600  # seconds

LOG_LEVEL=INFO|DEBUG
BOT_EDIT_DELAY=5  # seconds between edits
MAX_CONCURRENT_REQUESTS=5
```

### 8.2 Configuration File (YAML)

```yaml
mediawiki:
  url: https://example.com/wiki
  timeout: 30
  verify_ssl: true
  rate_limit:
    reads_per_second: 1
    edits_per_second: 0.2

indexing:
  auto_sync: true
  sync_interval_hours: 24
  batch_size: 100
  languages: [en, de, fr]

llm:
  provider: openai
  model: gpt-4
  temperature: 0.7
  max_tokens: 2000
  
vector_store:
  type: faiss
  dimension: 1536
  metric: cosine
  
agent:
  name: WikiAgent
  description: Knowledge base manager
  capabilities: [extract, analyze, suggest, edit]
```

---

## 9. Security Considerations

### 9.1 Authentication & Authorization

- **OAuth2:** Recommended for bot operations
- **Token Scopes:** Limit to `read:main`, `edit:main` only
- **Credential Storage:** Use environment variables or secure vaults (not in code)
- **Token Rotation:** Implement token refresh logic

### 9.2 Edit Safety

- **Edit Summaries:** Always include descriptive summaries
- **Minor Edits:** Mark routine maintenance edits as minor
- **Bot Flag:** Explicitly mark bot operations
- **Whitelist Mode:** Only edit whitelisted pages/categories initially
- **Dry-Run Mode:** Test changes before committing
- **Revert Capability:** Maintain version history for rollbacks

### 9.3 Data Privacy

- **Cache Management:** Don't cache sensitive user data
- **Log Sanitization:** Remove credentials from logs
- **Rate Limiting:** Protect against abuse
- **User-Agent:** Identify bot in all requests

---

## 10. Testing Strategy

### 10.1 Unit Tests

- MediaWiki API client mocking
- Parser and extraction logic
- Data model validation
- Cache behavior

### 10.2 Integration Tests

- Full workflow tests against test MediaWiki instance
- API endpoint testing
- Edit operation testing (on test wiki)
- Concurrent operation handling

### 10.3 Performance Tests

- Indexing performance for large wikis (10k+ pages)
- Search latency benchmarks
- Vector search efficiency
- Memory and disk usage profiling

---

## 11. Deployment

### 11.1 Deployment Targets

- **Docker Container:** Recommended for easy deployment
- **Python Virtual Environment:** For development/small deployments
- **Kubernetes:** For high-availability setups
- **Cloud Functions:** For serverless task scheduling

### 11.2 Dependencies

**Core:**
```
pywikibot>=3.0        # MediaWiki API client
requests>=2.28.0      # HTTP client
python-dotenv>=0.20   # Config management

**AI/ML:**
openai>=0.27.0        # OpenAI API (optional)
anthropic>=0.3.0      # Anthropic API (optional)
sentence-transformers # Embeddings (local)
faiss-cpu>=1.7.0      # Vector search

**Database:**
redis>=4.0.0          # Caching (optional)
sqlite3               # Local storage (built-in)

**Utils:**
pydantic>=1.10.0      # Data validation
loguru>=0.6.0         # Logging
```

### 11.3 Resource Requirements

- **CPU:** 2+ cores (4+ cores recommended for large wikis)
- **RAM:** 4GB minimum (8GB+ for wikis >50k pages)
- **Storage:** 10GB+ (50GB+ for large wikis + embeddings)
- **Network:** Consistent internet connection

---

## 12. Roadmap

### Phase 1 (MVP)
- [x] MediaWiki API integration
- [x] Page indexing
- [x] Basic search
- [x] Simple content analysis
- [x] Read operations tested

### Phase 2
- [ ] LLM integration
- [ ] Vector embeddings & semantic search
- [ ] Write/edit operations
- [ ] Automated suggestions
- [ ] Bot operation scheduling

### Phase 3
- [ ] Knowledge graph construction
- [ ] Advanced entity extraction
- [ ] Multi-language support
- [ ] Cache optimization
- [ ] Web UI dashboard

### Phase 4
- [ ] MediaWiki extension plugin
- [ ] Real-time collaboration features
- [ ] Advanced conflict resolution
- [ ] Custom LLM fine-tuning
- [ ] Enterprise deployment templates

---

## 13. References

- [MediaWiki API Documentation](https://www.mediawiki.org/wiki/API:Main_page)
- [MediaWiki REST API](https://www.mediawiki.org/wiki/RESTBase)
- [pywikibot Documentation](https://doc.wikimedia.org/pywikibot/latest/)
- [OAuth for MediaWiki](https://www.mediawiki.org/wiki/OAuth)
- [Bot Best Practices](https://en.wikipedia.org/wiki/Wikipedia:Bot_policy)

---

## Appendix: Example Bot Operations

### Example 1: Update Infobox Template

```python
agent.edit_page(
    title="Albert Einstein",
    action="update_infobox",
    changes={
        "birth_place": "Ulm, Germany",
        "death_place": "Princeton, New Jersey"
    },
    summary="Update biographical infobox data"
)
```

### Example 2: Add Cross-References

```python
agent.suggest_links(
    page="Machine Learning",
    category="Computer Science"
)
# Returns list of suggested links to related articles
```

### Example 3: Extract Key Facts

```python
facts = agent.extract_entities(
    page="Climate Change",
    entity_types=["concept", "location", "organization"]
)
```

---

**Document Version History:**
- v1.0: Initial specification (March 2026)
