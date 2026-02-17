def sql_prompt(question: str, intent_json: str, schema_text: str) -> str:
    return f"""
You are an expert SQL generator for marketing analytics.

Return ONLY SQL.
No explanation.
No markdown.
No backticks.

=============================
DATABASE SCHEMA:
{schema_text}
=============================

TABLE GRAIN DEFINITIONS:

- paid_media_events_new → campaign-level paid media performance
- crm_campaign_events → CRM campaign event-level data
- ga4_events → website event-level analytics data

IMPORTANT COLUMN NOTES:

- Sessions = COUNT(DISTINCT ga4_events.session_id)
- Revenue = SUM(ga4_events.purchase_value)
- Spend = SUM(paid_media_events_new.spend)
- Conversions = SUM(paid_media_events_new.conversions)
- Device in GA4 = device_category
- Device in paid media = device
- Country in GA4 = geo_country
- Country in paid media = country

=============================

USER QUESTION:
{question}

INTENT:
{intent_json}

=============================

CRITICAL RULES:

1) Respect table grain strictly.

2) Fact tables:
   - paid_media_events_new
   - crm_campaign_events
   - ga4_events

3) Never join raw fact tables directly.

If multiple fact tables are required:
  a) Aggregate each table separately at campaign_id level
  b) Then join aggregated results

4) Always use correct column names exactly as defined.

5) Do not invent tables or columns.

6) Use GROUP BY correctly when aggregations exist.

7) Use NULLIF() when dividing to prevent division by zero.

Return ONLY valid SQL.
"""
def intent_prompt(question: str) -> str:
    return f"""
You are a marketing analytics expert.

Extract structured intent from the question.

Return STRICT JSON only.
No explanation.
No markdown.

AVAILABLE TABLES:
- paid_media_events_new
- crm_campaign_events
- ga4_events

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
- Use only tables listed above.
- If multiple tables are required → joins_required = true
- Use correct column names exactly as defined in schema.
- Return valid JSON only.

Question:
{question}
"""
