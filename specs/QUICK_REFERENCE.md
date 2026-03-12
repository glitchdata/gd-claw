# Quick Reference Guide

**MediaWiki AI Agent - Quick Lookup**

---

## Document Guide

| Need | Read This |
|------|-----------|
| Overview | README.md |
| Full Spec | AGENT_SPECS.md |
| How to Build | IMPLEMENTATION_GUIDE.md |
| Code Examples | EXAMPLES.md |
| Track Progress | IMPLEMENTATION_CHECKLIST.md |
| How to Deploy | Dockerfile, docker-compose.yml |
| Configuration | config.yaml.example, .env.example |

---

## Component Directory

| Component | File | Purpose |
|-----------|------|---------|
| API Client | mediawiki/client.py | MediaWiki REST & Action APIs |
| Indexing | indexing/indexer.py | Full & incremental sync |
| Search | vector_store/base.py | Vector & semantic search |
| AI | ai/llm_client.py | LLM integration |
| Editing | operations/editor.py | Safe page editing |
| Analysis | analysis/quality.py | Content analysis |
| Knowledge Graph | knowledge_graph/graph.py | Entity relationships |
| REST API | api/app.py | FastAPI endpoints |

---

## Common Commands

```bash
# Setup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env && cp config.yaml.example config.yaml

# Development
python -m pytest tests/ -v --cov=src
python -m black src/ tests/
python -m mypy src/

# Run
python -m uvicorn src.api.app:app --reload

# Docker
docker build -f Dockerfile -t mediawiki-agent .
docker-compose up -d

# Testing
curl http://localhost:8000/health
curl "http://localhost:8000/api/search?q=test"
```

---

## Key Files & Line Numbers

### Specifications
- AGENT_SPECS.md § 2: Architecture
- AGENT_SPECS.md § 3: Features
- AGENT_SPECS.md § 4: MediaWiki APIs
- AGENT_SPECS.md § 5: Data Models
- AGENT_SPECS.md § 7: API Endpoints

### Implementation
- IMPLEMENTATION_GUIDE.md § 1: Project Structure
- IMPLEMENTATION_GUIDE.md § 2: Core Modules
- IMPLEMENTATION_GUIDE.md § 3: Code Patterns
- IMPLEMENTATION_GUIDE.md § 4: Development Workflow

### Examples
- EXAMPLES.md: 30+ practical code samples
- EXAMPLES.md § 13: Troubleshooting patterns

---

## API Endpoints Quick Reference

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Health check |
| `/api/search` | GET | Full-text search |
| `/api/page/{title}` | GET | Get page content |
| `/api/page/{title}/summary` | GET | Get summary |
| `/api/analyze/page/{title}` | GET | Analyze page |
| `/api/extract` | POST | Extract entities |
| `/api/edit` | POST | Edit page |
| `/api/sync/full` | POST | Full indexing |
| `/api/sync/incremental` | POST | Incremental sync |

Full reference: AGENT_SPECS.md § 7

---

## Configuration Quick Lookup

### Environment Variables
```bash
MEDIAWIKI_URL=https://wiki.example.com
MEDIAWIKI_BOT_USER=BotUser
MEDIAWIKI_BOT_PASSWORD=token
LLM_PROVIDER=openai
LLM_API_KEY=your_key
```

See `.env.example` for all options.

### YAML Config Sections
- `mediawiki:` - Wiki connection
- `indexing:` - Sync strategy
- `ai.llm:` - LLM selection
- `vector_store:` - Vector DB
- `cache:` - Caching
- `database:` - Persistence
- `agent:` - Features & safety
- `monitoring:` - Logging & metrics

See `config.yaml.example` for all options.

---

## Data Models Cheat Sheet

### PageMetadata
```python
title: str
pageid: int
namespace: int  # 0=Article, 10=Template
revision_id: int
categories: List[str]
templates: List[str]
```

### PageContent
```python
pageid: int
wiki_text: str
html: str
sections: List[Section]
tables: List[Table]
references: List[Reference]
```

### IndexEntry
```python
pageid: int
title: str
full_text: str
embeddings: List[float]
summary: str
keywords: List[str]
quality_score: float  # 0-1
related_pages: List[int]
```

See AGENT_SPECS.md § 5 for full definitions.

---

## Module Descriptions

| Module | Exports | Key Classes |
|--------|---------|-------------|
| mediawiki/ | MediaWikiClient | RESTClient, ActionClient |
| indexing/ | PageIndexer | PageIndexer, Parser, Normalizer |
| ai/ | LLMClient | LLMClient, EmbeddingGenerator |
| vector_store/ | VectorStore | FAISSVectorStore, PineconeStore |
| operations/ | Editor, Creator | PageEditor, PageCreator, OperationQueue |
| analysis/ | QualityAnalyzer | QualityAnalyzer, SuggestionGenerator |
| knowledge_graph/ | KnowledgeGraph | KnowledgeGraph, EntityExtractor |
| api/ | FastAPI app | Routes, Middleware |

See IMPLEMENTATION_GUIDE.md § 2 for full details.

---

## Phase Checklist Summary

| Phase | Duration | Key Deliverable |
|-------|----------|-----------------|
| 1 | Weeks 1-4 | Basic read-only API |
| 2 | Weeks 5-8 | Search & indexing |
| 3 | Weeks 9-12 | AI features |
| 4 | Weeks 13-16 | Editing & automation |
| 5 | Weeks 17-20 | Production-ready |
| 6 | Ongoing | Advanced features |

See IMPLEMENTATION_CHECKLIST.md for detailed tasks per phase.

---

## Testing Strategy

| Level | Coverage | Reference |
|-------|----------|-----------|
| Unit | 70%+ | AGENT_SPECS.md § 10.1 |
| Integration | Complex flows | AGENT_SPECS.md § 10.2 |
| Performance | Latency targets | AGENT_SPECS.md § 10.3 |
| Security | All threat vectors | AGENT_SPECS.md § 9 |
| E2E | Full workflows | IMPLEMENTATION_GUIDE.md |

---

## Deployment Options

### Local Development
```bash
# Use in-memory vectors, local SQLite
docker-compose up
```

### Small Deploy (< 50k pages)
```
VECTOR_DB_TYPE: faiss    # Local
CACHE_BACKEND: memory    # In-memory
DATABASE: sqlite         # Local file
```

### High Availability
```
VECTOR_DB_TYPE: pinecone # Cloud
CACHE_BACKEND: redis     # Separate service
DATABASE: postgresql     # Cloud DB
```

See docker-compose.yml for profiles and services.

---

## Common Issues

| Issue | Solution | Reference |
|-------|----------|-----------|
| Bot login fails | Check OAuth2 token | EXAMPLES.md |
| No search results | Run full sync | EXAMPLES.md |
| LLM API errors | Check quota/rate limits | EXAMPLES.md |
| Memory leak | Profile code | IMPLEMENTATION_GUIDE.md |
| Slow edits | Add rate limiting | AGENT_SPECS.md § 4.3 |
| Conflicts | Use merger | EXAMPLES.md |

See EXAMPLES.md § Advanced or AGENT_SPECS.md § Troubleshooting.

---

## Performance Targets

| Metric | Target |
|--------|--------|
| Search latency | < 500ms |
| Indexing speed | > 100 pages/sec |
| API response time | < 1s |
| Memory/page | < 1MB |
| Vector search | < 100ms |
| Edit operation | < 5 sec (rate limited) |

---

## Security Checklist

- [ ] Credentials in .env
- [ ] OAuth2 with minimal scopes
- [ ] Edit summaries required
- [ ] Bot flag enabled
- [ ] Whitelist mode for testing
- [ ] Rate limiting active
- [ ] Input validation active
- [ ] Audit logging enabled
- [ ] HTTPS enforced
- [ ] Dependencies updated

---

## Resources

| Type | Link | Usage |
|------|------|-------|
| MediaWiki API | mediawiki.org/wiki/API | API reference |
| pywikibot | doc.wikimedia.org/pywikibot | Bot library |
| FastAPI | fastapi.tiangolo.com | Web framework |
| FAISS | github.com/facebookresearch/faiss | Vector DB |
| OpenAI | openai.com/api | LLM API |

---

## Team Role Cheat Sheet

### Architect/PM
- Read: README.md, PACKAGE_OVERVIEW.md
- Review: AGENT_SPECS.md § 1-3, 12
- Track: IMPLEMENTATION_CHECKLIST.md

### Backend Dev
- Read: IMPLEMENTATION_GUIDE.md
- Study: Module descriptions § 2
- Reference: EXAMPLES.md during coding

### DevOps
- Review: Dockerfile, docker-compose.yml
- Follow: config.yaml.example, Deployment § 11
- Setup: Docker and Kubernetes

### QA/Testing
- Review: Testing Strategy § 10
- Execute: Test cases from IMPLEMENTATION_GUIDE.md
- Reference: EXAMPLES.md for test scenarios

### Frontend Dev (UI Phase 6)
- Review: Architecture § 2.1
- Study: API endpoints § 7
- Reference: EXAMPLES.md API usage

---

## Useful Patterns

### Rate Limiting
```python
@sleep_and_retry
@limits(calls=1, period=1)
def api_call():
    return requests.get(url)
```

### Retry Logic
```python
@retry(stop=stop_after_attempt(3),
       wait=wait_exponential())
def operation():
    return client.edit_page(...)
```

### Async Operations
```python
async def process_batch(pages):
    results = await asyncio.gather(*[
        process_page(p) for p in pages
    ])
    return results
```

See IMPLEMENTATION_GUIDE.md § Patterns for more.

---

## Useful Links

- Project Workspace: `/Users/terence/repo/gd-claw/`
- Main Config: `config.yaml` (copy from example)
- Env Config: `.env` (copy from .env.example)
- Source Code: `src/` (to be created)
- Tests: `tests/` (to be created)
- Docs: This folder (already populated)

---

**Last Updated:** March 12, 2026  
**Quick Ref Version:** 1.0

For detailed information, always refer to the full specification documents.
