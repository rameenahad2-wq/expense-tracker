import sqlite3

DATABASE_NAME = "expense_tracker.db"


def get_connection():
    return sqlite3.connect(DATABASE_NAME)


def initialize_database():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            expense_date TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def add_expense(title, category, amount, expense_date):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO expenses (title, category, amount, expense_date)
        VALUES (?, ?, ?, ?)
    """, (title, category, amount, expense_date))

    connection.commit()
    connection.close()


def get_expenses(search_text="", category="All"):
    connection = get_connection()
    cursor = connection.cursor()

    query = "SELECT * FROM expenses WHERE 1=1"
    parameters = []

    if search_text:
        query += " AND title LIKE ?"
        parameters.append(f"%{search_text}%")

    if category != "All":
        query += " AND category = ?"
        parameters.append(category)

    query += " ORDER BY id DESC"

    cursor.execute(query, parameters)
    expenses = cursor.fetchall()

    connection.close()
    return expenses


def delete_expense(expense_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))

    connection.commit()
    connection.close()


def get_total_expenses(search_text="", category="All"):
    connection = get_connection()
    cursor = connection.cursor()

    query = "SELECT COALESCE(SUM(amount), 0) FROM expenses WHERE 1=1"
    parameters = []

    if search_text:
        query += " AND title LIKE ?"
        parameters.append(f"%{search_text}%")

    if category != "All":
        query += " AND category = ?"
        parameters.append(category)

    cursor.execute(query, parameters)
    total = cursor.fetchone()[0]

    connection.close()
    return total