import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import pymysql

def resize_image(image_path, size):
    image = Image.open(image_path)
    resized_image = image.resize(size, Image.LANCZOS)
    return ImageTk.PhotoImage(resized_image)

def open_main_window():
    main_window = tk.Toplevel(root)
    background_image = resize_image("atmm.png", (1920, 1080))
    background_label = tk.Label(main_window, image=background_image)
    background_label.image = background_image 
    background_label.place(relwidth=1, relheight=1)
    main_window.title("ATM Main Menu")
    main_window.geometry("1920x1080")
    tk.Button(main_window, text="Withdraw", command=withdraw, font=('arial', 23, 'bold')).place(relx=0.5, rely=0.08, anchor='center')
    tk.Button(main_window, text="Deposit", command=deposit, font=('arial', 23, 'bold')).place(relx=0.5, rely=0.28, anchor='center')
    tk.Button(main_window, text="Balance Enquiry", command=balance_enquiry, font=('arial', 23, 'bold')).place(relx=0.5, rely=0.48, anchor='center')
    tk.Button(main_window, text="PIN Change", command=change_pin, font=('arial', 23, 'bold')).place(relx=0.5, rely=0.68, anchor='center')
    tk.Button(main_window, text="Account Details", command=account_details,font=('arial',23,'bold')).place(relx=0.5,rely=0.88,anchor='center')
    main_window.mainloop()

def account_details():
    details_window = tk.Toplevel(root)
    details_window.title("Account Details")
    details_window.geometry("2000x2000")
    background_image = resize_image("atmm.png", (1920, 1080))
    background_label = tk.Label(details_window, image=background_image)
    background_label.image = background_image  
    background_label.place(relwidth=1, relheight=1)
    tk.Button(details_window,text="View Details",command=lambda: details_process(accno_entry.get()),font=("comic sans", 20, "bold")).place(relx=0.5, rely=0.6, anchor="center")
    
def details_process(Account_Number):
    view_window = tk.Toplevel(root)
    view_window.title("Account Details")
    view_window.geometry("2000x2000")
    background_image = resize_image("atmm.png", (1920, 1080))
    background_label = tk.Label(view_window, image=background_image)
    background_label.image = background_image
    conn = pymysql.connect(host="localhost", user="root", password="", database="atmproject")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM details WHERE Account_Number=%s", (Account_Number,))
    result = cursor.fetchone()
    if result:
       
        account_info = (
           
            f" Name                     : {result[1]}\n"
            f" Date of Birth         : {result[3]}\n"
            f" Account Number  :{result[2]}\n"
            f" Balance                  : {result[4]}\n"
            f" City                         :{result[6]}\n"
            f" Mobile Number     :{result[7]}"
        )
        details_label = tk.Label(view_window, text=account_info, font=("Arial", 20), bg="white", justify="left")
        details_label.pack(padx=150, pady=150)
  
def withdraw():
    withdraw_window = tk.Toplevel(root)
    withdraw_window.title("Withdraw")
    withdraw_window.geometry("2000x2000")
    background_image = resize_image("atmm.png", (1920, 1080))
    background_label = tk.Label(withdraw_window, image=background_image)
    background_label.image = background_image  
    background_label.place(relwidth=1, relheight=1)
    tk.Label(withdraw_window, text="Enter the amount:", font=("arial", 15, "bold"), fg="black", bg="white").place(relx=0.5, rely=0.4, anchor="center")
    withdraw_entry = tk.Entry(withdraw_window, font=("caveat", 15, "bold"), fg="black", bg="white")
    withdraw_entry.place(relx=0.5, rely=0.5, anchor="center")
    withdraw_entry.focus_set()
    tk.Button(withdraw_window, text="Proceed", command=lambda: process_withdrawal(withdraw_entry.get()), font=("comic sans", 20, "bold")).place(relx=0.5, rely=0.6, anchor="center")
    withdraw_window.bind('<Return>', lambda event: process_withdrawal(withdraw_entry.get()))


def process_withdrawal(amount):
    account_number = accno_entry.get()
    if not account_number:
        messagebox.showerror("Input Error", "Please enter your account number.")
        return
    try:
        amount = float(amount)
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        conn = pymysql.connect(host="localhost", user="root", password="", database="atmproject")
        cursor = conn.cursor()
        cursor.execute("SELECT Balance FROM details WHERE Account_Number=%s", (account_number,))
        result = cursor.fetchone()
        if result:
            current_balance = result[0]
            if amount > current_balance:
                messagebox.showerror("Error", "Insufficient funds.")
            else:
                new_balance = current_balance - amount
                cursor.execute("UPDATE details SET Balance=%s WHERE Account_Number=%s", (new_balance, account_number))
                conn.commit()
                messagebox.showinfo("Success", f"Withdrawal successful! New balance: ${new_balance:.2f}")
        else:
            messagebox.showerror("Error", "Account not found.")
        conn.close()
    except ValueError as e:
        messagebox.showerror("Input Error", str(e))
    except pymysql.MySQLError as e:
        messagebox.showerror("Database Error", f"Database error: {e}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def deposit():
    deposit_window = tk.Toplevel(root)
    background_image = resize_image("atmm.png", (1920, 1080))
    background_label = tk.Label(deposit_window, image=background_image)
    background_label.image = background_image
    background_label.place(relwidth=1, relheight=1)
    deposit_window.title("Deposit")
    deposit_window.geometry("1920x1080")
    tk.Label(deposit_window, text="Enter the amount:", height=1, width=15, font=("arial", 15, "bold"), fg="black", bg="white").place(relx=0.5, rely=0.5, anchor="center")
    deposit_entry = tk.Entry(deposit_window, font=("caveat", 15, "bold"), fg="black", bg="white")
    deposit_entry.place(relx=0.5, rely=0.6, anchor="center")
    deposit_entry.focus_set()
    tk.Button(deposit_window, text="Proceed", command=lambda: update_balance(deposit_entry.get()), font=("comic sans", 20, "bold")).place(relx=0.5, rely=0.7, anchor="center")
    deposit_window.bind('<Return>', lambda event: update_balance(deposit_entry.get()))
def update_balance(deposit_amount):
    try:
        deposit_amount = float(deposit_amount)
        if deposit_amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        Account_Number = accno_entry.get()
        conn = pymysql.connect(host="localhost", user="root", password="", database="atmproject")
        cursor = conn.cursor()
        cursor.execute("SELECT Balance FROM details WHERE Account_Number=%s", (Account_Number,))
        result = cursor.fetchone()
        if result:
            current_balance = result[0]
            new_balance = current_balance + deposit_amount
            cursor.execute("UPDATE details SET Balance=%s WHERE Account_Number=%s", (new_balance, Account_Number))
            conn.commit()
            messagebox.showinfo("Success", f"Deposit successful! Current balance: ${new_balance:.2f}")
        else:
            messagebox.showerror("Error", "Account not found.")
        conn.close()
    except ValueError as e:
        messagebox.showerror("Input Error", str(e))
    except Exception as e:
        messagebox.showerror("Error", str(e))

def balance_enquiry():
    Account_number=accno_entry.get()
    enquiry_window = tk.Toplevel(root)
    background_image = resize_image("atmm.png", (1920, 1080))
    background_label = tk.Label(enquiry_window, image=background_image)
    background_label.image = background_image
    background_label.place(relwidth=1, relheight=1)
    enquiry_window.title("Balance Enquiry")
    enquiry_window.geometry("1920x1080")
    tk.Button(enquiry_window, text="Check Balance", command=lambda: show_balance(accno_entry.get()), font=("comic sans", 20, "bold")).place(relx=0.5, rely=0.6, anchor="center")
    
def show_balance(Account_Number):
    try:
        balance_window = tk.Toplevel(root)
        balance_window.title("Account Details")
        balance_window.geometry("2000x2000")
        background_image = resize_image("atmm.png", (1920, 1080))
        background_label = tk.Label(balance_window, image=background_image)
        background_label.image = background_image
        conn = pymysql.connect(host="localhost", user="root", password="", database="atmproject")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM details WHERE Account_Number=%s", (Account_Number))
        result = cursor.fetchone()
        if result:
       
             account_info = (
                f" Account Number: {result[2]}\n"
                f"             Balance: {result[4]}\n"
              )
             details_label = tk.Label(balance_window, text=account_info, font=("Arial", 20), bg="white", justify="left")
             details_label.pack(padx=150, pady=150)
  
        else:
            messagebox.showerror("Error", "Account not found.")
        conn.close()
    except Exception as e:
        messagebox.showerror("Error", str(e))

def change_pin():
    change_pin_window = tk.Toplevel(root)
    change_pin_window.title("Change PIN")
    change_pin_window.geometry("2000x2000")
    background_image = resize_image("atmm.png", (1920, 1080))
    background_label = tk.Label(change_pin_window, image=background_image)
    background_label.image = background_image
    background_label.place(relwidth=1, relheight=1)
    tk.Label(change_pin_window, text="Current PIN:", font=("arial", 15, "bold"), fg="black", bg="white").place(relx=0.5, rely=0.35, anchor="center")
    current_pin_entry = tk.Entry(change_pin_window, font=("caveat", 15, "bold"), show='*', fg="black", bg="white")
    current_pin_entry.place(relx=0.5, rely=0.45, anchor="center")
    current_pin_entry.focus_set()
    current_pin_entry.bind('<Return>', focus_next_widget)
    tk.Label(change_pin_window, text="New PIN:", font=("arial", 15, "bold"), fg="black", bg="white").place(relx=0.5, rely=0.55, anchor="center")
    new_pin_entry = tk.Entry(change_pin_window, font=("caveat", 15, "bold"), show='*', fg="black", bg="white")
    new_pin_entry.place(relx=0.5, rely=0.65, anchor="center")
    new_pin_entry.bind('<Return>', focus_next_widget)
    button=tk.Button(change_pin_window, text="Submit", command=lambda: process_pin_change(current_pin_entry.get(), new_pin_entry.get()), font=("comic sans", 20, "bold")).place(relx=0.5, rely=0.75, anchor="center")
    change_pin_window.bind('<Return>', lambda event: process_pin_change(current_pin_entry.get(), new_pin_entry.get()))

def process_pin_change(current_pin,new_pin,event=None):
    Account_Number = accno_entry.get()
    if not current_pin or not new_pin:
        messagebox.showerror("Input Error", "Please fill in all fields.")
        return
    if not new_pin.isdigit() or len(new_pin) != 4:
        messagebox.showerror("Input Error", "New PIN must be exactly 4 digits.")
        return
    try:
        conn = pymysql.connect(host="localhost", user="root", password="", database="atmproject")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM details WHERE Account_Number=%s AND Pin=%s", (Account_Number,current_pin))
        result = cursor.fetchone()
        if result:
            cursor.execute("UPDATE details SET Pin=%s WHERE Account_Number=%s", (new_pin,Account_Number))
            conn.commit()
            messagebox.showinfo("Success", "PIN changed successfully.")
        else:
            messagebox.showerror("Error", "Invalid account number or current PIN.")
        conn.close()
    except pymysql.MySQLError as e:
        messagebox.showerror("Database Error", f"Database error: {e}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def check_credentials():
    Account_Number = accno_entry.get()
    Pin = pin_entry.get()
    if not Account_Number.isdigit() or len(Account_Number) != 12:
        messagebox.showerror("Error", "Account number must be exactly 12 digits.")
        return
    if not Pin.isdigit() or len(Pin) != 4:
        messagebox.showerror("Error", "PIN must be exactly 4 digits.")
        return
    conn = pymysql.connect(host="localhost", user="root", password="", database="atmproject")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM details WHERE Account_Number=%s AND Pin=%s", (Account_Number, Pin))
    result = cursor.fetchone()
    conn.close()
    if result:
        messagebox.showinfo("Success", "Login Successfully!")
        open_main_window()
    else:
        messagebox.showerror("Error", "Invalid account number or PIN.")

def focus_next_widget(event):
    current_widget = event.widget
    next_widget = current_widget.tk_focusNext()
    if next_widget:
        next_widget.focus_set()
    return 'break' 

root = tk.Tk()
root.geometry("2000x2000")
root.title("Welcome to My App")
background_image = resize_image("atmm.png", (1920, 1080))
background_label = tk.Label(root, image=background_image)
background_label.image = background_image
background_label.place(relwidth=1, relheight=1)
label = tk.Label(root, text="WELCOME TO ATM!!", font=("arial", 24, "bold"), fg="#000000")
label.pack(pady=120)

accno_label = tk.Label(root, text="ACCOUNT NUMBER", font=('arial', 15, 'bold'))
accno_label.place(relx=0.5, rely=0.4, anchor='center')
accno_entry = tk.Entry(root, font=('arial', 20, 'bold'))
accno_entry.focus_set()
accno_entry.place(relx=0.5, rely=0.50, anchor='center')
accno_entry.bind('<Return>', focus_next_widget)

pin_label = tk.Label(root, text="PIN", font=('arial', 15, 'bold'), fg="black")
pin_label.place(relx=0.5, rely=0.6, anchor='center')
pin_entry = tk.Entry(root, font=('arial', 20, 'bold'), show='*')
pin_entry.place(relx=0.5, rely=0.7, anchor='center')
pin_entry.bind('<Return>', focus_next_widget)
button = tk.Button(root, text="PROCEED", font=("arial", 20, 'bold'), command=check_credentials)
button.place(relx=0.5, rely=0.8, anchor='center')
root.bind('<Return>', lambda event: check_credentials())

print("ATM")

root.mainloop()
