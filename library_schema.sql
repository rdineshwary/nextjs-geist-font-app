-- Books table
CREATE TABLE books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    isbn TEXT UNIQUE NOT NULL,
    genre TEXT NOT NULL,
    available BOOLEAN DEFAULT 1
);

-- Users table
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- Borrowings table
CREATE TABLE borrowings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER,
    user_id INTEGER,
    borrow_date DATE,
    return_date DATE,
    status TEXT,
    penalty_fee DECIMAL(10,2) DEFAULT 0.00,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (book_id) REFERENCES books (id),
    FOREIGN KEY (user_id) REFERENCES users (id)
);
