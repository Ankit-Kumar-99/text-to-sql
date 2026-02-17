# ===============================
# TABLE SCHEMA STRING (LLM)
# ===============================

TABLE_SCHEMAS = """
TABLE: campaign_performance
Grain: 1 row per campaign
Primary Key: id

Columns:
- camp_start_date (DATE)
- campaign_name (STRING)
- id (STRING)
- objective (STRING)
- impressions (INT)
- reach (INT)
- clicks (INT)
- ctr (FLOAT)
- spend (FLOAT)
- cpm (FLOAT)
- cpc (FLOAT)
- conversions (INT)
- conversion_rate (FLOAT)
- utm_source (STRING)
- utm_medium (STRING)
- utm_campaign (STRING)
- utm_content (STRING)
- creative (STRING)
- audience_segment (STRING)

----------------------------------------

TABLE: email_events
Grain: 1 row per email event

Columns:
- campaign_name (STRING)
- campaign_id (STRING)
- user_id (STRING)
- event_type (STRING)
- timestamp (DATETIME)
- camp_start_date (DATE)
- source_medium (STRING)
- spend (FLOAT)

Foreign Key: campaign_id → campaign_performance.id

----------------------------------------

TABLE: web_analytics
Grain: 1 row per web event

Columns:
- source (STRING)
- medium (STRING)
- campaign (STRING)
- campaign_id (STRING)
- user_pseudo_id (STRING)
- user_id (STRING)
- event_timestamp (DATETIME)
- event_date (DATE)
- event_name (STRING)
- session_id (STRING)
- page_location (STRING)
- page_referrer (STRING)
- page_title (STRING)
- device (STRING)
- country (STRING)
- engagement_time_ms (INT)
- scroll_percent (FLOAT)
- purchase_value (FLOAT)
- session_engaged (STRING)

Foreign Key: campaign_id → campaign_performance.id
"""

# ===============================
# SCHEMA DICT (VALIDATION)
# ===============================

SCHEMA_DICT = {
    "campaign_performance": {
        "camp_start_date", "campaign_name", "id", "objective",
        "impressions", "reach", "clicks", "ctr", "spend", "cpm", "cpc",
        "conversions", "conversion_rate", "utm_source", "utm_medium",
        "utm_campaign", "utm_content", "creative", "audience_segment"
    },
    "email_events": {
        "campaign_name", "campaign_id", "user_id", "event_type",
        "timestamp", "camp_start_date", "source_medium", "spend"
    },
    "web_analytics": {
        "source", "medium", "campaign", "campaign_id",
        "user_pseudo_id", "user_id", "event_timestamp", "event_date",
        "event_name", "session_id", "page_location", "page_referrer",
        "page_title", "device", "country", "engagement_time_ms",
        "scroll_percent", "purchase_value", "session_engaged"
    }
}
