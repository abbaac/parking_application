import tkinter as tk
import pymysql
from tkinter import messagebox
from . import globals

def get_current_parking_lot_name():
    try:
        con = pymysql.connect(host='localhost', user='root', password='root')
        mycursor = con.cursor()
    except:
        messagebox.showerror('Error', 'Database connection error!')
        return
    try:
        query = 'use parking_lot'
        mycursor.execute(query)
    except pymysql.err.ProgrammingError as e:
        if e.args[0] == 1049:
            messagebox.showerror('Error', 'Database does not exist!')
            return
        else:
            messagebox.showerror('Error', f'Database error: {e}')
            return
    except Exception as e:
        messagebox.showerror('Error', f'Unexpected error: {e}')
        return
    query = 'select parking_lot_name from admin_data where username=%s'
    mycursor.execute(query, (globals.username,))
    data = mycursor.fetchall()
    if data:
        return data[0][0]
    con.close()

def save_parking_lot_name(parking_lot_name):
    try:
        con = pymysql.connect(host='localhost', user='root', password='root')
        mycursor = con.cursor()
    except:
        messagebox.showerror('Error', 'Database connection error!')
        return
    try:
        query = 'use parking_lot'
        mycursor.execute(query)
    except pymysql.err.ProgrammingError as e:
        if e.args[0] == 1049:
            messagebox.showerror('Error', 'Database does not exist!')
            return
        else:
            messagebox.showerror('Error', f'Database error: {e}')
            return
    except Exception as e:
        messagebox.showerror('Error', f'Unexpected error: {e}')
        return
    query = 'update admin_data set parking_lot_name=%s'
    mycursor.execute(query, (parking_lot_name,))
    con.commit()
    con.close()



def settings(main_frame, root):
    settings_frame = tk.Frame(main_frame, bg='#DEDDE3')
    
    # Settings Label
    settings_lb = tk.Label(settings_frame, text="Settings", font=('arial', 24, 'bold'), bg='white', fg='black')
    settings_lb.pack(pady=30)
    
    # Parking Lot Name
    parking_lot_name_lb = tk.Label(settings_frame, text="Parking Lot Name:", font=('arial', 16), bg='white')
    parking_lot_name_lb.pack(anchor='w', padx=70, pady=10)
    parking_lot_name_entry = tk.Entry(settings_frame, font=('arial', 16), width=30)
    parking_lot_name_entry.pack(anchor='w', padx=70, pady=10)
    parking_lot_name_entry.insert(0, get_current_parking_lot_name())
    
    # Save Parking Lot Name Button
    save_parking_lot_name_btn = tk.Button(settings_frame, text="Save", font=('arial', 16), command=lambda: save_parking_lot_name(parking_lot_name_entry.get()))
    save_parking_lot_name_btn.pack(anchor='w', padx=70, pady=((10,70)))
    
    # Current Password
    edit_password_lb = tk.Label(settings_frame, text="Current Password:", font=('arial', 16), bg='white')
    edit_password_lb.pack(anchor='w', padx=70, pady=((5,10)))
    edit_password_entry = tk.Entry(settings_frame, font=('arial', 16), show='*', width=30)
    edit_password_entry.pack(anchor='w', padx=70, pady=10)
    
    # New Password
    confirm_password_lb = tk.Label(settings_frame, text="New Password:", font=('arial', 16), bg='white')
    confirm_password_lb.pack(anchor='w', padx=70, pady=10)
    confirm_password_entry = tk.Entry(settings_frame, font=('arial', 16), show='*', width=30)
    confirm_password_entry.pack(anchor='w', padx=70, pady=10)

    # Confirm Password
    confirm_password_lb = tk.Label(settings_frame, text="Confirm Password:", font=('arial', 16), bg='white')
    confirm_password_lb.pack(anchor='w', padx=70, pady=10)
    confirm_password_entry = tk.Entry(settings_frame, font=('arial', 16), show='*', width=30)
    confirm_password_entry.pack(anchor='w', padx=70, pady=10)
    
    # Save Password Button
    save_password_btn = tk.Button(settings_frame, text="Save", font=('arial', 16))
    save_password_btn.pack(anchor='w', padx=70, pady=10)
    
    settings_frame.pack(fill=tk.BOTH, expand=True)

# Example usage:
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Settings Example")
    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True)
    settings(main_frame, root)
    root.mainloop()
