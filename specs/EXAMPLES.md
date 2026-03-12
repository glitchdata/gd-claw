# Quick Start Examples

## Authentication

### Basic Setup

```python
from src.mediawiki.client import MediaWikiClient

# Initialize client
client = MediaWikiClient(
    url="https://en.wikipedia.org/wiki",
    bot_user="MyBot",
    bot_password="oauth2_token_or_password"
)
```

## Search Examples

### Simple Full-Text Search

```python
results = client.search("artificial intelligence", limit=10)

for result in results:
    print(f"{result.title} - Match: {result.relevance}")
    print(f"  Categories: {result.categories}")
```

### With Filters

```python
# Search with namespace filter
results = client.search(
    query="climate change",
    namespace=0,  # Only articles, not talk pages
    limit=20
)
```

## Content Analysis Examples

### Analyze Page Quality

```python
from src.analysis.quality import QualityAnalyzer

analyzer = QualityAnalyzer(client)
report = analyzer.analyze("Machine Learning")

print(f"Quality Score: {report.quality_score}")
print(f"Issues: {report.issues}")
print(f"Suggestions: {report.suggestions}")
```

### Extract Entities

```python
from src.ai.llm_client import LLMClient

llm = LLMClient(provider="openai", model="gpt-4")
page_content = client.get_page("Albert Einstein")

entities = llm.extract_entities(
    text=page_content.text,
    entity_types=["person", "location", "organization"]
)

for entity in entities:
    print(f"{entity.type}: {entity.value}")
```

## Content Creation Examples

### Create New Article

```python
from src.operations.creator import PageCreator

creator = PageCreator(client)

result = creator.create_page(
    title="Example Topic",
    content="""
== Overview ==
This is an introduction to the topic.

== History ==
Historical information here.

== References ==
* Source 1
* Source 2
""",
    summary="Created new article on Example Topic"
)

print(f"Created page: {result.pageid}")
```

### Update Existing Page

```python
from src.operations.editor import PageEditor

editor = PageEditor(client)

result = editor.edit_page(
    title="Example Topic",
    new_content="Updated content...",
    summary="Updated with new information",
    dry_run=False  # Set to True to test without committing
)
```

## Bulk Operations Examples

### Batch Update Pages

```python
from src.operations.queue import OperationQueue
import asyncio

queue = OperationQueue(client)

# Queue multiple edits
edits = [
    {
        "title": "Page 1",
        "content": "New content 1",
        "summary": "Update 1"
    },
    {
        "title": "Page 2", 
        "content": "New content 2",
        "summary": "Update 2"
    },
    # ... more edits
]

for edit in edits:
    queue.add_operation("edit", edit)

# Execute all at once (respects rate limits)
results = asyncio.run(queue.execute_all())

for result in results:
    print(f"{result.title}: {result.status}")
```

## Indexing Examples

### Full Wiki Indexing

```python
from src.indexing.indexer import PageIndexer
from src.vector_store.faiss_store import FAISSVectorStore
import asyncio

vector_store = FAISSVectorStore()
indexer = PageIndexer(client, vector_store)

# Index all pages
asyncio.run(indexer.full_sync())
print("Indexing complete!")
```

### Incremental Sync

```python
# Index only recently changed pages
asyncio.run(indexer.incremental_sync())
```

## Search with Embeddings

```python
# Semantic search using embeddings
results = vector_store.search(
    query="How does photosynthesis work?",
    top_k=5
)

for result in results:
    print(f"{result.title} (score: {result.similarity})")
```

## Knowledge Graph Examples

### Build Knowledge Graph

```python
from src.knowledge_graph.graph import KnowledgeGraph

kg = KnowledgeGraph(client, llm)

# Build from articles
articles = ["Quantum Mechanics", "Physics", "Albert Einstein"]

for article in articles:
    kg.add_page(article)

# Query relationships
relationships = kg.get_relationships("Albert Einstein")

for rel in relationships:
    print(f"{rel.source} --{rel.type}--> {rel.target}")
```

## CLI Usage

### Command Line Interface

```bash
# Search
python src/main.py search "machine learning" --limit 10

# Analyze page
python src/main.py analyze "Machine Learning"

# Create page
python src/main.py create "New Page" --file content.txt

# Edit page  
python src/main.py edit "Existing Page" --file updates.txt --summary "Updated"

# Sync wiki
python src/main.py sync full
python src/main.py sync incremental

# Extract entities
python src/main.py extract "Article Title" --types person,location,org
```

## API Usage Examples

### Using curl

```bash
# Search
curl "http://localhost:8000/api/search?q=artificial%20intelligence&limit=10"

# Get page
curl http://localhost:8000/api/page/Machine%20Learning

# Analyze page
curl http://localhost:8000/api/analyze/page/Machine%20Learning

# Get page summary
curl http://localhost:8000/api/page/Machine%20Learning/summary

# Extract entities
curl -X POST http://localhost:8000/api/extract \
  -H "Content-Type: application/json" \
  -d '{
    "page": "Albert Einstein",
    "entity_types": ["person", "location"]
  }'

# Edit page
curl -X POST http://localhost:8000/api/edit \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Page Title",
    "content": "New content",
    "summary": "Update"
  }'

# Full sync
curl -X POST http://localhost:8000/api/sync/full

# Check status
curl http://localhost:8000/status
```

### Using Python Requests

```python
import requests

API_URL = "http://localhost:8000"

# Search
response = requests.get(f"{API_URL}/api/search", params={
    "q": "artificial intelligence",
    "limit": 10
})
results = response.json()

# Get page
response = requests.get(f"{API_URL}/api/page/Machine%20Learning")
page = response.json()

# Analyze
response = requests.get(f"{API_URL}/api/analyze/page/Machine%20Learning")
analysis = response.json()

# Edit page
response = requests.post(f"{API_URL}/api/edit", json={
    "title": "Article Title",
    "content": "New content here",
    "summary": "Updated article"
})
result = response.json()
```

## Advanced Examples

### Custom LLM Prompts

```python
from src.ai.prompts import PromptTemplate

# Define custom extraction prompt
extraction_prompt = PromptTemplate(
    name="custom_extraction",
    template="""
Extract the following from the text:
1. Key concepts
2. Important dates
3. Notable people mentioned

Text:
{text}

Format as JSON with keys: concepts, dates, people
"""
)

result = llm.generate(extraction_prompt.format(text=page_text))
```

### Monitoring Sync Progress

```python
async def monitored_sync():
    indexer = PageIndexer(client, vector_store)
    
    # Watch progress
    async with asyncio.TaskGroup() as tg:
        # Run sync in background
        sync_task = tg.create_task(indexer.full_sync())
        
        # Monitor progress
        while not sync_task.done():
            status = indexer.get_status()
            print(f"Indexed: {status.pages_done}/{status.total_pages}")
            await asyncio.sleep(5)
    
    print("Sync complete!")
```

### Dry-Run Mode (Test Changes)

```python
# Test edits without committing
editor = PageEditor(client)

result = editor.edit_page(
    title="Article",
    new_content="New content",
    summary="Test edit",
    dry_run=True  # Preview only, no actual edit
)

if result.success:
    print("Edit preview looks good!")
    # Commit for real
    result = editor.edit_page(
        title="Article",
        new_content="New content",
        summary="Test edit",
        dry_run=False
    )
```

## Troubleshooting Examples

### Handle Edit Conflicts

```python
from src.operations.merger import ConflictResolver

resolver = ConflictResolver()

try:
    editor.edit_page(title, new_content, summary)
except EditConflictError as e:
    # Resolve conflict using 3-way merge
    resolved = resolver.resolve(
        current=e.current_content,
        new=new_content,
        original=e.original_content
    )
    editor.edit_page(title, resolved, summary)
```

### Retry Logic for Transient Errors

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
def fetch_page_with_retry(client, title):
    return client.get_page(title)

page = fetch_page_with_retry(client, "Article Title")
```

---

For more examples, see the `examples/` directory in the repository.
