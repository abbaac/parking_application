from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk  # Import from Pillow
import pymysql

login_window = Tk()
login_window.title('Login')
login_window.geometry('925x500+300+200')
login_window.configure(bg='#fff')
login_window.resizable(False, False)

def signup_page():
    login_window.destroy()
    import signup

def login():
    if username_entry.get() == 'Username' or password_entry.get() == 'Password':
        messagebox.showerror('Error', 'Please fill all the fields!')
    else:
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
        query = 'select * from admin_data where username=%s and password=%s'
        mycursor.execute(query, (username_entry.get(), password_entry.get()))
        data = mycursor.fetchall()
        if data:
            messagebox.showinfo('Success', 'Login successful!')
            login_window.destroy()
            import home
        else:
            messagebox.showerror('Error', 'Invalid username or password!')
        con.close()


# Store the image file path in a variable
icon_file_path = 'icons/owl.png'

# Load the icon image
icon_image = Image.open(icon_file_path)
icon_photo = ImageTk.PhotoImage(icon_image)
login_window.iconphoto(True, icon_photo)

# Open the image with PIL and convert it
img = Image.open('background.png')
img = img.resize((928, 500))  # Resize the image to match the window size
photo_img = ImageTk.PhotoImage(img)  # Convert to PhotoImage
Label(login_window, image=photo_img).place(x=-3, y=0)

frame = Frame(login_window, width=350, height=350, bg="white", pady="10")
frame.place(x=480, y=70)

heading = Label(frame, text="Login", font=('arial', 20, 'bold'), bg='white', fg='black')
heading.place(x=175, y=35, anchor='center')

def on_enter(e):
    if username_entry.get() == 'Username':
        username_entry.delete(0, END)

def on_leave(e):
    name = username_entry.get()
    if name == '':
        username_entry.insert(0, 'Username')

username_entry = Entry(frame, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11))
username_entry.place(x=30, y=80)
username_entry.insert(0, 'Username')
username_entry.bind("<FocusIn>", on_enter)
username_entry.bind("<FocusOut>", on_leave)

Frame(frame, width=295, height=2, bg='black').place(x=25, y=107)

def on_enter(e):
    if password_entry.get() == 'Password':
        password_entry.delete(0, END)

def on_leave(e):
    name = password_entry.get()
    if name == '':
        password_entry.insert(0, 'Password')

def hide():
    if password_entry.get() == 'Password':
        return
    if password_entry.cget('show') == '':
        eyeButton.config(image=open_eye)
        password_entry.config(show="*")
    else:
        eyeButton.config(image=close_eye)
        password_entry.config(show="")

password_entry = Entry(frame, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11)) 
password_entry.place(x=30, y=150)
password_entry.insert(0, 'Password')
password_entry.bind("<FocusIn>", on_enter)
password_entry.bind("<FocusOut>", on_leave)

close_eye = PhotoImage(file="icons/close_eye.png").subsample(3)
open_eye = PhotoImage(file="icons/open_eye.png").subsample(3)
eyeButton = Button(frame, image=close_eye, bd=0, bg="white", activebackground="white", cursor="hand2", command=hide)
eyeButton.place(relx=0.85, y=150)

Frame(frame, width=295, height=2, bg='black').place(x=25, y=177)


##########------------------------------------------------------------

Button(frame, text='Login', pady=6, width=39, bg='#F6BB42', fg='black', font=('arial', 9, 'bold'), command=login).place(x=30, y=210)
label = Label(frame, text="Don't have an account?", font=('arial', 10), bg='white', fg='black')
label.place(x=75, y=270)

sign_up = Button(frame, width=6, text='Sign Up', bg='white', fg='#F6BB42', border=0, font=('arial', 9, 'bold underline'), cursor='hand2', command=signup_page)
sign_up.place(x=215, y=271)


login_window.mainloop()
