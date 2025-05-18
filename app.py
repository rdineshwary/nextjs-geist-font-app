from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    
    # Create Books table
    c.execute('''CREATE TABLE IF NOT EXISTS books
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  title TEXT NOT NULL,
                  author TEXT NOT NULL,
                  isbn TEXT UNIQUE NOT NULL,
                  genre TEXT NOT NULL,
                  available BOOLEAN DEFAULT 1)''')
    
    # Create Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  student_id TEXT UNIQUE NOT NULL,
                  name TEXT NOT NULL,
                  email TEXT UNIQUE NOT NULL,
                  phone TEXT,
                  created_at TEXT DEFAULT CURRENT_TIMESTAMP)''')
    
    # Create Borrowings table
    c.execute('''CREATE TABLE IF NOT EXISTS borrowings
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  book_id INTEGER,
                  user_id INTEGER,
                  borrow_date DATE,
                  return_date DATE,
                  status TEXT,
                  penalty_fee DECIMAL(10,2) DEFAULT 0.00,
                  created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                  updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                  FOREIGN KEY (book_id) REFERENCES books (id),
                  FOREIGN KEY (user_id) REFERENCES users (id))''')
    
    # Add sample books if none exist
    c.execute("SELECT COUNT(*) FROM books")
    if c.fetchone()[0] == 0:
        sample_books = [
            ('The Great Gatsby', 'F. Scott Fitzgerald', '978-1234567890', 'Fiction', 1),
            ('A Brief History of Time', 'Stephen Hawking', '978-0987654321', 'Science', 1),
            ('Pride and Prejudice', 'Jane Austen', '978-5432109876', 'Literature', 1),
            ('The Art of Cooking', 'Julia Child', '978-6789054321', 'Cooking', 1),
            ('The Mystery of the Blue Train', 'Agatha Christie', '978-2468135790', 'Mystery', 1),
            ('Dune', 'Frank Herbert', '978-1357924680', 'Science Fiction', 1)
        ]
        c.executemany('INSERT INTO books (title, author, isbn, genre, available) VALUES (?, ?, ?, ?, ?)', sample_books)
    
    # Add sample users if none exist
    c.execute("SELECT COUNT(*) FROM users")
    if c.fetchone()[0] == 0:
        sample_users = [
            ('STD001', 'John Doe', 'john.doe@email.com', '123-456-7890'),
            ('STD002', 'Jane Smith', 'jane.smith@email.com', '098-765-4321'),
            ('STD003', 'Bob Wilson', 'bob.wilson@email.com', '555-123-4567')
        ]
        c.executemany('INSERT INTO users (student_id, name, email, phone, created_at) VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)', sample_users)
    
    # Add sample borrowings if none exist
    c.execute("SELECT COUNT(*) FROM borrowings")
    if c.fetchone()[0] == 0:
        sample_borrowings = [
            (1, 1, '2024-01-01', '2024-01-15', 'returned', 0.00),
            (2, 2, '2024-01-10', '2024-01-24', 'borrowed', 5.00),
            (3, 3, '2024-01-05', '2024-01-19', 'borrowed', 10.00)
        ]
        c.executemany('INSERT INTO borrowings (book_id, user_id, borrow_date, return_date, status, penalty_fee) VALUES (?, ?, ?, ?, ?, ?)', sample_borrowings)
    
    conn.commit()
    conn.close()

@app.route('/')
def dashboard():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    
    # Get counts for dashboard
    c.execute("SELECT COUNT(*) FROM books")
    total_books = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM users")
    total_users = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM borrowings WHERE status='borrowed'")
    active_borrowings = c.fetchone()[0]

    # Fetch recent activities: borrowings and user registrations
    recent_activities = []

    # Recent borrowings
    c.execute("""
        SELECT b.created_at, books.title, b.status
        FROM borrowings b
        JOIN books ON b.book_id = books.id
        ORDER BY b.created_at DESC
    """)
    borrowings = c.fetchall()
    for b in borrowings:
        status_class = 'status-borrowed' if b[2] == 'borrowed' else 'status-returned'
        status_text = b[2].title()
        description = f'Book Borrowed: "{b[1]}"' if b[2] == 'borrowed' else f'Book Returned: "{b[1]}"'
        recent_activities.append({
            'description': description,
            'date': b[0],
            'status_class': status_class,
            'status_text': status_text
        })

    # Recent user registrations
    c.execute("""
        SELECT student_id, name, created_at
        FROM users
        ORDER BY created_at DESC
    """)
    users = c.fetchall()
    for u in users:
        recent_activities.append({
            'description': f'New User Registration: "{u[1]}"',
            'date': u[2],
            'status_class': 'status-returned',
            'status_text': 'Completed'
        })

    # Sort all activities by date descending
    recent_activities.sort(key=lambda x: x['date'], reverse=True)

    conn.close()
    
    return render_template('dashboard.html', 
                         total_books=total_books,
                         total_users=total_users,
                         active_borrowings=active_borrowings,
                         recent_activities=recent_activities)

@app.route('/books', methods=['GET', 'POST'])
def books():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    
    if request.method == 'POST':
        if 'delete' in request.form:
            try:
                book_id = request.form['delete']
                c.execute("DELETE FROM books WHERE id=?", (book_id,))
                conn.commit()
            except sqlite3.Error as e:
                print(f"Database error: {e}")
                conn.rollback()
        else:
            title = request.form['title']
            author = request.form['author']
            isbn = request.form['isbn']
            genre = request.form['genre']
            try:
                c.execute("INSERT INTO books (title, author, isbn, genre, available) VALUES (?, ?, ?, ?, ?)",
                         (title, author, isbn, genre, 1))
                conn.commit()
            except sqlite3.Error as e:
                print(f"Database error: {e}")
                conn.rollback()
    
    c.execute("SELECT * FROM books")
    books = c.fetchall()
    conn.close()
    return render_template('books.html', books=books)

@app.route('/users', methods=['GET', 'POST'])
def users():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    
    if request.method == 'POST':
        if 'delete' in request.form:
            try:
                user_id = request.form['delete']
                c.execute("DELETE FROM users WHERE id=?", (user_id,))
                conn.commit()
            except sqlite3.Error as e:
                print(f"Database error: {e}")
                conn.rollback()
        else:
            student_id = request.form['student_id']
            name = request.form['name']
            email = request.form['email']
            phone = request.form['phone']
            try:
                c.execute("INSERT INTO users (student_id, name, email, phone) VALUES (?, ?, ?, ?)",
                         (student_id, name, email, phone))
                conn.commit()
            except sqlite3.Error as e:
                print(f"Database error: {e}")
                conn.rollback()
    
    c.execute("SELECT * FROM users")
    users = c.fetchall()
    conn.close()
    return render_template('users.html', users=users)

@app.route('/borrowings', methods=['GET', 'POST'])
def borrowings():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    
    if request.method == 'POST':
        if 'delete' in request.form:
            try:
                borrowing_id = request.form['delete']
                # Get book_id before deleting the borrowing
                c.execute("SELECT book_id FROM borrowings WHERE id=?", (borrowing_id,))
                book_id = c.fetchone()[0]
                # Update book availability and delete borrowing in a transaction
                c.execute("UPDATE books SET available=1 WHERE id=?", (book_id,))
                c.execute("DELETE FROM borrowings WHERE id=?", (borrowing_id,))
                conn.commit()
            except sqlite3.Error as e:
                print(f"Database error: {e}")
                conn.rollback()
        elif 'return' in request.form:
            try:
                borrowing_id = request.form['return']
                # Get book_id before updating status
                c.execute("SELECT book_id FROM borrowings WHERE id=?", (borrowing_id,))
                book_id = c.fetchone()[0]
                # Update borrowing status and book availability in a transaction
                c.execute("UPDATE borrowings SET status='returned' WHERE id=?", (borrowing_id,))
                c.execute("UPDATE books SET available=1 WHERE id=?", (book_id,))
                conn.commit()
            except sqlite3.Error as e:
                print(f"Database error: {e}")
                conn.rollback()
        elif 'edit_id' in request.form:
            try:
                book_id = request.form['edit_id']
                title = request.form['title']
                author = request.form['author']
                isbn = request.form['isbn']
                genre = request.form['genre']
                c.execute("UPDATE books SET title=?, author=?, isbn=?, genre=? WHERE id=?",
                         (title, author, isbn, genre, book_id))
                conn.commit()
            except sqlite3.Error as e:
                print(f"Database error: {e}")
                conn.rollback()
        else:
            # New borrowing
            try:
                book_id = request.form['book_id']
                user_id = request.form['user_id']
                borrow_date = request.form['borrow_date']
                return_date = request.form['return_date']
                
                c.execute("""
                    INSERT INTO borrowings (book_id, user_id, borrow_date, return_date, status, penalty_fee)
                    VALUES (?, ?, ?, ?, 'borrowed', 0.00)
                """, (book_id, user_id, borrow_date, return_date))
                c.execute("UPDATE books SET available=0 WHERE id=?", (book_id,))
                conn.commit()
            except sqlite3.Error as e:
                print(f"Database error: {e}")
                conn.rollback()
            except Exception as e:
                print(f"Error: {e}")
                conn.rollback()

    # Get available books, users and borrowings
    try:
        c.execute("SELECT id, title FROM books WHERE available=1")
        available_books = c.fetchall()
        
        c.execute("SELECT id, name FROM users")
        all_users = c.fetchall()
        
        c.execute("""
            SELECT b.id, books.title, users.name, b.borrow_date, b.return_date, b.status, b.penalty_fee
            FROM borrowings b
            JOIN books ON b.book_id = books.id
            JOIN users ON b.user_id = users.id
        """)
        borrowings = c.fetchall()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        available_books = []
        all_users = []
        borrowings = []
    conn.close()
    
    return render_template('borrowings.html', 
                         borrowings=borrowings,
                         available_books=available_books,
                         all_users=all_users,
                         today=datetime.now().strftime('%Y-%m-%d'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=8000)
