import io
from flask import Flask, render_template, request, redirect, send_file, url_for, session
import mysql.connector
from datetime import datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt

app = Flask(__name__)
app.secret_key = "your_secret_key"

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root"
)
cursor = conn.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS expense_tracker")
cursor.execute("USE expense_tracker")

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    username VARCHAR(50) NOT NULL PRIMARY KEY,
    password VARCHAR(255) NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    username VARCHAR(50) NOT NULL,
    expense_description VARCHAR(255) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    expense_date DATE NOT NULL,
    category VARCHAR(50) NOT NULL,
    PRIMARY KEY (username, expense_description, expense_date),
    FOREIGN KEY (username) REFERENCES users(username)
)
""")

conn.commit()
conn.close()


def check_account(username, password):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="root",
        database="expense_tracker"
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM users WHERE username=%s AND password=%s",
        (username, password)
    )
    account = cursor.fetchone()
    conn.close()
    return account


def get_account(username):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="root",
        database="expense_tracker"
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM users WHERE username=%s",
        (username,)
    )
    account = cursor.fetchone()
    conn.close()
    return account


def register_account(username, password):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="root",
        database="expense_tracker"
    )
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (username, password) VALUES (%s, %s)",
        (username, password)
    )
    conn.commit()
    conn.close()


@app.route('/index')
def index():
    if "loggedin" not in session:
        return redirect(url_for("login"))
    return render_template("index.html")


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username and password:
            account = check_account(username, password)
            if account:
                session["loggedin"] = True
                session["username"] = username
                return redirect(url_for("index"))
            else:
                msg = "Incorrect username or password!"
        else:
            msg = "Please fill out the form!"

    return render_template("login.html", msg=msg)


@app.route('/logout')
def logout():
    session.pop("loggedin", None)
    session.pop("username", None)
    return redirect(url_for("login"))


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username and password:
            if get_account(username):
                msg = "Account already exists!"
            else:
                register_account(username, password)
                return redirect(url_for("login"))
        else:
            msg = "Please fill out the form!"

    return render_template("register.html", msg=msg)


@app.route("/addExpense", methods=["GET", "POST"])
def addExpense():
    msg = ""
    if request.method == "POST":
        description = request.form.get("expense_description")
        category = request.form.get("category")
        amount = request.form.get("amount")
        date = request.form.get("expense_date")

        if not description or not category or not amount or not date:
            msg = "Please fill in all fields!"
        else:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="root",
                database="expense_tracker"
            )
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO expenses (username, expense_description, amount, expense_date, category) VALUES (%s, %s, %s, %s, %s)",
                (session["username"], description, amount, date, category)
            )
            conn.commit()
            conn.close()
            msg = "Expense added successfully!"

    return render_template("addExpense.html", msg=msg)


@app.route("/deleteExpense", methods=["GET", "POST"])
def deleteExpense():
    msg = ""
    if request.method == "POST":
        category = request.form.get("category")
        amount = request.form.get("amount")

        if not category or not amount:
            msg = "Please fill in all fields!"
        else:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="root",
                database="expense_tracker"
            )
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM expenses WHERE username = %s AND amount = %s AND category = %s",
                (session["username"], amount, category)
            )
            conn.commit()
            msg = "Expense deleted successfully!" if cursor.rowcount else "No matching expense found to delete."
            conn.close()

    return render_template("deleteExpense.html", msg=msg)


@app.route("/updateExpense", methods=["GET", "POST"])
def updateExpense():
    msg = ""
    if request.method == "POST":
        old_desc = request.form.get("old_description")
        old_date = request.form.get("old_date")
        new_desc = request.form.get("new_description")
        new_category = request.form.get("new_category")
        new_amount = request.form.get("new_amount")
        new_date = request.form.get("new_date")

        if not old_desc or not old_date or not new_desc or not new_category or not new_amount or not new_date:
            msg = "Please fill in all fields!"
        else:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="root",
                database="expense_tracker"
            )
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE expenses
                SET expense_description=%s, category=%s, amount=%s, expense_date=%s
                WHERE username=%s AND expense_description=%s AND expense_date=%s
            """, (new_desc, new_category, new_amount, new_date, session["username"], old_desc, old_date))
            conn.commit()
            msg = "Expense updated successfully!" if cursor.rowcount else "No matching expense found to update."
            conn.close()

    return render_template("updateExpense.html", msg=msg)


@app.route("/viewExpense")
def viewExpense():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="root",
        database="expense_tracker"
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT expense_description, amount, expense_date, category
        FROM expenses
        WHERE username = %s
        ORDER BY expense_date DESC
    """, (session["username"],))
    records = cursor.fetchall()
    conn.close()
    return render_template("viewExpense.html", expenses=records)


@app.route("/spendingSummary")
def spendingSummary():
    if "loggedin" not in session:
        return redirect(url_for("login"))
    return render_template("spendingSummary.html")


@app.route("/spendingSummaryChart")
def spendingSummaryChart():

    months = int(request.args.get("months", 3))
    today = datetime.today()
    start_date = today - timedelta(days=30*months)

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="root",
        database="expense_tracker"
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT amount, expense_date
        FROM expenses
        WHERE username=%s AND expense_date >= %s
    """, (session["username"], start_date))
    rows = cursor.fetchall()
    conn.close()

    if rows:
        dates = np.array([row['expense_date'] for row in rows])
        amounts = np.array([float(row['amount']) for row in rows])
        month_labels = []
        month_totals = []
        for i in range(months):
            month = today - timedelta(days=30*i)
            month_str = month.strftime("%Y-%m")
            mask = np.array([d.strftime("%Y-%m") == month_str for d in dates])
            total = np.sum(amounts[mask])
            month_labels.insert(0, month_str)
            month_totals.insert(0, total)
    else:
        month_labels = []
        month_totals = []

    fig, ax = plt.subplots(figsize=(8,4))
    ax.bar(month_labels, month_totals, color='skyblue')
    ax.set_title('Total Expenses per Month')
    ax.set_xlabel('Month')
    ax.set_ylabel('Total Expenses (€)')
    plt.tight_layout()
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    return send_file(img, mimetype='image/png')


if __name__ == "__main__":
    app.run(host="localhost", debug=True)
