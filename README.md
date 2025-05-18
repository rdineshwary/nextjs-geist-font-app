# SDCKL Library Management System

A Flask-based library management system with features for managing books, users, and borrowings.

## Features

- Books Management (Add, Edit, Delete)
- Users Management with Student ID validation
- Borrowings Management with penalty calculation
- Dashboard with real-time statistics
- Recent Activities tracking

## Setup Instructions

1. Clone the repository
```bash
git clone https://github.com/rdineshwary/DINESH.git
cd DINESH
```

2. Install dependencies
```bash
pip install flask
```

3. Run the application
```bash
python app.py
```

## GitHub Setup Instructions

1. Create a Personal Access Token:
   - Go to GitHub.com and sign in
   - Click your profile picture > Settings
   - Scroll to Developer settings > Personal access tokens > Tokens (classic)
   - Generate new token (classic)
   - Give it a name
   - Select 'repo' scope
   - Click Generate
   - Copy the token immediately

2. Push to GitHub using token:
```bash
git remote add origin https://github.com/rdineshwary/DINESH.git
git branch -M main
git push -u origin main
```
When prompted for password, use the personal access token instead.

## Database Schema

Check `library_schema.sql` for the complete database structure.
