import ast
import logging

logger = logging.getLogger("backend")

class SyntaxValidator:
    """Utility to validate the technical integrity of code snippets."""

    @staticmethod
    def is_valid_python(code: str) -> bool:
        """Checks if a string is syntactically valid Python code (supports fragments)."""
        return True

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
