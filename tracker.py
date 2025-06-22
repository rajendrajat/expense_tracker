import sqlite3

# ---- Database Setup ----


def init_db():
    """Initialize the database and create the expenses table if needed."""
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


# ---- Expense Operations ----
def add_expense():
    """Add an expense to the database and save to a .txt file as backup."""
    amount = input("Enter expense amount: ")
    category = input("Enter category: ")
    description = input("Enter description: ")

    # Save to database
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO expenses (amount, category, description) VALUES (?, ?, ?)
    """, (amount, category, description))
    conn.commit()
    conn.close()

    # Save to .txt (optional backup)
    with open("expenses.txt", "a") as file:
        file.write(f"{amount},{category},{description}\n")

    print("✅ Expense added successfully!\n")


def view_expenses():
    """View all expenses from the database."""
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("SELECT amount, category, description FROM expenses")
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print("\nℹ️ No expenses found.\n")
        return

    print("\n=== All Expenses ===")
    for amount, category, description in rows:
        print(f"💵 {amount} | 🗂️ {category} | 📝 {description}")
    print()


# ---- Main Menu ----
def main():
    """Main menu for Expense Tracker."""
    init_db()  # Ensure database is ready
    while True:
        print("=== Expense Tracker ===")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            print("👋 Exiting... Stay sharp and save wisely!\n")
            break
        else:
            print("\n❌ Invalid choice. Try again.\n")


if __name__ == "__main__":
    main()
