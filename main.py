"""
====================================================
             PYTHON EXPENSE TRACKER
====================================================
A beginner-friendly console-based Expense Tracker.

This project demonstrates:
- Classes and Objects
- Lists
- Dictionaries
- Functions
- Loops
- Conditionals
- File Handling
- Basic Exception Handling

Only Python's standard library is used (json, os, datetime).
====================================================
"""

import json
import os
from datetime import datetime

# Name of the file where all expenses will be saved
DATA_FILE = "expenses.json"


class ExpenseTracker:
    """
    The ExpenseTracker class handles everything related to expenses:
    adding, viewing, searching, saving and loading them.

    We use a CLASS here because it lets us group together:
    - the DATA (the list of expenses)
    - the BEHAVIOUR (the functions that work on that data)
    into a single, organised unit called an "object".
    """

    def __init__(self):
        """
        Constructor: runs automatically when an ExpenseTracker object
        is created.

        self.expenses is a LIST. Each item inside this list is a
        DICTIONARY representing one expense, for example:

            {
                "date": "22/07/2026",
                "category": "Food",
                "description": "Lunch",
                "amount": 300
            }

        We load any previously saved expenses immediately so the
        program "remembers" data between runs.
        """
        self.expenses = []
        self.load_data()

    # ------------------------------------------------------------
    # 1. ADD EXPENSE
    # ------------------------------------------------------------
    def add_expense(self):
        """
        Asks the user for expense details and stores them as a
        dictionary inside self.expenses (our list of expenses).
        """
        print("\n--- Add New Expense ---")

        date = input("Enter date (DD/MM/YYYY): ").strip()

        # Basic validation: make sure the date is in a valid format.
        # try/except is used here for EXCEPTION HANDLING.
        try:
            datetime.strptime(date, "%d/%m/%Y")
        except ValueError:
            print("Invalid date format! Please use DD/MM/YYYY. Expense not added.")
            return

        category = input("Enter category (e.g. Food, Travel, Bills): ").strip()
        description = input("Enter description: ").strip()

        # Amount must be a number, so we validate it using try/except.
        try:
            amount = float(input("Enter amount: ").strip())
        except ValueError:
            print("Invalid amount! Please enter a number. Expense not added.")
            return

        if amount <= 0:
            print("Amount must be greater than zero. Expense not added.")
            return

        # Build the dictionary that represents a single expense.
        expense = {
            "date": date,
            "category": category,
            "description": description,
            "amount": amount
        }

        # Add this dictionary to our list of expenses.
        self.expenses.append(expense)
        print("Expense added successfully!")

    # ------------------------------------------------------------
    # 2. VIEW ALL EXPENSES
    # ------------------------------------------------------------
    def view_expenses(self):
        """
        Displays all expenses in a neat, table-like format.
        Uses a LOOP to go through every dictionary in the list.
        """
        print("\n--- All Expenses ---")

        if not self.expenses:
            print("No expenses recorded yet.")
            return

        # Print table header
        print(f"{'Date':<12}{'Category':<12}{'Description':<20}{'Amount':<10}")
        print("-" * 54)

        # Loop through the list of dictionaries and print each one
        for expense in self.expenses:
            print(f"{expense['date']:<12}{expense['category']:<12}"
                  f"{expense['description']:<20}{expense['amount']:<10}")

        print("-" * 54)

    # ------------------------------------------------------------
    # 3. CATEGORY-WISE EXPENSE
    # ------------------------------------------------------------
    def category_expense(self):
        """
        Asks the user for a category, then displays every expense
        in that category along with the total spent.
        """
        print("\n--- Category-wise Expense ---")

        if not self.expenses:
            print("No expenses recorded yet.")
            return

        category = input("Enter category to search: ").strip()

        # We use a loop + conditional to filter matching expenses.
        matching_expenses = []
        total = 0

        for expense in self.expenses:
            # .lower() is used so search is not case-sensitive
            if expense["category"].lower() == category.lower():
                matching_expenses.append(expense)
                total += expense["amount"]

        if not matching_expenses:
            print(f"No expenses found in category '{category}'.")
            return

        print(f"\nExpenses in category '{category}':")
        print(f"{'Date':<12}{'Description':<20}{'Amount':<10}")
        print("-" * 42)
        for expense in matching_expenses:
            print(f"{expense['date']:<12}{expense['description']:<20}{expense['amount']:<10}")
        print("-" * 42)
        print(f"Total spent in '{category}': {total}")

    # ------------------------------------------------------------
    # 4. SEARCH EXPENSE
    # ------------------------------------------------------------
    def search_expense(self):
        """
        Lets the user search expenses by category, description, or date.
        Demonstrates conditionals (if/elif/else) and loops.
        """
        print("\n--- Search Expense ---")

        if not self.expenses:
            print("No expenses recorded yet.")
            return

        print("Search by:")
        print("1. Category")
        print("2. Description")
        print("3. Date")
        choice = input("Enter your choice (1-3): ").strip()

        keyword = input("Enter search keyword: ").strip().lower()
        results = []

        for expense in self.expenses:
            if choice == "1" and keyword in expense["category"].lower():
                results.append(expense)
            elif choice == "2" and keyword in expense["description"].lower():
                results.append(expense)
            elif choice == "3" and keyword in expense["date"].lower():
                results.append(expense)

        if choice not in ("1", "2", "3"):
            print("Invalid choice.")
            return

        if not results:
            print("No matching expenses found.")
            return

        print(f"\nFound {len(results)} matching expense(s):")
        print(f"{'Date':<12}{'Category':<12}{'Description':<20}{'Amount':<10}")
        print("-" * 54)
        for expense in results:
            print(f"{expense['date']:<12}{expense['category']:<12}"
                  f"{expense['description']:<20}{expense['amount']:<10}")

    # ------------------------------------------------------------
    # 5. VIEW TOTAL EXPENSE
    # ------------------------------------------------------------
    def total_expense(self):
        """
        Calculates and displays the total amount spent across
        all expenses using a simple loop.
        """
        print("\n--- Total Expense ---")

        if not self.expenses:
            print("No expenses recorded yet.")
            return

        total = 0
        for expense in self.expenses:
            total += expense["amount"]

        print(f"Total amount spent: {total}")

    # ------------------------------------------------------------
    # 6. SAVE DATA (FILE HANDLING)
    # ------------------------------------------------------------
    def save_data(self):
        """
        Saves the entire list of expense dictionaries into a JSON
        file so data is not lost when the program closes.
        """
        try:
            with open(DATA_FILE, "w") as file:
                json.dump(self.expenses, file, indent=4)
            print("Data saved successfully!")
        except Exception as error:
            print(f"Something went wrong while saving data: {error}")

    # ------------------------------------------------------------
    # 7. LOAD DATA (FILE HANDLING)
    # ------------------------------------------------------------
    def load_data(self):
        """
        Loads expenses from the JSON file when the program starts.
        If the file doesn't exist yet (first run), we simply start
        with an empty list instead of crashing.
        """
        if not os.path.exists(DATA_FILE):
            self.expenses = []
            return

        try:
            with open(DATA_FILE, "r") as file:
                self.expenses = json.load(file)
        except (json.JSONDecodeError, Exception) as error:
            print(f"Could not read saved data ({error}). Starting fresh.")
            self.expenses = []

    # ------------------------------------------------------------
    # BONUS: DELETE EXPENSE
    # ------------------------------------------------------------
    def delete_expense(self):
        """
        Bonus feature: deletes an expense chosen by its position
        in the list (index).
        """
        print("\n--- Delete Expense ---")

        if not self.expenses:
            print("No expenses recorded yet.")
            return

        self._print_indexed_expenses()

        try:
            choice = int(input("Enter the number of the expense to delete: "))
        except ValueError:
            print("Please enter a valid number.")
            return

        index = choice - 1
        if 0 <= index < len(self.expenses):
            removed = self.expenses.pop(index)
            print(f"Deleted expense: {removed['description']} ({removed['amount']})")
        else:
            print("Invalid expense number.")

    # ------------------------------------------------------------
    # BONUS: EDIT EXPENSE
    # ------------------------------------------------------------
    def edit_expense(self):
        """
        Bonus feature: lets the user edit an existing expense.
        Leaving a field blank keeps the old value.
        """
        print("\n--- Edit Expense ---")

        if not self.expenses:
            print("No expenses recorded yet.")
            return

        self._print_indexed_expenses()

        try:
            choice = int(input("Enter the number of the expense to edit: "))
        except ValueError:
            print("Please enter a valid number.")
            return

        index = choice - 1
        if not (0 <= index < len(self.expenses)):
            print("Invalid expense number.")
            return

        expense = self.expenses[index]
        print("Leave a field blank to keep its current value.")

        new_date = input(f"Date [{expense['date']}]: ").strip()
        new_category = input(f"Category [{expense['category']}]: ").strip()
        new_description = input(f"Description [{expense['description']}]: ").strip()
        new_amount = input(f"Amount [{expense['amount']}]: ").strip()

        if new_date:
            try:
                datetime.strptime(new_date, "%d/%m/%Y")
                expense["date"] = new_date
            except ValueError:
                print("Invalid date format, keeping old date.")

        if new_category:
            expense["category"] = new_category

        if new_description:
            expense["description"] = new_description

        if new_amount:
            try:
                expense["amount"] = float(new_amount)
            except ValueError:
                print("Invalid amount, keeping old amount.")

        print("Expense updated successfully!")

    # ------------------------------------------------------------
    # BONUS: MONTHLY EXPENSE SUMMARY
    # ------------------------------------------------------------
    def monthly_summary(self):
        """
        Bonus feature: groups expenses by month (MM/YYYY) and
        shows the total spent in each month.
        Demonstrates dictionaries used for grouping/aggregation.
        """
        print("\n--- Monthly Expense Summary ---")

        if not self.expenses:
            print("No expenses recorded yet.")
            return

        # This dictionary will map "MM/YYYY" -> total amount
        monthly_totals = {}

        for expense in self.expenses:
            # date is stored as DD/MM/YYYY, so split it to get MM/YYYY
            parts = expense["date"].split("/")
            month_key = f"{parts[1]}/{parts[2]}"

            if month_key in monthly_totals:
                monthly_totals[month_key] += expense["amount"]
            else:
                monthly_totals[month_key] = expense["amount"]

        print(f"{'Month':<10}{'Total Spent':<10}")
        print("-" * 20)
        for month, total in monthly_totals.items():
            print(f"{month:<10}{total:<10}")

    # ------------------------------------------------------------
    # BONUS: HIGHEST / LOWEST EXPENSE
    # ------------------------------------------------------------
    def highest_lowest_expense(self):
        """
        Bonus feature: finds and displays the highest and lowest
        single expenses recorded.
        """
        print("\n--- Highest & Lowest Expense ---")

        if not self.expenses:
            print("No expenses recorded yet.")
            return

        highest = self.expenses[0]
        lowest = self.expenses[0]

        for expense in self.expenses:
            if expense["amount"] > highest["amount"]:
                highest = expense
            if expense["amount"] < lowest["amount"]:
                lowest = expense

        print(f"Highest expense: {highest['description']} - {highest['amount']} "
              f"({highest['category']} on {highest['date']})")
        print(f"Lowest expense: {lowest['description']} - {lowest['amount']} "
              f"({lowest['category']} on {lowest['date']})")

    # ------------------------------------------------------------
    # HELPER FUNCTION (used by delete/edit)
    # ------------------------------------------------------------
    def _print_indexed_expenses(self):
        """
        Small helper function that prints all expenses along with
        their position number, so the user can pick one to edit
        or delete. The underscore prefix is just a convention
        meaning "this is a helper, used internally by the class".
        """
        for i, expense in enumerate(self.expenses, start=1):
            print(f"{i}. {expense['date']} | {expense['category']} | "
                  f"{expense['description']} | {expense['amount']}")

    # ------------------------------------------------------------
    # MAIN MENU LOOP
    # ------------------------------------------------------------
    def run(self):
        """
        Displays the menu in a loop and calls the correct function
        based on the user's choice. The program keeps running
        until the user chooses to exit.
        """
        while True:
            print("\n======== Expense Tracker ========")
            print("1. Add Expense")
            print("2. View Expenses")
            print("3. Category-wise Expense")
            print("4. Search Expense")
            print("5. View Total Expense")
            print("6. Save Data")
            print("7. Exit")
            print("8. Delete Expense (Bonus)")
            print("9. Edit Expense (Bonus)")
            print("10. Monthly Summary (Bonus)")
            print("11. Highest/Lowest Expense (Bonus)")

            choice = input("Enter your choice: ").strip()

            # A simple if/elif chain to route the user's choice
            if choice == "1":
                self.add_expense()
            elif choice == "2":
                self.view_expenses()
            elif choice == "3":
                self.category_expense()
            elif choice == "4":
                self.search_expense()
            elif choice == "5":
                self.total_expense()
            elif choice == "6":
                self.save_data()
            elif choice == "7":
                self.save_data()  # auto-save before exiting
                print("Data saved. Goodbye!")
                break
            elif choice == "8":
                self.delete_expense()
            elif choice == "9":
                self.edit_expense()
            elif choice == "10":
                self.monthly_summary()
            elif choice == "11":
                self.highest_lowest_expense()
            else:
                print("Invalid choice! Please enter a number between 1 and 11.")


# --------------------------------------------------------
# PROGRAM ENTRY POINT
# --------------------------------------------------------
if __name__ == "__main__":
    tracker = ExpenseTracker()  
    tracker.run()               