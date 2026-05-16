def reverse_string(s: str) -> str:
    # LOW BUG: Missing docstring
    return s[::-1]


def capitalize_words(s: str) -> str:
    # LOW BUG: Missing docstring
    return " ".join(w.capitalize() for w in s.split())
