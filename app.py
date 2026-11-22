import os
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

import mysql.connector

from connector import get_connection


DATABASE_NAME = os.environ.get("HOSPITAL_DB_NAME", "hospitalmanagementd")
MAX_DISPLAY_ROWS = 500


class HospitalDashboard:
    def __init__(self, root, connection):
        self.root = root
        self.connection = connection
        self.tables = []

        root.title("Hospital Management System")
        root.geometry("1180x760")
        root.minsize(850, 580)

        self._build_interface()
        self.load_tables()

    def _build_interface(self):
        style = ttk.Style()
        if "clam" in style.theme_names():
            style.theme_use("clam")
        style.configure("Title.TLabel", font=("Segoe UI", 19, "bold"))
        style.configure("Metric.TLabel", font=("Segoe UI", 18, "bold"))
        style.configure("MetricName.TLabel", font=("Segoe UI", 10))
        style.configure("Treeview", rowheight=25)

        header = ttk.Frame(self.root, padding=(18, 14))
        header.pack(fill="x")
        ttk.Label(header, text="Hospital Management System",
                  style="Title.TLabel").pack(side="left")
        ttk.Label(header, text="Database: " + DATABASE_NAME).pack(side="right")

        self.metrics = ttk.Frame(self.root, padding=(18, 0, 18, 12))
        self.metrics.pack(fill="x")

        body = ttk.Panedwindow(self.root, orient="vertical")
        body.pack(fill="both", expand=True, padx=18, pady=(0, 16))

        records = ttk.Frame(body, padding=8)
        body.add(records, weight=3)
        table_bar = ttk.Frame(records)
        table_bar.pack(fill="x", pady=(0, 8))
        ttk.Label(table_bar, text="Table:").pack(side="left")
        self.table_choice = tk.StringVar()
        self.table_picker = ttk.Combobox(
            table_bar, textvariable=self.table_choice, state="readonly", width=32
        )
        self.table_picker.pack(side="left", padx=(8, 8))
        self.table_picker.bind("<<ComboboxSelected>>", self.show_selected_table)
        ttk.Button(table_bar, text="Refresh", command=self.refresh).pack(side="left")
        self.status = ttk.Label(table_bar, text="")
        self.status.pack(side="right")

        grid_frame = ttk.Frame(records)
        grid_frame.pack(fill="both", expand=True)
        self.data_grid = ttk.Treeview(grid_frame, show="headings")
        vertical = ttk.Scrollbar(
            grid_frame, orient="vertical", command=self.data_grid.yview
        )
        horizontal = ttk.Scrollbar(
            grid_frame, orient="horizontal", command=self.data_grid.xview
        )
        self.data_grid.configure(
            yscrollcommand=vertical.set, xscrollcommand=horizontal.set
        )
        self.data_grid.grid(row=0, column=0, sticky="nsew")
        vertical.grid(row=0, column=1, sticky="ns")
        horizontal.grid(row=1, column=0, sticky="ew")
        grid_frame.rowconfigure(0, weight=1)
        grid_frame.columnconfigure(0, weight=1)

        query_panel = ttk.LabelFrame(body, text="MySQL query", padding=10)
        body.add(query_panel, weight=2)
        ttk.Label(
            query_panel,
            text="Run SQL statements. Result sets are limited to "
            + str(MAX_DISPLAY_ROWS)
            + " displayed rows. Transactional changes remain pending until committed.",
        ).pack(anchor="w", pady=(0, 6))
        self.query_input = tk.Text(query_panel, height=5, wrap="none")
        self.query_input.pack(fill="both", expand=True)
        query_controls = ttk.Frame(query_panel)
        query_controls.pack(fill="x", pady=(8, 0))
        ttk.Button(query_controls, text="Run query", command=self.run_query).pack(
            side="left"
        )
        ttk.Button(query_controls, text="Commit", command=self.commit).pack(
            side="left", padx=(8, 0)
        )
        ttk.Button(query_controls, text="Rollback", command=self.rollback).pack(
            side="left", padx=(8, 0)
        )
        ttk.Button(query_controls, text="Clear", command=self.clear_query).pack(
            side="left", padx=(8, 0)
        )
        ttk.Label(
            query_controls,
            text="MySQL DDL may commit implicitly.",
        ).pack(side="right")

    def load_tables(self):
        cursor = self.connection.cursor()
        try:
            cursor.execute("SHOW TABLES")
            self.tables = [row[0] for row in cursor.fetchall()]
        finally:
            cursor.close()

        self.table_picker["values"] = self.tables
        self._show_metrics()
        if self.tables:
            self.table_picker.current(0)
            self.show_selected_table()
        else:
            self.status.configure(text="No tables found")
            self._display_rows([], [])

    def _show_metrics(self):
        for child in self.metrics.winfo_children():
            child.destroy()

        candidates = [
            ("Patients", ("patient", "patients")),
            ("Doctors", ("doctor", "doctors")),
            ("Appointments", ("appointment", "appointments")),
        ]
        table_lookup = {name.lower(): name for name in self.tables}
        counts = [("Database tables", len(self.tables))]

        for label, names in candidates:
            table_name = next((table_lookup[name] for name in names
                               if name in table_lookup), None)
            if table_name is not None:
                counts.append((label, self._count_rows(table_name)))

        for label, value in counts:
            card = ttk.LabelFrame(self.metrics, padding=(14, 8))
            card.pack(side="left", fill="x", expand=True, padx=(0, 10))
            ttk.Label(card, text=str(value), style="Metric.TLabel").pack(anchor="w")
            ttk.Label(card, text=label, style="MetricName.TLabel").pack(anchor="w")

    def _count_rows(self, table_name):
        quoted_name = "`" + table_name.replace("`", "``") + "`"
        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM " + quoted_name)
            return cursor.fetchone()[0]
        finally:
            cursor.close()

    def show_selected_table(self, _event=None):
        table_name = self.table_choice.get()
        if table_name not in self.tables:
            return
        quoted_name = "`" + table_name.replace("`", "``") + "`"
        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT * FROM " + quoted_name + " LIMIT %s",
                           (MAX_DISPLAY_ROWS,))
            rows = cursor.fetchall()
            columns = [description[0] for description in cursor.description]
        except mysql.connector.Error as error:
            self.show_database_error(error)
            return
        finally:
            cursor.close()
        self._display_rows(columns, rows)
        self.status.configure(
            text="Showing up to "
            + str(MAX_DISPLAY_ROWS)
            + " rows from "
            + table_name
        )

    def run_query(self):
        statement = self.query_input.get("1.0", "end-1c").strip()
        if not statement:
            messagebox.showwarning("SQL query", "Enter a SQL statement first.",
                                   parent=self.root)
            return

        cursor = self.connection.cursor()
        try:
            cursor.execute(statement)
            if cursor.description is not None:
                columns = [description[0] for description in cursor.description]
                rows = cursor.fetchmany(MAX_DISPLAY_ROWS)
                self._display_rows(columns, rows)
                self.status.configure(
                    text="Query returned "
                    + str(len(rows))
                    + " displayed row(s)"
                )
            else:
                affected_rows = cursor.rowcount
                self._display_rows([], [])
                if affected_rows >= 0:
                    self.status.configure(
                        text="Statement executed. Affected rows: "
                        + str(affected_rows)
                        + ". Commit or roll back transactional changes."
                    )
                else:
                    self.status.configure(
                        text="Statement executed. Commit or roll back "
                        "transactional changes if needed."
                    )
        except mysql.connector.Error as error:
            self.show_database_error(error)
        finally:
            cursor.close()

    def commit(self):
        try:
            self.connection.commit()
            self.refresh()
            self.status.configure(text="Transaction committed.")
        except mysql.connector.Error as error:
            self.show_database_error(error)

    def rollback(self):
        try:
            self.connection.rollback()
            self.refresh()
            self.status.configure(text="Transaction rolled back.")
        except mysql.connector.Error as error:
            self.show_database_error(error)

    def _display_rows(self, columns, rows):
        self.data_grid.delete(*self.data_grid.get_children())
        self.data_grid["columns"] = columns
        for column in columns:
            self.data_grid.heading(column, text=column)
            self.data_grid.column(column, width=150, minwidth=80, stretch=True)
        for row in rows:
            self.data_grid.insert(
                "", "end", values=tuple(self._format_value(value) for value in row)
            )

    @staticmethod
    def _format_value(value):
        if value is None:
            return "NULL"
        if isinstance(value, bytes):
            return value.hex()
        return str(value)

    def clear_query(self):
        self.query_input.delete("1.0", "end")

    def refresh(self):
        try:
            self.load_tables()
        except mysql.connector.Error as error:
            self.show_database_error(error)

    def show_database_error(self, error):
        messagebox.showerror("Database error", str(error), parent=self.root)


def main():
    root = tk.Tk()
    root.withdraw()
    password = os.environ.get("HOSPITAL_DB_PASSWORD")
    if not password:
        password = simpledialog.askstring(
            "MySQL password",
            "Enter the MySQL password for the configured database user:",
            show="*",
            parent=root,
        )
    if password is None:
        root.destroy()
        return

    connection = None
    try:
        connection = get_connection(password=password)
        root.deiconify()
        HospitalDashboard(root, connection)
    except (mysql.connector.Error, ValueError) as error:
        messagebox.showerror("Could not connect to MySQL", str(error), parent=root)
        if connection is not None:
            connection.close()
        root.destroy()
        return

    def close_app():
        connection.close()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", close_app)
    root.mainloop()


if __name__ == "__main__":
    main()
