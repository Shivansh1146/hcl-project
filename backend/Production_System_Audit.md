# Production-Level System Audit Report: AI Code Reviewer

🔴 **CRITICAL BUGS**
* **Signature Bypass**: `verify_signature` does not abort processing if `GITHUB_WEBHOOK_SECRET` is missing. It logs a warning but returns `None`, allowing unauthenticated payloads to proceed to the analysis pipeline.
    * *Location*: `backend/main.py`
    * *Reason*: The function lacks an `raise HTTPException` or return value check in the caller.
    * *Impact*: Exposure to mock webhook attacks and unauthorized analysis costs.
* **Silent Partial Processing**: If a large PR is split into chunks and some chunks fail (e.g., 429 Rate Limit), the system returns `"partial"` but `process_webhook` treats this as `"success"`.
    * *Location*: `backend/services/ai_service.py` & `backend/main.py`
    * *Reason*: The `try...except` block in the pipeline incorrectly classifies partial successes as a total success.
    * *Impact*: Vulnerabilities in unreviewed chunks are permanently ignored as the SHA is marked "completed".
* **SHA Lockout**: If a crash occurs between `claim_sha_for_processing` and `initiate_review`, the SHA is stuck in `pending` for 30 minutes with no record in the PR dashboard.
    * *Location*: `backend/stats_store.py`
    * *Reason*: Non-atomic transition between SHA claiming and PR record creation.
    * *Impact*: Total system silence for the developer on updated PRs with no way to force a retry.

🟡 **LOGIC FLAWS**
* **Dashboard Flicker**: The UI clears the entire list container (`root.innerHTML = ''`) every 3 seconds before the API response returns.
    * *Location*: `backend/static/index.html`
    * *Reason*: Naive polling implementation without virtual DOM or state diffing.
    * *Impact*: Poor user experience; dashboard appears to "blink" or stay empty during high API latency.
* **Stat Contamination**: Global severity metrics include issues from PRs that ultimately failed or were aborted.
    * *Location*: `backend/stats_store.py`
    * *Reason*: `get_stats` aggregates all rows in `issues` without joining the `prs` table to check the final `status`.
    * *Impact*: Misleading decision intelligence; stats reflect "ghost issues" that were never actually reported.

🟢 **EDGE CASE FAILURES**
* **Chunk Context Loss**: `_get_line_aware_chunks` splits diffs at arbitrary character boundaries. If a file header or hunk is split, the AI loses the context of the filename and line offsets for that chunk.
    * *Location*: `backend/services/ai_service.py`
    * *Reason*: Chars-based splitting versus semantic hunk-based splitting.
    * *Impact*: High rate of "No suggestions found" or broken line mapping for large files.
* **Empty Diff Over-Blocking**: PRs with only metadata/comment changes result in an empty diff which triggers a `BLOCK` decision by default.
    * *Location*: `backend/main.py`
    * *Reason*: Fail-to-BLOCK logic does not distinguish between "Process Error" and "Nothing to Review".
    * *Impact*: Unnecessary developer friction for non-code updates.

⚠️ **SILENT FAILURES**
* **Syntax Over-Pruning**: Valid security risks are silently discarded if the AI includes conversational prefixes (e.g., "Refactored: pass") that fail the Python parser.
    * *Location*: `backend/main.py`
    * *Reason*: `SyntaxValidator` uses binary pass/fail without attempt at heuristic cleaning.
    * *Impact*: Critical vulnerabilities are identified by AI but never reach the developer because of formatting noise.
