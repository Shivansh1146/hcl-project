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
        description = issue.get("description", "")

        # 1. Identity Check: Reject if the fix is identical to the old code
        if fix == old:
            logger.warning(f"🚫 HALLUCINATION DETECTED: AI suggested a fix that is identical to the existing code at line {issue.get('line')}.")
            return False

        # 2. Semantic Identity: Reject if they only differ by whitespace
        if "".join(fix.split()) == "".join(old.split()):
            logger.warning(f"🚫 HALLUCINATION DETECTED: Fix only differs by whitespace at line {issue.get('line')}.")
            return False

        # 3. Description Hallucination Check:
        # If the description claims the code is "X" but it's actually "Y", reject it.
        # We look for backticked code in the description.
        desc_snippets = re.findall(r'`([^`]+)`', description)
        for snippet in desc_snippets:
            # If the AI claims the code says something that isn't in the original line
            if len(snippet) > 4 and snippet not in old and snippet not in fix:
                logger.warning(f"🚫 HALLUCINATION DETECTED: Description mentions code `{snippet}` which is not in the original line or fix.")
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
        
        # Keywords to look for (longer than 2 chars to avoid 'is', 'if', etc.)
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
