-- Drop existing tables if they exist
DROP TABLE IF EXISTS borrowings;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS books;

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
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Borrowings table
CREATE TABLE borrowings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER,
    user_id INTEGER,
    borrow_date DATE,
    return_date DATE,
    status TEXT CHECK(status IN ('borrowed', 'returned')),
    penalty_fee DECIMAL(10,2) DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (book_id) REFERENCES books (id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);

-- Insert sample books
INSERT INTO books (title, author, isbn, genre, available) VALUES
('The Great Gatsby', 'F. Scott Fitzgerald', '978-1234567890', 'Fiction', 1),
('A Brief History of Time', 'Stephen Hawking', '978-0987654321', 'Science', 1),
('Pride and Prejudice', 'Jane Austen', '978-5432109876', 'Literature', 1),
('The Art of Cooking', 'Julia Child', '978-6789054321', 'Cooking', 1),
('The Mystery of the Blue Train', 'Agatha Christie', '978-2468135790', 'Mystery', 1),
('Dune', 'Frank Herbert', '978-1357924680', 'Science Fiction', 1);

-- Insert sample users
INSERT INTO users (student_id, name, email, phone) VALUES
('STD001', 'John Doe', 'john.doe@email.com', '123-456-7890'),
('STD002', 'Jane Smith', 'jane.smith@email.com', '098-765-4321'),
('STD003', 'Bob Wilson', 'bob.wilson@email.com', '555-123-4567');

-- Insert sample borrowings
INSERT INTO borrowings (book_id, user_id, borrow_date, return_date, status, penalty_fee) VALUES
(1, 1, '2024-01-01', '2024-01-15', 'returned', 0.00),
(2, 2, '2024-01-10', '2024-01-24', 'borrowed', 0.00),
(3, 3, '2024-01-05', '2024-01-19', 'borrowed', 0.00);

-- Create indexes for better performance
CREATE INDEX idx_books_isbn ON books(isbn);
CREATE INDEX idx_users_student_id ON users(student_id);
CREATE INDEX idx_borrowings_status ON borrowings(status);
CREATE INDEX idx_borrowings_dates ON borrowings(borrow_date, return_date);
