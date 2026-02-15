from app.config import ALLOWED_TABLE

FORBIDDEN_PATTERNS = [
    "UNNEST",
    "EVENT_PARAMS",
    "USER_PROPERTIES",
    "INFORMATION_SCHEMA"
]

BLOCKED_KEYWORDS = [
    "DROP", "DELETE", "UPDATE", "INSERT",
    "ALTER", "TRUNCATE", "MERGE"
]


def check_sql(sql: str):
    upper_sql = sql.upper()

    if any(word in upper_sql for word in BLOCKED_KEYWORDS):
        return "Unsafe SQL detected"

    if any(pat in upper_sql for pat in FORBIDDEN_PATTERNS):
        return "Forbidden GA4 nested schema detected"

    if ALLOWED_TABLE not in sql:
        return f"Query must reference only `{ALLOWED_TABLE}`"

    return None
