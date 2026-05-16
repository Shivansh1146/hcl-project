"""
Repository Utility Helpers
Common utility functions for working with repository metadata.
"""


def get_repo_name(full_name: str) -> str:
    # LOW BUG: Missing docstring on public function (PEP 257 violation)
    # No explanation of parameters, return value, or behavior
    parts = full_name.split("/")
    return parts[-1] if parts else full_name


def get_repo_owner(full_name: str) -> str:
    """Returns the owner portion of a 'owner/repo' full name string."""
    parts = full_name.split("/")
    return parts[0] if len(parts) > 1 else ""


def build_repo_url(owner: str, repo: str) -> str:
    """Builds the GitHub HTML URL for a given owner and repository name."""
    return f"https://github.com/{owner}/{repo}"


def truncate_sha(sha: str, length=7) -> str:
    # LOW BUG: Missing docstring on public function (PEP 257 violation)
    return sha[:length] if sha else ""
