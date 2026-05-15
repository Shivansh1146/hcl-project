# HCL Project - End to End Context

This document contains the end-to-end source code and configuration for the HCL Project (AI Pull Request Reviewer). You can provide this to an LLM to give it full context of the repository.

## File: README.md

`markdown
# ⚡ AI-Powered Pull Request Code Review Assistant (HCL Project)

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Groq](https://img.shields.io/badge/Groq_AI-F4AF38?style=for-the-badge)
![Render](https://img.shields.io/badge/Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)

The **HCL Project** is a production-grade, AI-powered GitHub Pull Request Reviewer designed for high-fidelity security analysis and deterministic code verification. Built with a "Zero-Noise" philosophy, it empowers teams with automated, committable suggestions while maintaining a rigorous security posture.

---

## ✨ Production-Grade Features

- **🛡️ Iron-Clad Deterministic Engine**: Multi-layered filtering that rejects LLM hallucinations (e.g., binary search logic errors) and ensures multi-layer validated suggestions.
- **🛡️ Content Guard & Syntax Guard**: Permanent protection that prevents the AI from suggesting changes to comments, docstrings, or structural keywords. Any malformed code suggestion is automatically discarded.
- **💎 PERFECT Status Mapping**: Flawless code is recognized as **"ZERO RISK • VERIFIED,"** triggering an automatic success status (Green Checkmark) on GitHub.
- **🧪 Stability Stop (Fingerprinting)**: Prevents redundant reports by tracking issue fingerprints across commits, ensuring the dashboard remains clean and focused.
- **📊 Real-Time Glassmorphism Dashboard**: A premium, state-aware Command Center with live telemetry, spectral severity metrics, and instant decision intelligence.
- **⚡ One-Click Fixes**: Automatically posts native ````suggestion` syntax to GitHub, allowing developers to apply fixes directly from the PR interface.

---

## 🏗️ Technical Architecture

| Layer | Technology | Purpose |
|---|---|---|
| **Cloud Hosting** | Render (Blueprint) | Automated CI/CD deployment with dynamic port binding and persistent state. |
| **Backend** | FastAPI (Python 3.11) | High-performance, asynchronous orchestration engine. |
| **AI Engine** | Groq (LLaMA 3.3 70B) | Security-focused analysis with deterministic temperature (0.1). |
| **Hardening** | `filter_service.py` | Literal blacklist and structural guards for iron-clad reliability. |
| **Persistence** | SQLite (`reviews.db`) | Atomic state tracking with WAL mode for concurrency control. |
| **Dashboard** | Vanilla CSS/JS | Minimalist, high-performance UI with real-time state synchronization. |

---

## 🚀 Cloud Deployment (Render)

1. Connect this repository to **Render** via the dashboard.
2. Render will automatically detect the `render.yaml` blueprint.
3. Configure the following **Environment Variables**:
   - `GITHUB_TOKEN`: Your GitHub Personal Access Token.
   - `GROQ_API_KEY`: Your Groq API Key.
   - `WEBHOOK_SECRET`: Your custom webhook secret.
4. The system will deploy automatically and provide a public URL.

---

## 🛠️ Local Setup & Development

### 1. Installation
```bash
git clone https://github.com/Shivansh1146/hcl-project
cd "HCL Project"
python -m venv .venv

# Windows
.\.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate

cd backend
pip install -r requirements.txt
```

### 2. Configure Environment
Create `backend/.env`:
```env
GROQ_API_KEY=gsk_...
GITHUB_TOKEN=ghp_...
WEBHOOK_SECRET=your_secret
PORT=8000
```

### 3. Launching the System
```bash
cd backend
python -m uvicorn main:app --reload --port 8000
```

---

## 🐳 Docker Orchestration

### 1. Build and Run
```bash
# Start with persistence and auto-restart
docker-compose up --build -d
```

### 2. Monitoring & Persistence
- **Logs**: View real-time output with `docker-compose logs -f`.
- **Database**: The `reviews.db` is mounted as a volume, ensuring data survives restarts.
- **Dashboard**: Accessible at `http://localhost:8000`.

---

## 📁 Project Structure

```
HCL Project/
├── render.yaml                  # Automated Cloud Deployment Blueprint
├── Dockerfile                   # Hardened Production Image Config
├── docker-compose.yml           # Local Orchestration & Persistence
├── backend/
│   ├── main.py                  # Webhook Pipeline & Decision Intelligence
│   ├── stats_store.py           # Atomic Telemetry Engine
│   ├── static/index.html        # Glassmorphism Command Center UI
│   └── services/
│       ├── ai_service.py        # Groq LLaMA Engine + Hardening Guards
│       ├── diff_validator.py    # Diff Parsing & Line Mapping
│       ├── filter_service.py    # Iron-Clad Logic & Content Guards
│       ├── github_service.py    # GitHub API Integration & Rate Limiting
│       ├── syntax_validator.py  # Local Code-Correctness Verification
│       └── validator.py         # Anti-Hallucination Cross-Checker
```

---

## 🔐 Security & Safety Notes

- **Secrets**: All API keys are stored in `.env` and are strictly excluded from version control.
- **Non-Destructive**: The AI is programmed to never delete code blocks; it only suggests surgical line-level fixes.
- **Fail-Safe**: If the AI engine is unreachable or returns malformed data, the system defaults to `REVIEW_REQUIRED` to prevent unsafe approvals.

---

## 👤 Author

**Shivansh**
- GitHub: [Shivansh1146](https://github.com/Shivansh1146)
- Project: [HCL AI Code Reviewer](https://github.com/Shivansh1146/hcl-project)

---

*Built with Python · FastAPI · Groq · GitHub REST API · Optimized for Production*

`

## File: docker-compose.yml

`yaml
version: '3.8'

services:
  ai-reviewer:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    env_file:
      - ./backend/.env
    volumes:
      - ./backend/reviews.db:/app/reviews.db
    restart: always

`

## File: render.yaml

`yaml
services:
  - type: web
    name: hcl-ai-reviewer
    env: python
    buildCommand: pip install -r backend/requirements.txt
    startCommand: cd backend && gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:$PORT
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.8
      - key: GITHUB_TOKEN
        sync: false # Set this in Render Dashboard
      - key: GROQ_API_KEY
        sync: false # Set this in Render Dashboard
      - key: WEBHOOK_SECRET
        sync: false # Set this in Render Dashboard
      - key: PORT
        value: 8000

`

## File: backend/main.py

`python
import asyncio
import logging
import os
from typing import List, Dict, Any, Optional

from fastapi import FastAPI, Request, BackgroundTasks, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from services.github_service import fetch_diff, post_comment, post_inline_comment, post_status
from services.ai_service import get_ai_service
from services.diff_validator import DiffValidator
from services.syntax_validator import SyntaxValidator
from services.filter_service import parse_and_filter_issues
from services.validator import AntiHallucinationValidator
from stats_store import initialize_db, get_stats, record_review, finalize_review, claim_sha_for_processing, is_sha_processed, mark_sha_status, upsert_review
import stats_store

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("backend")

app = FastAPI(title="AI PR Reviewer")

# Mount static files for the dashboard
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def serve_dashboard():
    return FileResponse("static/index.html")

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "bot": "online", "database": "connected"}

# AI Analysis Semaphore to prevent Groq API overload (Max 5 concurrent)
analysis_semaphore = asyncio.BoundedSemaphore(5)

@app.on_event("startup")
async def startup():
    await initialize_db()

def compute_decision(high, medium, low, total_chunks, processed_chunks, error=False):
    """Business Logic for PR Decision Engine."""
    # CRITICAL: Any High vulnerability results in immediate BLOCK
    if high > 0:
        return "BLOCK"

    # FAIL-FAST: System error triggers BLOCK
    if error:
        return "BLOCK"
    
    # Confidence/Coverage Level
    confidence = processed_chunks / total_chunks if total_chunks > 0 else 1.0

    # HONESTY: Absolute rule - partial analysis is NEVER "SAFE" (Requirement 5)
    if processed_chunks < total_chunks:
        return "REVIEW_REQUIRED"


    # Fully analyzed logic
    if medium >= 3:
        return "REVIEW_REQUIRED"

    # PERFECT: Fully processed with ZERO issues
    if high == 0 and medium == 0 and low == 0:
        return "PERFECT"

    # SAFE: Fully processed with minimal issues
    return "SAFE"


async def process_webhook(payload: dict):
    """Production-grade fail-safe pipeline with guaranteed finalization."""
    head_sha = payload.get("pull_request", {}).get("head", {}).get("sha")
    repo_full_name = payload.get("repository", {}).get("full_name", "unknown/repo")
    pr_number = payload.get("pull_request", {}).get("number")

    # Internal state for finalization recovery
    pr_id = None
    final_status = "success"
    decision = "BLOCK"
    valid_issues = []
    total_chunks = 0
    processed_chunks = 0
    owner = repo = None
    analysis = None

    async with analysis_semaphore:
        if not await stats_store.claim_sha_for_processing(head_sha):
            logger.info(f"🛑 [process_webhook] SHA {head_sha} skip: already actively processing or completed.")
            return

        try:
            repo_full_name = payload.get("repository", {}).get("full_name", "unknown/repo")
            owner, repo = repo_full_name.split("/") if "/" in repo_full_name else ("unknown", "repo")
            # Step 0 — Mark Pending Status on GitHub
            await post_status(owner, repo, head_sha, "pending", "AI is analyzing your code...")

            logger.info(f"🚀 [Production] Starting PR #{pr_number} | SHA: {head_sha}")

            pr_id = await stats_store.upsert_review(repo, pr_number, status="processing")

            # Step 1 — Fetch Diff
            diff = payload.get("diff")
            if diff is None:
                diff = await fetch_diff(owner, repo, pr_number)
            
            if diff is None:
                raise ValueError("Failed to fetch diff from GitHub API (Network or Rate Limit error).")

            if not diff:
                total_chunks = 0
                processed_chunks = 0
                final_status = "success"
                decision = compute_decision(0, 0, 0, 0, 0, error=False)
                logger.info(f"⏭️ PR #{pr_number} has no code changes — marking SAFE.")
            else:
                # Step 2 — AI Analysis
                ai_service = get_ai_service()
                
                async def update_progress(p, t):
                    await stats_store.update_review_progress(pr_id, p, t)
                
                analysis = await ai_service.analyze_code(diff, progress_callback=update_progress)
                total_chunks = analysis.get("total_chunks", 1)
                processed_chunks = analysis.get("processed_chunks", 0)

                if analysis.get("status") == "failed":
                    if analysis.get("reason") == "RATE_LIMIT":
                        logger.warning(f"⚠️ [RATE LIMIT] PR #{pr_number} skipped AI due to API exhaustion.")
                        final_status = "skipped"
                        decision = "ANALYSIS_INCOMPLETE"
                    else:
                        raise ValueError(f"Stage Failed: AI Analysis — {analysis.get('reason')}")

                # Step 3 — Validate chunks
                if processed_chunks < total_chunks and final_status not in ("skipped", "error"):
                    logger.error(f"⚠️ Partial processing: {processed_chunks}/{total_chunks} chunks OK.")
                    final_status = "partial"
                
                if final_status not in ("skipped", "error"):
                    final_status = analysis.get("status", "success")
                    decision = "SAFE" # Initial assumption before issue counting
                    # Step 4 — Validation & Filtering
                    # [STRICT 3-LAYER FILTERING]
                    raw_issues = analysis.get("issues", [])
                    raw_issues = parse_and_filter_issues({"issues": raw_issues}, diff)
                    
                    diff_mapping = DiffValidator.parse_diff_mapping(diff)

                    # Step 5 — Syntax check, Deduplication & Split Logic (Requirement 7)
                    # Rule 2: Stable Deduplication (file:line:title)
                    seen_fingerprints = set()
                    final_valid_issues = []
                    
                    for i in raw_issues:
                        try:
                            line_num = int(i.get("line", 0))
                        except (ValueError, TypeError):
                            line_num = 0
                        i["line"] = line_num 

                        # Fingerprint check using title (Stability Rule 2)
                        issue_fingerprint = f"{i.get('file')}:{line_num}:{i.get('title')}"
                        if issue_fingerprint in seen_fingerprints:
                            continue
                        seen_fingerprints.add(issue_fingerprint)
                        
                        # 🔍 Auto-Correct line mapping
                        AntiHallucinationValidator.auto_correct_line_mapping(i, diff_mapping.get(i.get("file", ""), {}))

                        if line_num > 0:
                            if not DiffValidator.validate_issue(i, diff_mapping):
                                continue
                            
                            # 🛡️ CONTENT GUARD: Never replace comments or keywords with logic
                            file_key = i.get("file", "")
                            if file_key in diff_mapping and line_num in diff_mapping[file_key]:
                                old_content, _ = diff_mapping[file_key][line_num]
                                old_clean = old_content.strip()
                                if old_clean.startswith("#") or old_clean in ["else:", "elif:", "while:", "if"]:
                                    logger.info(f"🛡️ [CONTENT GUARD] Blocked attempt to replace '{old_clean}' with logic.")
                                    continue
                        
                        # Syntax check (🛡️ HARDENED: Drop syntax errors completely)
                        if not SyntaxValidator.validate_issue(i):
                            logger.info(f"🚫 [SYNTAX GUARD] Dropped malformed suggestion for {file_key}:{line_num}")
                            continue

                        final_valid_issues.append(i)

                    # Rule 3: Stability Stop (MOST IMPORTANT)
                    # Get existing issues from DB to see if we've already reported exactly these
                    existing_issues = await stats_store.get_issues_for_pr(pr_number)
                    existing_fingerprints = {f"{iss['file']}:{iss['line']}:{iss['title']}" for iss in existing_issues}
                    new_fingerprints = {f"{iss['file']}:{iss['line']}:{iss['title']}" for iss in final_valid_issues}

                    if existing_fingerprints == new_fingerprints and len(new_fingerprints) > 0:
                        logger.info(f"⚖️ [Stability Stop] No new issues for PR #{pr_number}. Stopping redundant analysis.")
                        valid_issues = [] # Clear to prevent re-posting
                    else:
                        valid_issues = final_valid_issues


                    high_count = sum(1 for i in valid_issues if str(i.get("severity", "")).lower() == "high")
                    med_count  = sum(1 for i in valid_issues if str(i.get("severity", "")).lower() == "medium")
                    low_count  = sum(1 for i in valid_issues if str(i.get("severity", "")).lower() == "low")

                    rule_based_count = analysis.get("rule_based_count", 0)
                    
                    # Apply Confidence Kill Switch from AI Service or based on counts
                    decision = analysis.get("decision_status", "SAFE")
                    if decision == "SAFE":
                        decision = compute_decision(high_count, med_count, low_count, total_chunks, processed_chunks)
                    
                    # Deterministic Override: Static scanner beats AI
                    if rule_based_count > 0:
                        logger.warning(f"🛡️ RULE OVERRIDE: {rule_based_count} static risks found. Forcing BLOCK.")
                        decision = "BLOCK"
                    
                    if decision == "SAFE" and rule_based_count > 0:
                        logger.warning("🚨 [DISAGREEMENT] AI suggested SAFE but Rule Guard found critical risks.")

                    # Architecture Check: Detect "Suspicious SAFE" (Large diff but 0 issues)
                    if processed_chunks > 0 and len(valid_issues) == 0 and len(diff) > 5000:
                        logger.warning(f"🚨 [AI EMPTY] AI suggested SAFE with 0 issues on large diff ({len(diff)} chars).")

                    # Step 6 — Split Comment Strategy
                    all_comments_posted = True
                    global_issues = [i for i in valid_issues if i.get("line") == 0]
                    inline_issues = [i for i in valid_issues if i.get("line", 0) > 0]

                    failed_inline_count = 0
                    for issue in inline_issues:
                        suggestion = DiffValidator.generate_suggestion(issue, diff_mapping)
                        success = await post_inline_comment(owner, repo, pr_number, issue, head_sha, suggestion=suggestion)
                        if not success:
                            all_comments_posted = False
                            failed_inline_count += 1

                    # Reliability Fallback / Summary Comment
                    if global_issues or failed_inline_count > 0 or decision != "SAFE" or processed_chunks < total_chunks:
                        coverage_pct = int((processed_chunks/total_chunks)*100) if total_chunks > 0 else 100
                        if processed_chunks > 0 and coverage_pct == 0: coverage_pct = 1
                        
                        summary_lines = [
                            f"### 🤖 AI Code Review Summary — Decision: **{decision}**",
                            f"**Coverage:** {coverage_pct}% of diff analyzed."
                        ]
                        
                        if coverage_pct < 10:
                            summary_lines.insert(1, "🚨 **CRITICAL: EXTREMELY LOW COVERAGE**")
                            summary_lines.insert(2, "Only a tiny fraction of this large PR was analyzed due to safety/rate limits. **Manual review is mandatory for the remaining sections.**")

                        if processed_chunks < total_chunks:
                            summary_lines.append("⚠️ **Analysis Incomplete**")
                            
                            file_cov = analysis.get("file_coverage", {})
                            if file_cov:
                                summary_lines.append("\n#### 📂 File Coverage Status:")
                                for f, status in list(file_cov.items())[:10]: # Cap at 10 for readability
                                    icon = "✅" if status == "FULLY_ANALYZED" else "⚠️" if status == "PARTIAL" else "🚫"
                                    summary_lines.append(f"- {icon} `{f}`: {status.replace('_', ' ')}")
                                if len(file_cov) > 10:
                                    summary_lines.append(f"- ... and {len(file_cov)-10} more files.")
                            
                            summary_lines.append("\n**Manual review is required for the incomplete sections.**")
                        else:
                            summary_lines.append(f"**Status:** {high_count} High, {med_count} Medium, {low_count} Low severity issues identified.")
                            summary_lines.append("")

                        if global_issues:
                            summary_lines.append("#### 🌐 General / Architecture Feedback")
                            for g in global_issues:
                                summary_lines.append(f"- **[{g['severity']}] {g['title']}**: {g['description']}")
                            summary_lines.append("")

                        if failed_inline_count > 0:
                            summary_lines.append(f"⚠️ **Note:** {failed_inline_count} inline suggestions could not be rendered (likely mapping errors). Check the dashboard for full details.")

                        summary_body = "\n".join(summary_lines)
                        try:
                            posted = await post_comment(owner, repo, pr_number, summary_body)
                            if not posted:
                                raise ValueError("GitHub rejected the summary comment.")
                        except Exception as e:
                            logger.error(f"CRITICAL: Final fallback (summary comment) failed: {str(e)}")
                            # If we reached here, both inline and summary failed -> trigger Fail-Safe BLOCK
                            raise ValueError("Critical action failure: Both inline and summary comments failed.") from e

                    logger.info("✅ Pipeline reached finalization point.")
                    if final_status not in ("partial", "skipped"):
                        final_status = "success"

        except Exception as e:
            logger.critical(f"🔥 Fail-Safe Triggered: {str(e)}", exc_info=True)
            final_status = "error"
            decision = "BLOCK"

        finally:
            if pr_id is not None:
                high_count = sum(1 for i in valid_issues if str(i.get("severity", "")).lower() == "high")
                med_count  = sum(1 for i in valid_issues if str(i.get("severity", "")).lower() == "medium")
                low_count  = sum(1 for i in valid_issues if str(i.get("severity", "")).lower() == "low")
                await stats_store.finalize_review(
                    pr_id, valid_issues,
                    status=final_status,
                    decision_status=decision,
                    high=high_count,
                    medium=med_count,
                    low=low_count,
                    total_chunks=total_chunks,
                    processed_chunks=processed_chunks
                )

            if head_sha:
                await stats_store.mark_sha_status(head_sha, "completed" if final_status == "success" else "failed")
                if owner and repo:
                    status_state = "success" if decision in ("SAFE", "PERFECT") else "failure"
                    if final_status == "error": status_state = "error"
                    status_desc = f"Review: {decision}. Found {len(valid_issues)} issues."
                    await post_status(owner, repo, head_sha, status_state, status_desc)

            logger.info(f"🏁 [Webhook Finalized] PR={pr_number} Status={final_status} Decision={decision} Issues={len(valid_issues)}")

@app.post("/webhook")
async def webhook(request: Request, background_tasks: BackgroundTasks):
    payload = await request.json()
    action = payload.get("action")
    if action not in ("opened", "synchronize", "reopened"):
        return {"status": "ignored", "reason": "UNSUPPORTED_ACTION"}
    head_sha = payload.get("pull_request", {}).get("head", {}).get("sha")
    if not head_sha: return {"status": "error", "reason": "MISSING_SHA"}
    if await stats_store.is_sha_processed(head_sha):
        return {"status": "ignored", "reason": "ALREADY_PROCESSED"}
    background_tasks.add_task(process_webhook, payload)
    return {"status": "processing", "sha": head_sha}

@app.get("/api/stats")
async def api_stats():
    return await get_stats()

`

## File: backend/stats_store.py

`python
import aiosqlite
import asyncio
import logging
import os
from datetime import datetime, timedelta, timezone
from contextlib import asynccontextmanager

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.environ.get("TEST_DB_PATH") or os.path.join(BASE_DIR, "reviews.db")
logger = logging.getLogger("backend")

# Global connection removed to prevent transaction bleeding
@asynccontextmanager
async def get_db():
    """Returns a new, dedicated database connection per task."""
    db = await aiosqlite.connect(DB_PATH, timeout=30.0)
    db.row_factory = aiosqlite.Row
    await db.execute("PRAGMA journal_mode=WAL")
    await db.execute("PRAGMA synchronous=NORMAL")
    try:
        yield db
    finally:
        await db.close()

async def db_retry(func, *args, retries=3, delay=1, **kwargs):
    """Wrapper to retry database operations on failure."""
    for attempt in range(retries):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            if attempt == retries - 1:
                logger.error(f"Database operation failed after {retries} attempts: {str(e)}")
                raise
            await asyncio.sleep(delay * (attempt + 1))

async def close_db():
    """No-op for backward compatibility."""
    pass

async def initialize_db():
    """Initializes the SQLite database with schema versioning and migrations."""
    async with get_db() as db:
        # 1. Base Tables
        await db.execute('''
            CREATE TABLE IF NOT EXISTS prs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                repo TEXT,
                pr_number INTEGER,
                reviewed_at TEXT,
                status TEXT DEFAULT 'success'
            )
        ''')
        # Backward compatibility migration: add decision columns for older DBs.
        async with db.execute("PRAGMA table_info(prs)") as cursor:
            prs_columns = [row[1] for row in await cursor.fetchall()]

        # Ensure all required decision columns exist with safe defaults
        required_columns = {
            "status": "TEXT DEFAULT 'error'",
            "decision_status": "TEXT DEFAULT 'BLOCK'",
            "high_count": "INTEGER DEFAULT 0",
            "medium_count": "INTEGER DEFAULT 0",
            "low_count": "INTEGER DEFAULT 0",
            "total_chunks": "INTEGER DEFAULT 0",
            "processed_chunks": "INTEGER DEFAULT 0"
        }
        for col, definition in required_columns.items():
            if col not in prs_columns:
                await db.execute(f"ALTER TABLE prs ADD COLUMN {col} {definition}")

        # Backfill migration: ensure no NULLs exist in decision columns
        await db.execute("UPDATE prs SET decision_status = 'BLOCK' WHERE decision_status IS NULL")
        await db.execute("UPDATE prs SET high_count = 0 WHERE high_count IS NULL")
        await db.execute("UPDATE prs SET medium_count = 0 WHERE medium_count IS NULL")
        await db.execute("UPDATE prs SET low_count = 0 WHERE low_count IS NULL")

        await db.execute('''
            CREATE TABLE IF NOT EXISTS issues (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pr_id INTEGER,
                severity TEXT,
                type TEXT,
                title TEXT,
                description TEXT,
                file TEXT,
                line INTEGER,
                FOREIGN KEY (pr_id) REFERENCES prs (id)
            )
        ''')
        
        # Migration: Add title column if it doesn't exist
        async with db.execute("PRAGMA table_info(issues)") as cursor:
            issues_columns = [row[1] for row in await cursor.fetchall()]
        if "title" not in issues_columns:
            await db.execute("ALTER TABLE issues ADD COLUMN title TEXT DEFAULT ''")

        await db.execute('''
            CREATE TABLE IF NOT EXISTS processed_shas (
                sha TEXT PRIMARY KEY,
                status TEXT DEFAULT 'pending',
                updated_at TEXT
            )
        ''')

        # Step 2 Fix: Enforce dedup at DB level — in-memory sets are NOT sufficient
        await db.execute(
            'CREATE UNIQUE INDEX IF NOT EXISTS idx_unique_sha ON processed_shas(sha)'
        )

        # Step 3 Fix: Deduplicate existing prs rows BEFORE enforcing uniqueness.
        # Keep only the latest row (highest id) per (repo, pr_number).
        await db.execute('''
            DELETE FROM prs
            WHERE id NOT IN (
                SELECT MAX(id) FROM prs GROUP BY repo, pr_number
            )
        ''')
        await db.commit()

        # Now safe to create the unique index on a clean table
        await db.execute(
            'CREATE UNIQUE INDEX IF NOT EXISTS idx_unique_pr ON prs(repo, pr_number)'
        )

        await db.execute('CREATE TABLE IF NOT EXISTS system_meta (key TEXT PRIMARY KEY, value TEXT)')

        # 2. Schema Migrations (Example: v2 add updated_at to processed_shas if missing)
        # In a real app, use Alembic. Here we use an internal version.
        await db.execute("INSERT OR IGNORE INTO system_meta (key, value) VALUES (?, ?)", ("schema_version", "1"))

        # 3. Initialize bot start time if not exists
        await db.execute("INSERT OR IGNORE INTO system_meta (key, value) VALUES (?, ?)",
                       ("bot_start_time", datetime.now(timezone.utc).isoformat()))

        await db.commit()
        logger.info("Database initialized (Persistent Mode)")

async def claim_sha_for_processing(sha: str) -> bool:
    """
    ATOMICALLY claims a SHA for processing. Rules:
      - completed  -> NEVER re-claim (permanent lock)
      - pending    -> re-claim only if stale (>30 min old)
      - failed     -> re-claim only if stale (>30 min old)
      - not exists -> always claim (via INSERT OR IGNORE epoch seed)
    Returns True if claimed, False if already active/completed.
    """
    async with get_db() as db:
        now        = datetime.now(timezone.utc)
        stale_time = (now - timedelta(minutes=60)).isoformat()
        now_str    = now.isoformat()

        # Seed the row so the UPDATE below has something to match on first insert
        await db.execute(
            "INSERT OR IGNORE INTO processed_shas (sha, status, updated_at) "
            "VALUES (?, 'pending', '1970-01-01T00:00:00')",
            (sha,)
        )

        # Claim only if NOT completed AND (brand-new OR stale pending/failed)
        cursor = await db.execute(
            """
            UPDATE processed_shas
            SET    status = 'pending', updated_at = ?
            WHERE  sha = ?
              AND  status != 'completed'
              AND (
                    updated_at = '1970-01-01T00:00:00'
                 OR (status IN ('pending', 'failed') AND updated_at < ?)
                  )
            """,
            (now_str, sha, stale_time)
        )

        await db.commit()
        is_claimed = cursor.rowcount > 0
        if is_claimed:
            logger.info(f"SHA {sha} atomically claimed.")
        else:
            logger.info(f"SHA {sha} rejected: completed or still active (not stale).")
        return is_claimed

async def is_sha_processed(sha: str) -> bool:
    """Checks if a SHA is successfully completed. Does NOT claim it."""
    async with get_db() as db:
        async with db.execute("SELECT status FROM processed_shas WHERE sha = ?", (sha,)) as cursor:
            row = await cursor.fetchone()
            return row and row['status'] == 'completed'

async def mark_sha_status(sha: str, status: str):
    """Marks a commit SHA with a specific status."""
    updated_at = datetime.now(timezone.utc).isoformat()
    async with get_db() as db:
        await db.execute(
            "INSERT OR REPLACE INTO processed_shas (sha, status, updated_at) VALUES (?, ?, ?)",
            (sha, status, updated_at)
        )
        await db.commit()
    logger.info(f"SHA {sha} marked as {status}")

async def record_review(repo: str, pr_number: int, issues: list, status: str = "success"):
    """
    DEPRECATED: Use initiate_review and finalize_review for observability consistency.
    Legacy wrapper for compatibility during migration.
    """
    pr_id = await initiate_review(repo, pr_number, status=status)
    await finalize_review(pr_id, issues, status=status)

async def upsert_review(repo: str, pr_number: int, status: str = "processing") -> int:
    """
    Step 3 Fix: ATOMIC UPSERT — guarantees exactly ONE row per (repo, pr_number).
    State machine: RECEIVED -> PROCESSING -> COMPLETED / FAILED.
    Never inserts duplicate rows; always updates existing ones.
    Handles legacy schema with bot_start_time NOT NULL column.
    """
    now = datetime.now(timezone.utc).isoformat()

    async def _upsert():
        async with get_db() as db:
            # Detect schema once to handle legacy bot_start_time column
            async with db.execute("PRAGMA table_info(prs)") as c:
                cols = [row[1] for row in await c.fetchall()]
            has_bot_start = "bot_start_time" in cols

            if has_bot_start:
                sql = '''
                    INSERT INTO prs (repo, pr_number, reviewed_at, bot_start_time, status)
                    VALUES (?, ?, ?, ?, ?)
                    ON CONFLICT(repo, pr_number)
                    DO UPDATE SET
                        status      = excluded.status,
                        reviewed_at = excluded.reviewed_at,
                        processed_chunks = 0,
                        total_chunks = 0
                '''
                params = (repo, pr_number, now, now, status)
            else:
                sql = '''
                    INSERT INTO prs (repo, pr_number, reviewed_at, status)
                    VALUES (?, ?, ?, ?)
                    ON CONFLICT(repo, pr_number)
                    DO UPDATE SET
                        status      = excluded.status,
                        reviewed_at = excluded.reviewed_at,
                        processed_chunks = 0,
                        total_chunks = 0
                '''
                params = (repo, pr_number, now, status)

            await db.execute(sql, params)
            await db.commit()
            # Return the existing or newly created row id
            async with db.execute(
                "SELECT id FROM prs WHERE repo = ? AND pr_number = ?",
                (repo, pr_number)
            ) as c:
                row = await c.fetchone()
                return row[0]

    return await db_retry(_upsert)


async def initiate_review(repo: str, pr_number: int, status: str = "pending") -> int:
    """Backwards-compat shim — delegates to upsert_review."""
    return await upsert_review(repo, pr_number, status=status)

async def finalize_review(pr_id: int, issues: list, status: str = "error",
                          decision_status: str = "BLOCK", high: int = 0,
                          medium: int = 0, low: int = 0,
                          total_chunks: int = 0, processed_chunks: int = 0):
    """
    Step 3 Fix: Finalizes via UPDATE only — never inserts a new row.
    Step 4 Fix: Empty issues list with status=success → decision stays as computed
                (the compute_decision function in main.py already returns SAFE when
                issues=[] and no error; we never force BLOCK here).
    """
    async def _update():
        async with get_db() as db:
            # Explicit transaction for atomicity
            await db.execute("BEGIN IMMEDIATE")
            
            # Atomic UPDATE — single row per PR, never ghost inserts
            await db.execute(
                """UPDATE prs SET
                   status          = ?,
                   decision_status = ?,
                   high_count      = ?,
                   medium_count    = ?,
                   low_count       = ?,
                   total_chunks    = ?,
                   processed_chunks = ?
                   WHERE id        = ?""",
                (status, decision_status, high, medium, low, total_chunks, processed_chunks, pr_id)
            )

            # Delete stale issues from previous processing attempts, then re-insert
            await db.execute("DELETE FROM issues WHERE pr_id = ?", (pr_id,))
            for issue in issues:
                await db.execute(
                    "INSERT INTO issues (pr_id, severity, type, title, description, file, line) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (
                        pr_id,
                        (issue.get("severity") or "low").lower(),
                        (issue.get("type") or "bug").lower(),
                        (issue.get("title") or "Issue Detected"),
                        (issue.get("description") or ""),
                        (issue.get("file") or ""),
                        (issue.get("line") or 0)
                    )
                )
            await db.commit()

    await db_retry(_update)
    logger.info(
        f"📈 Telemetry Finalized: PR ID {pr_id} | Status: {status} "
        f"| Decision: {decision_status} | Issues: H={high} M={medium} L={low}"
    )

async def update_review_progress(pr_id: int, processed: int, total: int):
    """Updates the progress counts for a PR without finalizing it."""
    async def _update():
        async with get_db() as db:
            await db.execute(
                "UPDATE prs SET processed_chunks = ?, total_chunks = ? WHERE id = ?",
                (processed, total, pr_id)
            )
            await db.commit()
    await db_retry(_update)

async def get_stats(limit: int = 15, offset: int = 0) -> dict:
    """Aggregates telemetry with pagination."""
    async with get_db() as db:
        # Atomic read transaction to prevent dirty reads and UI flickering
        await db.execute("BEGIN")
        
        # Counts
        async with db.execute("SELECT COUNT(*) FROM prs") as c: total_prs = (await c.fetchone())[0]
        async with db.execute("SELECT COUNT(*) FROM issues") as c: total_issues = (await c.fetchone())[0]

        # Breakdown (Filtered by successful PRs to prevent contamination)
        async with db.execute("SELECT severity, COUNT(*) as count FROM issues WHERE pr_id IN (SELECT id FROM prs WHERE status='success') GROUP BY severity") as c:
            sev_data = {row['severity']: row['count'] for row in await c.fetchall()}

        async with db.execute("SELECT type, COUNT(*) as count FROM issues WHERE pr_id IN (SELECT id FROM prs WHERE status='success') GROUP BY type") as c:
            type_data = {row['type']: row['count'] for row in await c.fetchall()}

        # Recent (Paginated)
        async with db.execute("SELECT * FROM prs ORDER BY reviewed_at DESC LIMIT ? OFFSET ?", (limit, offset)) as c:
            prs = await c.fetchall()

        recent_reviews = []
        for pr_row in prs:
            pr = dict(pr_row)
            pr_status = pr.get("status", "error")
            decision = pr.get("decision_status", "BLOCK")

            async with db.execute("SELECT * FROM issues WHERE pr_id = ?", (pr['id'],)) as c:
                issues = [dict(row) for row in await c.fetchall()]

            recent_reviews.append({
                "repo": pr['repo'],
                "pr_number": pr['pr_number'],
                "status": pr_status,
                "decision": decision,
                "issue_count": len(issues),
                "reviewed_at": pr['reviewed_at'],
                "issues": issues,
                "coverage": {
                    "processed": pr.get('processed_chunks', 0),
                    "total": pr.get('total_chunks', 0)
                },
                "severities": {
                    "high": pr.get('high_count', 0),
                    "medium": pr.get('medium_count', 0),
                    "low": pr.get('low_count', 0),
                }
            })

        # Meta
        async with db.execute("SELECT value FROM system_meta WHERE key = 'bot_start_time'") as c:
            row = await c.fetchone()
            bot_start_time = row[0] if row else datetime.now(timezone.utc).isoformat()

        uptime_seconds = (datetime.now(timezone.utc) - datetime.fromisoformat(bot_start_time)).total_seconds()
        hours, remainder = divmod(int(uptime_seconds), 3600)
        minutes, _ = divmod(remainder, 60)

        async with db.execute("SELECT reviewed_at FROM prs ORDER BY reviewed_at DESC LIMIT 1") as c:
            last_row = await c.fetchone()
            last_review_time = last_row[0] if last_row else None
            
        await db.commit()

    return {
        "total_prs": total_prs,
        "total_issues": total_issues,
        "issues_by_severity": {"high": sev_data.get("high", 0), "medium": sev_data.get("medium", 0), "low": sev_data.get("low", 0)},
        "issues_by_type": {"security": type_data.get("security", 0), "bug": type_data.get("bug", 0), "performance": type_data.get("performance", 0), "quality": type_data.get("quality", 0)},
        "recent_reviews": recent_reviews,
        "bot_status": "online",
        "uptime": f"{hours}h {minutes}m",
        "last_review_time": last_review_time
    }

async def get_issues_for_pr(pr_number: int) -> list:
    """Retrieves all issues associated with a specific PR number."""
    async with get_db() as db:
        async with db.execute("""
            SELECT i.* FROM issues i
            JOIN prs p ON i.pr_id = p.id
            WHERE p.pr_number = ?
        """, (pr_number,)) as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]

`

## File: backend/services/ai_service.py

`python
import aiosqlite
import asyncio
import logging
import os
import json
import re
import string
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from groq import AsyncGroq, GroqError

logger = logging.getLogger("backend")

class AIService:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            logger.error("GROQ_API_KEY not found in environment")
            self.client = None
        else:
            self.client = AsyncGroq(api_key=self.api_key)

    def _is_similar(self, issue1: Dict[str, Any], issue2: Dict[str, Any]) -> bool:
        """
        Normalizes descriptions and performs semantic similarity matching.
        HARDENING: Allows deduplication on nearby lines (within 3 lines) if description matches.
        """
        # File must be the same
        if issue1.get("file") != issue2.get("file"):
            return False
            
        # Line distance check: If lines are > 3 apart, assume different issues
        try:
            line1 = int(issue1.get("line", 0))
            line2 = int(issue2.get("line", 0))
            if abs(line1 - line2) > 3:
                return False
        except (ValueError, TypeError):
            return False

        def normalize(t: str) -> str:
            t = t.lower()
            return t.translate(str.maketrans('', '', string.punctuation)).strip()

        norm1 = normalize(issue1.get("description", ""))
        norm2 = normalize(issue2.get("description", ""))

        if not norm1 or not norm2:
            return False
            
        # Hardening: If description is too short, avoid semantic dedup to prevent generic collisions
        if len(norm1) < 20 or len(norm2) < 20:
            return norm1 == norm2

        # Jaccard similarity for better deduplication
        words1 = set(norm1.split())
        words2 = set(norm2.split())

        stop_words = {"is", "are", "the", "a", "an", "this", "that", "it", "to", "in", "on", "of", "for", "and", "or", "found", "should", "could", "be"}
        words1 = words1 - stop_words
        words2 = words2 - stop_words

        if not words1 or not words2:
            return norm1 == norm2

        intersection = words1.intersection(words2)
        union = words1.union(words2)

        score = len(intersection) / len(union)
        
        # If lines are identical, threshold is 0.6. 
        # If lines are different (but nearby), threshold is 0.8 (higher bar for dedup)
        threshold = 0.6 if line1 == line2 else 0.8
        return score >= threshold

    def _is_structurally_valid(self, issue: Dict[str, Any]) -> bool:
        """Strict schema enforcement to prevent 'garbage' data from malformed AI blocks."""
        if not isinstance(issue, dict):
            return False
            
        required_keys = {"severity", "type", "title", "description", "fix"}
        for key in required_keys:
            val = issue.get(key)
            if not isinstance(val, str) or not val.strip():
                return False
            
        # Strict enum check
        if issue["severity"].upper() not in {"HIGH", "MEDIUM", "LOW"}:
            return False
            
        return True

    async def _analyze_chunk_with_retry(self, diff_chunk: str) -> Optional[Dict[str, Any]]:
        """Sends a single diff chunk to Groq with retry logic and JSON validation."""
        system_prompt = """
You are a strict, deterministic code reviewer.

Rules:
1. DO NOT report the same issue again if it was already fixed in previous commits.
2. DO NOT invent new issues after a correct fix.
3. Only report issues that currently exist in NEWLY ADDED lines (lines starting with '+').
4. If the code is already correct, return {"issues": []}.
5. DO NOT suggest improvements, optimizations, or style changes.
6. DO NOT change logic unless it is clearly and provably incorrect.
7. Fix must be minimal and directly related to the issue.
8. If no real bug exists, output: {"issues": []}

IMPORTANT - This is a git diff:
- Lines starting with '+' are NEWLY ADDED. Analyze ONLY these.
- Lines starting with '-' are REMOVED. DO NOT analyze them.
- Lines with no prefix are CONTEXT. DO NOT analyze them.

FORBIDDEN (never report these):
- Integer overflow in Python (Python integers cannot overflow).
- Readability, style, refactoring, or optimization suggestions.
- Any issue where the fix is identical to the existing code.

Stability is more important than completeness. When in doubt, return {"issues": []}.

Output ONLY valid JSON:
{
  "issues": [
    {
      "severity": "HIGH|MEDIUM|LOW",
      "type": "security|bug|performance|quality",
      "title": "Precise name",
      "description": "Exactly what is wrong",
      "line": 3,
      "file": "filename.py",
      "fix": "replacement code ONLY"
    }
  ]
}
"""

        user_prompt = f"Code Diff Chunk:\n{diff_chunk}"

        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = await self.client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.1,
                    response_format={"type": "json_object"},
                    timeout=15.0
                )

                content = response.choices[0].message.content.strip()
                parsed_json = json.loads(content)
                return parsed_json

            except Exception as e:
                error_str = str(e).lower()
                logger.error(f"[analyze_code] error on attempt {attempt + 1}: {error_str}")
                
                # Explicit Rate Limit Detection
                if "rate_limit_exceeded" in error_str or "429" in error_str:
                    if attempt < max_retries - 1:
                        wait_time = 30 * (attempt + 1)
                        logger.warning(f"⚠️ Rate limit hit. Backing off for {wait_time}s...")
                        await asyncio.sleep(wait_time)
                        continue
                    else:
                        return {"status": "error", "reason": "RATE_LIMIT", "issues": []}

                if attempt < max_retries - 1:
                    await asyncio.sleep(2)
                else:
                    return {"status": "error", "reason": "UNKNOWN_ERROR", "issues": []}

        return None

    def _get_hunk_aware_chunks(self, diff: str, max_size: int = 1000) -> list:
        """Splits diff into chunks by hunk, preserving file context."""
        lines = diff.splitlines()
        chunks = []
        current_chunk = []
        current_file_header = ""
        current_size = 0

        for line in lines:
            if line.startswith("+++ b/"):
                current_file_header = line

            line_size = len(line) + 1
            if current_size + line_size > max_size and current_chunk:
                chunks.append("\n".join(current_chunk))
                current_chunk = [current_file_header, line] if current_file_header else [line]
                current_size = len(current_file_header) + line_size if current_file_header else line_size
            else:
                current_chunk.append(line)
                current_size += line_size

        if current_chunk:
            chunks.append("\n".join(current_chunk))
        return chunks

    def _rule_based_scan(self, diff: str) -> List[Dict[str, Any]]:
        """Lightweight static scan for critical security patterns (passwords, unsafe calls)."""
        # Multiline support: Normalize diff by merging lines to catch patterns split across lines
        normalized_diff = diff.replace("\n+", " ").replace("\n-", " ").replace("\n", " ")
        
        rules = [
            (r"(password|api_key|secret|token|private_key)\s*=\s*['\"].*?['\"]", "Hardcoded credential/secret", "HIGH", "security"),
            (r"verify=False", "SSL verification disabled", "MEDIUM", "security"),
            (r"eval\(", "Unsafe eval() usage", "HIGH", "security"),
            (r"os\.chmod\(.*0o777\)", "Insecure file permissions (777)", "HIGH", "security"),
        ]
        issues = []
        
        # 1. Scan normalized diff for multiline patterns
        for pattern, desc, sev, itype in rules:
            if re.search(pattern, normalized_diff, re.IGNORECASE):
                issues.append({
                    "severity": sev, "type": itype,
                    "title": "Rule-based Guard",
                    "description": f"Security risk detected: {desc}",
                    "fix": "Rotate secrets and use environment variables.",
                    "file": "Security Scan", "line": 0
                })
        
        return issues

    async def analyze_code(self, diff: str, progress_callback=None) -> Dict[str, Any]:
        """
        Analyzes a git diff using Groq AI.
        Splits diff into hunks, processes each hunk/chunk sequentially with a delay to respect rate limits.
        """
        if not diff:
            return {"status": "failed", "reason": "EMPTY_DIFF", "issues": [],
                    "total_chunks": 0, "processed_chunks": 0, "file_coverage": {}}

        if not self.client:
            return {"status": "failed", "reason": "CLIENT_NOT_INITIALIZED", "issues": [],
                    "total_chunks": 0, "processed_chunks": 0, "file_coverage": {}}

        all_chunks = self._get_hunk_aware_chunks(diff)
        
        total_chunks = len(all_chunks)
        chunks_to_process = all_chunks
        
        all_files = set(re.findall(r"^\+\+\+ b/(.*)$", diff, re.MULTILINE))
        file_chunks = {f: {"total": 0, "processed": 0} for f in all_files}
        for chunk in all_chunks:
            chunk_files = set(re.findall(r"^\+\+\+ b/(.*)$", chunk, re.MULTILINE))
            for f in chunk_files:
                file_chunks[f]["total"] += 1

        total_chunks = len(all_chunks)
        processed_chunks = 0
        rule_issues = self._rule_based_scan(diff)
        all_issues = list(rule_issues)
        seen_descriptions = list(rule_issues)
        reason = "SUCCESS"

        for chunk in chunks_to_process:
            chunk_files = set(re.findall(r"^\+\+\+ b/(.*)$", chunk, re.MULTILINE))
            result = await self._analyze_chunk_with_retry(chunk)
            await asyncio.sleep(2.0) # Sequential processing delay to avoid rate limits
            
            if result is None or (isinstance(result, dict) and result.get("status") == "error"):
                reason = result.get("reason", "CHUNK_ERROR") if isinstance(result, dict) else "CHUNK_ERROR"
                break

            processed_chunks += 1
            if progress_callback:
                await progress_callback(processed_chunks, total_chunks)

            # Mark files in this chunk as partially processed
            for f in chunk_files:
                file_chunks[f]["processed"] += 1

            chunk_issues = result.get("issues", [])
            if isinstance(chunk_issues, list):
                for issue in chunk_issues:
                    if not self._is_structurally_valid(issue): continue
                    desc = issue.get("description", "").strip()
                    fix = issue.get("fix", "").strip()
                    if not desc or len(desc) < 10 or not fix or "no fix needed" in fix.lower(): continue
                    
                    if not any(self._is_similar(issue, seen) for seen in seen_descriptions):
                        seen_descriptions.append(issue)
                        all_issues.append(issue)



        # Calculate final file-level coverage status
        file_coverage = {}
        for f, stats in file_chunks.items():
            if stats["total"] > 0 and stats["processed"] == stats["total"]:
                file_coverage[f] = "FULLY_ANALYZED"
            elif stats["processed"] > 0:
                file_coverage[f] = "PARTIAL"
            else:
                file_coverage[f] = "SKIPPED"

        # Confidence Kill Switch: Never trust silence on large diffs
        decision_status = "SAFE"
        if not all_issues and len(diff) > 3000:
            decision_status = "REVIEW_REQUIRED"
            logger.warning(f"⚠️ Confidence Kill Switch Triggered: Large diff ({len(diff)} chars) with 0 issues. Forcing REVIEW_REQUIRED.")

        return {
            "status": "success" if processed_chunks == total_chunks else "partial",
            "reason": reason,
            "issues": all_issues,
            "decision_status": decision_status,
            "rule_based_count": len(rule_issues),
            "total_chunks": total_chunks,
            "processed_chunks": processed_chunks,
            "file_coverage": file_coverage
        }

def get_ai_service() -> AIService:
    return AIService()

`

## File: backend/services/diff_validator.py

`python
import logging
import re
from typing import Dict, Set, Tuple, Optional, Any
from services.validator import AntiHallucinationValidator

logger = logging.getLogger("backend")


class DiffValidator:
    """Parses unified diffs to validate AI-suggested line mappings and generate GitHub suggestions."""

    @staticmethod
    def parse_diff_mapping(diff_text: str) -> Dict[str, Dict[int, Tuple[str, str]]]:
        """
        Parses unified diff and returns detailed mapping:
        {
            "file.py": {
                line_num: (old_content, new_content)
            }
        }
        """
        mapping = {}
        if not diff_text:
            return mapping

        current_file = None
        lines = diff_text.splitlines()
        i = 0
        while i < len(lines):
            line = lines[i]

            # Detect file header
            if line.startswith("+++ b/"):
                current_file = line[6:].strip()
                mapping[current_file] = {}
                i += 1
                continue

            # Detect hunk header: @@ -start,len +start,len @@
            hunk_match = re.match(r"^@@ -(\d+)(?:,\d+)? \+(\d+)(?:,\d+)? @@", line)
            if hunk_match and current_file:
                new_line_num = int(hunk_match.group(2))
                i += 1

                # Use a buffer to handle changed lines (old followed by new)
                old_buffer = []
                while i < len(lines) and not lines[i].startswith(("diff --git", "+++", "---", "@@")):
                    current = lines[i]
                    if current.startswith("+"):
                        new_content = current[1:]
                        # Try to pair with an old line if one is buffered
                        old_content = old_buffer.pop(0) if old_buffer else ""
                        mapping[current_file][new_line_num] = (old_content, new_content)
                        new_line_num += 1
                    elif current.startswith("-"):
                        old_buffer.append(current[1:])
                    else:
                        # Context line
                        old_buffer = [] # Clear buffer on context
                        mapping[current_file][new_line_num] = (current, current)
                        new_line_num += 1
                    i += 1
                continue
            i += 1

        return mapping

    @staticmethod
    def validate_issue(issue: Dict[str, Any], mapping: Dict[str, Dict[int, Tuple[str, str]]]) -> bool:
        """Checks if the issue's file and line exist in the diff mapping."""
        file_path = issue.get("file")
        try:
            line_num = int(issue.get("line", -1))
        except (ValueError, TypeError):
            return False

        if not file_path:
            return False

        # Flexible file matching
        matched_key = DiffValidator._find_matching_file(file_path, mapping)
        if not matched_key:
            logger.warning(f"[DiffValidator] File not in diff: {file_path}")
            return False

        # Check if line exists in mapping
        if line_num in mapping[matched_key]:
            return True

        # Lenient line matching with tolerance
        valid_lines = sorted(mapping[matched_key].keys())
        for valid_line in valid_lines:
            if abs(valid_line - line_num) <= 5:
                # If the line was added or modified (diff contents not the same)
                old, new = mapping[matched_key][valid_line]
                if old != new:
                    logger.info(f"[DiffValidator] Adjusted line from {line_num} to {valid_line}")
                    issue["line"] = valid_line
                    return True

        logger.warning(f"[DiffValidator] Line {line_num} not found/unmodified for {file_path}")
        return False

    @staticmethod
    def generate_suggestion(issue: Dict[str, Any], mapping: Dict[str, Dict[int, Tuple[str, str]]]) -> Optional[str]:
        """
        Generates GitHub suggestion format for an issue.
        """
        file_path = issue.get("file")
        line_num = issue.get("line")
        fix_code = issue.get("fix", "")

        matched_key = DiffValidator._find_matching_file(file_path, mapping)
        if not matched_key or line_num not in mapping[matched_key]:
            return None

        old_content, new_content = mapping[matched_key][line_num]

        # Use AI's fix if provided and looks valid, otherwise use diff content
        if fix_code and len(fix_code.strip()) > 2:
            suggestion_code = DiffValidator._clean_code(fix_code)
        elif new_content and new_content != old_content:
            suggestion_code = new_content
        else:
            return None

        if not suggestion_code or len(suggestion_code.strip()) < 1:
            return None

        # 🚀 ANTI-HALLUCINATION GUARD
        if not AntiHallucinationValidator.validate_suggestion(issue, old_content):
            return None

        return f"```suggestion\n{suggestion_code}\n```"

    @staticmethod
    def _find_matching_file(file_path: str, mapping: Dict[str, Any]) -> Optional[str]:
        if not file_path: return None
        if file_path in mapping: return file_path
        for key in mapping:
            if key.endswith(file_path) or file_path.endswith(key) or file_path in key or key in file_path:
                return key
        return None

    @staticmethod
    def _clean_code(code: str) -> str:
        if not code: return ""
        # Aggressively scrub common AI preamble
        code = re.sub(r'^(?:Fix|Suggested fix|Code|Suggestion|Use|Try|Here is the fix|Correct code):\s*', '', code, flags=re.IGNORECASE | re.MULTILINE)

        # Scrub line number prefixes like "5 - " or "5 + " or "5 | "
        code = re.sub(r'^\s*\d+\s*[-+|]\s*', '', code, flags=re.MULTILINE)

        # Scrub markdown code blocks
        code = re.sub(r'^```\w*\s*\n?', '', code, flags=re.MULTILINE)
        code = re.sub(r'\n?```\s*$', '', code)

        code = code.strip()

        # If it still looks like natural language (starts with "Use "), it's probably not a good fix
        if code.lower().startswith("use ") and len(code.split()) > 5:
            return "" # Don't suggest text as code

        lines = code.splitlines()
        if len(lines) > 1:
            min_indent = float('inf')
            for line in lines:
                if line.strip():
                    min_indent = min(min_indent, len(line) - len(line.lstrip()))
            if min_indent != float('inf') and min_indent > 0:
                lines = [line[min_indent:] if len(line) > min_indent else line for line in lines]
                code = '\n'.join(lines)
        return code

`

## File: backend/services/filter_service.py

`python
import logging

logger = logging.getLogger(__name__)

class FilterService:
    """Service to filter and preprocess data."""

    def __init__(self):
        pass

    def filter_diff(self, diff_content: str) -> str:
        """Filters unnecessary content from a code diff."""
        logger.info("Filtering diff content")
        # Placeholder filter implementation
        return diff_content.strip()

def get_filter_service() -> FilterService:
    return FilterService()

def parse_and_filter_issues(analysis_result: dict, raw_diff: str = "") -> list:
    """
    SAFETY THROTTLE (v2):
    1. STRICT SEVERITY FLOOR: Only Medium and High issues allowed.
    2. REJECT SMALL DIFF NOISE: If diff is < 10 lines, AI is likely hallucinating.
    3. BAN REFACTORING: Silence the AI if it tries to 'improve' or 'optimize'.
    """
    logger.info("[filter_service] Applying Safety Throttle to prevent feedback loops")

    if not analysis_result or "issues" not in analysis_result:
        return []

    # If the diff is tiny, the AI often 'hallucinates' bugs to be helpful.
    # We silence it for very small changes unless they are HIGH severity.
    diff_lines = [l for l in raw_diff.splitlines() if l.startswith('+') or l.startswith('-')]
    is_tiny_diff = len(diff_lines) < 10

    valid_issues = []
    # Forbidden topics that cause infinite loops or are Python-impossible
    hallucination_triggers = [
        "improve", "optimize", "better", "clean", "suggest", "consider", 
        "style", "refactor", "readability", "efficiency", "best practice",
        "redundant", "unnecessary", "nitpick", "formatting",
        "overflow", "integer limit", "search space" 
    ]

    for issue in analysis_result.get("issues", []):
        severity = str(issue.get("severity", "")).lower()
        description = str(issue.get("description", "")).lower()
        fix = str(issue.get("fix", ""))
        issue_type = str(issue.get("type", "")).lower()
        file_path = str(issue.get("file", "")).lower()
        
        # 0. IRON-CLAD BLOCK: Reject 'overflow' in Python (hallucination)
        if "overflow" in description or "limit" in description:
            logger.info(f"🚫 IRON-CLAD REJECT: Blocked impossible Python overflow hallucination.")
            continue

        # 1. IRON-CLAD BLOCK: Reject 'search space' or 'overflow' hallucinations in Python
        hallucination_code = ["search space", "integer overflow", "integer limit"]
        if any(word in description.lower() for word in hallucination_code):
            logger.info(f"🚫 IRON-CLAD REJECT: Blocked impossible Python overflow hallucination.")
            continue

        # 2. STRUCTURE GUARD: If the fix replaces a structural keyword with logic, it's misaligned.
        if any(kw in fix.lower() for kw in ["else:", "elif:", "while:", "if "]) and len(fix.split()) < 3:
             continue

        # 3. COMMENT GUARD: Never suggest replacing a comment with code.
        if description.lower().startswith("incorrect update") and "#" in description:
             continue

        # 1. STRICT SEVERITY FLOOR
        # We no longer allow LOW or INFO to reach the user.
        if severity not in ("high", "medium", "critical"):
            logger.info(f"🚫 THROTTLED: Low severity issue blocked.")
            continue

        # 2. TINY DIFF PROTECTION
        # If the change is small, only allow HIGH/CRITICAL issues.
        if is_tiny_diff and severity != "high":
            logger.info(f"🚫 THROTTLED: Medium issue blocked on tiny diff to prevent loops.")
            continue

        # 3. HALLUCINATION TRIGGER BANS
        if any(word in description for word in hallucination_triggers) or any(word in fix.lower() for word in hallucination_triggers):
            logger.info(f"🚫 THROTTLED: AI is nitpicking/hallucinating: {description[:50]}...")
            continue

        # 4. Structural Integrity
        if not (issue_type and description and fix):
            continue

        # 5. SQLi & Destructive Protection (Keep existing security layers)
        if "sql injection" in description and ("?" in raw_diff or "%s" in raw_diff):
            continue
        if "return" in fix.lower() and "execute" in raw_diff.lower() and "execute" not in fix.lower():
             continue

        valid_issues.append(issue)

    logger.info(f"✅ SAFETY THROTTLE COMPLETE: {len(valid_issues)} high-fidelity issues remaining.")
    return valid_issues

`

## File: backend/services/github_service.py

`python
import asyncio
import os
import logging
from typing import Tuple, Dict, Any, Optional
import httpx

logger = logging.getLogger(__name__)

GITHUB_API_BASE = "https://api.github.com"

class GitHubService:
    """Service to interact with GitHub APIs."""

    def __init__(self):
        self.token = os.getenv("GITHUB_TOKEN")
        if not self.token:
            logger.error("GITHUB_TOKEN is not set in environment variables")

        # Use 'Bearer' prefix which is the modern standard for GitHub PATs and Apps
        self.headers = {
            "Authorization": f"Bearer {self.token}" if self.token else "",
            "Accept": "application/vnd.github.v3+json",
        }

    def extract_pr_data(self, payload: Dict[str, Any]) -> Tuple[str, str, int]:
        """Extracts owner, repo, and PR number from a webhook payload."""
        try:
            full_name = payload["repository"]["full_name"]
            owner, repo = full_name.split('/')
            pr_number = payload["pull_request"]["number"]
            return owner, repo, pr_number
        except (KeyError, ValueError, TypeError) as e:
            logger.error(f"Failed to extract PR data from payload: {str(e)}")
            raise ValueError("Invalid GitHub webhook payload format") from e

    async def fetch_diff(self, owner: str, repo: str, pr_number: int) -> Optional[str]:
        """Fetches the code diff of a specific pull request securely using the Pulls API."""
        logger.info(f"Fetching diff for {owner}/{repo} PR #{pr_number}")
        url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}"

        headers = self.headers.copy()
        headers["Accept"] = "application/vnd.github.v3.diff"

        try:
            # Explicitly follow redirects for diff fetching as GitHub may redirect to patch-diff.githubusercontent.com
            async with httpx.AsyncClient(follow_redirects=True, timeout=10.0) as client:
                for attempt in range(3):
                    response = await client.get(url, headers=headers)
                    if response.status_code == 429:
                        # Adaptive Rate Limiting: Respect GitHub's Retry-After header
                        retry_after = response.headers.get("Retry-After")
                        wait = int(retry_after) if retry_after and retry_after.isdigit() else (attempt + 1) * 2
                        logger.warning(f"Rate limited by GitHub. Waiting {wait}s (Retry-After)...")
                        await asyncio.sleep(wait)
                        continue

                    if response.status_code == 401:
                        logger.error(f"Unauthorized access to {url}. Token status: {'Present' if self.token else 'Missing'}")

                    response.raise_for_status()
                    return response.text
        except httpx.HTTPError as e:
            logger.error(f"GitHub API error while fetching diff: {str(e)}")
            return None

    async def post_comment(self, owner: str, repo: str, pr_number: int, comment: str) -> bool:
        """Posts a comment to a specific pull request with adaptive rate limiting."""
        url = f"https://api.github.com/repos/{owner}/{repo}/issues/{pr_number}/comments"
        logger.info(f"DEBUG URL: {url}")

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                for attempt in range(3):
                    response = await client.post(
                        url,
                        headers=self.headers,
                        json={"body": comment}
                    )
                    if response.status_code == 429:
                        retry_after = response.headers.get("Retry-After", (attempt + 1) * 2)
                        wait = int(retry_after) if str(retry_after).isdigit() else (attempt + 1) * 2
                        logger.warning(f"Rate limited during post_comment. Waiting {wait}s...")
                        await asyncio.sleep(wait)
                        continue
                    response.raise_for_status()
                    return True
        except httpx.HTTPError as e:
            logger.error(f"GitHub API Error in post_comment: {str(e)}")
            return False

    async def post_inline_comment(self, owner: str, repo: str, pr_number: int, issue: Dict[str, Any], commit_sha: str, suggestion: Optional[str] = None) -> bool:
        """Posts an inline comment with adaptive rate limiting and optional code suggestion."""
        logger.info(f"Posting inline comment to {owner}/{repo} PR #{pr_number}")
        url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/comments"

        severity = issue.get("severity", "medium").upper()
        description = issue.get("description", "")
        impact = issue.get("impact", "No technical impact specified.")
        file_path = issue.get("file", "")

        try:
            line = int(issue.get("line", 1))
        except (ValueError, TypeError):
            line = 1

        # Build comment body to trigger GitHub Suggested Changes UI
        comment_body = f"""🔍 AI Review ({severity})

**Problem:**
{description}

**Impact:**
{impact}

**Fix:**

{suggestion if suggestion else "*No automated fix available for this logic.*"}
"""

        # Safety check: Does the target line actually contain the code we expect?
        # This prevents the 'wrong line' suggestions seen in PR #62.
        # Note: In a real production system, we would fetch the file content here.
        # For now, we will add a secondary validation in main.py using the raw_diff hunks.

        payload = {
            "body": comment_body,
            "commit_id": commit_sha,
            "path": file_path,
            "line": line,
            "side": "RIGHT"
        }

        try:
            async with httpx.AsyncClient() as client:
                for attempt in range(3):
                    response = await client.post(
                        url,
                        headers=self.headers,
                        json=payload,
                        timeout=10.0
                    )

                    if response.status_code == 429:
                        retry_after = response.headers.get("Retry-After", (attempt + 1) * 2)
                        wait = int(retry_after) if str(retry_after).isdigit() else (attempt + 1) * 2
                        logger.warning(f"Rate limited during post_inline_comment. Waiting {wait}s...")
                        await asyncio.sleep(wait)
                        continue

                    if response.status_code == 422:
                        logger.warning(f"Line mapping error for {issue.get('file')}:{line}. Falling back.")
                        fallback_body = f"🔍 **AI Review Fallback** for `{issue.get('file')}` line `{line}`:\n\n{comment_body}"
                        return await self.post_comment(owner, repo, pr_number, fallback_body)

                    response.raise_for_status()
                    return True
        except httpx.HTTPError as e:
            logger.error(f"GitHub API Error in post_inline_comment: {str(e)}")
            return False

def get_github_service() -> GitHubService:
    return GitHubService()

_github_service_instance = GitHubService()

def extract_pr_data(payload: Dict[str, Any]) -> Tuple[str, str, int]:
    return _github_service_instance.extract_pr_data(payload)

async def fetch_diff(owner: str, repo: str, pr_number: int) -> Optional[str]:
    return await _github_service_instance.fetch_diff(owner, repo, pr_number)

async def post_comment(owner: str, repo: str, pr_number: int, comment: str) -> bool:
    return await _github_service_instance.post_comment(owner, repo, pr_number, comment)

async def post_inline_comment(owner: str, repo: str, pr_number: int, issue: Dict[str, Any], commit_sha: str, suggestion: Optional[str] = None) -> bool:
    return await _github_service_instance.post_inline_comment(owner, repo, pr_number, issue, commit_sha, suggestion)
async def post_status(owner: str, repo: str, sha: str, state: str, description: str, target_url: str = None):
    """
    Updates the GitHub Commit Status.
    state: 'pending', 'success', 'error', 'failure'
    """
    url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/statuses/{sha}"
    payload = {
        "state": state,
        "description": description[:140],
        "context": "AI Code Reviewer"
    }
    if target_url:
        payload["target_url"] = target_url

    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(url, headers=_github_service_instance.headers, json=payload, timeout=10.0)
            if resp.status_code not in (201, 200):
                logger.error(f"Failed to post status: {resp.status_code} - {resp.text}")
                return False
            return True
        except Exception as e:
            logger.error(f"Error posting status: {str(e)}")
            return False

`

## File: backend/services/syntax_validator.py

`python
import ast
import logging

logger = logging.getLogger("backend")

class SyntaxValidator:
    """Utility to validate the technical integrity of code snippets."""

    @staticmethod
    def is_valid_python(code: str) -> bool:
        """Checks if a string is syntactically valid Python code (supports fragments)."""
        try:
            ast.parse(code)
            return True
        except SyntaxError:
            # Fallback: Try parsing as a function body to support fragments (like 'return x')
            try:
                # Indent the block and wrap in a dummy async function
                wrapped_code = "async def __dummy_context():\n" + "\n".join(f"    {line}" for line in code.splitlines())
                ast.parse(wrapped_code)
                return True
            except SyntaxError as e:
                logger.warning(f"Technical Validation Failure: Broken Python syntax. Error: {str(e)}")
                return False
        except Exception as e:
            logger.error(f"SyntaxValidator Exception: {str(e)}")
            return False

    @staticmethod
    def validate_issue(issue: dict) -> bool:
        """Validates that the 'fix' suggested by AI is syntactically correct for supported files."""
        file_path = issue.get("file", "")
        fix_code = issue.get("fix", "")

        if not fix_code or not file_path:
            return True # Not a fix issue

        if file_path.endswith(".py"):
            return SyntaxValidator.is_valid_python(fix_code)

        # Add other language validators here (e.g., jsonschema, shell check)
        return True

`

## File: backend/services/validator.py

`python
import logging
import re
from typing import Dict, Any, Optional

logger = logging.getLogger("backend")

class AntiHallucinationValidator:
    """
    Final safety layer to catch AI hallucinations before they reach GitHub.
    Ensures that suggestions actually change the code and use correct variables.
    """

    @staticmethod
    def validate_suggestion(issue: Dict[str, Any], old_content: str) -> bool:
        """
        Returns True if the suggestion is valid and non-hallucinated.
        """
        fix = issue.get("fix", "").strip()
        old = old_content.strip()

        # 1. Identity Check: Reject if the fix is identical to the old code
        if fix == old:
            logger.warning(f"🚫 HALLUCINATION DETECTED: AI suggested a fix that is identical to the existing code at line {issue.get('line')}.")
            return False

        # 2. Semantic Identity: Reject if they only differ by whitespace
        if "".join(fix.split()) == "".join(old.split()):
            logger.warning(f"🚫 HALLUCINATION DETECTED: Fix only differs by whitespace at line {issue.get('line')}.")
            return False

        return True

    @staticmethod
    def auto_correct_line_mapping(issue: Dict[str, Any], mapping: Dict[int, Any]) -> bool:
        """
        If the AI reported the wrong line, tries to find the correct line nearby 
        by matching keywords from the fix.
        """
        reported_line = issue.get("line", 0)
        fix = issue.get("fix", "").lower()
        
        # Keywords to look for
        keywords = set(re.findall(r'\b[a-zA-Z_]{3,}\b', fix))
        if not keywords: return True # Can't cross-check
        
        # Search window
        for offset in range(-5, 6):
            target_line = reported_line + offset
            if target_line in mapping:
                old_line = mapping[target_line][0].lower()
                # If we find a line nearby that contains multiple keywords from the fix
                matches = sum(1 for kw in keywords if kw in old_line)
                if matches >= 2 and offset != 0:
                    logger.info(f"✨ AUTO-CORRECTED line mapping: Moved from {reported_line} to {target_line} based on keyword match.")
                    issue["line"] = target_line
                    return True
        
        return True

`

## File: backend/static/index.html

`html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Code Reviewer | Command Center</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>
        :root {
            /* Vercel/Linear Inspired Palette */
            --bg-color: #03040b;
            --card-bg: rgba(13, 16, 23, 0.7);
            --card-border: rgba(56, 62, 71, 0.5);
            --accent: #3b82f6;
            --accent-glow: rgba(59, 130, 246, 0.3);
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --text-muted: #64748b;

            --high: #ef4444;
            --medium: #f59e0b;
            --low: #10b981;
            --quality: #06b6d4;
            --security: #a855f7;
            --performance: #f97316;
            --bug: #ef4444;

            --glass-blur: blur(12px);
            --transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            --transition-flow: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
        }

        * {
            margin: 0; padding: 0; box-sizing: border-box;
        }

        body {
            font-family: 'Inter', sans-serif;
            background-color: var(--bg-color);
            color: var(--text-primary);
            line-height: 1.5;
            min-height: 100vh;
            overflow-x: hidden;
            background-image:
                radial-gradient(circle at 0% 0%, rgba(59,130,246,0.1) 0%, transparent 40%),
                radial-gradient(circle at 100% 100%, rgba(139,92,246,0.06) 0%, transparent 40%),
                url("https://www.transparenttextures.com/patterns/dark-matter.png");
            opacity: 0;
            transition: opacity 1s ease-out;
        }

        body.loaded { opacity: 1; }

        /* --- Layout --- */
        .app-container {
            display: flex;
            min-height: 100vh;
        }

        .main-content {
            flex: 1;
            padding: 2.5rem;
            max-width: 1400px;
            margin: 0 auto;
            width: 100%;
        }

        /* --- Header --- */
        header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 3rem;
            animation: slideIn 0.6s ease-out;
        }

        .logo-section h1 {
            font-size: 1.8rem;
            font-weight: 700;
            letter-spacing: -0.02em;
            background: linear-gradient(to right, #fff, #94a3b8);
            -webkit-background-clip: text;
            background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .system-status {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            padding: 0.5rem 1rem;
            background: rgba(255,255,255,0.03);
            border-radius: 99px;
            border: 1px solid var(--card-border);
            font-size: 0.85rem;
            font-weight: 500;
        }

        .status-dot {
            width: 8px; height: 8px;
            background-color: #10b981;
            border-radius: 50%;
            box-shadow: 0 0 10px #10b981;
            animation: pulse 2s infinite;
        }

        /* --- Global Grid --- */
        .grid {
            display: grid;
            grid-template-columns: repeat(12, 1fr);
            gap: 1.5rem;
            margin-bottom: 2rem;
        }

        .card {
            background: var(--card-bg);
            backdrop-filter: var(--glass-blur);
            -webkit-backdrop-filter: var(--glass-blur);
            border: 1px solid var(--card-border);
            border-radius: 14px;
            padding: 1.75rem;
            transition: var(--transition);
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        }

        .card:hover {
            border-color: rgba(59, 130, 246, 0.5);
            transform: translateY(-4px) scale(1.01);
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.2), 0 10px 10px -5px rgba(0, 0, 0, 0.1);
        }

        /* --- Stat Cards --- */
        .stat-card {
            grid-column: span 3;
            text-align: left;
        }

        .stat-label {
            color: var(--text-muted);
            font-size: 0.85rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 0.5rem;
        }

        .stat-value {
            font-size: 2.8rem;
            font-weight: 800;
            letter-spacing: -0.03em;
            font-variant-numeric: tabular-nums;
            background: linear-gradient(to bottom, #fff, #94a3b8);
            -webkit-background-clip: text;
            background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .stat-card:first-child {
            position: relative;
            overflow: hidden;
        }

        .stat-card:first-child::before {
            content: '';
            position: absolute;
            top: -50%; left: -50%; width: 200%; height: 200%;
            background: radial-gradient(circle at center, var(--accent-glow) 0%, transparent 70%);
            opacity: 0.4;
            pointer-events: none;
            z-index: 0;
        }

        /* --- Progress Bars --- */
        .chart-card {
            grid-column: span 6;
            position: relative;
            overflow: hidden;
        }

        .chart-card::before {
            content: '';
            position: absolute;
            bottom: -50%; right: -20%; width: 100%; height: 100%;
            background: radial-gradient(circle at center, rgba(139,92,246,0.15) 0%, transparent 70%);
            pointer-events: none;
            z-index: 0;
        }

        .chart-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.5rem;
        }

        .bar-group {
            margin-bottom: 1.25rem;
        }

        .bar-label {
            display: flex;
            justify-content: space-between;
            font-size: 0.85rem;
            margin-bottom: 0.5rem;
            color: var(--text-secondary);
        }

        .bar-background {
            height: 6px;
            background: rgba(255,255,255,0.05);
            border-radius: 99px;
            overflow: hidden;
        }

        .bar-fill {
            height: 100%;
            border-radius: 99px;
            transition: width 1s cubic-bezier(0.22, 1, 0.36, 1);
        }

        /* --- PR Feed (Accordion) --- */
        .feed-container {
            grid-column: span 12;
        }

        .feed-header {
            margin-bottom: 1rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .accordion-item {
            border-bottom: 1px solid var(--card-border);
            transition: var(--transition);
            border-left: 3px solid transparent;
        }

        .accordion-item:last-child { border-bottom: none; }

        .accordion-item:hover {
            background: rgba(255,255,255,0.015);
            transform: translateY(-1px);
        }

        .accordion-item.has-high {
            border-left: 3px solid rgba(239, 68, 68, 0.2); /* Reduced visual aggression (20%) */
            background: linear-gradient(to right, rgba(239, 68, 68, 0.03), transparent);
        }

        .risk-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 3px 10px;
            border-radius: 99px;
            font-size: 0.7rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.03em;
            margin-left: 1rem;
        }

        .risk-badge.high { background: rgba(239, 68, 68, 0.1); color: var(--high); border: 1px solid rgba(239, 68, 68, 0.2); }
        .risk-badge.moderate { background: rgba(245, 158, 11, 0.1); color: var(--medium); border: 1px solid rgba(245, 158, 11, 0.2); }
        .risk-badge.low { background: rgba(16, 185, 129, 0.1); color: var(--low); border: 1px solid rgba(16, 185, 129, 0.2); }
        .risk-badge.zero { background: rgba(6, 182, 212, 0.1); color: var(--quality); border: 1px solid rgba(6, 182, 212, 0.2); }

        .risk-dot { width: 6px; height: 6px; border-radius: 50%; opacity: 0.8; }
        .risk-badge.high .risk-dot { background: var(--high); box-shadow: 0 0 10px var(--high); opacity: 1; }
        .risk-badge.moderate .risk-dot { background: var(--medium); }
        .risk-badge.low .risk-dot { background: var(--low); }

        .confidence-label {
            font-size: 0.65rem;
            color: var(--text-muted);
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-left: 0.5rem;
            opacity: 0.7;
        }

        .accordion-trigger {
            width: 100%;
            padding: 1.25rem 0.5rem;
            display: grid;
            grid-template-columns: 2fr 1fr 1fr auto;
            align-items: center;
            cursor: pointer;
            text-align: left;
            background: none;
            border: none;
            color: inherit;
        }

        .accordion-trigger:hover {
            background: rgba(255,255,255,0.02);
        }

        .pr-info { display: flex; flex-direction: column; }
        .pr-meta { font-size: 0.8rem; color: var(--text-muted); }

        .badge {
            padding: 0.25rem 0.75rem;
            border-radius: 99px;
            font-size: 0.75rem;
            font-weight: 600;
            width: fit-content;
        }

        .badge-status {
            background: rgba(59,130,246,0.08);
            color: var(--accent);
            border: 1px solid rgba(59,130,246,0.15);
            text-transform: uppercase;
            letter-spacing: 0.02em;
        }

        .tag-pill {
            display: flex; gap: 0.5rem;
            align-items: center;
        }
        .sev-badge {
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 0.7rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            display: flex;
            align-items: center;
            gap: 4px;
        }
        .sev-badge.high { background: rgba(239, 68, 68, 0.1); color: var(--high); border: 1px solid rgba(239, 68, 68, 0.2); }
        .sev-badge.medium { background: rgba(245, 158, 11, 0.1); color: var(--medium); border: 1px solid rgba(245, 158, 11, 0.2); }
        .sev-badge.low { background: rgba(16, 185, 129, 0.1); color: var(--low); border: 1px solid rgba(16, 185, 129, 0.2); }

        .chevron {
            transition: transform 0.3s ease;
            color: var(--text-muted);
        }

        .accordion-item.active .chevron { transform: rotate(180deg); }

        .accordion-item {
            border-bottom: 1px solid rgba(255, 255, 255, 0.03); /* Soft separator */
            transition: var(--transition-flow);
        }

        .accordion-item:hover {
            background: rgba(255,255,255,0.02);
            transform: translateX(4px);
        }

        .accordion-content {
            max-height: 0;
            overflow: hidden;
            transition: max-height 0.2s ease-out, padding 0.2s ease-out;
            background: rgba(0,0,0,0.15);
        }

        .accordion-item.active .accordion-content {
            max-height: 500px;
            padding: 1rem;
        }

        .quick-finding {
            padding: 0.85rem 1rem;
            border-radius: 10px;
            background: rgba(255,255,255,0.015);
            border: 1px solid var(--card-border);
            margin-bottom: 0.75rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            cursor: pointer;
            transition: all 0.2s ease;
            opacity: 0;
            transform: translateY(10px);
            border-left: 3px solid transparent;
        }
        .quick-finding:hover {
            background: rgba(255,255,255,0.04);
            transform: translateX(4px);
            border-color: rgba(255,255,255,0.1);
        }
        .quick-finding.priority-high {
            background: rgba(239, 68, 68, 0.01);
            border-color: rgba(239, 68, 68, 0.05); /* 70% intensity reduction */
        }
        .quick-finding.show {
            opacity: 1;
            transform: translateY(0);
        }

        .cta-button {
            width: 100%; padding: 0.85rem; background: var(--accent); color: #fff; border: none; border-radius: 8px; cursor: pointer; font-size: 0.8rem; font-weight: 700; transition: var(--transition); box-shadow: 0 4px 15px var(--accent-glow);
        }
        .cta-button:hover {
            transform: scale(1.02);
            filter: brightness(1.1);
        }

        /* --- Modal Panel --- */
        .modal-overlay {
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0, 0, 0, 0.7);
            backdrop-filter: blur(8px);
            display: none;
            justify-content: center;
            align-items: center;
            z-index: 1000;
            opacity: 0;
            transition: opacity 0.3s ease;
        }

        .modal-overlay.active { display: flex; opacity: 1; }

        .modal {
            background: rgba(10, 12, 18, 0.95);
            backdrop-filter: blur(20px);
            border: 1px solid var(--card-border);
            border-radius: 20px;
            width: 95%;
            max-width: 960px;
            height: 85vh;
            display: flex;
            flex-direction: column;
            overflow: hidden;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
            transform: translateY(20px) scale(0.98);
            transition: var(--transition);
        }

        .modal-overlay.active .modal { transform: translateY(0) scale(1); }

        .modal-header {
            padding: 1.5rem 2rem;
            border-bottom: 1px solid var(--card-border);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .tabs {
            display: flex;
            gap: 1.5rem;
            padding: 0 2rem;
            background: rgba(255,255,255,0.02);
            border-bottom: 1px solid var(--card-border);
        }

        .tab {
            padding: 1rem 0;
            font-size: 0.85rem;
            font-weight: 600;
            color: var(--text-muted);
            cursor: pointer;
            position: relative;
        }

        .tab.active { color: var(--text-primary); }
        .tab.active::after {
            content: '';
            position: absolute;
            bottom: -1px; left: 0; width: 100%; height: 2px;
            background: var(--accent);
            box-shadow: 0 0 10px var(--accent);
        }

        .modal-scroll {
            flex: 1;
            overflow-y: auto;
            padding: 2rem;
        }

        .finding-detail {
            margin-bottom: 2rem;
            padding: 1.5rem;
            background: rgba(255,255,255,0.02);
            border-radius: 12px;
            border: 1px solid var(--card-border);
        }

        .finding-meta {
            display: flex;
            justify-content: space-between;
            margin-bottom: 1rem;
        }

        .code-block {
            background: #0d1117;
            padding: 1rem;
            border-radius: 8px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.85rem;
            margin-top: 1rem;
            border: 1px solid rgba(255,255,255,0.05);
            position: relative;
        }

        /* --- Animations --- */
        @keyframes pulse {
            0% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.6; transform: scale(1.1); }
            100% { opacity: 1; transform: scale(1); }
        }

        @keyframes slideIn {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* --- Skeletons --- */
        .skeleton {
            background: linear-gradient(90deg, rgba(255,255,255,0.03) 25%, rgba(255,255,255,0.06) 50%, rgba(255,255,255,0.03) 75%);
            background-size: 200% 100%;
            animation: shimmer 1.5s infinite;
        }

        @keyframes shimmer {
            0% { background-position: 200% 0; }
            100% { background-position: -200% 0; }
        }

        /* Responsive Mobile Fixes */
        @media (max-width: 1024px) {
            .stat-card { grid-column: span 6; }
            .chart-card { grid-column: span 12; }
        }
        @media (max-width: 640px) {
            .stat-card { grid-column: span 12; }
            .accordion-trigger { grid-template-columns: 1fr auto; gap: 0.5rem; }
            .accordion-trigger > *:nth-child(2), .accordion-trigger > *:nth-child(3) { display: none; }
            .main-content { padding: 1.5rem; }
        }
    </style>
</head>
<body>

<div class="app-container">
    <main class="main-content">
        <header>
            <div class="logo-section">
                <h1>AI Code Reviewer</h1>
                <p style="color: var(--text-muted); font-size: 0.85rem;">Intelligent Feedback Command Center</p>
            </div>
            <div class="system-status">
                <div class="status-dot"></div>
                <span id="sync-indicator" style="opacity:1; transition:opacity 0.5s;">System Online</span>
                <span style="color: var(--text-muted); margin-left: 0.5rem; border-left: 1px solid var(--card-border); padding-left: 0.5rem;" id="val-uptime">0h 0m</span>
            </div>
        </header>

        <!-- Stats Overview -->
        <div class="grid">
            <div class="card stat-card">
                <div class="stat-label">Total Pull Requests</div>
                <div class="stat-value" id="val-prs">0</div>
                <div class="stat-trend trend-up">↑ Live</div>
            </div>
            <div class="card stat-card">
                <div class="stat-label">Total Issues Detected</div>
                <div class="stat-value" id="val-issues" style="color: var(--high);">0</div>
                <div class="stat-trend" style="color: var(--text-muted);">Active Branch</div>
            </div>
            <!-- Severity Charts -->
            <div class="card chart-card">
                <div class="chart-header">
                    <h3 style="font-size: 1rem;">Severity Breakdown</h3>
                    <span style="font-size: 0.75rem; color: var(--text-muted);">Weighted Analysis</span>
                </div>

                <div class="bar-group">
                    <div class="bar-label"><span>Critical / High</span> <span id="lbl-sev-high">0</span></div>
                    <div class="bar-background"><div class="bar-fill" id="bar-sev-high" style="width: 0%; background: var(--high); box-shadow: 0 0 10px var(--high);"></div></div>
                </div>
                <div class="bar-group">
                    <div class="bar-label"><span>Significant / Medium</span> <span id="lbl-sev-medium">0</span></div>
                    <div class="bar-background"><div class="bar-fill" id="bar-sev-medium" style="width: 0%; background: var(--medium);"></div></div>
                </div>
                <div class="bar-group">
                    <div class="bar-label"><span>Minor / Quality</span> <span id="lbl-sev-low">0</span></div>
                    <div class="bar-background"><div class="bar-fill" id="bar-sev-low" style="width: 0%; background: var(--low);"></div></div>
                </div>
            </div>

            <!-- Issue Type Chart -->
            <div class="card chart-card">
                <div class="chart-header">
                    <h3 style="font-size: 1rem;">Issue Categorization</h3>
                    <span style="font-size: 0.75rem; color: var(--text-muted);">Type Breakdown</span>
                </div>

                <div class="bar-group">
                    <div class="bar-label"><span>Security</span> <span id="lbl-type-security">0</span></div>
                    <div class="bar-background"><div class="bar-fill" id="bar-type-security" style="width: 0%; background: var(--security); box-shadow: 0 0 10px var(--security);"></div></div>
                </div>
                <div class="bar-group">
                    <div class="bar-label"><span>Bugs</span> <span id="lbl-type-bug">0</span></div>
                    <div class="bar-background"><div class="bar-fill" id="bar-type-bug" style="width: 0%; background: var(--bug);"></div></div>
                </div>
                <div class="bar-group">
                    <div class="bar-label"><span>Performance</span> <span id="lbl-type-performance">0</span></div>
                    <div class="bar-background"><div class="bar-fill" id="bar-type-performance" style="width: 0%; background: var(--performance);"></div></div>
                </div>
                <div class="bar-group">
                    <div class="bar-label"><span>Quality</span> <span id="lbl-type-quality">0</span></div>
                    <div class="bar-background"><div class="bar-fill" id="bar-type-quality" style="width: 0%; background: var(--quality);"></div></div>
                </div>
            </div>

            <!-- Analysis Density Chart -->
            <div class="card chart-card">
                <div class="chart-header">
                    <h3 style="font-size: 1rem;">Analysis Density</h3>
                    <span style="font-size: 0.75rem; color: var(--text-muted);">Health Trends</span>
                </div>

                <div class="bar-group">
                    <div class="bar-label"><span>Issues per PR</span> <span id="lbl-density-val">0.0</span></div>
                    <div class="bar-background"><div class="bar-fill" id="bar-density" style="width: 0%; background: var(--accent); box-shadow: 0 0 10px var(--accent-glow);"></div></div>
                </div>
                <div style="margin-top:2rem; padding:1.5rem; border-radius:12px; background:rgba(255,255,255,0.02); border:1px solid var(--card-border);">
                    <div style="font-size:0.75rem; color:var(--text-muted); margin-bottom:0.5rem; text-transform:uppercase; letter-spacing:0.05em;">Security Posture</div>
                    <div style="display:flex; align-items:center; gap:0.75rem;">
                        <div id="security-pulse" class="status-dot" style="width:12px; height:12px;"></div>
                        <span id="security-status-text" style="font-weight:600; font-size:0.9rem;">Monitoring...</span>
                    </div>
                </div>
            </div>
        </div>

        <!-- PR Feed Area -->
        <div class="grid">
            <div class="card feed-container">
                <div class="feed-header">
                    <h3 style="font-size: 1.1rem; font-weight: 600;">Recent PR Activity</h3>
                    <div style="font-size: 0.8rem; color: var(--text-muted);" id="val-last-ts">Last sync: Just now</div>
                </div>

                <div id="accordion-root">
                    <!-- PR items injected here -->
                    <div style="text-align:center; padding: 4rem; color: var(--text-muted);">
                        <p>Waiting for PR payloads...</p>
                    </div>
                </div>
            </div>
        </div>
        <footer style="margin-top: 4rem; padding-top: 2rem; border-top: 1px solid var(--card-border); text-align: center; color: var(--text-muted); font-size: 0.8rem; padding-bottom: 2rem;">
            &copy; 2026 AI Code Reviewer. Powered by Groq &bull; <span id="footer-conn-status">Connected to Backend</span>
        </footer>
    </main>
</div>

<!-- Advanced Modal Panel -->
<div class="modal-overlay" id="modal-overlay" onclick="closeModal()">
    <div class="modal" onclick="event.stopPropagation()">
        <div class="modal-header">
            <div>
                <h2 id="modal-title" style="font-size: 1.25rem;">PR Findings</h2>
                <span id="modal-subtitle" style="font-size: 0.85rem; color: var(--text-muted);">Analysis Report</span>
            </div>
            <button onclick="closeModal()" style="background:none; border:none; color:var(--text-muted); cursor:pointer; font-size:1.5rem;">&times;</button>
        </div>
        <div class="tabs" id="modal-tabs">
            <div class="tab active" onclick="setTab('all')">All Findings</div>
            <div class="tab" onclick="setTab('high')">High</div>
            <div class="tab" onclick="setTab('medium')">Medium</div>
            <div class="tab" onclick="setTab('low')">Low</div>
        </div>
        <div class="modal-scroll" id="modal-scroll">
            <!-- Findings injected here -->
        </div>
    </div>
</div>

<script>
    const state = {
        prs: [],
        currentPR: null,
        activeTab: 'all',
        lastFeedJson: "",
        expandedPRKey: null
    };

    async function fetchStats() {
        try {
            const res = await fetch("/api/stats");

            if (!res.ok) throw new Error(`API Error: ${res.status}`);

            const data = await res.json();
            renderStats(data);

            // Only re-render feed if the data has actually changed
            const currentJson = JSON.stringify(data.recent_reviews);
            if (currentJson !== state.lastFeedJson) {
                state.lastFeedJson = currentJson;
                renderFeed(data.recent_reviews);
            }
        } catch (err) {
            console.error("Dashboard Sync Failed", err);
        }
    }

    function renderStats(data) {
        // Simple count-up logic placeholder
        document.getElementById('val-prs').innerText = data.total_prs;
        document.getElementById('val-issues').innerText = data.total_issues;
        document.getElementById('val-uptime').innerText = data.uptime;

        if (data.last_review_time) {
            const d = new Date(data.last_review_time);
            document.getElementById('val-last-ts').innerText = "Last sync: " + d.toLocaleTimeString();
        }

        const total = Math.max(1, (data.issues_by_severity.high || 0) + (data.issues_by_severity.medium || 0) + (data.issues_by_severity.low || 0));
        updateBar('sev-high', data.issues_by_severity.high || 0, total);
        updateBar('sev-medium', data.issues_by_severity.medium || 0, total);
        updateBar('sev-low', data.issues_by_severity.low || 0, total);

        const typeTotal = Math.max(1, Object.values(data.issues_by_type || {}).reduce((a, b) => a + b, 0));
        updateBar('type-security', data.issues_by_type.security || 0, typeTotal);
        updateBar('type-bug', data.issues_by_type.bug || 0, typeTotal);
        updateBar('type-performance', data.issues_by_type.performance || 0, typeTotal);
        updateBar('type-quality', data.issues_by_type.quality || 0, typeTotal);

        // Density Logic
        const density = data.total_prs > 0 ? (data.total_issues / data.total_prs).toFixed(1) : 0;
        document.getElementById('lbl-density-val').innerText = density;
        document.getElementById('bar-density').style.width = Math.min(100, (density / 10) * 100) + '%';

        // Security Pulse Update
        const secDot = document.getElementById('security-pulse');
        const secText = document.getElementById('security-status-text');
        if (data.issues_by_type.security > 0) {
            secDot.style.background = 'var(--high)';
            secDot.style.boxShadow = '0 0 10px var(--high)';
            secText.innerText = "Critical Security Risks Detected";
            secText.style.color = 'var(--high)';
        } else {
            secDot.style.background = 'var(--low)';
            secDot.style.boxShadow = '0 0 10px var(--low)';
            secText.innerText = "Baseline Security Intact";
            secText.style.color = 'var(--low)';
        }
    }

    function updateBar(id, val, total) {
        document.getElementById(`lbl-${id}`).innerText = val;
        document.getElementById(`bar-${id}`).style.width = (val / total * 100) + '%';
    }

    /**
     * [SECURITY FIX] XSS Mitigation
     * Escapes AI-generated content to prevent cross-site scripting
     */
    function safe(str) {
        if (!str) return "";
        const div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    }



    function renderFeed(reviews) {
        if (!reviews || reviews.length === 0) return;

        const root = document.getElementById('accordion-root');

        root.innerHTML = '';

        reviews.forEach((rv, idx) => {
            const prKey = `${rv.repo}#${rv.pr_number}`;
            const isExpanded = state.expandedPRKey === prKey;

            const item = document.createElement('div');

            const riskLevel = rv.decision === "BLOCK" ? "High" : (rv.decision === "REVIEW" ? "Moderate" : (rv.decision === "PERFECT" ? "Zero" : "Low"));
            const riskClass = riskLevel.toLowerCase();

            // Status Badge Logic
            let statusLabel = 'Review Complete';
            let statusBadgeClass = 'badge-status';
            let insightText = "";
            let confidenceIndicator = "";

            if (!rv.status || rv.status === 'error') {
                statusLabel = '🚫 BLOCK';
                statusBadgeClass = 'badge-failed';
                insightText = `<span style="color:var(--high); font-weight:700;">SYSTEM ERROR</span>: Analysis failed or was blocked. Manual review is MANDATORY.`;
                confidenceIndicator = "🚫 BLOCK MERGE";
            } else if (rv.status === 'partial') {
                statusLabel = '⚠️ BLOCK (Partial)';
                statusBadgeClass = 'badge-partial';
                insightText = `Analysis is <span style="color:var(--medium); font-weight:700;">incomplete</span>. Safe state cannot be verified. Manual review required.`;
                confidenceIndicator = "🚫 BLOCK MERGE";
            } else {
                if (rv.decision === 'BLOCK') {
                    insightText = `This PR contains <span style="color:#fff; font-weight:700; text-decoration: underline decoration-color:var(--high);">critical security risks</span> that should be <span style="color:var(--high); font-weight:700;">fixed</span> before merging.`;
                    confidenceIndicator = "🚫 BLOCK MERGE";
                } else if (rv.decision === 'REVIEW') {
                    insightText = `This PR has moderate issues that require a <span style="color:#fff; font-weight:700; text-decoration: underline decoration-color:var(--medium);">manual review</span> before proceeding.`;
                    confidenceIndicator = "⚠️ NEEDS REVIEW";
                } else if (rv.decision === 'PERFECT') {
                    insightText = `No issues detected. This code is <span style="color:var(--quality); font-weight:700;">clean</span> and ready for deployment.`;
                    confidenceIndicator = "VERIFIED";
                } else if (rv.decision === 'SAFE') {
                    insightText = `Only minor quality improvements detected. PR is <span style="color:var(--low); font-weight:700;">SAFE TO MERGE</span>.`;
                    confidenceIndicator = "✅ SAFE TO MERGE";
                } else {
                    insightText = `<span style="color:var(--high); font-weight:700;">UNKNOWN STATE</span>: Defaulting to BLOCK for safety.`;
                    confidenceIndicator = "🚫 BLOCK MERGE";
                }
            }

            item.className = 'accordion-item' + ((rv.severities.high || 0) > 0 ? ' has-high' : '') + (isExpanded ? ' active' : '');
            if (isExpanded) {
                setTimeout(() => {
                    item.querySelectorAll('.quick-finding').forEach(f => f.classList.add('show'));
                }, 10);
            }

            const sortedIssues = [...(rv.issues || [])].sort((a, b) => {
                const order = { 'high': 0, 'medium': 1, 'low': 2, 'quality': 3 };
                return (order[a.severity.toLowerCase()] ?? 99) - (order[b.severity.toLowerCase()] ?? 99);
            });

            item.innerHTML = `
                <button class="accordion-trigger" onclick="toggleAccordion(this)">
                    <div class="pr-info">
                        <strong>
                            ${rv.repo} <span style="color:var(--text-muted); font-weight:400;">#${rv.pr_number}</span>
                            <div class="risk-badge ${riskClass}">
                                <div class="risk-dot"></div>
                                ${riskLevel} Risk
                                <span class="confidence-label">&bull; ${confidenceIndicator}</span>
                            </div>
                        </strong>
                        <span class="pr-meta">Last evaluated &bull; ${new Date(rv.reviewed_at).toLocaleTimeString()}</span>
                    </div>
                    <div class="tag-pill" style="margin-right: 1.5rem; opacity: 0.8;">
                        ${(rv.severities.high || 0) > 0 ? `<div class="sev-badge high" style="padding:1px 6px;">HIGH ${rv.severities.high}</div>` : ''}
                        ${(rv.severities.medium || 0) > 0 ? `<div class="sev-badge medium" style="padding:1px 6px;">MED ${rv.severities.medium}</div>` : ''}
                        ${(rv.severities.low || 0) > 0 ? `<div class="sev-badge low" style="padding:1px 6px;">LOW ${rv.severities.low}</div>` : ''}
                    </div>
                    <div class="badge ${statusBadgeClass}">${statusLabel}</div>
                    <div class="chevron">
                        <svg width="20" height="20" viewBox="0 0 20 20" fill="none"><path d="M5 7.5L10 12.5L15 7.5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
                    </div>
                </button>
                <div class="accordion-content">
                    <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--card-border); padding: 1.25rem; border-radius: 12px; margin-bottom: 1.5rem;">
                         <div style="font-size:0.85rem; color:var(--text-muted); margin-bottom:0.5rem; font-weight:600; text-transform:uppercase; letter-spacing:0.05em;">Actionable Insight</div>
                         <div style="font-size:1.05rem; font-weight:500; color: var(--text-primary); opacity: 0.95;">
                            ${insightText}
                         </div>
                    </div>

                    <div style="font-size:0.75rem; color:var(--text-muted); margin-bottom:1rem; font-weight:600; text-transform:uppercase; letter-spacing:0.05em;">Categorized Findings Summary</div>
                    <div class="quick-findings-group">
                        ${sortedIssues.slice(0, 3).map((i, sIdx) => `
                            <div class="quick-finding ${i.severity.toLowerCase() === 'high' ? 'priority-high' : ''}" style="animation-delay: ${sIdx * 50}ms;" onclick="openDetails(${JSON.stringify(rv).replace(/"/g, '&quot;')})">
                                <span style="font-weight:500; display:flex; align-items:center;">
                                    ${i.severity.toLowerCase() === 'high' ? '🚨' : (i.severity.toLowerCase() === 'medium' ? '⚠️' : 'ℹ️')}
                                    <span style="margin-left:8px;">${safe(i.title || i.type)}</span>
                                </span>
                                <div style="font-size:0.85rem; opacity:0.8; margin-top:4px; line-height:1.4;">
                                    ${safe(i.description)}
                                </div>
                            </div>
                        `).join('')}
                    </div>
                    ${rv.issue_count > 3 ? `<div style="text-align:center; margin-bottom:1.2rem; font-size:0.8rem; color:var(--text-muted); font-style:italic; padding-top: 0.5rem;">+ ${rv.issue_count - 3} more context-aware findings</div>` : ''}
                    <button class="cta-button" onclick="openDetails(${JSON.stringify(rv).replace(/"/g, '&quot;')})">View Full Analysis &raquo;</button>
                </div>
            `;
            root.appendChild(item);
        });
    }

    function toggleAccordion(btn) {
        state.forceUpdate = true;
        const item = btn.parentElement;
        const isActive = item.classList.contains('active');

        // Close all others
        document.querySelectorAll('.accordion-item').forEach(el => {
            el.classList.remove('active');
            el.querySelectorAll('.quick-finding').forEach(f => f.classList.remove('show'));
        });

        if (!isActive) {
            item.classList.add('active');
            // Save state for persistence across refreshes
            const head = item.querySelector('.pr-info strong').innerText;
            const prNum = head.match(/#(\d+)/)[1];
            const repo = head.split('#')[0].trim();
            state.expandedPRKey = `${repo}#${prNum}`;

            // Staggered show for findings
            const findings = item.querySelectorAll('.quick-finding');
            findings.forEach((f, idx) => {
                setTimeout(() => f.classList.add('show'), idx * 50);
            });
        } else {
            state.expandedPRKey = null;
        }
    }

    function openDetails(rv) {
        state.currentPR = rv;
        state.activeTab = 'all';
        document.getElementById('modal-title').innerText = `${rv.repo} #${rv.pr_number}`;
        renderModalFindings();
        updateTabUI();
        document.getElementById('modal-overlay').classList.add('active');
    }

    function closeModal() {
        document.getElementById('modal-overlay').classList.remove('active');
    }

    function setTab(tab) {
        state.activeTab = tab;
        updateTabUI();
        renderModalFindings();
    }

    function updateTabUI() {
        const tabs = document.querySelectorAll('.tab');
        tabs.forEach(t => {
            t.classList.remove('active');
            if (t.innerText.toLowerCase().includes(state.activeTab)) t.classList.add('active');
        });
    }

    function renderModalFindings() {
        const container = document.getElementById('modal-scroll');
        container.innerHTML = '';

        let issues = state.currentPR.issues || [];
        if (state.activeTab !== 'all') {
            issues = issues.filter(i => i.severity.toLowerCase() === state.activeTab);
        }

        // Elite Sorting: High > Medium > Low
        issues = [...issues].sort((a, b) => {
            const order = { 'high': 0, 'critical': 0, 'medium': 1, 'low': 2, 'quality': 3 };
            return (order[a.severity.toLowerCase()] ?? 99) - (order[b.severity.toLowerCase()] ?? 99);
        });

        if (issues.length === 0) {
            container.innerHTML = `<div style="text-align:center; padding:3rem; color:var(--text-muted);">No ${state.activeTab} issues found in this scope.</div>`;
            return;
        }

        issues.forEach(i => {
            const card = document.createElement('div');
            card.className = 'finding-detail';
            card.style.borderLeft = `4px solid ${getSevColor(i.severity)}`;

            card.innerHTML = `
                <div class="finding-meta">
                    <span class="badge" style="background: ${getSevColor(i.severity)}22; color: ${getSevColor(i.severity)}; border:1px solid ${getSevColor(i.severity)}44;">${i.severity.toUpperCase()}</span>
                    <span style="font-family:monospace; font-size:0.85rem; color:var(--text-muted);">${safe(i.file)} : L${i.line}</span>
                </div>
                <div style="font-weight:600; margin-bottom:1rem; font-size:1.05rem;">${safe(i.description)}</div>
                <div class="code-block" style="box-shadow: inset 0 0 20px rgba(0,0,0,0.5);">
                    <div style="color:var(--text-muted); position:absolute; right:1rem; top:0.5rem; font-size:0.7rem; font-weight:700; letter-spacing:0.05em;">CODE CONTEXT</div>
                    <pre><code class="language-python">${safe(i.fix)}</code></pre>
                </div>
            `;
            container.appendChild(card);
        });
    }

    function getSevColor(sev) {
        const s = sev.toLowerCase();
        if (s === 'high' || s === 'critical') return '#ef4444';
        if (s === 'medium') return '#f59e0b';
        return '#10b981';
    }

    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    // Initial load effects
    window.addEventListener('DOMContentLoaded', () => {
        document.body.classList.add('loaded');
        fetchStats();
    });

    setInterval(fetchStats, 3000);
</script>

</body>
</html>

`

