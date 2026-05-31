# Personal Expense Tracker

A simple command-line application to track expenses. This application allows users to add, view, delete expenses, and generate reports on their spending habits. It uses a JSON file to store data and matplotlib to visualize expense distribution.

## Features

- **Add Expense**: Enter details for new expenses including amount, category, date, and description.

- **View Expenses**: Display all expenses or filter by category.

- **Delete Expense**: Remove an expense entry by its index.

- **Generate Report**: Create a bar chart showing the distribution of expenses by category.

## Requirements

- Python 3.x

- Matplotlib library

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/Atpswift/expense-tracker-python.git

   ```

2. **Navigate to the Project Directory**:

   ```bash
   cd expense-tracker

   ```

3. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt

   ```

## Usage

1. **Run the application**:

   ```bash
   python expense_tracker.py

   ```

2. **Follow the On-Screen Instructions**:

   - **Add an Expense**: Enter the amount, category, date (or leave blank for today), and description.

   - **View Expenses**: Filter by category or view all expenses.

   - **Delete an Expense**: Provide the index of the expense you want to delete.

   - **Generate a Report**: View a bar chart of expenses categorized by type.

## Code Overview

- **`ExpenseTracker` Class**:

  - **`__init__()`**: Initializes the class and loads existing expenses.

  - **`load_data()`**: Loads expenses from a JSON file.

  - **`save_data()`**: Save expenses to a JSON file.

  - **`add_expenses()`**: Adds a new expense.

  - **`delete_expense()`**: Deletes an expense by index.

  - **`view_expenses()`**: View expenses with optional category filtering.

  - **`generate_report()`**: Generates a bar chart of expenses by category.

  - **`run()`**: Main loop to handle user interactions.

## Manual Testing

I performed the following tests to validate functionality of the program:

1. **Add Expense**: Verified that expenses are added and saved correctly.

2. **View Expenses**: Ensured all expenses are displayed and filtering works.

3. **Delete Expense**: Confirmed that the correct expense is deleted and the list updates.

4. **Generate Report**: Checked that the bar chart accurately represents expense distribution.

## Deployment 

You can see the deployment here: https://python-expense-tracker896-f8aa49a1c241.herokuapp.com/

