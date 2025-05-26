import datetime
from typing import List, Dict

"""
------------------------------------------------------------------------------
|   Date     |     Category      |   Amount    |        Description          |
------------------------------------------------------------------------------
| 2025-05-20 | Groceries         |    $45.90   | Fruits and veggies          |
| 2025-05-21 | Transportation    |    $10.00   | Bus fare                    |
| 2025-05-22 | Dining Out        |    $25.50   | Lunch with friends          |
------------------------------------------------------------------------------
"""


class ExpenseTracker:
    def __init__(self):
        self.expenses = []

    def add_expense(self, date: str, amount: float, category: str, description: str = ""):
        """Add a new expense to the tracker"""
        try:
            parsed_date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
            expense = {
                'date': parsed_date,
                'amount': amount,
                'category': category,
                'description': description
            }
            self.expenses.append(expense)
            return True
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
            return False

    def filter_expenses(self, start_date: str = None, end_date: str = None, category: str = None) -> List[Dict]:
        """Filter expenses by date range and/or category"""
        filtered = self.expenses.copy()

        if start_date:
            start = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
            filtered = [e for e in filtered if e['date'] >= start]

        if end_date:
            end = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
            filtered = [e for e in filtered if e['date'] <= end]

        if category:
            filtered = [e for e in filtered if e['category'].lower() == category.lower()]

        return filtered

    def get_summary(self) -> Dict:
        """Generate summary of expenses by category and total"""
        summary = {
            'categories': {},
            'total': 0.0
        }

        for expense in self.expenses:
            category = expense['category']
            amount = expense['amount']

            if category not in summary['categories']:
                summary['categories'][category] = 0.0
            summary['categories'][category] += amount
            summary['total'] += amount

        return summary


def display_menu():
    # Display menu
    print("\nExpense Tracker Menu:")
    print("1. Add New Expense")
    print("2. View All Expenses")
    print("3. Filter Expenses")
    print("4. View Summary")
    print("5. Exit")


def get_user_input(prompt, input_type=str):
    while True:
        try:
            user_input = input(prompt)
            if input_type == float:
                return float(user_input)
            return user_input
        except ValueError:
            print(f"Invalid input. Please enter a valid {input_type.__name__}.")


def main():
    tracker = ExpenseTracker()

    while True:
        display_menu()
        choice = get_user_input("Enter your choice (1-5): ")
        if not choice.isdigit():
            print("Invalid choice. Please enter a number between 1 and 5.")
            continue
        else:
           choice =  int(choice)


        if choice == 1:
            print("\nAdd New Expense:")
            print("(Enter 'q' at any time to cancel)")

            # Date input with continuous validation
            while True:
                date = input("Enter date (YYYY-MM-DD): ").strip()
                if date.lower() == 'q':
                    print("Expense entry cancelled.")
                    break  # Exit completely

                try:
                    datetime.datetime.strptime(date, "%Y-%m-%d")
                    # Date is valid - proceed to amount entry
                    while True:
                        amount_str = input("Enter amount: ").strip()
                        if amount_str.lower() == 'q':
                            print("Expense entry cancelled.")
                            break

                        try:
                            amount = float(amount_str)
                            if amount >= 0:
                                # Amount is valid - proceed to category
                                while True:
                                    category = input("Enter category: ").strip()
                                    if category.lower() == 'q':
                                        print("Expense entry cancelled.")
                                        break

                                    if category:
                                        # All inputs valid - add expense
                                        description = input("Enter description (optional): ").strip()
                                        if tracker.add_expense(date, amount, category, description):
                                            print(f"Expense added successfully!")
                                        else:
                                            print("Failed to add expense.")
                                        break  # Exit category loop
                                    print("Category cannot be empty. Try again.")
                                break  # Exit amount loop
                            print("Amount must be positive. Try again.")
                        except ValueError:
                            print("Invalid amount. Please enter a number (e.g., 15.99)")
                    break  # Exit date loop

                except ValueError:
                    print("Invalid format. Please use YYYY-MM-DD (e.g., 2023-12-31)")

        elif choice == 2:
            print("\nAll Expenses:\n")
            # Print header with aligned columns
            print(f"{'Date':<12} | {'Category':<15} | {'Amount':>10} | Description")
            print("-" * 60)
            # Print each expense with consistent formatting
            for expense in tracker.expenses:
                date_str = expense['date'].strftime("%Y-%m-%d")  # Convert date to string
                category = expense['category']
                amount = float(expense['amount'])
                description = expense['description']
                print(f"{date_str:<12} | {category:<15} | {f'${amount:.2f}':>10} | {description}")


        elif choice == 3:
            print("\nFilter Expenses:")
            start_date = get_user_input("Enter start date (YYYY-MM-DD, leave empty for no filter): ")
            try:
                datetime.datetime.strptime(start_date, "%Y-%m-%d")
            except ValueError:
                print("Invalid start date format. Skipping.")
                start_date = None

            end_date = get_user_input("Enter end date (YYYY-MM-DD, leave empty for no filter): ")
            try:
                datetime.datetime.strptime(end_date, "%Y-%m-%d")
            except ValueError:
                print("Invalid start date format. Skipping.")
                end_date = None

            category = get_user_input("Enter category to filter by (leave empty for no filter): ")

            filtered = tracker.filter_expenses(
                start_date if start_date else None,
                end_date if end_date else None,
                category if category else None
            )

            print("\nFiltered Expenses:")
            print("-" * 85)  # Header separator
            print(f"| {'Date':<10} | {'Category':<20} | {'Amount':>12} | {'Description':<31} |")
            print("-" * 85)
            for expense in filtered:
                date_str = expense['date'].strftime("%Y-%m-%d")  # Format date as string
                amount = float(expense['amount'])  # Ensure amount is numeric
                print(
                    f"| {date_str:<10} | {expense['category']:<20} | {f'${amount:>.2f}':>11} | {expense['description']:<31} |")
            print("-" * 85)

        elif choice == 4:
            summary = tracker.get_summary()
            print("\nExpense Summary:")
            print("-" * 37)  # Header separator
            print(f"| {'Category':<20} | {'Amount':>10} |")
            print("-" * 37)
            for category, amount in sorted(summary['categories'].items()):
                print(f"| {category:<20} | ${amount:>9.2f} |")
            print("-" * 37)
            print(f"| {'TOTAL':<20} | ${summary['total']:>9.2f} |")
            print("-" * 37)

        elif choice == 5:
            print("Exiting Expense Tracker. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 5.")


if __name__ == "__main__":
    main()
