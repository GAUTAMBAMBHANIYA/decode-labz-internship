# ==========================================
# EXPENSE TRACKER PRO
# Part 1 - Setup & File Handling
# ==========================================

import os
import json
from datetime import datetime

DATA_FILE = "expenses.json"

expenses = []
budget_limit = 10000


# ==========================================
# SCREEN UTILITIES
# ==========================================

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def pause():
    input("\nPress Enter to continue...")


# ==========================================
# FILE HANDLING
# ==========================================

def save_data():
    data = {
        "budget_limit": budget_limit,
        "expenses": expenses
    }

    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)


def load_data():
    global expenses
    global budget_limit

    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as file:
                data = json.load(file)

                expenses = data.get("expenses", [])
                budget_limit = data.get("budget_limit", 10000)

        except:
            expenses = []
            budget_limit = 10000


# ==========================================
# DATE & TIME
# ==========================================

def current_datetime():
    return datetime.now().strftime("%d-%m-%Y %H:%M:%S")


# ==========================================
# HEADER
# ==========================================

def show_header():

    clear_screen()

    print("=" * 60)
    print("             EXPENSE TRACKER PRO")
    print("=" * 60)
    print("Track Your Daily Expenses Easily")
    print("=" * 60)


# ==========================================
# CATEGORY LIST
# ==========================================

def get_categories():

    return [
        "Food",
        "Travel",
        "Shopping",
        "Bills",
        "Medical",
        "Education",
        "Entertainment",
        "Other"
    ]


# ==========================================
# DISPLAY CATEGORIES
# ==========================================

def show_categories():

    categories = get_categories()

    print("\nAvailable Categories:\n")

    for index, category in enumerate(categories, start=1):
        print(f"{index}. {category}")


# ==========================================
# SELECT CATEGORY
# ==========================================

def choose_category():

    categories = get_categories()

    while True:

        try:
            show_categories()

            choice = int(
                input("\nSelect Category Number: ")
            )

            if 1 <= choice <= len(categories):
                return categories[choice - 1]

            else:
                print("Invalid Choice!")

        except ValueError:
            print("Enter Valid Number!")


# ==========================================
# TOTAL EXPENSE
# ==========================================

def get_total_expense():

    total = 0

    for expense in expenses:
        total += expense["amount"]

    return total


# ==========================================
# BUDGET CHECK
# ==========================================

def check_budget():

    total = get_total_expense()

    if total >= budget_limit:

        print("\n⚠ WARNING!")
        print("Budget Limit Reached!")
        print(f"Budget : ₹{budget_limit}")
        print(f"Spent  : ₹{total}")


# ==========================================
# STARTUP
# ==========================================

load_data()
# ==========================================
# ADD NEW EXPENSE
# ==========================================

def add_expense():

    show_header()

    try:

        title = input("Expense Title : ").strip()

        amount = float(input("Amount (₹): "))

        if amount <= 0:
            print("Amount must be greater than zero.")
            pause()
            return

        category = choose_category()

        note = input("Note (Optional): ")

        expense = {
            "title": title,
            "amount": amount,
            "category": category,
            "note": note,
            "date": current_datetime()
        }

        expenses.append(expense)

        save_data()

        print("\nExpense Added Successfully.")

        check_budget()

    except ValueError:
        print("\nInvalid Amount!")

    pause()


# ==========================================
# VIEW ALL EXPENSES
# ==========================================

def view_expenses():

    show_header()

    if len(expenses) == 0:
        print("No Expenses Found.")
        pause()
        return

    print("-" * 90)

    for index, expense in enumerate(expenses, start=1):

        print(f"{index}. {expense['title']}")
        print(f"   Amount   : ₹{expense['amount']}")
        print(f"   Category : {expense['category']}")
        print(f"   Date     : {expense['date']}")
        print(f"   Note     : {expense['note']}")
        print("-" * 90)

    pause()


# ==========================================
# SEARCH EXPENSE
# ==========================================

def search_expense():

    show_header()

    keyword = input("Enter Title to Search : ").lower()

    found = False

    print()

    for expense in expenses:

        if keyword in expense["title"].lower():

            found = True

            print("-" * 80)
            print("Title    :", expense["title"])
            print("Amount   : ₹", expense["amount"])
            print("Category :", expense["category"])
            print("Date     :", expense["date"])
            print("Note     :", expense["note"])

    if not found:
        print("No Expense Found.")

    pause()


# ==========================================
# DELETE EXPENSE
# ==========================================

def delete_expense():

    show_header()

    if len(expenses) == 0:
        print("Expense List Empty.")
        pause()
        return

    view_expenses()

    try:

        number = int(input("\nEnter Expense Number to Delete : "))

        if 1 <= number <= len(expenses):

            deleted = expenses.pop(number - 1)

            save_data()

            print("\nExpense Deleted Successfully.")
            print("Deleted :", deleted["title"])

        else:
            print("Invalid Number.")

    except ValueError:
        print("Enter Valid Number.")

    pause()


# ==========================================
# CLEAR ALL EXPENSES
# ==========================================

def clear_all_expenses():

    show_header()

    if len(expenses) == 0:
        print("Expense List Already Empty.")
        pause()
        return

    choice = input("Delete ALL Expenses? (yes/no): ").lower()

    if choice == "yes":

        expenses.clear()

        save_data()

        print("\nAll Expenses Deleted Successfully.")

    else:

        print("\nOperation Cancelled.")

    pause()
# ==========================================
# EDIT EXPENSE
# ==========================================

def edit_expense():

    show_header()

    if len(expenses) == 0:
        print("No Expenses Available.")
        pause()
        return

    view_expenses()

    try:
        index = int(input("\nEnter Expense Number to Edit: ")) - 1

        if index < 0 or index >= len(expenses):
            print("Invalid Expense Number.")
            pause()
            return

        expense = expenses[index]

        print("\nLeave blank to keep old value.")

        title = input(f"Title ({expense['title']}): ")
        if title:
            expense["title"] = title

        amount = input(f"Amount ({expense['amount']}): ")
        if amount:
            expense["amount"] = float(amount)

        note = input(f"Note ({expense['note']}): ")
        if note:
            expense["note"] = note

        category = input("Change Category? (yes/no): ").lower()

        if category == "yes":
            expense["category"] = choose_category()

        expense["date"] = current_datetime()

        save_data()

        print("\nExpense Updated Successfully.")

    except ValueError:
        print("Invalid Input.")

    pause()


# ==========================================
# EXPENSE STATISTICS
# ==========================================

def show_statistics():

    show_header()

    if len(expenses) == 0:
        print("No Expense Found.")
        pause()
        return

    amounts = [expense["amount"] for expense in expenses]

    print("=" * 45)
    print("          EXPENSE STATISTICS")
    print("=" * 45)

    print(f"Total Transactions : {len(expenses)}")
    print(f"Total Expense      : ₹{sum(amounts):.2f}")
    print(f"Highest Expense    : ₹{max(amounts):.2f}")
    print(f"Lowest Expense     : ₹{min(amounts):.2f}")
    print(f"Average Expense    : ₹{sum(amounts)/len(amounts):.2f}")

    pause()


# ==========================================
# CATEGORY REPORT
# ==========================================

def category_report():

    show_header()

    if len(expenses) == 0:
        print("No Expenses Available.")
        pause()
        return

    report = {}

    for expense in expenses:

        category = expense["category"]

        report[category] = report.get(category, 0) + expense["amount"]

    print("=" * 45)
    print("        CATEGORY REPORT")
    print("=" * 45)

    for category, total in report.items():
        print(f"{category:<20} ₹{total:.2f}")

    pause()


# ==========================================
# TODAY'S EXPENSE
# ==========================================

def today_expense():

    show_header()

    today = datetime.now().strftime("%d-%m-%Y")

    total = 0

    print("Today's Expenses\n")

    for expense in expenses:

        if expense["date"].startswith(today):

            print(f"{expense['title']}  ₹{expense['amount']}")

            total += expense["amount"]

    print("\n--------------------------")
    print(f"Today's Total : ₹{total:.2f}")

    pause()


# ==========================================
# MONTHLY REPORT
# ==========================================

def monthly_report():

    show_header()

    current_month = datetime.now().strftime("%m-%Y")

    total = 0

    print("Monthly Report\n")

    for expense in expenses:

        expense_month = expense["date"][3:10]

        if expense_month == current_month:

            print(
                f"{expense['title']} | "
                f"{expense['category']} | "
                f"₹{expense['amount']}"
            )

            total += expense["amount"]

    print("\n----------------------------")
    print(f"Monthly Expense : ₹{total:.2f}")

    pause()


# ==========================================
# FINAL REPORT
# ==========================================

def final_report():

    show_header()

    if len(expenses) == 0:
        print("No Expense Available.")
        pause()
        return

    total = get_total_expense()

    print("=" * 50)
    print("            FINAL REPORT")
    print("=" * 50)

    print(f"Transactions : {len(expenses)}")
    print(f"Total Spent  : ₹{total:.2f}")
    print(f"Budget Limit : ₹{budget_limit:.2f}")
    print(f"Remaining    : ₹{budget_limit-total:.2f}")

    print("\nThank You For Using Expense Tracker Pro!")

    pause()
# ==========================================
# CHANGE BUDGET
# ==========================================

def change_budget():

    global budget_limit

    show_header()

    try:
        new_budget = float(input("Enter New Budget Limit : ₹"))

        if new_budget <= 0:
            print("Budget should be greater than 0.")
        else:
            budget_limit = new_budget
            save_data()
            print("Budget Updated Successfully!")

    except ValueError:
        print("Invalid Budget.")

    pause()


# ==========================================
# MAIN MENU
# ==========================================

def menu():

    while True:

        show_header()

        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Search Expense")
        print("4. Edit Expense")
        print("5. Delete Expense")
        print("6. Clear All Expenses")
        print("7. Expense Statistics")
        print("8. Category Report")
        print("9. Today's Expense")
        print("10. Monthly Report")
        print("11. Change Budget")
        print("12. Final Report")
        print("13. Exit")

        print("=" * 60)

        choice = input("Enter Your Choice : ")

        if choice == "1":
            add_expense()

        elif choice == "2":
            view_expenses()

        elif choice == "3":
            search_expense()

        elif choice == "4":
            edit_expense()

        elif choice == "5":
            delete_expense()

        elif choice == "6":
            clear_all_expenses()

        elif choice == "7":
            show_statistics()

        elif choice == "8":
            category_report()

        elif choice == "9":
            today_expense()

        elif choice == "10":
            monthly_report()

        elif choice == "11":
            change_budget()

        elif choice == "12":
            final_report()

        elif choice == "13":

            show_header()

            print("Saving Data...")

            save_data()

            print("\nThank You For Using")
            print("Expense Tracker Pro ❤️")
            print("\nProject Developed Using Python")
            print("DecodeLabs Internship Project")

            break

        else:

            print("Invalid Choice!")
            pause()


# ==========================================
# PROGRAM START
# ==========================================

if __name__ == "__main__":
    menu()
