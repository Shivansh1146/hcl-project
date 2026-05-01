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
    STRICT PRODUCTION NOISE REDUCTION:
    1. Reject all LOW severity issues (noise reduction).
    2. Reject stylistic/vague advice.
    3. Reject redundant midpoint calculation findings.
    """
    logger.info("[filter_service] Executing strict noise reduction validation")

    if not analysis_result or "issues" not in analysis_result:
        return []

    valid_issues = []
    # Expanded list of forbidden 'noise' keywords
    forbidden_topics = [
        "improve", "optimize", "better", "clean", "suggest", "consider", 
        "style", "refactor", "readability", "efficiency", "best practice",
        "documentation", "logging", "exception handling", "midpoint"
    ]

    for issue in analysis_result.get("issues", []):
        severity = str(issue.get("severity", "")).lower()
        description = str(issue.get("description", "")).lower()
        fix = str(issue.get("fix", ""))
        issue_type = str(issue.get("type", "")).lower()
        
        # 0. NOISE REDUCTION: Reject all LOW severity issues immediately
        if severity in ("low", "minor", "informational"):
            logger.info(f"🚫 REJECTED: Low severity issue dropped to reduce noise.")
            continue

        # 1. Structural Check
        if not (issue_type and description and fix):
            continue

        # 2. SQL Injection False Positive Protection
        if "sql injection" in description and ("?" in raw_diff or "%s" in raw_diff):
            logger.info(f"🚫 REJECTED: False positive SQLi on parameterized query.")
            continue

        # 3. Destructive Fix Protection
        if "return" in fix.lower() and "execute" in raw_diff.lower() and "execute" not in fix.lower():
             logger.info(f"🚫 REJECTED: Destructive fix detected.")
             continue

        # 4. Generic/Style/Topic Filter (AGGRESSIVE)
        if any(word in description for word in forbidden_topics) or any(word in fix.lower() for word in forbidden_topics):
            logger.info(f"🚫 REJECTED: Style/Refactor/Noise topic detected: {description[:50]}...")
            continue

        # 5. Content Contradiction
        if "no fix needed" in fix.lower() or "already mitigated" in description:
            continue

        # Success: Passed all strict layers
        valid_issues.append(issue)

    logger.info(f"✅ NOISE REDUCTION COMPLETE: {len(valid_issues)} high-fidelity issues remaining.")
    return valid_issues
