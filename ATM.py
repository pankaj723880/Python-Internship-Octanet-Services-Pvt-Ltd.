import tkinter as tk
from tkinter import messagebox
import sqlite3

class ATM:
    def __init__(self):
        self.balance = 1000  # Initial balance
        self.pin = "1234"  # Default PIN
        self.transaction_history = []  # List to store transaction history
        self.create_database()

    def create_database(self):
        """Create or connect to SQLite database and create necessary tables."""
        self.conn = sqlite3.connect("atm.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                transaction_type TEXT,
                amount REAL,
                balance_after REAL
            )
        ''')
        self.conn.commit()

    def validate_pin(self, entered_pin):
        """Validate entered PIN"""
        return entered_pin == self.pin
    
    def check_balance(self):
        """Return current account balance"""
        return f"Current Balance: Rs{self.balance}"
    
    def withdraw_cash(self, amount):
        """Withdraw cash if sufficient balance exists"""
        if amount > self.balance:
            return "Insufficient balance!"
        elif amount <= 0:
            return "Invalid amount! Enter a positive value."
        else:

            self.balance -= amount
            self.transaction_history.append(f"Withdrawn: Rs{amount}")
            self.record_transaction("Withdraw", amount)
            return f"Withdrawal successful! Rs{amount} withdrawn."
    
    def deposit_cash(self, amount):
        """Deposit cash into the account"""
        if amount <= 0:
            return "Invalid amount! Enter a positive value."
        else:
            self.balance += amount
            self.transaction_history.append(f"Deposited: Rs{amount}")
            self.record_transaction("Deposit", amount)
            return f"Deposit successful! Rs{amount} deposited."
    
    def change_pin(self, old_pin, new_pin):
        """Change PIN if the old PIN is correct"""
        if not self.validate_pin(old_pin):
            return "Incorrect old PIN!"
        elif len(new_pin) != 4 or not new_pin.isdigit():
            return "New PIN must be a 4-digit number."
        else:
            self.pin = new_pin
            return "PIN changed successfully!"
    
    def transaction_history_display(self):
        """Return the transaction history"""
        return "\n".join(self.transaction_history) if self.transaction_history else "No transactions yet."

    def record_transaction(self, transaction_type, amount):
        """Record transaction in the database"""
        self.cursor.execute('''
            INSERT INTO transactions (transaction_type, amount, balance_after)
            VALUES (?, ?, ?)
        ''', (transaction_type, amount, self.balance))
        self.conn.commit()

    def get_transaction_history(self):
        """Fetch transaction history from the database"""
        self.cursor.execute('SELECT * FROM transactions')
        return self.cursor.fetchall()


class ATMApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ATM Machine")
        self.root.geometry("400x600")
        self.root.config(bg="#f0f0f0")  # Light background color
        
        self.atm = ATM()  # Create ATM instance
        self.create_widgets()

    def create_widgets(self):
        """Create GUI components"""
        self.welcome_frame = tk.Frame(self.root, bg="#4CAF50", pady=20)
        self.welcome_frame.pack(fill="x")

        self.welcome_label = tk.Label(self.welcome_frame, text="Welcome to ATM", font=("Arial", 20), fg="white", bg="#4CAF50")
        self.welcome_label.pack()

        self.login_frame = tk.Frame(self.root, pady=20, bg="#f0f0f0")
        self.login_frame.pack(pady=10)

        self.pin_label = tk.Label(self.login_frame, text="Enter PIN:", font=("Arial", 12))
        self.pin_label.grid(row=0, column=0, padx=10)
        self.pin_entry = tk.Entry(self.login_frame, show="*", font=("Arial", 12))
        self.pin_entry.grid(row=0, column=1, padx=10)

        self.login_button = tk.Button(self.login_frame, text="Login", command=self.login, font=("Arial", 12), bg="#4CAF50", fg="white", relief="flat")
        self.login_button.grid(row=1, columnspan=2, pady=10)

        self.transaction_buttons_frame = tk.Frame(self.root, pady=10, bg="#f0f0f0")
        self.transaction_buttons_frame.pack(fill="x")

        self.transaction_buttons = []
        self.create_transaction_buttons()

        self.hide_transaction_buttons()

        self.amount_label = tk.Label(self.root, text="Enter Amount:", font=("Arial", 12))
        self.amount_entry = tk.Entry(self.root, font=("Arial", 12))

        self.old_pin_label = tk.Label(self.root, text="Enter Old PIN:", font=("Arial", 12))
        self.old_pin_entry = tk.Entry(self.root, show="*", font=("Arial", 12))
        self.new_pin_label = tk.Label(self.root, text="Enter New PIN:", font=("Arial", 12))
        self.new_pin_entry = tk.Entry(self.root, show="*", font=("Arial", 12))

    def create_transaction_buttons(self):
        """Create buttons for ATM transactions"""
        self.balance_button = tk.Button(self.transaction_buttons_frame, text="Check Balance", command=self.show_balance, font=("Arial", 12), bg="#4CAF50", fg="white", relief="flat")
        self.withdraw_button = tk.Button(self.transaction_buttons_frame, text="Withdraw Cash", command=lambda: self.show_amount_input("withdraw"), font=("Arial", 12), bg="#4CAF50", fg="white", relief="flat")
        self.deposit_button = tk.Button(self.transaction_buttons_frame, text="Deposit Cash", command=lambda: self.show_amount_input("deposit"), font=("Arial", 12), bg="#4CAF50", fg="white", relief="flat")
        self.change_pin_button = tk.Button(self.transaction_buttons_frame, text="Change PIN", command=self.show_pin_input, font=("Arial", 12), bg="#4CAF50", fg="white", relief="flat")
        self.history_button = tk.Button(self.transaction_buttons_frame, text="Transaction History", command=self.view_history, font=("Arial", 12), bg="#4CAF50", fg="white", relief="flat")
        
        self.transaction_buttons = [
            self.balance_button, self.withdraw_button, self.deposit_button, self.change_pin_button, self.history_button
        ]

    def login(self):
        """Validate PIN and show ATM options"""
        entered_pin = self.pin_entry.get()
        if self.atm.validate_pin(entered_pin):
            self.pin_entry.delete(0, tk.END)
            self.pin_label.grid_forget()
            self.pin_entry.grid_forget()
            self.login_button.grid_forget()
            self.show_transaction_buttons()
        else:
            messagebox.showerror("Error", "Invalid PIN")

    def show_transaction_buttons(self):
        """Show transaction buttons after successful login"""
        for btn in self.transaction_buttons:
            btn.pack(pady=10)

    def hide_transaction_buttons(self):
        """Hide transaction buttons before login"""
        for btn in self.transaction_buttons:
            btn.pack_forget()

    def show_amount_input(self, action):
        """Show input field for Withdraw and Deposit"""
        self.amount_label.pack()
        self.amount_entry.pack()
        self.amount_entry.delete(0, tk.END)

        self.confirm_button = tk.Button(self.root, text="Confirm", font=("Arial", 12), command=lambda: self.process_amount(action), bg="#4CAF50", fg="white", relief="flat")
        self.confirm_button.pack(pady=10)

    def process_amount(self, action):
        """Process Withdrawal or Deposit"""
        try:
            amount = float(self.amount_entry.get())
            if action == "withdraw":
                message = self.atm.withdraw_cash(amount)
            else:
                message = self.atm.deposit_cash(amount)
            messagebox.showinfo(action.capitalize(), message)

            # Update the balance display after transaction
            self.show_balance()

            self.amount_label.pack_forget()
            self.amount_entry.pack_forget()
            self.confirm_button.pack_forget()
        except ValueError:
            messagebox.showerror("Error", "Invalid amount!")

    def show_pin_input(self):
        """Show input fields for changing PIN"""
        self.old_pin_label.pack()
        self.old_pin_entry.pack()
        self.new_pin_label.pack()
        self.new_pin_entry.pack()

        self.pin_confirm_button = tk.Button(self.root, text="Confirm", font=("Arial", 12), command=self.process_pin_change, bg="#4CAF50", fg="white", relief="flat")
        self.pin_confirm_button.pack(pady=10)

    def process_pin_change(self):
        """Change PIN"""
        old_pin = self.old_pin_entry.get()
        new_pin = self.new_pin_entry.get()
        message = self.atm.change_pin(old_pin, new_pin)
        messagebox.showinfo("Change PIN", message)

        self.old_pin_label.pack_forget()
        self.old_pin_entry.pack_forget()
        self.new_pin_label.pack_forget()
        self.new_pin_entry.pack_forget()
        self.pin_confirm_button.pack_forget()

    def show_balance(self):
        """Show the current balance"""
        balance_message = self.atm.check_balance()  # Access check_balance via the ATM instance
        messagebox.showinfo("Balance", balance_message)

    def view_history(self):
        """View transaction history"""
        history = self.atm.get_transaction_history()
        history_message = "\n".join([f"{transaction[1]} Rs{transaction[2]} - Balance after: Rs{transaction[3]}" for transaction in history])
        messagebox.showinfo("Transaction History", history_message if history else "No transaction history yet.")


if __name__ == "__main__":
    root = tk.Tk()
    app = ATMApp(root)
    root.mainloop()

