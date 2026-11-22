# 🏥 Hospital Management System

> A lightweight desktop dashboard for exploring and managing hospital data stored in MySQL.

**Python · Tkinter · MySQL**

The app opens a native desktop interface—no browser, HTML, or CSS required. It discovers the tables in your configured MySQL database, lets you browse their records, and provides a SQL editor for database operations.

## ✨ Features

- **Live database overview** — see the database's table count and patient, doctor, and appointment totals when matching tables are present.
- **Browse records** — choose a discovered table and view up to 500 records at a time.
- **SQL workspace** — run MySQL statements and inspect tabular results or affected-row counts.
- **Transaction controls** — commit or roll back pending transactional changes from the interface.
- **Safer credential handling** — enter the password in a masked prompt or provide it through an environment variable; credentials are not stored in the source.
- **Native interface** — built with Python's Tkinter and ttk widgets.

## 🚀 Getting started

### Requirements

- Python with Tkinter available
- A running MySQL server
- Access to the `hospitalmanagementd` database (the default database name)
- The MySQL Connector/Python package

Install the connector if it is not already installed:

```powershell
python -m pip install mysql-connector-python
```

### Configure the connection

By default, the app connects to MySQL on `localhost` as `root`, using the database `hospitalmanagementd`. It asks for the password when it starts.

To override the connection settings, set these environment variables in PowerShell before launching:

```powershell
$env:HOSPITAL_DB_HOST = "localhost"
$env:HOSPITAL_DB_USER = "root"
$env:HOSPITAL_DB_NAME = "hospitalmanagementd"
$env:HOSPITAL_DB_PASSWORD = "your-mysql-password"
```

If `HOSPITAL_DB_PASSWORD` is set, the app uses it instead of displaying the password prompt. Avoid putting real passwords in source files or committing them to version control.

### Run the app

From the project directory:

```powershell
python app.py
```

## 🧭 Using the dashboard

1. Connect to MySQL using the password prompt or environment variable.
2. Select a table from the **Table** menu to browse its records.
3. Enter a SQL statement in the **MySQL query** panel and select **Run query**.
4. Review result rows in the grid, or check the status bar for the affected-row count.
5. Use **Commit** or **Rollback** to finish pending transactional changes.

Result grids display at most 500 rows. Use a SQL `LIMIT` clause when you need to control which records are returned. Some MySQL DDL statements commit implicitly, so they may not be reversible with **Rollback**.

> **Use care with data-changing statements.** The SQL editor executes statements with the privileges of the configured MySQL user. Back up important data before running destructive operations.

## 📁 Project structure

```text
hospitalmanagement/
├── app.py                 # Tkinter dashboard and SQL editor
├── connector.py           # MySQL connection configuration
├── README.md              # Project guide
└── sql-schema.sql         # Database table definitions and example queries
```

## ⚙️ Database notes

The dashboard reads the database schema at startup, so table names can vary. Patient, doctor, and appointment summary cards appear when the database contains tables named `patient`/`patients`, `doctor`/`doctors`, or `appointment`/`appointments`. The database itself must already exist and be accessible to the configured MySQL user.

`sql-schema.sql` creates the tables and includes example read queries; it does not contain personal or patient seed data.
