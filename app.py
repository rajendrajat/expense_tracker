from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


def init_db():
    """Initialize the database and create the expenses table if it doesn't exist."""
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            description TEXT
        )
    """)
    conn.commit()
    conn.close()


def get_expenses():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("SELECT amount, category, description FROM expenses")
    rows = cursor.fetchall()
    conn.close()
    return rows


def add_expense(amount, category, description):
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO expenses (amount, category, description) VALUES (?, ?, ?)
    """, (amount, category, description))
    conn.commit()
    conn.close()


@app.route('/')
def index():
    expenses = get_expenses()
    return render_template('index.html', expenses=expenses)


@app.route('/add', methods=['POST'])
def add():
    amount = request.form.get('amount')
    category = request.form.get('category')
    description = request.form.get('description')
    add_expense(amount, category, description)
    return redirect("/")


if __name__ == '__main__':
    init_db()    # ✅ Ensure table is created
    app.run(debug=True)
