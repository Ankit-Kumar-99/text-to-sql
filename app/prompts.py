def intent_prompt(question: str) -> str:
    return f"""
You are a marketing analytics expert.

Extract structured intent from the question.

Return STRICT JSON only.

FORMAT:
{{
  "tables_required": [],
  "columns_required": [],
  "aggregations": [],
  "filters": [],
  "group_by": [],
  "order_by": "",
  "limit": null,
  "joins_required": true/false
}}

Rules:
- Only include necessary tables.
- If multiple tables → joins_required = true
- Return valid JSON only.

Question:
{question}
"""


def sql_prompt(question: str, intent_json: dict, schema_text: str) -> str:
    return f"""
You are an expert SQL generator.

Return ONLY SQL.
No explanation.
No markdown.
No backticks.

=============================
DATABASE SCHEMA:
{schema_text}
=============================

USER QUESTION:
{question}

INTENT:
{intent_json}

CRITICAL RULES:
- Respect table grain.
- campaign_performance is campaign-level.
- email_events and web_analytics are event-level.
- If multiple fact tables:
  1) Aggregate separately
  2) Then join
- Never join raw fact tables directly.
- Use correct column names.
"""
