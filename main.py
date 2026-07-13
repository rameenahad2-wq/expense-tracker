import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from database import (
    initialize_database,
    add_expense,
    get_expenses,
    delete_expense,
    get_total_expenses,
)


class ExpenseTrackerApp:
    CATEGORIES = ["Food", "Transport", "Bills", "Shopping", "Entertainment", "Other"]

    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("950x620")
        self.root.minsize(800, 520)

        initialize_database()
        self.setup_style()
        self.create_widgets()
        self.refresh_expenses()

    def setup_style(self):
        style = ttk.Style()
        style.theme_use("clam")

        self.bg_color = "#eff6ff"
        self.card_bg = "#ffffff"
        self.input_bg = "#f8fafc"

        self.root.configure(bg=self.bg_color)

        style.configure("TLabel", background=self.bg_color, foreground="#0f172a")
        style.configure("Title.TLabel", font=("Segoe UI", 20, "bold"), background=self.bg_color, foreground="#0f172a")
        style.configure("Total.TLabel", font=("Segoe UI", 14, "bold"), background=self.bg_color, foreground="#0f172a")

        style.configure("Card.TLabelframe", background=self.card_bg, bordercolor="#cbd5e1", relief="flat", padding=12)
        style.configure("Card.TLabelframe.Label", background=self.card_bg, foreground="#0f172a", font=("Segoe UI", 10, "bold"))
        style.configure("Card.TFrame", background=self.card_bg)

        style.configure("TEntry", fieldbackground=self.input_bg, background=self.input_bg, foreground="#0f172a")
        style.configure("TCombobox", fieldbackground=self.input_bg, background=self.input_bg, foreground="#0f172a")

        style.configure("Treeview", rowheight=28, font=("Segoe UI", 10), background="#ffffff", fieldbackground="#f8fafc", foreground="#0f172a", bordercolor="#cbd5e1")
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#2563eb", foreground="#ffffff")
        style.map("Treeview.Heading", background=[("active", "#1d4ed8")])

        style.configure("Add.TButton", font=("Segoe UI", 10, "bold"), background="#2563eb", foreground="#ffffff")
        style.map("Add.TButton", background=[("active", "#1d4ed8")], foreground=[("active", "#ffffff")])

        style.configure("Delete.TButton", font=("Segoe UI", 10, "bold"), background="#ef4444", foreground="#ffffff")
        style.map("Delete.TButton", background=[("active", "#dc2626")], foreground=[("active", "#ffffff")])

    def create_widgets(self):
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(2, weight=1)

        title_label = ttk.Label(
            self.root,
            text="Expense Tracker",
            style="Title.TLabel"
        )
        title_label.grid(row=0, column=0, padx=20, pady=(18, 10), sticky="w")

        self.create_form_section()
        self.create_table_section()
        self.create_bottom_section()

    def create_form_section(self):
        form_frame = ttk.LabelFrame(self.root, text="Add New Expense", padding=15, style="Card.TLabelframe")
        form_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        for column in range(4):
            form_frame.columnconfigure(column, weight=1)

        ttk.Label(form_frame, text="Expense Title").grid(
            row=0, column=0, padx=5, pady=(0, 5), sticky="w"
        )
        ttk.Label(form_frame, text="Category").grid(
            row=0, column=1, padx=5, pady=(0, 5), sticky="w"
        )
        ttk.Label(form_frame, text="Amount ($)").grid(
            row=0, column=2, padx=5, pady=(0, 5), sticky="w"
        )
        ttk.Label(form_frame, text="Date (YYYY-MM-DD)").grid(
            row=0, column=3, padx=5, pady=(0, 5), sticky="w"
        )

        self.title_entry = ttk.Entry(form_frame)
        self.title_entry.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        self.category_combo = ttk.Combobox(
            form_frame,
            values=self.CATEGORIES,
            state="readonly"
        )
        self.category_combo.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.category_combo.set("Food")

        self.amount_entry = ttk.Entry(form_frame)
        self.amount_entry.grid(row=1, column=2, padx=5, pady=5, sticky="ew")

        self.date_entry = ttk.Entry(form_frame)
        self.date_entry.grid(row=1, column=3, padx=5, pady=5, sticky="ew")
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

        add_button = ttk.Button(
            form_frame,
            text="Add Expense",
            style="Add.TButton",
            command=self.handle_add_expense
        )
        add_button.grid(row=2, column=0, columnspan=4, padx=5, pady=(12, 0))

    def create_table_section(self):
        table_frame = ttk.LabelFrame(self.root, text="Expenses", padding=12, style="Card.TLabelframe")
        table_frame.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")

        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(1, weight=1)

        filter_frame = ttk.Frame(table_frame)
        filter_frame.grid(row=0, column=0, pady=(0, 10), sticky="ew")

        ttk.Label(filter_frame, text="Search:").pack(side="left", padx=(0, 5))

        self.search_entry = ttk.Entry(filter_frame, width=30)
        self.search_entry.pack(side="left", padx=(0, 12))
        self.search_entry.bind("<Return>", lambda event: self.refresh_expenses())

        ttk.Label(filter_frame, text="Category:").pack(side="left", padx=(0, 5))

        self.filter_category_combo = ttk.Combobox(
            filter_frame,
            values=["All"] + self.CATEGORIES,
            state="readonly",
            width=16
        )
        self.filter_category_combo.pack(side="left", padx=(0, 12))
        self.filter_category_combo.set("All")

        ttk.Button(
            filter_frame,
            text="Search",
            command=self.refresh_expenses
        ).pack(side="left", padx=4)

        ttk.Button(
            filter_frame,
            text="Reset",
            command=self.reset_filters
        ).pack(side="left", padx=4)

        columns = ("ID", "Title", "Category", "Amount", "Date")

        self.expense_tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            selectmode="browse"
        )

        self.expense_tree.heading("ID", text="ID")
        self.expense_tree.heading("Title", text="Expense Title")
        self.expense_tree.heading("Category", text="Category")
        self.expense_tree.heading("Amount", text="Amount")
        self.expense_tree.heading("Date", text="Date")

        self.expense_tree.column("ID", width=60, anchor="center")
        self.expense_tree.column("Title", width=280)
        self.expense_tree.column("Category", width=150, anchor="center")
        self.expense_tree.column("Amount", width=130, anchor="e")
        self.expense_tree.column("Date", width=150, anchor="center")

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.expense_tree.yview
        )
        self.expense_tree.configure(yscrollcommand=scrollbar.set)

        self.expense_tree.grid(row=1, column=0, sticky="nsew")
        scrollbar.grid(row=1, column=1, sticky="ns")

    def create_bottom_section(self):
        bottom_frame = ttk.Frame(self.root, style="Card.TFrame")
        bottom_frame.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="ew")

        bottom_frame.columnconfigure(0, weight=1)

        self.total_label = ttk.Label(
            bottom_frame,
            text="Total Expenses: $0.00",
            style="Total.TLabel"
        )
        self.total_label.grid(row=0, column=0, sticky="w")

        delete_button = ttk.Button(
            bottom_frame,
            text="Delete Selected",
            style="Delete.TButton",
            command=self.handle_delete_expense
        )
        delete_button.grid(row=0, column=1, sticky="e")

    def handle_add_expense(self):
        title = self.title_entry.get().strip()
        category = self.category_combo.get().strip()
        amount_text = self.amount_entry.get().strip()
        expense_date = self.date_entry.get().strip()

        if not title or not category or not amount_text or not expense_date:
            messagebox.showerror("Missing Information", "Please fill in every field.")
            return

        try:
            amount = float(amount_text)

            if amount <= 0:
                messagebox.showerror(
                    "Invalid Amount",
                    "Amount must be greater than zero."
                )
                return

            datetime.strptime(expense_date, "%Y-%m-%d")

        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Enter a valid amount and date in YYYY-MM-DD format."
            )
            return

        try:
            add_expense(title, category, amount, expense_date)
            self.clear_form()
            self.refresh_expenses()
            messagebox.showinfo("Success", "Expense added successfully.")

        except Exception as error:
            messagebox.showerror("Database Error", f"Could not add expense.\n{error}")

    def handle_delete_expense(self):
        selected_item = self.expense_tree.selection()

        if not selected_item:
            messagebox.showwarning(
                "No Selection",
                "Please select an expense to delete."
            )
            return

        values = self.expense_tree.item(selected_item[0], "values")
        expense_id = values[0]
        expense_title = values[1]

        confirmed = messagebox.askyesno(
            "Confirm Delete",
            f"Do you want to delete '{expense_title}'?"
        )

        if not confirmed:
            return

        try:
            delete_expense(expense_id)
            self.refresh_expenses()
            messagebox.showinfo("Deleted", "Expense deleted successfully.")

        except Exception as error:
            messagebox.showerror(
                "Database Error",
                f"Could not delete expense.\n{error}"
            )

    def refresh_expenses(self):
        search_text = self.search_entry.get().strip()
        category = self.filter_category_combo.get()

        for item in self.expense_tree.get_children():
            self.expense_tree.delete(item)

        expenses = get_expenses(search_text, category)

        for expense in expenses:
            expense_id, title, expense_category, amount, expense_date = expense

            self.expense_tree.insert(
                "",
                "end",
                values=(
                    expense_id,
                    title,
                    expense_category,
                    f"${amount:.2f}",
                    expense_date
                )
            )

        total = get_total_expenses(search_text, category)
        self.total_label.config(text=f"Total Expenses: ${total:.2f}")

    def reset_filters(self):
        self.search_entry.delete(0, tk.END)
        self.filter_category_combo.set("All")
        self.refresh_expenses()

    def clear_form(self):
        self.title_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)

        self.category_combo.set("Food")

        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

        self.title_entry.focus()


if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()
        