from app.config import ALLOWED_TABLE

VALID_EVENT_NAMES = [
    "click",
    "page_view",
    "purchase",
    "scroll",
    "session_start",
    "first_visit",
    "user_engagement"
]

SCHEMA_COLUMNS = [
    "campaign",
    "event_name",
    "event_date",
    "user_pseudo_id",
    "session_id",
    "geo_country",
    "purchase_value",
    "engagement_time_msec",
    "device_category",
    "page_location"
]
