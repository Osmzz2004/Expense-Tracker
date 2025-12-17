<<<<<<< HEAD
Expense Tracker Application

Overview

The Expense Tracker is a web application built with Flask that allows users to manage their personal expenses. Users can register and log in, add new expenses, update or delete existing expenses, view a list of all expenses, and analyze their spending through a dashboard.

Setting up the Application

1. Make sure Python 3.x is installed on your system.
2. Make sure MySQL server is installed and running locally. Default username is root and password is root.
3. Install the required Python packages using pip:
   pip install flask mysql-connector-python numpy matplotlib
4. Copy the project files into a folder on your computer.
5. The application automatically creates the database (expense_tracker) and tables (users and expenses) on first run. No manual SQL setup is required.


Features

Register and Login
  Users can create a new account or log in to an existing account. Sessions keep users logged in securely.

Add Expense
  Users can add a new expense by providing description, category, amount, and date. All fields are validated to ensure they are filled.

Update Expense
  Users can update an existing expense by specifying the current description and date and providing new values. If the expense does not exist, a message notifies the user.

Delete Expense
  Users can delete an expense by specifying the category and amount. If no matching expense exists, a message is displayed.

View Expenses
  Users can see a list of all their expenses sorted by date. Each entry shows the description, category, amount, and date.

Spending Dashboard
  Users can visualize their total expenses per month. Features include:
    - Time Range Selection: Users can select to view expenses for the past 3, 6, or 12 months.
    - Monthly Totals Calculation: The application calculates the total expenses for each month in the selected range.
    - Bar Chart Visualization: A bar chart shows monthly totals using Matplotlib.
    - Interactive Updates: Selecting a different time range updates the chart dynamically without reloading the page.
=======
# Expense-Tracker
A Flask-based expense tracker web application that allows users to securely register and log in to manage personal expenses. The application supports full CRUD operations, MySQL database integration, session-based authentication, and a visual monthly spending summary generated using Matplotlib.

Features
- User registration and login
- Secure session-based authentication
- Add, view, update, and delete expenses
- Expenses linked to individual users
- Monthly spending summary with graphical visualization
- Automatic database and table creation

Technologies Used
- Python (Flask)
- MySQL
- HTML & Jinja2 Templates
- Matplotlib & NumPy

How to Run
1.Clone the repository
2.Set up a MySQL database and update credentials in app.py
3.Create and activate a virtual environment
4.Install dependencies
5.Run the application using python app.py
6.Open http://localhost:5000 in your browser

Purpose
This project demonstrates core web development concepts including authentication, database operations, data visualization, and backend–frontend integration using Flask.
>>>>>>> 369222a1d83453f01f95514f83824aa6ca4c5d2b
