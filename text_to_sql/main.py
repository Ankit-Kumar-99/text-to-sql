# import os
# import re
# import time
# from dotenv import load_dotenv
# from google import genai

# # ============================================================
# # 1. Load API Key
# # ============================================================
# load_dotenv()
# API_KEY = os.getenv("GEMINI_API_KEY")

# if not API_KEY:
#     raise ValueError("❌ GEMINI_API_KEY not found in .env")

# # ============================================================
# # 2. Gemini Client
# # ============================================================
# client = genai.Client(api_key=API_KEY)

# MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

# GEN_CONFIG = {
#     "temperature": 0.2,
#     "max_output_tokens": 512
# }

# # ============================================================
# # 3. Allowed Schema + Guards
# # ============================================================
# ALLOWED_TABLE = "marketing_lens.ga4_events"

# VALID_EVENT_NAMES = [
#     "click",
#     "page_view",
#     "purchase",
#     "scroll",
#     "session_start",
#     "first_visit",
#     "user_engagement"
# ]

# FORBIDDEN_PATTERNS = [
#     "UNNEST",
#     "EVENT_PARAMS",
#     "USER_PROPERTIES",
#     "INFORMATION_SCHEMA"
# ]

# BLOCKED_KEYWORDS = [
#     "DROP", "DELETE", "UPDATE", "INSERT",
#     "ALTER", "TRUNCATE", "MERGE"
# ]

# # ============================================================
# # 4. Schema Context + Few-shot Examples
# # ============================================================
# schema_context = f"""
# You are a senior analytics engineer and BigQuery SQL expert.

# Task:
# Convert natural language marketing questions into correct BigQuery SQL.

# Database Table (Flattened):
# `{ALLOWED_TABLE}`

# Columns:
# - campaign (STRING)
# - event_name (STRING)
# - event_date (STRING YYYYMMDD)
# - user_pseudo_id (STRING)
# - session_id (STRING)
# - geo_country (STRING)
# - purchase_value (FLOAT64)
# - engagement_time_msec (INT64)
# - device_category (STRING)
# - page_location (STRING)

# Important Notes:
# - This is a FLATTENED table.
# - Do NOT use GA4 raw export nested fields like event_params.
# - Do NOT use UNNEST().
# - Use ONLY the columns listed above.
# - Valid event_name values: {", ".join(VALID_EVENT_NAMES)}

# Output Rules:
# - Return ONLY SQL (no explanation, no markdown).
# - Only SELECT queries are allowed.
# - Use COUNT(*) instead of COUNT(column).
# - Use CTEs if multi-step logic is needed.

# Examples:

# Q: How many clicks for Campaign X?
# SQL:
# SELECT COUNT(*) AS total_clicks
# FROM `{ALLOWED_TABLE}`
# WHERE event_name = 'click'
#   AND campaign = 'Campaign X';

# Q: Revenue by country?
# SQL:
# SELECT geo_country, SUM(purchase_value) AS revenue
# FROM `{ALLOWED_TABLE}`
# WHERE event_name = 'purchase'
# GROUP BY geo_country;
# """

# # ============================================================
# # 5. Helpers
# # ============================================================
# def extract_sql(text: str) -> str:
#     """Extract clean SQL from model output."""
#     text = text.strip()
#     match = re.search(r"```sql(.*?)```", text, re.DOTALL | re.IGNORECASE)
#     if match:
#         return match.group(1).strip()
#     return text


# def call_gemini(prompt: str, retries: int = 2) -> str:
#     """Call Gemini with retry support."""
#     for attempt in range(retries):
#         try:
#             response = client.models.generate_content(
#                 model=MODEL_NAME,
#                 contents=prompt,
#                 config=GEN_CONFIG
#             )
#             return extract_sql(response.text)

#         except Exception as e:
#             if attempt < retries - 1:
#                 time.sleep(1.5)
#             else:
#                 raise e


# # ============================================================
# # 6. Safety + Schema Validation
# # ============================================================
# def check_sql(sql: str):
#     """Return reason if SQL is invalid, else None."""
#     upper_sql = sql.upper()

#     # Block unsafe keywords
#     if any(word in upper_sql for word in BLOCKED_KEYWORDS):
#         return "Unsafe SQL keyword detected (non-SELECT operation)"

#     # Block forbidden GA4 nested schema usage
#     if any(pat in upper_sql for pat in FORBIDDEN_PATTERNS):
#         return "Forbidden GA4 raw schema detected (UNNEST/event_params)"

#     # Ensure correct table is referenced
#     if ALLOWED_TABLE not in sql:
#         return f"Query must reference only `{ALLOWED_TABLE}`"

#     return None


# # ============================================================
# # 7. Step 1: Generate SQL
# # ============================================================
# def generate_sql(question: str) -> str:
#     prompt = f"""
# {schema_context}

# User Question:
# {question}

# Return ONLY the SQL query:
# """
#     return call_gemini(prompt)


# # ============================================================
# # 8. Step 2: Review + Fix SQL
# # ============================================================
# def review_sql(question: str, sql_query: str) -> str:
#     review_prompt = f"""
# You are a SQL reviewer.

# Question:
# {question}

# Generated SQL:
# {sql_query}

# Checklist:
# - Fully answers the question
# - Uses only allowed schema columns
# - Uses valid event_name values
# - Avoids GA4 nested fields (no event_params, no UNNEST)
# - Uses correct filters, joins, and aggregations

# If incorrect, rewrite the SQL.

# Return ONLY final SQL:
# """
#     return call_gemini(review_prompt)


# # ============================================================
# # 9. Terminal Loop
# # ============================================================
# print("\n✅ Marketing Lens NL → SQL Generator (Production Style)")
# print("Type 'exit' to quit.\n")

# while True:
#     question = input("Ask your marketing question: ").strip()

#     if question.lower() == "exit":
#         print("Goodbye 👋")
#         break

#     try:
#         # ----------------------------
#         # Step 1: Generate SQL
#         # ----------------------------
#         sql_1 = generate_sql(question)

#         reason = check_sql(sql_1)
#         if reason:
#             print("\n❌ Generated SQL rejected:", reason)
#             print("\n--- SQL Output ---\n", sql_1, "\n")
#             continue

#         # ----------------------------
#         # Step 2: Review + Improve SQL
#         # ----------------------------
#         sql_final = review_sql(question, sql_1)

#         reason = check_sql(sql_final)

#         # ----------------------------
#         # Step 3: Auto-Retry Once if Invalid
#         # ----------------------------
#         if reason:
#             print("\n⚠️ Final SQL rejected:", reason)
#             print("\n--- Rejected SQL ---\n", sql_final, "\n")

#             retry_prompt = f"""
# The SQL is invalid because: {reason}

# Rewrite the query correctly using ONLY:
# `{ALLOWED_TABLE}`

# Rules:
# - No UNNEST
# - No event_params
# - Only SELECT
# - Use correct event_name values

# Question:
# {question}

# Return ONLY SQL:
# """
#             sql_final = call_gemini(retry_prompt)

#             reason2 = check_sql(sql_final)
#             if reason2:
#                 print("\n❌ Retry failed again:", reason2)
#                 print("\n--- Retry SQL ---\n", sql_final, "\n")
#                 continue

#         # ----------------------------
#         # Output Final SQL
#         # ----------------------------
#         print("\n===============================")
#         print("✅ Final Validated SQL Query:\n")
#         print(sql_final)
#         print("===============================\n")

#     except Exception as e:
#         print("\n❌ Gemini API Error:")
#         print(e)
#         print("\nCheck quota/billing or retry.\n")


from app.nl2sql import generate_valid_sql

print("\n✅ Marketing Lens NL → SQL Generator")
print("Type 'exit' to quit.\n")

while True:
    question = input("Ask your marketing question: ").strip()

    if question.lower() == "exit":
        print("Goodbye 👋")
        break

    try:
        sql = generate_valid_sql(question)

        print("\n===============================")
        print("✅ Final SQL Query:\n")
        print(sql)
        print("===============================\n")

    except Exception as e:
        print("\n❌ Error:", e, "\n")
