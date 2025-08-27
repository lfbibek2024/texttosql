import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from retriever.schema_retriever import get_schema_context
from generator.text2sql import generate_sql
from validator.sql_validator import validate_sql
from dotenv import load_dotenv

load_dotenv()

# Example orchestration function
def process_nl_query(nl_query, db_id):
    schema_context = get_schema_context(db_id, nl_query)
    sql_query = generate_sql(nl_query, schema_context)
    is_valid, error = validate_sql(sql_query, schema_context)
    return sql_query, is_valid, error
