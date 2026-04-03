***

# 🤖 Code Review Bot

A comprehensive, automated code review assistant designed to integrate directly with GitHub Pull Requests. This bot acts as intelligent middleware, combining the speed and deterministic precision of static analysis tools with the context-aware reasoning of Large Language Models (LLMs) to catch bugs, security vulnerabilities, and maintainability issues.

## 🌟 Key Features

* **Hybrid Analysis Engine:**
    * **Ruff:** Lightning-fast Python linting and code formatting checks (targets `E` and `F` rules).
    * **Bandit:** Security-focused static analysis to detect common Python vulnerabilities.
    * *(Extensible)* **Semgrep:** Ready-to-use module included for deeper security rule analysis.
* **AI-Powered Reasoning (Google Gemini):**
    * Utilizes `gemini-2.5-flash` (with fallback to `gemini-pro`) to detect logic bugs, evaluate code maintainability, and suggest complex refactoring.
    * Outputs specific, actionable findings mapped directly to the diff.
* **Context-Aware Reviews via RAG:**
    * Uses **Google Gemini Embeddings** (`text-embedding-004`) and **FAISS** vector storage to index repository files.
    * Ensures LLM suggestions are grounded in your actual codebase, understanding project-specific utilities, and configuration patterns rather than reviewing isolated snippets.
* **Smart Deduplication:**
    * Local **SQLite** database (`bot_memory.db`) generates SHA-256 fingerprint hashes for every comment.
    * Prevents spam by ensuring the bot never posts the exact same comment on the same line across multiple commits.
* **Seamless GitHub Integration:**
    * Automated HMAC-secured Webhook handling (via FastAPI).
    * Smart Diff Parsing: Automatically ignores generated code, locked files, and migrations (`venv/`, `node_modules/`, `.lock`, etc.).
    * Posts inline batch reviews and comprehensive summary reports directly to the Pull Request.

---

## 🏗 Architecture & Workflow

1.  **Event Trigger:** A GitHub Webhook fires when a PR is opened or synchronized.
2.  **Fetch & Filter:** `GitHubClient` fetches the PR diff. `DiffParser` extracts valid Python files.
3.  **Static Analysis:** `RuffRunner` and `BanditRunner` scan the target files locally.
4.  **RAG Indexing:** `FAISSIndexer` embeds repository context using Gemini, and `Retriever` fetches the most relevant code chunks for the current diff.
5.  **LLM Review:** The diff and the retrieved context are passed to `LLMReviewer` (Gemini) using a strict JSON-enforced system prompt.
6.  **Aggregation & Deduplication:** `Aggregator` combines static and LLM findings. `Deduplicator` filters out previously posted comments.
7.  **Action:** Inline comments and a high-level summary report are posted to GitHub via the REST API.

---

## 🚀 Getting Started

### Prerequisites

* **Python:** 3.11+ (See `runtime.txt`)
* **GitHub Account:** A Personal Access Token (PAT) with `repo` scopes.
* **Google Gemini API Key:** For embeddings and LLM generation.

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/code-review-bot.git
cd code-review-bot
```

### 2. Environment Setup
Create a virtual environment and install the dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### 3. Configuration
Create a `.env` file in the root directory and populate it with your credentials:
```env
# GitHub Configuration
GITHUB_TOKEN=your_github_pat_token
GITHUB_WEBHOOK_SECRET=your_webhook_secret_string

# AI Configuration
GEMINI_API_KEY=your_google_gemini_api_key
```

### 4. Run the Server
Start the FastAPI server. The background deduplication database (`bot_memory.db`) will initialize automatically.
```bash
uvicorn app.main:app --reload
```
The server will be available at `http://127.0.0.1:8000`.

---

## 🔗 Connecting to GitHub

To receive webhooks locally, you must expose your local server to the internet using a tool like [ngrok](https://ngrok.com/).

1. **Expose the port:**
   ```bash
   ngrok http 8000
   ```
2. **Configure the Webhook in GitHub:**
   * Navigate to your target repository: **Settings → Webhooks → Add webhook**
   * **Payload URL:** `https://<your-ngrok-url>.ngrok.app/webhook`
   * **Content type:** `application/json`
   * **Secret:** The exact value of your `GITHUB_WEBHOOK_SECRET`
   * **Events:** Select "Let me select individual events" -> Check **Pull requests**.

---

## 📂 Project Structure

```text
code-review-bot/
├── app/
│   ├── analysis/       # Static analysis runners (Ruff, Bandit, Semgrep, Aggregator)
│   ├── github/         # GH API client, webhook handler (FastAPI), Diff parser
│   ├── llm/            # Gemini generative model integration and system prompts
│   ├── rag/            # FAISS indexing, Gemini embeddings, and context retrieval
│   ├── storage/        # SQLite DB init, Deduplication logic, Pydantic models
│   └── main.py         # FastAPI application entry point
├── bad_code.py         # Sample file for testing tools
├── check_models.py     # Script to verify available Gemini models
├── debug_webhook.py    # Script to simulate GitHub webhook payloads locally
├── test_*.py           # Modular testing scripts for LLM, Aggregator, Parser, etc.
├── requirements.txt    # Python dependencies
└── .env                # Environment variables (not tracked)
```

---

## 🧪 Testing and Debugging

The repository includes several modular test scripts to verify components without triggering full webhooks:

* **Test Static Analysis:** Runs Ruff and Bandit against `bad_code.py`.
    ```bash
    python test_analysis.py
    ```
* **Test Diff Parsing:** Verifies the file filtering logic (ignoring migrations, locks, etc.).
    ```bash
    python test_parser.py
    ```
* **Test LLM Connection:** Sends a mock diff to Gemini to verify JSON formatting and response.
    ```bash
    python test_llm.py
    ```
* **Simulate Webhook Event:** Bypasses GitHub and sends a mock HMAC-signed payload to your local FastAPI server.
    ```bash
    python debug_webhook.py
    ```

---

## 🛠 Extensibility

* **Adding New Tools:** Create a new runner class in `app/analysis/` that returns a list of `Finding` Pydantic models, then register it in `app/analysis/aggregator.py`.
* **Customizing the AI:** You can adjust the LLM persona, strictness, and output format by editing `app/llm/prompts.py`.
