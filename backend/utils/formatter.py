import json
from typing import Dict, Any, List

class Formatter:
    """Utility class for formatting data structures."""

    @staticmethod
    def format_review_comment(analysis_result: Dict[str, Any]) -> str:
        """Formats the AI analysis result into a markdown-friendly PR comment."""
        formatted_json = json.dumps(analysis_result, indent=2)
        return f"### AI Code Review\n\n```json\n{formatted_json}\n```"

    @staticmethod
    def format_error(error_message: str) -> Dict[str, str]:
        """Standardizes error response formatting."""
        return {
            "error": True,
            "message": error_message
        }

def format_comment(issues: List[Dict[str, Any]]) -> str:
    """Formats the filtered issues into a Markdown comment for GitHub PR."""
    if not issues:
        return "### AI Code Review\n\nNo significant bug or security issues found! Code looks clean."

    comment = "### AI Code Review Analyzer\n\n"
    for idx, issue in enumerate(issues, 1):
        severity = str(issue.get("severity", "medium")).upper()
        type_ = str(issue.get("type", "unknown")).capitalize()
        desc = issue.get("description", "")
        fix = issue.get("fix", "")

        comment += f"**{idx}. [{severity}] {type_}**\n"
        comment += f"**Issue:** {desc}\n\n"
        comment += f"**Recommended Fix:**\n```python\n{fix}\n```\n\n---\n"

    return comment

def format_inline_issue(issue: Dict[str, Any]) -> str:
    """Formats a single issue for an inline GitHub string comment."""
    severity = str(issue.get("severity", "medium")).upper()
    desc = issue.get("description", "")
    fix = issue.get("fix", "")

    comment = f"🔍 **AI Review ({severity})**\n\n"
    comment += f"**Problem:**\n{desc}\n\n"
    comment += f"**Fix:**\n```suggestion\n{fix}\n```"

    return comment
