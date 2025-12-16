# Part 1 import libraries
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import ttk
import json
from tkinter import filedialog
import sys
import os

# part 2 fix imports
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_dir)

# PART 3 import classes
from classes_9_gui import Budget
import functions_gui as functions

# PART 4 global instances
grocery = Budget("Grocery")
car = Budget("Car")

# Save Function
def handle_save_expenses():
    data_to_save = {
        "Grocery": grocery.get_expenses_list(),
        "Car": car.get_expenses_list()
    }
    file_path = filedialog.asksaveasfilename(
        defaultextension=".json",
        filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")]
    )
    if file_path:
        try:
            with open(file_path, 'w') as f:
                json.dump(data_to_save, f, indent=4)
            messagebox.showinfo("Success", "Expenses saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save file: {e}")

# Load Function
def handle_load_expenses():
    file_path = filedialog.askopenfilename(
        filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")]
    )
    if file_path:
        try:
            with open(file_path, 'r') as f:
                loaded_data = json.load(f)

            # Reset Data
            grocery.expenses = []
            grocery.categories = []
            car.expenses = []
            car.categories = []
            grocery_list.delete(0, tk.END)
            car_list.delete(0, tk.END)

            # Load Grocery
            if "Grocery" in loaded_data:
                g_data = loaded_data["Grocery"]
                if g_data:
                    grocery.add_expenses(g_data)
                    for item, cost in g_data:
                        grocery_list.insert(tk.END, f"{item}: ${float(cost):.2f}")

            # Load Car
            if "Car" in loaded_data:
                c_data = loaded_data["Car"]
                if c_data:
                    car.add_expenses(c_data)
                    for item, cost in c_data:
                        car_list.insert(tk.END, f"{item}: ${float(cost):.2f}")

            messagebox.showinfo("Success", "Expenses loaded successfully!")
            if income_entry.get():
                handle_calculate_balance()

        except Exception as e:
            messagebox.showerror("Error", f"Could not load file: {e}")

# Part 5: Add Expense
def handle_add_expense():
    try:
        selected_type = category_var.get()
        item_name = item_entry.get()
        cost_str = cost_entry.get()

        if not item_name or not cost_str:
             messagebox.showwarning("Input Error", "Please fill in all fields.")
             return
        cost = float(cost_str)
        if cost <= 0:
            messagebox.showwarning("Input Error", "Cost must be greater than 0.")
            return
           
        expense_data = [(item_name, cost)]

        if selected_type == "Grocery":
            grocery.add_expenses(expense_data)
            grocery_list.insert(tk.END, f"{item_name}: ${cost:.2f}")
        else:
            car.add_expenses(expense_data)
            car_list.insert(tk.END, f"{item_name}: ${cost:.2f}")
           
        item_entry.delete(0, tk.END)
        cost_entry.delete(0, tk.END)

    except ValueError:
        messagebox.showerror("Input Error", "Cost must be a valid number (e.g., 4.99).")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")

# part 6: Calculate Function
def handle_calculate_balance():
    try:
        income_str = income_entry.get()
        if not income_str:
            messagebox.showwarning("Input Error", "Please enter your income.")
            return

        monthly_income = float(income_str)
        exp_grocery = grocery.get_expenses()
        exp_car = car.get_expenses()
        total_expenses = exp_grocery + exp_car

        bal = functions.calc_balance(monthly_income, total_expenses)
        status_message = functions.financial_status(bal)

        # DEBUG: Print to console to prove it's working
        print(f"Calculated Balance: {bal}")
        print(f"Status Message: {status_message}")

        results_text = (
            f"Monthly Income: ${monthly_income:,.2f}\n"
            f"Total Grocery Expenses: ${exp_grocery:,.2f}\n"
            f"Total Car Expenses: ${exp_car:,.2f}\n"
            f"--- TOTAL EXPENSES ---: ${total_expenses:,.2f}\n"
            f"--- REMAINING BALANCE ---: ${bal:,.2f}"
        )
       
        results_label.config(text=results_text)
        status_label.config(text=status_message)
       
        if bal < 0:
            status_label.config(fg="#E74C3C") # Red
        elif bal == 0:
            status_label.config(fg="#3498DB") # Blue
        else:
            status_label.config(fg="#2ECC71") # Green

    except ValueError:
        messagebox.showerror("Input Error", "Income must be a valid number.")

# PART 7 Setup Window
root = tk.Tk()
root.withdraw()
user_name = simpledialog.askstring("Welcome", "Please enter your name to begin:")
if not user_name: user_name = "Buddy"
root.deiconify()

root.title(f"{user_name}'s BudgetBuddy")
# CHANGED: Made height shorter (680) so it fits on all screens
root.geometry("500x680")
root.config(bg="#F4F6F7")

welcome_label = tk.Label(root, text=f"Welcome, {user_name}!", font=("Arial", 16, "bold"), bg="#F4F6F7", fg="#2C3E50")
welcome_label.pack(pady=5)

# File Buttons (Top)
file_frame = tk.Frame(root, pady=5, bg="#F4F6F7")
file_frame.pack(fill="x")
save_btn = tk.Button(file_frame, text="Save Expenses", command=handle_save_expenses, bg="#95A5A6", fg="white")
save_btn.pack(side=tk.LEFT, padx=20, expand=True)
load_btn = tk.Button(file_frame, text="Load Expenses", command=handle_load_expenses, bg="#95A5A6", fg="white")
load_btn.pack(side=tk.LEFT, padx=20, expand=True)

# Part 8: Income
income_frame = tk.Frame(root, pady=5, bg="#F4F6F7")
income_frame.pack(fill="x")
tk.Label(income_frame, text="Enter Monthly Income:", font=("Arial", 12), bg="#F4F6F7").pack(side=tk.LEFT, padx=10)
income_entry = tk.Entry(income_frame, width=20, font=("Arial", 12))
income_entry.pack(side=tk.LEFT, padx=10)

# part 9: Add Expenses
expense_frame = tk.Frame(root, pady=5, relief="groove", borderwidth=2, bg="#EBF5FB")
expense_frame.pack(fill="x", padx=10, pady=5)
tk.Label(expense_frame, text="Add an Expense", font=("Arial", 14, "bold"), bg="#EBF5FB").grid(row=0, column=0, columnspan=2, pady=5)

tk.Label(expense_frame, text="Category:", bg="#EBF5FB").grid(row=1, column=0, sticky="e", padx=5)
category_var = tk.StringVar(value="Grocery")
category_menu = ttk.OptionMenu(expense_frame, category_var, "Grocery", "Grocery", "Car")
category_menu.grid(row=1, column=1, sticky="w", padx=5)

tk.Label(expense_frame, text="Item Name:", bg="#EBF5FB").grid(row=2, column=0, sticky="e", padx=5)
item_entry = tk.Entry(expense_frame)
item_entry.grid(row=2, column=1, sticky="w", padx=5)

tk.Label(expense_frame, text="Cost:", bg="#EBF5FB").grid(row=3, column=0, sticky="e", padx=5)
cost_entry = tk.Entry(expense_frame)
cost_entry.grid(row=3, column=1, sticky="w", padx=5)

add_button = tk.Button(expense_frame, text="Add Expense", command=handle_add_expense, bg="#5DADE2", fg="white", font=("Arial", 10, "bold"))
add_button.grid(row=4, column=0, columnspan=2, pady=10)

# Part 10: Lists
lists_frame = tk.Frame(root, bg="#F4F6F7")
lists_frame.pack(fill="x", padx=10, pady=5)
tk.Label(lists_frame, text="Grocery Expenses", font=("Arial", 12, "bold"), bg="#F4F6F7").pack()
grocery_list = tk.Listbox(lists_frame, height=4, width=40, relief="groove", borderwidth=2)
grocery_list.pack(pady=2)
tk.Label(lists_frame, text="Car Expenses", font=("Arial", 12, "bold"), bg="#F4F6F7").pack()
car_list = tk.Listbox(lists_frame, height=4, width=40, relief="groove", borderwidth=2)
car_list.pack(pady=2)

# Part 11: Calculate Button
calculate_frame = tk.Frame(root, pady=5, bg="#F4F6F7")
calculate_frame.pack(fill="x")
calculate_button = tk.Button(calculate_frame, text="Calculate Balance", font=("Arial", 14, "bold"), bg="#2ECC71", fg="white", command=handle_calculate_balance)
calculate_button.pack(pady=5)

# part 12: Results
results_frame = tk.Frame(root, relief="sunken", borderwidth=2, bg="white")
results_frame.pack(fill="x", padx=10, pady=10)

# CHANGED: I MOVED THE STATUS MESSAGE TO THE TOP OF THE BOX
status_label = tk.Label(results_frame, text="Status will appear here", font=("Arial", 14, "bold"), justify=tk.CENTER, bg="white")
status_label.pack(padx=10, pady=5)

results_label = tk.Label(results_frame, text="Details...", font=("Arial", 12), justify=tk.LEFT, height=5, bg="white")
results_label.pack(padx=10, pady=5, fill="x")

# Part 13: Start
root.mainloop()