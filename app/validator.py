import re
from app.schema import SCHEMA_DICT


def extract_tables_and_aliases(sql):
    alias_map = {}
    pattern = r"(FROM|JOIN)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*(?:AS\s+)?([a-zA-Z_][a-zA-Z0-9_]*)?"
    matches = re.findall(pattern, sql, re.IGNORECASE)

    for match in matches:
        table = match[1]
        alias = match[2] if match[2] else table
        alias_map[alias] = table

    return alias_map


def extract_column_references(sql):
    pattern = r"([a-zA-Z_][a-zA-Z0-9_]*)\.([a-zA-Z_][a-zA-Z0-9_]*)"
    return re.findall(pattern, sql)


def validate_sql(sql):
    alias_map = extract_tables_and_aliases(sql)

    for alias, table in alias_map.items():
        if table not in SCHEMA_DICT:
            print(f"❌ Invalid table: {table}")
            return False

    column_refs = extract_column_references(sql)

    for alias, column in column_refs:
        if alias not in alias_map:
            continue
        table_name = alias_map[alias]
        if column not in SCHEMA_DICT.get(table_name, {}):
            print(f"❌ Invalid column '{column}' in table '{table_name}'")
            return False

    print("✅ SQL Validation Passed")
    return True
