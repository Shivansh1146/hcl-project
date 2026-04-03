import re

def validate_all_issues(issues, diff):
    """
    Cross-checks the LLM's hallucinated variable names and types
    against the actual code in the git diff.
    """
    validated = []

    # Extract only added/modified lines to check what variables actually exist
    diff_lines = [line[1:].strip() for line in diff.split('\n') if (line.startswith('+') and not line.startswith('+++'))]
    diff_text = "\n".join(diff_lines)

    for issue in issues:
        desc = issue.get("description", "")
        fix = issue.get("fix", "")

        # 1. Type Corrector for Secrets
        secret_keywords = ["API_KEY", "AWS_SECRET", "TOKEN", "PASSWORD", "SECRET_KEY"]
        if any(keyword in fix or keyword in desc for keyword in secret_keywords):
            # Override wrong typing (like "weak password" being tagged as a logic bug)
            issue["type"] = "security"

        # 2. Variable Hallucination Corrector
        # If the LLM says "password = ..." but the actual code diff says "API_KEY = ..."
        # we try to catch that hallucination.
        for line in diff_lines:
            if " = " in line:
                var_name = line.split(" = ")[0].strip()
                if any(sec in var_name.upper() for sec in ["API_KEY", "SECRET", "PASS"]):
                    # If we find a real secret variable in the diff, and the LLM used something else in the fix:
                    if "password =" in fix.lower() and var_name.lower() != "password":
                        issue["fix"] = fix.replace("password", var_name)
                        issue["description"] = desc.replace("password", var_name)
                    if "password = " in fix and var_name != "password":
                        issue["fix"] = fix.replace("password = ", f"{var_name} = ")

        validated.append(issue)

    return validated
