import json
import re
from app.gemini_client import generate_response
from app.prompts import intent_prompt, sql_prompt
from app.schema import TABLE_SCHEMAS
from app.validator import validate_sql


def clean_sql_output(sql_text):
    sql_text = re.sub(r"```sql", "", sql_text, flags=re.IGNORECASE)
    sql_text = re.sub(r"```", "", sql_text)
    return sql_text.strip()


def generate_sql(question: str):

    print("\n🔍 Extracting Intent...")
    intent_raw = generate_response(intent_prompt(question))

    try:
        intent_json = json.loads(intent_raw)
    except:
        print("❌ Intent JSON parsing failed")
        print(intent_raw)
        return None

    print("✅ Intent Extracted")
    print(json.dumps(intent_json, indent=2))

    print("\n🛠 Generating SQL...")
    sql_raw = generate_response(
        sql_prompt(question, json.dumps(intent_json, indent=2), TABLE_SCHEMAS)
    )

    sql_clean = clean_sql_output(sql_raw)

    if validate_sql(sql_clean):
        print("\n🎯 Final SQL:\n")
        print(sql_clean)
        return sql_clean

    print("❌ SQL failed validation.")
    return None
