import json
import os
import csv
from datetime import datetime

FILE_NAME = "expenses.json"


# -------------------- FILE HANDLING --------------------

def load_expenses():
    if not os.path.exists(FILE_NAME):
        return []

    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def save_expenses(expenses):
    with open(FILE_NAME, "w", encoding="utf-8") as file:
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


def get_expense_id(expenses):
    while True:
        try:
            expense_id = int(input("Enter expense ID: "))

            if any(expense["id"] == expense_id for expense in expenses):
                return expense_id

            print("Expense ID not found.")

        except ValueError:
            print("Please enter a valid ID.")


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
        "id": max((expense["id"] for expense in expenses), default=0) + 1,
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

    print("-" * 90)
    print(
        f"{'ID':<5}"
        f"{'Amount':<12}"
        f"{'Category':<18}"
        f"{'Description':<25}"
        f"{'Date'}"
    )
    print("-" * 90)

    for expense in expenses:
        print(
            f"{expense['id']:<5}"
            f"₹{expense['amount']:<11.2f}"
            f"{expense['category']:<18}"
            f"{expense['description']:<25}"
            f"{expense['date']}"
        )

    print("-" * 90)


# -------------------- UPDATE EXPENSE --------------------

def update_expense(expenses):
    print("\n--- Update Expense ---")

    if not expenses:
        print("No expenses available.")
        return

    view_expenses(expenses)

    expense_id = get_expense_id(expenses)

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

                if not description:
                    print("Description cannot be empty.")
                    return

                expense["description"] = description

            elif choice == "4":

                expense["amount"] = get_amount()
                expense["category"] = get_category()

                description = input("Enter new description: ").strip()

                if not description:
                    print("Description cannot be empty.")
                    return

                expense["description"] = description

            else:
                print("Invalid option.")
                return

            save_expenses(expenses)

            print("Expense updated successfully!")

            return


# -------------------- DELETE EXPENSE --------------------

def delete_expense(expenses):
    print("\n--- Delete Expense ---")

    if not expenses:
        print("No expenses available.")
        return

    view_expenses(expenses)

    expense_id = get_expense_id(expenses)

    for expense in expenses:

        if expense["id"] == expense_id:

            confirm = input(
                f"Delete '{expense['description']}'? (y/n): "
            ).lower()

            if confirm == "y":

                expenses.remove(expense)

                # Re-number IDs after deletion
                for i, item in enumerate(expenses, start=1):
                    item["id"] = i

                save_expenses(expenses)

                print("Expense deleted successfully!")

            else:
                print("Deletion cancelled.")

            return


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

        category_totals[category] = (
            category_totals.get(category, 0)
            + expense["amount"]
        )

    print("\nCategory-wise Spending:")

    for category, amount in category_totals.items():

        print(f"{category:<20} ₹{amount:.2f}")


# -------------------- MONTHLY SUMMARY --------------------

def show_monthly_summary(expenses):
    print("\n--- Monthly Summary ---")

    if not expenses:
        print("No expenses available.")
        return

    month = input(
        "Enter month (YYYY-MM): "
    ).strip()

    try:
        datetime.strptime(month, "%Y-%m")

    except ValueError:

        print(
            "Invalid month. Use YYYY-MM, "
            "for example 2026-10."
        )

        return

    monthly_expenses = [
        expense
        for expense in expenses
        if expense["date"].startswith(month)
    ]

    if not monthly_expenses:

        print(
            f"No expenses found for {month}."
        )

        return

    total = sum(
        expense["amount"]
        for expense in monthly_expenses
    )

    print(
        f"\nTotal spending for {month}: "
        f"₹{total:.2f}"
    )

    category_totals = {}

    for expense in monthly_expenses:

        category = expense["category"]

        category_totals[category] = (
            category_totals.get(category, 0)
            + expense["amount"]
        )

    print("\nCategory-wise spending:")

    for category, amount in category_totals.items():

        print(
            f"{category:<20} ₹{amount:.2f}"
        )


# -------------------- CSV EXPORT --------------------

def export_to_csv(expenses):
    print("\n--- Export Expenses to CSV ---")

    if not expenses:

        print("No expenses available to export.")

        return

    file_name = "expenses_export.csv"

    try:

        with open(
            file_name,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=[
                    "id",
                    "amount",
                    "category",
                    "description",
                    "date"
                ]
            )

            writer.writeheader()

            writer.writerows(expenses)

        print(
            f"Expenses exported successfully "
            f"to '{file_name}'."
        )

    except OSError as error:

        print(
            f"Could not export expenses: {error}"
        )


# -------------------- MAIN MENU --------------------

def main():

    expenses = load_expenses()

    while True:

        print("\n" + "=" * 45)

        print(
            "             EXPENSE TRACKER"
        )

        print("=" * 45)

        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Update Expense")
        print("4. Delete Expense")
        print("5. Expense Summary")
        print("6. Monthly Summary")
        print("7. Export to CSV")
        print("8. Exit")

        choice = input(
            "\nEnter your choice: "
        ).strip()

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

            show_monthly_summary(expenses)

        elif choice == "7":

            export_to_csv(expenses)

        elif choice == "8":

            print(
                "\nThank you for using Expense Tracker!"
            )

            break

        else:

            print(
                "Invalid choice. Please try again."
            )


# -------------------- PROGRAM START --------------------

if __name__ == "__main__":
    main()
    
