Code Review Bot

A comprehensive, automated code review assistant designed to integrate directly with GitHub Pull Requests.
This bot combines deterministic static analysis tools with context-aware Large Language Models (LLMs) to catch bugs, security vulnerabilities, and style issues.

Overview

The Code Review Bot acts as intelligent middleware between your GitHub repository and multiple code analysis tools.

When a Pull Request is opened or updated, the bot automatically:

Fetches the code changes

Runs a suite of analysis tools

Generates actionable feedback

Posts inline comments and a summary report directly on the PR

It leverages Retrieval-Augmented Generation (RAG) to provide the LLM with relevant repository context, ensuring AI-generated suggestions are grounded in the actual codebase rather than isolated snippets.

Key Features
Hybrid Analysis Engine

Combines the precision of static linters with the reasoning capabilities of LLMs.

Ruff

Extremely fast Python linting

Code formatting checks

Bandit

Security-focused static analysis

Detects common Python vulnerabilities

Gemini (LLM)

Logic bug detection

Maintainability analysis

Complex refactoring suggestions

Context-Aware Reviews (RAG)

Uses FAISS vector storage to index repository files

Enables the LLM to understand project-specific utilities and configuration patterns

Smart Deduplication

Tracks posted comments in a local SQLite database

Prevents repeated comments across multiple commits

GitHub Integration

Automated webhook handling

Inline comments for specific lines of code

Summary reports for high-level feedback

Configurable

Modular architecture

Easily extensible to add new analysis tools

Architecture

The system is built using FastAPI and follows a modular design:

Components

Webhook Handler
Listens for GitHub pull_request events.

Diff Parser
Identifies valid Python files and filters out generated code or migrations.

Aggregator
Orchestrates the entire review workflow:

Executes RuffRunner and BanditRunner

Embeds code context using GeminiEmbeddings

Retrieves similar code chunks via FAISSIndexer

Sends the diff and context to the LLMReviewer

GitHub Client
Posts aggregated findings back to GitHub, ensuring only new and unique comments are published.

Installation
Prerequisites

Python 3.9+

A GitHub account and repository

Google Gemini API key

Setup Steps
1. Clone the Repository
git clone https://github.com/rishabh766/code-review-bot.git
cd code-review-bot

2. Create a Virtual Environment
python -m venv venv
source venv/bin/activate
# On Windows: venv\Scripts\activate

3. Install Dependencies
pip install -r requirements.txt

Environment Configuration

Create a .env file in the root directory:

# GitHub Configuration
GITHUB_TOKEN=your_github_pat_token
GITHUB_WEBHOOK_SECRET=your_webhook_secret

# AI Configuration
GEMINI_API_KEY=your_google_gemini_api_key

Usage
Running the Server

Start the FastAPI server using Uvicorn:

uvicorn app.main:app --reload


The server will be available at:

http://127.0.0.1:8000

Configuring the GitHub Webhook
1. Expose Local Server
ngrok http 8000

2. GitHub Webhook Setup

Go to:

Repository Settings → Webhooks → Add webhook


Configure:

Payload URL

https://your-url.ngrok.io/webhook


Content type: application/json

Secret: Same value as GITHUB_WEBHOOK_SECRET

Events: Pull requests

Testing

You can test individual components using the provided scripts.

Test Static Analysis Tools
python test_analysis.py

Test LLM Connection
python test_llm.py

Simulate Webhook Event
python debug_webhook.py

Project Structure
app/
├── analysis/     # Wrappers for static analysis tools (Ruff, Bandit)
├── github/       # GitHub API client and diff parsing logic
├── llm/          # Prompts and Gemini model interface
├── rag/          # Embedding, indexing, and FAISS retrieval logic
├── storage/      # Database models and deduplication logic
└── main.py       # Application entry point
