import re
from app.schema import SCHEMA_DICT


def extract_tables_and_aliases(sql: str):
    """
    Extract table names and their aliases from FROM and JOIN clauses.
    Returns: {alias: table_name}
    """
    alias_map = {}

    pattern = r"(FROM|JOIN)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*(?:AS\s+)?([a-zA-Z_][a-zA-Z0-9_]*)?"
    matches = re.findall(pattern, sql, re.IGNORECASE)

    for match in matches:
        table = match[1]
        alias = match[2] if match[2] else table
        alias_map[alias.lower()] = table.lower()

    return alias_map


def extract_column_references(sql: str):
    """
    Extract column references of the form alias.column
    Returns list of tuples: [(alias, column), ...]
    """
    pattern = r"([a-zA-Z_][a-zA-Z0-9_]*)\.([a-zA-Z_][a-zA-Z0-9_]*)"
    matches = re.findall(pattern, sql)
    return [(alias.lower(), column.lower()) for alias, column in matches]


def validate_sql(sql: str):
    sql = sql.strip()

    alias_map = extract_tables_and_aliases(sql)

    # ------------------------------
    # Validate Tables
    # ------------------------------
    for alias, table in alias_map.items():
        if table not in SCHEMA_DICT:
            print(f"❌ Invalid table: {table}")
            return False

    # ------------------------------
    # Validate Columns
    # ------------------------------
    column_refs = extract_column_references(sql)

    for alias, column in column_refs:
        if alias not in alias_map:
            continue  # Skip unknown aliases (e.g., subqueries)

        table_name = alias_map[alias]

        valid_columns = {col.lower() for col in SCHEMA_DICT.get(table_name, {})}

        if column not in valid_columns:
            print(f"❌ Invalid column '{column}' in table '{table_name}'")
            return False

    print("✅ SQL Validation Passed")
    return True
