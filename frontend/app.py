import streamlit as st
import os
import sys
import sqlite3
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from retriever.schema_retriever import get_schema_context
from generator.text2sql import generate_sql
from validator.sql_validator import validate_sql
from dotenv import load_dotenv

load_dotenv()

def get_sql_result(nl_query, db_id):
    # 1. Retrieve schema context from ChromaDB
    schema_context = get_schema_context(db_id, nl_query)
    # 2. Generate SQL using OpenAI
    sql_query = generate_sql(nl_query, schema_context)
    # 3. Execute SQL on SQLite and return result
    try:
        conn = sqlite3.connect("leafpay.db")
        cursor = conn.cursor()
        cursor.execute(sql_query)
        if sql_query.strip().lower().startswith("select"):
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            conn.close()
            return sql_query, columns, rows, None
        else:
            conn.commit()
            conn.close()
            return sql_query, None, None, "Query executed successfully."
    except Exception as e:
        return sql_query, None, None, f"SQL execution error: {e}"

# --- Streamlit Frontend ---
st.markdown("""
<h1 style='color:#4F8BF9;'>Generative AI Text-to-SQL System</h1>
<p style='font-size:1.1em;'>Ask questions about your <b>leafpay</b> database using natural language.<br>
<b>Example:</b> <i>list all existing users</i>, <i>show all transactions for Alice</i>, <i>total balance for Bob</i></p>
<hr>
""", unsafe_allow_html=True)

nl_query = st.text_input("Enter your question:", placeholder="e.g. list all existing users")
db_id = "leafpay"  # Only one database used

if st.button("Get Result"):
    if nl_query:
        with st.spinner("Generating and executing SQL..."):
            sql_query, columns, rows, error = get_sql_result(nl_query, db_id)
        st.markdown("---")
        st.markdown("**Generated SQL:**")
        st.code(sql_query, language="sql")
        if error:
            st.error(error)
        elif columns and rows is not None:
            st.markdown("**Result:**")
            st.dataframe({col: [row[i] for row in rows] for i, col in enumerate(columns)})
        else:
            st.success("Query executed successfully.")
    else:
        st.warning("Please enter a question before clicking 'Get Result'.")
        st.warning("Please enter a question.")