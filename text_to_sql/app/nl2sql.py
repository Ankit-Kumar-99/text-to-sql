from app.prompts import sql_generation_prompt, sql_review_prompt
from app.gemini_client import call_gemini
from app.validator import check_sql
from app.config import ALLOWED_TABLE


def generate_valid_sql(question: str) -> str:
    """
    Production NL → SQL pipeline:

    Step 1: Generate SQL
    Step 2: Review + improve SQL
    Step 3: If forbidden GA4 schema appears, auto-retry once
    """

    # ----------------------------
    # Step 1: Generate SQL
    # ----------------------------
    sql_query = call_gemini(sql_generation_prompt(question))

    reason = check_sql(sql_query)
    if reason:
        raise ValueError(f"Generated SQL rejected: {reason}")

    # ----------------------------
    # Step 2: Review SQL
    # ----------------------------
    final_sql = call_gemini(sql_review_prompt(question, sql_query))

    reason = check_sql(final_sql)

    # ----------------------------
    # Step 3: Auto-Retry if Forbidden Schema Detected
    # ----------------------------
    if reason and "Forbidden GA4 nested schema" in reason:
        retry_prompt = f"""
You generated SQL using forbidden GA4 raw export fields.

Fix the SQL using ONLY this flattened table:

`{ALLOWED_TABLE}`

Rules:
- Do NOT use UNNEST
- Do NOT use event_params
- Use campaign column directly
- Use purchase_value column directly
- Return ONLY SQL

Question:
{question}
"""
        final_sql = call_gemini(retry_prompt)

        reason2 = check_sql(final_sql)
        if reason2:
            raise ValueError(f"Retry SQL rejected: {reason2}")

    # ----------------------------
    # Final Validation
    # ----------------------------
    if reason:
        raise ValueError(f"Final SQL rejected: {reason}")

    return final_sql
