# MediaWiki AI Agent

An intelligent AI agent for automated knowledge base management and intelligent content analysis in MediaWiki instances.

## Overview

The MediaWiki AI Agent is a sophisticated system that bridges AI capabilities with MediaWiki wikis. It enables:

- **Intelligent Content Analysis** - Assess page quality, completeness, and relationships
- **Automated Knowledge Management** - Create, update, and organize wiki pages at scale  
- **Semantic Search** - Find relevant content using embeddings and natural language
- **Knowledge Extraction** - Extract entities, facts, and relationships from wiki text
- **Content Suggestions** - Generate intelligent improvement recommendations
- **Bot Operations** - Automate routine maintenance and bulk editing tasks

## Features

### 🔍 Indexing & Search
- Full-text search across all wiki pages
- Semantic search using embeddings
- Advanced filtering (namespace, category, date range)
- Real-time incremental indexing of recent changes

### 🤖 AI-Powered Analysis
- Page quality scoring and gap detection
- Content completeness assessment
- Readability and citation analysis
- Cross-page relationship discovery
- Stub article identification
- Duplicate content detection

### 📝 Content Generation
- Extracting structured entities and facts
- Generating article summaries
- Creating suggestions for improvements
- Draft content from structured data

### ✏️ Automated Editing
- Intelligent page creation and updates
- Template standardization
- Category management
- Redirect creation
- Conflict resolution

### 📊 Knowledge Management
- Knowledge graph construction
- Entity relationship discovery
- Topic modeling and clustering
- Content organization analysis

## Quick Start

### Prerequisites

- Python 3.9+
- MediaWiki instance (local or cloud)
- LLM API key (OpenAI, Anthropic, or use local models)
- Vector DB (FAISS built-in, optional external like Pinecone)

### Installation

```bash
# Clone repository
git clone https://github.com/yourusername/mediawiki-agent.git
cd mediawiki-agent

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy configuration templates
cp .env.example .env
cp config.yaml.example config.yaml
```

### Configuration

Edit `.env` with your credentials:

```bash
MEDIAWIKI_URL=https://your-wiki.com/wiki
MEDIAWIKI_BOT_USER=YourBotAccount
MEDIAWIKI_BOT_PASSWORD=your_bot_password
LLM_PROVIDER=openai
LLM_API_KEY=your_openai_key
```

Edit `config.yaml` for more detailed settings (optional).

### Basic Usage

```bash
# Start the API server
python -m uvicorn src.api.app:app --reload

# In another terminal, test the agent
curl http://localhost:8000/health

# Search the wiki
curl "http://localhost:8000/api/search?q=machine%20learning&limit=10"

# Analyze a page
curl http://localhost:8000/api/analyze/page/Machine%20Learning

# Perform full sync
curl -X POST http://localhost:8000/api/sync/full
```

## API Documentation

### Core Endpoints

#### Health Check
```bash
GET /health
```

#### Search
```bash
GET /api/search?q={query}&limit=10&namespace=0
```

#### Get Page
```bash
GET /api/page/{title}
GET /api/page/{title}/summary
```

#### Analyze Page
```bash
GET /api/analyze/page/{title}
```

#### Extract Entities
```bash
POST /api/extract
Content-Type: application/json

{
  "page": "Article Title",
  "entity_types": ["person", "organization", "location"]
}
```

#### Edit Page
```bash
POST /api/edit
Content-Type: application/json

{
  "title": "Article Title",
  "content": "New content here",
  "summary": "Updated with new information"
}
```

#### Synchronization
```bash
POST /api/sync/full          # Full wiki indexing
POST /api/sync/incremental   # Sync recent changes
POST /api/reindex            # Rebuild vector index
```

See [API.md](docs/API.md) for full endpoint documentation.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    AI Agent Core                                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   LLM/Embeddings   Knowledge Graph  Vector DB    │          │
│  │   Interface  │  │  Manager     │  │  Interface   │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                           ▲
                           │ (REST APIs)
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│               MediaWiki Instance                                │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │REST API  │  │Action API│  │Database  │  │Extensions│       │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘       │
└─────────────────────────────────────────────────────────────────┘
```

## Project Structure

```
mediawiki-agent/
├── src/
│   ├── core/              # Core agent and configuration
│   ├── mediawiki/         # MediaWiki API clients
│   ├── indexing/          # Content indexing and parsing
│   ├── ai/                # LLM integration
│   ├── knowledge_graph/   # Knowledge graph management
│   ├── vector_store/      # Vector DB abstraction
│   ├── operations/        # Content editing/creation
│   ├── analysis/          # Content analysis
│   ├── api/               # REST API endpoints
│   └── utils/             # Utility functions
├── tests/                 # Unit and integration tests
├── docs/                  # Documentation
├── scripts/               # Utility scripts
└── docker/                # Docker configuration
```

See [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md) for detailed architecture and development guide.

## Configuration

### Environment Variables (.env)

```bash
# Required
MEDIAWIKI_URL=https://example.com/wiki
MEDIAWIKI_BOT_USER=BotUsername
MEDIAWIKI_BOT_PASSWORD=password_or_oauth_token

# AI/LLM
LLM_PROVIDER=openai|anthropic|local
LLM_MODEL=gpt-4|claude-3|etc
LLM_API_KEY=your_key

# Vector Store
VECTOR_DB_TYPE=faiss|pinecone|milvus
CACHE_BACKEND=memory|redis
LOG_LEVEL=INFO
```

### Configuration File (config.yaml)

Comprehensive settings for:
- MediaWiki connection and API parameters
- Indexing strategy (full vs incremental)
- LLM selection and parameters
- Vector store configuration
- Caching and database settings
- Agent capabilities and safety features
- API server settings

See [config.yaml.example](config.yaml.example) for all available options.

## Development

### Running Tests

```bash
# Unit tests
pytest tests/unit -v

# Integration tests (requires test wiki)
pytest tests/integration -v

# With coverage
pytest tests/ --cov=src --cov-report=html
```

### Code Style

```bash
# Format code
black src/ tests/

# Lint
flake8 src/ tests/

# Type checking
mypy src/
```

### Building Docker Image

```bash
docker build -f docker/Dockerfile -t mediawiki-agent:latest .
docker run -e MEDIAWIKI_URL=... -e MEDIAWIKI_BOT_USER=... mediawiki-agent
```

## Deployment

See [DEPLOYMENT.md](docs/DEPLOYMENT.md) for:
- Production deployment strategies
- Docker and Kubernetes setup
- Performance tuning
- Monitoring and logging
- Scaling considerations

## Security

### Important Security Practices

⚠️ **Before deploying to production:**

1. ✅ Store all credentials in environment variables (never commit to git)
2. ✅ Use OAuth2 with minimal scopes for bot operations
3. ✅ Enable edit summaries and bot flags
4. ✅ Start with dry-run mode and whitelist mode enabled
5. ✅ Test all scripts on a test wiki first
6. ✅ Implement rate limiting to avoid overwhelming the wiki
7. ✅ Monitor edit logs and maintain rollback capability
8. ✅ Keep dependencies updated

## Troubleshooting

### Common Issues

**Bot login fails**
- Verify credentials in .env
- Check OAuth2 token expiration
- Ensure bot account has necessary permissions

**Search returns no results**
- Run `POST /api/sync/full` to index wiki
- Wait for indexing to complete
- Check wiki has content

**LLM API errors**
- Verify API key is correct
- Check rate limits and quotas
- Test with `mock_llm: true` in config

See [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) for more help.

## Examples

See [examples/](examples/) directory for:
- Basic search operations
- Content extraction
- Bot editing scripts
- Knowledge graph queries
- Batch operations

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure tests pass and code is formatted
5. Submit a pull request

## License

This project is licensed under the Apache License 2.0 - see [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [pywikibot](https://doc.wikimedia.org/pywikibot/)
- API powered by OpenAI/Anthropic
- Vector search with [FAISS](https://github.com/facebookresearch/faiss)

## Support

- **Issues & Bugs:** Open a GitHub issue
- **Documentation:** See [docs/](docs/) folder
- **Questions:** Start a discussion on GitHub

## Related Projects

- [pywikibot](https://github.com/wikimedia/pywikibot) - Official MediaWiki bot library
- [mwclient](https://github.com/mwclient/mwclient) - Alternative MediaWiki client
- [LangChain](https://github.com/langchain-ai/langchain) - LLM orchestration framework
- [LlamaIndex](https://www.llamaindex.ai/) - Data indexing for LLMs

---

**Last Updated:** March 2026  
**Current Version:** 0.1.0 (Alpha)

For detailed specifications, see [AGENT_SPECS.md](AGENT_SPECS.md)
