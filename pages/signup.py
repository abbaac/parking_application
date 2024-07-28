# from tkinter import *
# from tkinter import messagebox
# from PIL import Image, ImageTk, ImageOps  # Import from Pillow
# import pymysql

# def login_page():
#     signup_window.destroy()
#     from . import login

# def clear():
#     username_entry.delete(0, END)
#     parking_lot_name_entry.delete(0, END)
#     password_entry.delete(0, END)
#     password_2_entry.delete(0, END)

# def connect_database():
#     if username_entry.get() == '' or parking_lot_name_entry.get() == '' or password_entry.get() == '' or password_2_entry.get() == '':
#         messagebox.showerror('Error', 'Please fill all the fields!')
#     elif password_entry.get() != password_2_entry.get():
#         messagebox.showerror('Error', 'Passwords do not match!')
#     else:
#         try:
#             con = pymysql.connect(host='localhost', user='root', password='root')
#             mycursor = con.cursor()
#         except:
#             messagebox.showerror('Error', 'Database connection error!')
#             return
#         try:
#             query = 'create database parking_lot'
#             mycursor.execute(query)
#             query = 'use parking_lot'
#             mycursor.execute(query)
#             query = 'create table admin_data(id int auto_increment primary key not null, username varchar(50), parking_lot_name varchar(50), password varchar(50))'
#             mycursor.execute(query)
#         except pymysql.err.ProgrammingError as e:
#             if e.args[0] == 1007:  # Error code for "database exists"
#                 mycursor.execute('use parking_lot')  # Corrected method name here
#             else:
#                 messagebox.showerror('Error', f'Database error: {e}')
#                 return  
#         except Exception as e:
#             messagebox.showerror('Error', f'Unexpected error: {e}')
#             return
        
#         query='select * from admin_data where username=%s'
#         mycursor.execute(query, (username_entry.get()))
#         data = mycursor.fetchall()
#         if data:
#             messagebox.showerror('Error', 'Username already exists!')
#             return
#         else:
#             query = 'insert into admin_data(username, parking_lot_name, password) values(%s, %s, %s)'
#             mycursor.execute(query, (username_entry.get(), parking_lot_name_entry.get(), password_entry.get()))
#             con.commit()
#             con.close()
#             messagebox.showinfo('Success', 'Account created successfully!')
#             clear()
#             signup_window.destroy()
#             import login


# signup_window=Tk()
# signup_window.title('Signup')

# # Store the image file path in a variable
# icon_file_path = 'icons/owl.png'

# # Load the icon image
# icon_image = Image.open(icon_file_path)
# icon_photo = ImageTk.PhotoImage(icon_image)
# signup_window.iconphoto(True, icon_photo)


# background = Image.open('icons/background.png')
# background = background.convert('L').point(lambda x: 0 if x<128 else 255, '1')
# background = ImageTk.PhotoImage(background)

# background_label = Label(signup_window, image=background)
# background_label.place(x=0, y=0)


# signup_frame = Frame(signup_window, width=300, height=450, bg="white", pady="10")
# signup_frame.place(relx=0.65, rely=0.05)

# heading = Label(signup_frame, text="Signup", font=('arial', 20, 'bold'), bg='white', fg='#F6BB42',)
# heading.place(relx=0.5, rely=0.04, anchor='center')

# username = Label(signup_frame, text="Username", font=('arial', 10, 'bold'), bg='white', fg='black')
# username.place(relx=0.05, rely=0.15)
# username_entry = Entry(signup_frame, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11)) 
# username_entry.place(relx=0.05, rely=0.2)
# Frame(signup_frame, width=265, height=2, bg='black').place(relx=0.05, rely=0.25)


# parking_lot_name = Label(signup_frame, text="Parking Lot Name", font=('arial', 10, 'bold'), bg='white', fg='black')
# parking_lot_name.place(relx=0.05, rely=0.35)
# parking_lot_name_entry = Entry(signup_frame, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11)) 
# parking_lot_name_entry.place(relx=0.05, rely=0.4)
# Frame(signup_frame, width=265, height=2, bg='black').place(relx=0.05, rely=0.45)


# password = Label(signup_frame, text="Password", font=('arial', 10, 'bold'), bg='white', fg='black')
# password.place(relx=0.05, rely=0.55)
# password_entry = Entry(signup_frame, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11)) 
# password_entry.place(relx=0.05, rely=0.6)
# Frame(signup_frame, width=265, height=2, bg='black').place(relx=0.05, rely=0.65)


# password_2 = Label(signup_frame, text="Confirm Password", font=('arial', 10, 'bold'), bg='white', fg='black')
# password_2.place(relx=0.05, rely=0.75)
# password_2_entry = Entry(signup_frame, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11)) 
# password_2_entry.place(relx=0.05, rely=0.8)
# Frame(signup_frame, width=265, height=2, bg='black').place(relx=0.05, rely=0.85)


# signup_button = Button(signup_frame, text='Sign Up', pady=6, width=30, bg='#F6BB42', fg='black', font=('arial', 10, 'bold'), command=connect_database)
# signup_button.place(relx=0.5, rely=0.94, anchor=CENTER)

# log_in_label = Label(signup_frame, text="Have an account?", font=('arial', 10), bg='white', fg='black')
# log_in_label.place(relx=0.45, rely=0.1)

# login_button = Button(signup_frame, width=6, text='Log In', bg='white', fg='#F6BB42', border=0, font=('arial', 9, 'bold underline'), cursor='hand2', command=login_page)
# login_button.place(relx=0.89, rely=0.13, anchor='center')



# signup_window.geometry('925x500+300+200')

# signup_window.configure(bg='#fff')

# signup_window.resizable(False, False)

# signup_window.mainloop()


from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk, ImageOps  # Import from Pillow
import pymysql

def show_signup_page():

    def login_page():
        signup_window.destroy()
        from . import login
        login.show_login_page()

    def clear():
        username_entry.delete(0, END)
        parking_lot_name_entry.delete(0, END)
        password_entry.delete(0, END)
        password_2_entry.delete(0, END)

    def connect_database():
        if username_entry.get() == '' or parking_lot_name_entry.get() == '' or password_entry.get() == '' or password_2_entry.get() == '':
            messagebox.showerror('Error', 'Please fill all the fields!')
        elif password_entry.get() != password_2_entry.get():
            messagebox.showerror('Error', 'Passwords do not match!')
        else:
            try:
                con = pymysql.connect(host='localhost', user='root', password='root')
                mycursor = con.cursor()
            except:
                messagebox.showerror('Error', 'Database connection error!')
                return
            try:
                query = 'create database parking_lot'
                mycursor.execute(query)
                query = 'use parking_lot'
                mycursor.execute(query)
                query = 'create table admin_data(id int auto_increment primary key not null, username varchar(50), parking_lot_name varchar(50), password varchar(50))'
                mycursor.execute(query)
            except pymysql.err.ProgrammingError as e:
                if e.args[0] == 1007:  # Error code for "database exists"
                    mycursor.execute('use parking_lot')  # Corrected method name here
                else:
                    messagebox.showerror('Error', f'Database error: {e}')
                    return  
            except Exception as e:
                messagebox.showerror('Error', f'Unexpected error: {e}')
                return
            
            query='select * from admin_data where username=%s'
            mycursor.execute(query, (username_entry.get()))
            data = mycursor.fetchall()
            if data:
                messagebox.showerror('Error', 'Username already exists!')
                return
            else:
                query = 'insert into admin_data(username, parking_lot_name, password) values(%s, %s, %s)'
                mycursor.execute(query, (username_entry.get(), parking_lot_name_entry.get(), password_entry.get()))
                con.commit()
                con.close()
                messagebox.showinfo('Success', 'Account created successfully!')
                clear()
                signup_window.destroy()
                from . import login
                login.show_login_page()

    signup_window = Tk()
    signup_window.title('Signup')

    # Store the image file path in a variable
    icon_file_path = 'icons/owl.png'

    # Load the icon image
    icon_image = Image.open(icon_file_path)
    icon_photo = ImageTk.PhotoImage(icon_image)
    signup_window.iconphoto(True, icon_photo)

    background = Image.open('icons/background.png')
    background = background.convert('L').point(lambda x: 0 if x<128 else 255, '1')
    background = ImageTk.PhotoImage(background)

    background_label = Label(signup_window, image=background)
    background_label.place(x=0, y=0)

    signup_frame = Frame(signup_window, width=300, height=450, bg="white", pady="10")
    signup_frame.place(relx=0.65, rely=0.05)

    heading = Label(signup_frame, text="Signup", font=('arial', 20, 'bold'), bg='white', fg='#F6BB42',)
    heading.place(relx=0.5, rely=0.04, anchor='center')

    username = Label(signup_frame, text="Username", font=('arial', 10, 'bold'), bg='white', fg='black')
    username.place(relx=0.05, rely=0.15)
    username_entry = Entry(signup_frame, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11)) 
    username_entry.place(relx=0.05, rely=0.2)
    Frame(signup_frame, width=265, height=2, bg='black').place(relx=0.05, rely=0.25)

    parking_lot_name = Label(signup_frame, text="Parking Lot Name", font=('arial', 10, 'bold'), bg='white', fg='black')
    parking_lot_name.place(relx=0.05, rely=0.35)
    parking_lot_name_entry = Entry(signup_frame, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11)) 
    parking_lot_name_entry.place(relx=0.05, rely=0.4)
    Frame(signup_frame, width=265, height=2, bg='black').place(relx=0.05, rely=0.45)

    password = Label(signup_frame, text="Password", font=('arial', 10, 'bold'), bg='white', fg='black')
    password.place(relx=0.05, rely=0.55)
    password_entry = Entry(signup_frame, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11)) 
    password_entry.place(relx=0.05, rely=0.6)
    Frame(signup_frame, width=265, height=2, bg='black').place(relx=0.05, rely=0.65)

    password_2 = Label(signup_frame, text="Confirm Password", font=('arial', 10, 'bold'), bg='white', fg='black')
    password_2.place(relx=0.05, rely=0.75)
    password_2_entry = Entry(signup_frame, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11)) 
    password_2_entry.place(relx=0.05, rely=0.8)
    Frame(signup_frame, width=265, height=2, bg='black').place(relx=0.05, rely=0.85)

    signup_button = Button(signup_frame, text='Sign Up', pady=6, width=30, bg='#F6BB42', fg='black', font=('arial', 10, 'bold'), command=connect_database)
    signup_button.place(relx=0.5, rely=0.94, anchor=CENTER)

    log_in_label = Label(signup_frame, text="Have an account?", font=('arial', 10), bg='white', fg='black')
    log_in_label.place(relx=0.45, rely=0.1)

    login_button = Button(signup_frame, width=6, text='Log In', bg='white', fg='#F6BB42', border=0, font=('arial', 9, 'bold underline'), cursor='hand2', command=login_page)
    login_button.place(relx=0.89, rely=0.13, anchor='center')

    signup_window.geometry('925x500+300+200')
    signup_window.configure(bg='#fff')
    signup_window.resizable(False, False)
    signup_window.mainloop()
