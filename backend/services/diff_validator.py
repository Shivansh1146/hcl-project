import re
import logging

logger = logging.getLogger("backend")

class DiffValidator:
    """Parses unified diffs to validate AI-suggested line mappings."""

    @staticmethod
    def parse_diff_mapping(diff_text: str) -> dict:
        """
        Parses a unified diff and returns a mapping of {file_path: set(added_line_numbers)}.
        This is used to verify that AI isn't hallucinating line numbers.
        """
        mapping = {}
        current_file = None
        current_line_in_file = 0

        lines = diff_text.splitlines()
        for line in lines:
            # Detect file header
            if line.startswith("+++ b/"):
                current_file = line[6:]
                mapping[current_file] = set()
                continue

            # Detect hunk header: @@ -start,len +start,len @@
            hunk_match = re.match(r"^@@ -\d+,\d+ \+(\d+),\d+ @@", line)
            if hunk_match:
                current_line_in_file = int(hunk_match.group(1))
                continue

            if current_file:
                if line.startswith("+"):
                    # This is an added/modified line
                    mapping[current_file].add(current_line_in_file)
                    current_line_in_file += 1
                elif line.startswith("-"):
                    # This is a removed line (doesn't count towards new line numbers)
                    continue
                else:
                    # Context line
                    current_line_in_file += 1

        return mapping

    @staticmethod
    def validate_issue(issue: dict, mapping: dict) -> bool:
        """Checks if the issue's file and line exist in the diff mapping."""
        file_path = issue.get("file")
        try:
            line_num = int(issue.get("line", -1))
        except (ValueError, TypeError):
            return False

        if not file_path or file_path not in mapping:
            logger.warning(f"[DiffValidator] File not in diff: {file_path}")
            return False

        if line_num not in mapping[file_path]:
            logger.warning(f"[DiffValidator] Line {line_num} not in added lines for {file_path}")
            return False

        return True
