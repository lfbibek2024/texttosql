-- SQLite schema and sample data for leafpay system
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT,
    created_at TEXT
);

CREATE TABLE IF NOT EXISTS "transactions" (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    amount REAL,
    type TEXT,
    created_at TEXT
);


CREATE TABLE IF NOT EXISTS production (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    product_name TEXT,
    quantity INTEGER,
    produced_at TEXT
);

CREATE TABLE IF NOT EXISTS balance (
    user_id INTEGER PRIMARY KEY,
    balance REAL,
    last_updated TEXT
);

INSERT INTO users (id, name, email, created_at) VALUES
    (1, 'Alice', 'alice@example.com', '2025-01-01'),
    (2, 'Bob', 'bob@example.com', '2025-01-02'),
    (3, 'Charlie', 'charlie@example.com', '2025-01-03');
INSERT INTO "transactions" (id, user_id, amount, type, created_at) VALUES
    (1, 1, 100.0, 'credit', '2025-01-10'),
    (2, 1, 50.0, 'debit', '2025-01-11'),
    (3, 2, 200.0, 'credit', '2025-01-12');

INSERT INTO production (id, user_id, product_name, quantity, produced_at) VALUES
    (1, 1, 'Widget', 10, '2025-01-15'),
    (2, 2, 'Gadget', 5, '2025-01-16');

INSERT INTO balance (user_id, balance, last_updated) VALUES
    (1, 50.0, '2025-01-20'),
    (2, 200.0, '2025-01-20'),
    (3, 0.0, '2025-01-20');
