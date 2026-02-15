from app.config import ALLOWED_TABLE
from app.schema import VALID_EVENT_NAMES, SCHEMA_COLUMNS

BASE_CONTEXT = f"""
You are a senior analytics engineer and BigQuery SQL expert.

Task:
Convert natural language marketing questions into correct BigQuery SQL.

Database Table (Flattened):
`{ALLOWED_TABLE}`

Columns:
{", ".join(SCHEMA_COLUMNS)}

Important Notes:
- This is a FLATTENED table.
- Do NOT use GA4 nested fields like event_params.
- Do NOT use UNNEST().
- Valid event_name values: {", ".join(VALID_EVENT_NAMES)}

Rules:
- Return ONLY SQL (no markdown, no explanation)
- Only SELECT queries allowed
- Use COUNT(*) instead of COUNT(column)
- Use CTEs if multi-step logic is required
"""


def sql_generation_prompt(question: str) -> str:
    return f"""
{BASE_CONTEXT}

User Question:
{question}

Return ONLY the SQL query:
"""


def sql_review_prompt(question: str, sql_query: str) -> str:
    return f"""
You are a SQL reviewer.

Question:
{question}

Generated SQL:
{sql_query}

Checklist:
- Fully answers the question
- Uses only allowed schema columns
- Avoids forbidden GA4 nested fields
- Uses correct filters and aggregations

If incorrect, rewrite SQL.

Return ONLY final SQL:
"""
