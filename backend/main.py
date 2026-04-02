import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Ensure requirements specify exact functions
from services.github_service import extract_pr_data, fetch_diff, post_comment, post_inline_comment
from services.ai_service import analyze_code
from services.filter_service import parse_and_filter_issues
from utils.formatter import format_comment, format_inline_issue

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s"
)

app = FastAPI(
    title="Project API",
    description="Backend API for the full-stack project.",
    version="1.0.0"
)

# CORS configuration for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory deduplication set for processed commit SHAs
processed_shas = set()

@app.get("/api/health")
async def health_check():
    """Health check endpoint to verify backend status."""
    return {"status": "healthy"}

@app.get("/api/info")
async def get_info():
    """Returns some generic info to display on the frontend."""
    return {
        "message": "Welcome to the API!",
        "services": ["github", "ai", "filter"]
    }

@app.post("/webhook")
async def webhook(request: Request):
    """Full AI Code Review pipeline webhook endpoint."""
    try:
        payload = await request.json()
        print("[webhook] Payload received")

        # Stage 1
        if "pull_request" not in payload:
            return {"status": "ignored", "reason": "No pull_request in payload"}

        # Stage 2
        action = payload.get("action")
        if action not in ["opened", "synchronize"]:
            print(f"[webhook] Skipping action: {action}")
            return {"status": "ignored", "reason": f"Skipping action: {action}"}

        # Stage 3
        owner, repo, pr_number = extract_pr_data(payload)

        # SHA Deduplication Tracking
        head_sha = payload.get("pull_request", {}).get("head", {}).get("sha")
        if not head_sha:
            return {"status": "error", "reason": "No commit SHA found in payload"}

        if head_sha in processed_shas:
            print(f"[webhook] SHA {head_sha} already processed — duplicate skipped")
            return {"status": "duplicate skipped"}
        processed_shas.add(head_sha)

        print("[webhook] PR detected")

        # Stage 4
        diff = fetch_diff(owner, repo, pr_number)
        if not diff:
            print("[webhook] Empty diff — skipping")
            return {"status": "no changes"}
        print("[fetch_diff] success")

        # Stage 5
        analysis_result = analyze_code(diff)
        print("[analyze_code] success")

        # Stage 6
        issues = parse_and_filter_issues(analysis_result)

        # Stage 7
        if not issues:
            print("[webhook] No issues found — skipping comment")
            return {"status": "clean"}

        # Stage 8 & 9 & 10
        success_count = 0
        for issue in issues:
            formatted_body = format_inline_issue(issue)
            issue["formatted_body"] = formatted_body
            if post_inline_comment(owner, repo, pr_number, issue, head_sha):
                print("[post_inline_comment] success")
                success_count += 1
            else:
                print("[post_inline_comment] error")

        if success_count > 0:
            print("[webhook] successfully posted inline comments")
            return {"status": "success", "issues_commented": success_count}
        else:
            return {"status": "error", "reason": "Failed to post inline comments"}

    except Exception as e:
        print(f"[webhook] error: {str(e)}")
        return {"status": "error", "message": str(e)}
