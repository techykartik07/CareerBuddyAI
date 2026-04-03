import re


def extract_email(text: str) -> str | None:
    """Return the first email address found in text."""
    matches = re.findall(r'[\w.+-]+@[\w-]+\.[a-zA-Z]+', text)
    return matches[0] if matches else None


def extract_phone(text: str) -> str | None:
    """Return the first phone number found in text."""
    matches = re.findall(r'[\+\(]?[0-9][0-9\s\-\(\)]{7,}[0-9]', text)
    return matches[0].strip() if matches else None


def extract_name(text: str) -> str | None:
    """
    Best-effort name extraction: assumes the name is on the first
    non-empty line of the resume.
    """
    for line in text.splitlines():
        stripped = line.strip()
        if stripped:
            return stripped
    return None


def extract_contact_info(text: str) -> dict:
    """Return a dict with name, email, and phone extracted from text."""
    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
    }
