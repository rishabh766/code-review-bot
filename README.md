Code Review Bot
A comprehensive, automated code review assistant designed to integrate directly with GitHub Pull Requests. This bot combines deterministic static analysis tools with context-aware Large Language Models (LLMs) to catch bugs, security vulnerabilities, and style issues.

Overview
The Code Review Bot acts as an intelligent middleware between your GitHub repository and code analysis tools. When a Pull Request is opened or updated, the bot automatically fetches the changes, runs a suite of analysis tools, and posts actionable feedback directly to the PR as inline comments and a summary report.

It leverages Retrieval-Augmented Generation (RAG) to provide the LLM with relevant repository context, ensuring that AI-generated suggestions are grounded in the actual codebase rather than isolated snippets.

Key Features
Hybrid Analysis Engine: Combines the precision of static linters with the reasoning capabilities of LLMs.

Ruff: Extremely fast Python linting and code formatting checks.

Bandit: Security-focused static analysis to find common vulnerabilities.

Gemini (LLM): AI-powered review for logic bugs, maintainability, and complex refactoring suggestions.

Context-Aware Reviews (RAG): Uses FAISS vector storage to index repository files, allowing the LLM to understand project-specific utilities and configuration patterns.

Smart Deduplication: Tracks posted comments in a local SQLite database to prevent spamming the same issues across multiple commits.

GitHub Integration:

Automated webhook handling.

Inline comments for specific lines of code.

Summary reports for high-level feedback.

Configurable: Easily extensible architecture for adding new analysis tools.

Architecture
The system is built with FastAPI and follows a modular design:

Webhook Handler: Listens for GitHub pull_request events.

Diff Parser: identifying valid Python files and filtering out generated code or migrations.

Aggregator: Orchestrates the review workflow:

Executes RuffRunner and BanditRunner.

Embeds code context using GeminiEmbeddings.

Retrieves similar code chunks via FAISSIndexer.

Sends the diff and context to the LLMReviewer.

GitHub Client: Posts the aggregated findings back to GitHub, ensuring only new, unique comments are published.

Installation
Prerequisites
Python 3.9+

A GitHub Account and Repository

Google Gemini API Key

Setup Steps
Clone the Repository

Bash

git clone https://github.com/rishabh766/code-review-bot.git
cd code-review-bot
Create a Virtual Environment

Bash

python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
Install Dependencies

Bash

pip install -r requirements.txt
Environment Configuration Create a .env file in the root directory with the following variables:

Ini, TOML

# GitHub Configuration
GITHUB_TOKEN=your_github_pat_token
GITHUB_WEBHOOK_SECRET=your_webhook_secret

# AI Configuration
GEMINI_API_KEY=your_google_gemini_api_key
Usage
Running the Server
Start the FastAPI server using Uvicorn:

Bash

uvicorn app.main:app --reload
The server will start at http://127.0.0.1:8000.

Configuring the Webhook
Expose your local server to the internet (e.g., using ngrok):

Bash

ngrok http 8000
Go to your GitHub Repository Settings > Webhooks > Add webhook.

Set the Payload URL to your ngrok URL + /webhook (e.g., https://your-url.ngrok.io/webhook).

Set Content type to application/json.

Set the Secret to match the GITHUB_WEBHOOK_SECRET in your .env file.

Select specific events: Pull requests.

Testing
You can verify the components individually using the provided test scripts:

Test Analysis Tools:

Bash

python test_analysis.py
Test LLM Connection:

Bash

python test_llm.py
Simulate Webhook Event:

Bash

python debug_webhook.py
Project Structure
app/analysis/: wrappers for static analysis tools (Ruff, Bandit).

app/github/: GitHub API client and diff parsing logic.

app/llm/: Prompts and interface for the Gemini model.

app/rag/: Embedding, indexing, and retrieval logic using FAISS.

app/storage/: Database models and deduplication logic.

app/main.py: Application entry point.
