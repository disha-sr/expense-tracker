# Expense Tracker 💰

A simple command-line Expense Tracker built with Python.
The project allows users to enter their expenses, select a category, and save the expense data to a CSV file.

## Features

* Add a new expense
* Enter expense name and amount
* Select an expense category
* Store expenses in a CSV file
* Display expense information
* Simple command-line interface

## Categories

The Expense Tracker currently supports:

* Food
* Home
* Work
* Fun
* Misc

## Technologies Used

* **Python**
* **CSV**
* **Object-Oriented Programming (OOP)**
* **Git & GitHub**

## Project Structure

```text
Expense Tracker/
│
├── expense.py
├── expense_tracker.py
├── .gitignore
├── README.md
└── expenses.csv
```

> `expenses.csv` is used to store expense data locally and is excluded from GitHub using `.gitignore`.

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/disha-sr/expense-tracker.git
```

### 2. Navigate to the project

```bash
cd expense-tracker
```

### 3. Run the application

```bash
python expense_tracker.py
```

## Example

```text
Running Expense Tracker!
Getting user expense!

Enter expense name: Burger
Enter expense amount: 12

Select a category:
 1. Food
 2. Home
 3. Work
 4. Fun
 5. Misc

Enter a category number [1-5]: 1

Saving user expense <Expense: Burger, Food, $12.00>
```

## Future Improvements

Some features planned for future versions:

* View all saved expenses
* Calculate total expenses
* Calculate expenses by category
* Add date and time to each expense
* Edit or delete expenses
* Monthly expense summaries
* Add a graphical user interface

## Author

**Disha Srivastava**

GitHub: [@disha-sr](https://github.com/disha-sr)
