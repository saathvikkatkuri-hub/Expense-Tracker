import json
import os
from datetime import datetime

FILE_NAME = "expenses.json"


# -------------------- FILE HANDLING --------------------

def load_expenses():
    if not os.path.exists(FILE_NAME):
        return []

    try:
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def save_expenses(expenses):
    with open(FILE_NAME, "w") as file:
        json.dump(expenses, file, indent=4)


# -------------------- INPUT VALIDATION --------------------

def get_amount():
    while True:
        try:
            amount = float(input("Enter amount: "))

            if amount <= 0:
                print("Amount must be greater than 0.")
                continue

            return amount

        except ValueError:
            print("Please enter a valid number.")


def get_category():
    categories = [
        "Food",
        "Travel",
        "Shopping",
        "Bills",
        "Entertainment",
        "Education",
        "Health",
        "Other"
    ]

    print("\nCategories:")
    for i, category in enumerate(categories, start=1):
        print(f"{i}. {category}")

    while True:
        try:
            choice = int(input("Choose category: "))

            if 1 <= choice <= len(categories):
                return categories[choice - 1]

            print("Invalid category choice.")

        except ValueError:
            print("Please enter a number.")


# -------------------- ADD EXPENSE --------------------

def add_expense(expenses):
    print("\n--- Add Expense ---")

    amount = get_amount()
    category = get_category()

    description = input("Enter description: ").strip()

    while not description:
        print("Description cannot be empty.")
        description = input("Enter description: ").strip()

    expense = {
        "id": len(expenses) + 1,
        "amount": amount,
        "category": category,
        "description": description,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    expenses.append(expense)
    save_expenses(expenses)

    print("Expense added successfully!")


# -------------------- VIEW EXPENSES --------------------

def view_expenses(expenses):
    print("\n--- All Expenses ---")

    if not expenses:
        print("No expenses found.")
        return

    print("-" * 80)
    print(f"{'ID':<5}{'Amount':<12}{'Category':<18}{'Description':<25}{'Date'}")
    print("-" * 80)

    for expense in expenses:
        print(
            f"{expense['id']:<5}"
            f"₹{expense['amount']:<11.2f}"
            f"{expense['category']:<18}"
            f"{expense['description']:<25}"
            f"{expense['date']}"
        )

    print("-" * 80)


# -------------------- UPDATE EXPENSE --------------------

def update_expense(expenses):
    print("\n--- Update Expense ---")

    if not expenses:
        print("No expenses available.")
        return

    view_expenses(expenses)

    try:
        expense_id = int(input("Enter expense ID to update: "))
    except ValueError:
        print("Invalid ID.")
        return

    for expense in expenses:
        if expense["id"] == expense_id:

            print("\n1. Update Amount")
            print("2. Update Category")
            print("3. Update Description")
            print("4. Update All")

            choice = input("Choose option: ")

            if choice == "1":
                expense["amount"] = get_amount()

            elif choice == "2":
                expense["category"] = get_category()

            elif choice == "3":
                description = input("Enter new description: ").strip()

                if description:
                    expense["description"] = description
                else:
                    print("Description cannot be empty.")
                    return

            elif choice == "4":
                expense["amount"] = get_amount()
                expense["category"] = get_category()

                description = input("Enter new description: ").strip()

                if description:
                    expense["description"] = description
                else:
                    print("Description cannot be empty.")
                    return

            else:
                print("Invalid option.")
                return

            save_expenses(expenses)
            print("Expense updated successfully!")
            return

    print("Expense ID not found.")


# -------------------- DELETE EXPENSE --------------------

def delete_expense(expenses):
    print("\n--- Delete Expense ---")

    if not expenses:
        print("No expenses available.")
        return

    view_expenses(expenses)

    try:
        expense_id = int(input("Enter expense ID to delete: "))
    except ValueError:
        print("Invalid ID.")
        return

    for expense in expenses:
        if expense["id"] == expense_id:

            confirm = input(
                f"Delete '{expense['description']}'? (y/n): "
            ).lower()

            if confirm == "y":
                expenses.remove(expense)

                for i, expense in enumerate(expenses, start=1):
                    expense["id"] = i

                save_expenses(expenses)
                print("Expense deleted successfully!")
                print("Expense deleted successfully!")
            else:
                print("Deletion cancelled.")

            return

    print("Expense ID not found.")


# -------------------- SUMMARY --------------------

def show_summary(expenses):
    print("\n--- Expense Summary ---")

    if not expenses:
        print("No expenses available.")
        return

    total = sum(expense["amount"] for expense in expenses)

    print(f"\nTotal Spending: ₹{total:.2f}")

    category_totals = {}

    for expense in expenses:
        category = expense["category"]

        if category not in category_totals:
            category_totals[category] = 0

        category_totals[category] += expense["amount"]

    print("\nCategory-wise Spending:")

    for category, amount in category_totals.items():
        print(f"{category:<20} ₹{amount:.2f}")


# -------------------- MAIN MENU --------------------

def main():
    expenses = load_expenses()

    while True:
        print("\n")
        print("=" * 40)
        print("        EXPENSE TRACKER")
        print("=" * 40)

        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Update Expense")
        print("4. Delete Expense")
        print("5. Expense Summary")
        print("6. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            add_expense(expenses)

        elif choice == "2":
            view_expenses(expenses)

        elif choice == "3":
            update_expense(expenses)

        elif choice == "4":
            delete_expense(expenses)

        elif choice == "5":
            show_summary(expenses)

        elif choice == "6":
            print("\nThank you for using Expense Tracker!")
            break

        else:
            print("Invalid choice. Please try again.")


# -------------------- PROGRAM START --------------------

if __name__ == "__main__":
    main()