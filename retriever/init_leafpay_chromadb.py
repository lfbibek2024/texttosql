import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
import os
from dotenv import load_dotenv

def main():
    load_dotenv()
    client = chromadb.Client(Settings())
    openai_api_key = os.getenv("OPENAI_API_KEY")
    openai_ef = None
    if openai_api_key:
        try:
            openai_ef = embedding_functions.OpenAIEmbeddingFunction(
                api_key=openai_api_key,
                model_name="text-embedding-ada-002"
            )
        except Exception:
            openai_ef = None
    # If no API key, fallback to no embedding function (pure text search)
    # Delete existing collection if it exists
    try:
        client.delete_collection("leafpay")
        print("Deleted existing 'leafpay' collection in ChromaDB.")
    except Exception:
        pass
    if openai_ef:
        collection = client.get_or_create_collection(
            name="leafpay",
            embedding_function=openai_ef
        )
    else:
        collection = client.get_or_create_collection(name="leafpay")

    # Schema, sample queries, and example rows for each table
    docs = [
        # Schema (match actual SQLite schema)
        "Table: users (id INTEGER PRIMARY KEY, name TEXT, email TEXT, created_at TEXT)",
        "Table: transactions (id INTEGER PRIMARY KEY, user_id INTEGER, amount REAL, type TEXT, created_at TEXT)",
        "Table: production (id INTEGER PRIMARY KEY, user_id INTEGER, product_name TEXT, quantity INTEGER, produced_at TEXT)",
        "Table: balance (user_id INTEGER PRIMARY KEY, balance REAL, last_updated TEXT)",
        # Example rows
        "users: (1, 'Alice', 'alice@example.com', '2025-01-01')",
        "users: (2, 'Bob', 'bob@example.com', '2025-01-02')",
        "users: (3, 'Charlie', 'charlie@example.com', '2025-01-03')",
        "transactions: (1, 1, 100.0, 'credit', '2025-01-10')",
        "transactions: (2, 1, 50.0, 'debit', '2025-01-11')",
        "transactions: (3, 2, 200.0, 'credit', '2025-01-12')",
        "production: (1, 1, 'Widget', 10, '2025-01-15')",
        "production: (2, 2, 'Gadget', 5, '2025-01-16')",
        "balance: (1, 50.0, '2025-01-20')",
        "balance: (2, 200.0, '2025-01-20')",
        "balance: (3, 0.0, '2025-01-20')",
        # Example queries (match actual table names and columns)
        "SELECT * FROM users;",
        "SELECT * FROM users WHERE id = 1;",
        "SELECT SUM(amount) FROM transactions WHERE user_id = 1;",
        "SELECT * FROM production WHERE product_name = 'Widget';",
        "SELECT balance FROM balance WHERE user_id = 1;",
        "SELECT u.name, b.balance FROM users u JOIN balance b ON u.id = b.user_id;",
        "SELECT t.id, t.amount, t.created_at, u.id, u.name, u.email FROM transactions t JOIN users u ON t.user_id = u.id WHERE u.name = 'Alice';",
        "SELECT COUNT(*) FROM production WHERE produced_at >= '2025-01-01';",
        "SELECT * FROM transactions WHERE type = 'credit' AND amount > 1000;"
    ]
    metadatas = [{"type": "schema_or_example"}] * len(docs)
    ids = [f"doc_{i}" for i in range(len(docs))]
    collection.add(documents=docs, metadatas=metadatas, ids=ids)
    print("Initialized 'leafpay' collection in ChromaDB with schema, example data, and sample rows.")

if __name__ == "__main__":
    main()
