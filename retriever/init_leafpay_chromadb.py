import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
import os
from dotenv import load_dotenv

def main():
    docs = [
        # --- Schema ---
        "Table: users (id INTEGER PRIMARY KEY, name TEXT, email TEXT, created_at TEXT)",
        "users.id: Unique user identifier (INTEGER PRIMARY KEY)",
        "users.     : User's full name (TEXT)",
        "users.email: User's email address (TEXT)",
        "users.created_at: Account creation date (TEXT)",
        "Table: transactions (id INTEGER PRIMARY KEY, user_id INTEGER, amount REAL, type TEXT, created_at TEXT)",
        "transactions.id: Unique transaction identifier (INTEGER PRIMARY KEY)",
        "transactions.user_id: User who made the transaction (INTEGER, FK to users.id)",
        "transactions.amount: Transaction amount (REAL)",
        "transactions.type: Transaction type (TEXT: credit/debit)",
        "transactions.created_at: Transaction date (TEXT)",
        "Table: production (id INTEGER PRIMARY KEY, user_id INTEGER, product_name TEXT, quantity INTEGER, produced_at TEXT)",
        "production.id: Unique production identifier (INTEGER PRIMARY KEY)",
        "production.user_id: User who produced (INTEGER, FK to users.id)",
        "production.product_name: Name of product (TEXT)",
        "production.quantity: Quantity produced (INTEGER)",
        "production.produced_at: Production date (TEXT)",
        "Table: balance (user_id INTEGER PRIMARY KEY, balance REAL, last_updated TEXT)",
        "balance.user_id: User identifier (INTEGER PRIMARY KEY, FK to users.id)",
        "balance.balance: Current balance (REAL)",
        "balance.last_updated: Last update date (TEXT)",
        # --- Relationships ---
        "transactions.user_id references users.id",
        "production.user_id references users.id",
        "balance.user_id references users.id",
        # --- Example rows ---
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
        # --- Example queries ---
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
    # Initialize ChromaDB client and collection
    client = chromadb.Client(Settings(
        persist_directory="./chromadb_data"
    ))
    collection = client.get_or_create_collection("leafpay")
    metadatas = [{"type": "schema_or_example"}] * len(docs)
    ids = [f"doc_{i}" for i in range(len(docs))]
    collection.add(documents=docs, metadatas=metadatas, ids=ids)
    print("Initialized 'leafpay' collection in ChromaDB with schema, example data, and sample rows.")

if __name__ == "__main__":
    main()
