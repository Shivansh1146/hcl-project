# ⚡ AI-Powered Pull Request Code Review Assistant

A production-grade, full-stack application that intercepts GitHub Pull Request payloads (Webhooks) in real-time, extracts the exact code that was changed, uses artificial intelligence (OpenAI `gpt-4o-mini`) to detect bugs and security flaws, and dynamically comments the fixes directly onto the specific lines natively in the GitHub PR.

---

## 🏗️ Core System Architecture
- **Backend Network**: Python + FastAPI
- **Frontend Panel**: HTML + CSS (Inter Font) + Vanilla Javascript Web Form
- **AI Engine**: OpenAI API (`gpt-4o-mini`)
- **Integration Layer**: GitHub REST API (Webhooks & Comments)

---

## ⚙️ The 10-Stage Pipeline Engine (`main.py`)
The entire webhook pipeline executes exactly like this upon a GitHub `POST`:
1. **Payload Capture**: Validates standard JSON payload & ensures action is strictly `opened` or `synchronize`.
2. **Action Validation**: Explicitly ignores spam events (like PRs closing).
3. **Commit Hashing & Deduplication**: Extracts `payload["pull_request"]["head"]["sha"]` and checks an internal highly-performant Python `Set()` to prevent duplicate AI triggers.
4. **Git Diff Extraction**: Reaches into GitHub securely to pull only the changed patches of code (`fetch_diff()`), bailing cleanly if empty.
5. **AI Dispatching**: Fires the Raw Diff string securely into `analyze_code()` via OpenAI.
6. **Smart Filtering**: Triggers `parse_and_filter_issues()` to grade and drop false positives.
7. **Clean Exit Logic**: Compiles surviving issues into structured GitHub Markdown. If no issues survive, it halts operations quietly rather than spamming empty comments.
8. **Markdown Formatting**: Executes markdown templates via `format_inline_issue()`.
9. **Inline Output Execution**: Pings the GitHub API in a loop targeting the distinct `commit_sha` and referencing the `path` and `line` mapped dynamically inside the AI response.
10. **Error Catching**: Implements a Try-Catch fallback. If GitHub kicks back a `422 Unprocessable Entity` (Because AI guessed an invalid line number), it catches the crash and seamlessly drops the issue inside the main PR thread instead of failing!

---

## 🧠 The AI Brain & Diff Chunking (`ai_service.py`)
Transforming standard OpenAI generation into a **Hardened Senior Security Engine**:
- **Persona Lock**: Prompt strictly locks OpenAI into analyzing code under the persona of a *Senior Security Engineer*. This prevents it from nitpicking spelling errors.
- **Chunking Matrix**: Massive pull requests crush context sizes. If a diff exceeds `8000` chars, it natively slices the diff into exact blocks of `4000` executing the AI function repeatedly.
- **Semantic Deduplication**: Because chunking processing isolation produces duplicates, we execute `_is_similar()` on descriptions—which translates spaces to lowercase, mathematically deletes punctuation, isolates root subset components (ignoring stop words like 'and, are, on, of, for'), and guarantees identical issues from chunks are collapsed together into one dictionary!
- **Retry Safety**: Wraps the OpenAI SDK call in `_analyze_chunk_with_retry`. Max 3 attempts allowing automatic 1-second interval resets upon connection drops.
- **Strict JSON Targeting**: AI must return valid JSON forcing: `type` (bug|security|performance), `severity` (high|medium|low), `file` (from patch headers), and a physical `line` integer prediction.

---

## 🛡️ Heuristics Filtration Control (`filter_service.py`)
LLMs hallucinate stylistic junk. To kill this, every AI response triggers a mathematical scoring phase:
- Initial Score = `0`
- `+2` Points if severity string equates to `high`.
- `+1` Point if string length spans longer than 30 characters minimizing vague spam.
- `-2` Points if descriptions utilize weak vocabulary arrays `['improve', 'optimize', 'better', 'clean']`.
- Drops any JSON object if score results in `< 1`. Pure signal, zero noise.

---

## 🛠️ Quick Start Guide

### 1. Set Up Your Environment
Launch your terminal and create a `.env` file within the `backend/` directory harboring your valid secret credentials:
```env
OPENAI_API_KEY=sk-...
GITHUB_TOKEN=ghp_...
```

### 2. Install Dependencies
Initialize a sterile virtual environment and install the FastAPI tracking requirements.
```powershell
python -m venv venv
.\venv\Scripts\activate
cd backend
pip install -r requirements.txt
```

### 3. Spin Up the FastAPI Backend
Initialize the standard backend gateway pipeline natively:
```powershell
python -m uvicorn main:app --reload --port 8001
```

### 4. Enable Webhook Routing
To permit GitHub to push webhook events directly into your locally running machine, spin up localtunnel:
```powershell
npx -y localtunnel --port 8001
```

## 🔌 Securing the GitHub Integration
1. Copy the `localtunnel` URL dynamically generated (e.g., `https://shaky-doodles-kneel.loca.lt`).
2. Navigate to your target **GitHub Repository** -> **Settings** -> **Webhooks** -> **Add webhook**.
3. Set **Payload URL** to `https://<YOUR_URL>.loca.lt/webhook`.
4. Set **Content type** to `application/json`.
5. Under triggers, click **"Let me select individual events"**, actively check **Pull requests**, and click **Save**.

## 🔥 Validation Testing
Ready to watch it work? Open a new Git branch and introduce critical (simulated) failures to any file:
```python
password = "123456"
query = "SELECT * FROM users WHERE id=" + user_input
```
Open a Pull Request into your tracker, and your assistant will instantaneously parse the event payload, flag the malicious logic, and securely execute an inline comment directly onto the vulnerable lines requiring remediation!
