from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mediawiki-ai-agent",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="An AI agent for intelligent MediaWiki knowledge base management",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/mediawiki-agent",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
    install_requires=[
        "pywikibot>=3.0.0",
        "requests>=2.28.0",
        "python-dotenv>=0.20.0",
        "pydantic>=1.10.0",
        "fastapi>=0.104.0",
        "uvicorn>=0.24.0",
        "openai>=0.27.0",
        "sentence-transformers>=2.2.0",
        "faiss-cpu>=1.7.0",
        "loguru>=0.6.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
        "anthropic": ["anthropic>=0.3.0"],
        "pinecone": ["pinecone-client>=2.2.0"],
        "redis": ["redis>=4.0.0"],
    },
    entry_points={
        "console_scripts": [
            "mediawiki-agent=src.main:cli",
        ],
    },
)
