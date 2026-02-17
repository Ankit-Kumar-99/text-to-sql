# ===============================
# TABLE SCHEMA STRING (LLM)
# ===============================

TABLE_SCHEMAS = """
TABLE: paid_media_events_new
Grain: 1 row per campaign
Primary Key: campaign_id

Columns:
- campaign_id (STRING)
- campaign_name (STRING)
- objective (STRING)
- geo_country (STRING)
- device (STRING)
- impressions (INTEGER)
- reach (INTEGER)
- clicks (INTEGER)
- ctr (FLOAT)
- spend (INTEGER)
- cpm (FLOAT)
- cpc (FLOAT)
- conversions (INTEGER)
- conversion_rate (FLOAT)
- utm_source (STRING)
- utm_medium (STRING)
- utm_campaign (STRING)
- utm_content (STRING)
- creative_type (STRING)
- audience_segment (STRING)
- country (STRING)
- state (STRING)

----------------------------------------

TABLE: crm_campaign_events
Grain: 1 row per CRM campaign event

Columns:
- campaign_id (STRING)
- campaign (STRING)
- customer_id (STRING)
- event_type (STRING)
- timestamp (TIMESTAMP)
- camp_start_date (STRING)
- source (STRING)

Foreign Key: campaign_id → paid_media_events_new.campaign_id

----------------------------------------

TABLE: ga4_events
Grain: 1 row per website event

Columns:
- source (STRING)
- medium (STRING)
- campaign (STRING)
- campaign_id (STRING)
- user_pseudo_id (INTEGER)
- customer_id (STRING)
- event_timestamp (TIMESTAMP)
- event_date (DATE)
- event_name (STRING)
- session_id (INTEGER)
- ga_session_start (INTEGER)
- ga_session_number (INTEGER)
- page_location (STRING)
- page_referrer (STRING)
- page_title (STRING)
- page_type (STRING)
- device_category (STRING)
- geo_country (STRING)
- engagement_time_msec (INTEGER)
- purchase_value (INTEGER)
- scroll_percent (FLOAT)
- session_engaged (INTEGER)

Foreign Key: campaign_id → paid_media_events_new.campaign_id
"""
# ===============================
# SCHEMA DICT (VALIDATION)
# ===============================

SCHEMA_DICT = {
    "paid_media_events_new": {
        "campaign_id", "campaign_name", "objective", "geo_country",
        "device", "impressions", "reach", "clicks", "ctr", "spend",
        "cpm", "cpc", "conversions", "conversion_rate",
        "utm_source", "utm_medium", "utm_campaign", "utm_content",
        "creative_type", "audience_segment", "country", "state"
    },
    "crm_campaign_events": {
        "campaign_id", "campaign", "customer_id", "event_type",
        "timestamp", "camp_start_date", "source"
    },
    "ga4_events": {
        "source", "medium", "campaign", "campaign_id",
        "user_pseudo_id", "customer_id", "event_timestamp",
        "event_date", "event_name", "session_id",
        "ga_session_start", "ga_session_number",
        "page_location", "page_referrer", "page_title",
        "page_type", "device_category", "geo_country",
        "engagement_time_msec", "purchase_value",
        "scroll_percent", "session_engaged"
    }
}
