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

def parse_and_filter_issues(analysis_result: dict) -> list:
    """Extracts and filters valid issues from AI analysis using a strict scoring system."""
    logger.info("[filter_service] Filtering issues")
    if not analysis_result or "issues" not in analysis_result:
        return []

    vague_words = ["improve", "optimize", "better", "clean"]

    valid_issues = []
    for issue in analysis_result.get("issues", []):
        if issue.get("type") and issue.get("description") and issue.get("fix"):
            score = 0
            severity = str(issue.get("severity", "")).lower()
            description = str(issue.get("description", "")).lower()

            # Apply Scoring Logic
            if severity == "high":
                score += 2

            if len(description) > 30:
                score += 1

            if any(word in description for word in vague_words):
                score -= 2

            # Filter boundary
            if score >= 1:
                valid_issues.append(issue)
            else:
                logger.info(f"[filter_service] Issue rejected, score [{score}] too low. Substring: {description[:40]}...")

    return valid_issues
