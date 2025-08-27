# Uses OpenAI LLM to generate SQL from NL and schema context

# Uses OpenAI LLM to generate SQL from NL and schema context (OpenAI >=1.0.0)
import openai
import os
from dotenv import load_dotenv

load_dotenv()

def generate_sql(nl_query, schema_context):
    api_key = os.getenv("OPENAI_API_KEY")
    prompt = f"""
You are an expert SQL generator. Given the following database schema and a user's question, write a syntactically correct SQL query for a PostgreSQL database. Only return the SQL query, nothing else.

Schema:
{schema_context}

User question:
{nl_query}
"""
    try:
        client = openai.OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4.1-nano-2025-04-14",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that writes SQL queries."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=256,
            temperature=0
        )
        sql_query = response.choices[0].message.content.strip()
        return sql_query
    except Exception as e:
        return f"-- Error generating SQL: {e}"
