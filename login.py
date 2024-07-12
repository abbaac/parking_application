from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk  # Import from Pillow

root = Tk()
root.title('Login')
root.geometry('925x500+300+200')
root.configure(bg='#fff')
root.resizable(False, False)

def login():
    username = user.get()
    password = code.get()

    if username == 'admin' and password == "1234":
        screen=Toplevel(root)
        screen.title('Welcome')
        screen.geometry('300x200+500+300')
        screen.configure(bg='#fff')

        Label(screen, text="Hello Everyone!", font=('arial', 20, 'bold'), bg='white', fg='black').pack(pady=20)

        screen.mainloop()

    elif username != 'admin' or password != '1234':
        messagebox.showerror('Error', 'Invalid Username or Password!')
         

# Open the image with PIL and convert it
img = Image.open('background.png')
img = img.resize((928, 500))  # Resize the image to match the window size
photo_img = ImageTk.PhotoImage(img)  # Convert to PhotoImage
Label(root, image=photo_img).place(x=-3, y=0)

frame = Frame(root, width=350, height=350, bg="white", pady="10")
frame.place(x=480, y=70)

heading = Label(frame, text="Login", font=('arial', 20, 'bold'), bg='white', fg='black')
heading.place(x=175, y=35, anchor='center')

##########------------------------------------------------------------
def on_enter(e):
        if user.get() == 'Username':
            user.delete(0, END)

def on_leave(e):
    name=user.get()
    if name == '':
        user.insert(0, 'Username')

user = Entry(frame, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11))
user.place(x=30, y=80)
user.insert(0, 'Username')
user.bind("<FocusIn>", on_enter)
user.bind("<FocusOut>", on_leave)

Frame(frame, width=295, height=2, bg='black').place(x=25, y=107)
##########

##########
def on_enter(e):
        if code.get() == 'Password':
            code.delete(0, END)

def on_leave(e):
    name=code.get()
    if name == '':
        code.insert(0, 'Password')

def hide():
    if code.get() == 'Password':
        return
    if code.cget('show') == '':
        eyeButton.config(image=open_eye)
        code.config(show="*")
    else:
        eyeButton.config(image=close_eye)
        code.config(show="")

code = Entry(frame, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11)) 
code.place(x=30, y=150)
code.insert(0, 'Password')
code.bind("<FocusIn>", on_enter)
code.bind("<FocusOut>", on_leave)

close_eye = PhotoImage(file="icons/close_eye.png").subsample(3)
open_eye = PhotoImage(file="icons/open_eye.png").subsample(3)
eyeButton = Button(frame, image=close_eye, bd=0, bg="white", activebackground="white", cursor="hand2", command=hide)
eyeButton.place(relx=0.85, y=150)

Frame(frame, width=295, height=2, bg='black').place(x=25, y=177)


##########------------------------------------------------------------

Button(frame, text='Login', pady=6, width=39, bg='#F6BB42', fg='black', font=('arial', 9, 'bold'), command=login).place(x=30, y=210)
label=Label(frame, text="Don't have an account?", font=('arial', 10), bg='white', fg='black')
label.place(x=75, y=270)

sign_up = Button(frame, width=6 ,text='Sign Up', bg='white', fg='#F6BB42', border=0, font=('arial', 9, 'bold'))
sign_up.place(x=215, y=271)


root.mainloop()