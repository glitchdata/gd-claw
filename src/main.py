"""Main entry point for MediaWiki AI Agent."""

import sys
import click
from pathlib import Path

from src.core import configure_logging, get_logger, get_settings
from src.mediawiki import MediaWikiClient


# Configure logging
configure_logging()
logger = get_logger(__name__)


@click.group()
@click.version_option("0.1.0")
def cli():
    """MediaWiki AI Agent - Intelligent knowledge base manager."""
    pass


@cli.command()
@click.option("--host", default="0.0.0.0", help="API host")
@click.option("--port", default=8000, help="API port")
@click.option("--reload", is_flag=True, help="Enable auto-reload")
def serve(host: str, port: int, reload: bool):
    """Start the REST API server."""
    try:
        import uvicorn
        from src.api.app import app
        
        logger.info(f"Starting API server on {host}:{port}")
        uvicorn.run(
            "src.api.app:app",
            host=host,
            port=port,
            reload=reload,
            log_level="info",
        )
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        sys.exit(1)


@cli.command()
@click.argument("query")
@click.option("--limit", default=10, help="Number of results")
def search(query: str, limit: int):
    """Search the wiki."""
    try:
        settings = get_settings()
        client = MediaWikiClient(
            url=settings.mediawiki.url,
            bot_user=settings.mediawiki.bot_user,
            bot_password=settings.mediawiki.bot_password,
        )
        
        logger.info(f"Searching for: {query}")
        results = client.search(query, limit=limit)
        
        click.echo(f"\nFound {len(results)} results:\n")
        for result in results:
            click.echo(f"  {result.title}")
            click.echo(f"    ID: {result.pageid}, Relevance: {result.relevance:.2%}")
            click.echo(f"    {result.snippet}\n")
            
    except Exception as e:
        logger.error(f"Search failed: {e}")
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("title")
def analyze(title: str):
    """Analyze a page."""
    try:
        settings = get_settings()
        client = MediaWikiClient(
            url=settings.mediawiki.url,
            bot_user=settings.mediawiki.bot_user,
            bot_password=settings.mediawiki.bot_password,
        )
        
        logger.info(f"Analyzing page: {title}")
        metadata = client.get_page_metadata(title)
        
        click.echo(f"\nPage Analysis: {metadata.title}")
        click.echo(f"  ID: {metadata.pageid}")
        click.echo(f"  Namespace: {metadata.namespace}")
        click.echo(f"  Size: {metadata.length_bytes} bytes")
        click.echo(f"  Categories: {', '.join(metadata.categories) or 'None'}")
        click.echo(f"  References: {metadata.references}")
        click.echo()
        
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
def check():
    """Check configuration and connectivity."""
    try:
        settings = get_settings()
        
        click.echo("Configuration Check:")
        click.echo(f"  MediaWiki URL: {settings.mediawiki.url}")
        click.echo(f"  Bot User: {settings.mediawiki.bot_user}")
        click.echo(f"  LLM Provider: {settings.llm.provider}")
        click.echo(f"  Vector Store: {settings.vector_store.type}")
        
        logger.info("Attempting to connect to MediaWiki...")
        client = MediaWikiClient(
            url=settings.mediawiki.url,
            bot_user=settings.mediawiki.bot_user,
            bot_password=settings.mediawiki.bot_password,
        )
        
        # Try a simple search to verify connectivity
        results = client.search("main", limit=1)
        
        click.echo("\n✓ Configuration is valid")
        click.echo("✓ MediaWiki connectivity OK")
        
    except Exception as e:
        logger.error(f"Configuration check failed: {e}")
        click.echo(f"\n✗ Configuration check failed:", err=True)
        click.echo(f"  {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    cli()
