from tkinter import *
from tkinter import messagebox
from tkinter import filedialog

root = Tk()
# root.attributes('-fullscreen', True)
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth()-300, root.winfo_screenheight() - 100))
root.title('Owcular Parking Lot Management System')

menu_bar_colour = "#383838"

def switch(button, page):
    for btn in [dashboard_icon_btn, annotation_icon_btn, settings_icon_btn]:
        btn.config(relief=RAISED, bg=menu_bar_colour)

    for frame in main_frame.winfo_children():
        frame.destroy()
        root.update()

    button.config(relief=SUNKEN, bg="yellow")

    page()

#icons
toggle_icon = PhotoImage(file='icons/owl.png')
dashboard_icon = PhotoImage(file='icons/dashboard.png').subsample(15)
annotation_icon = PhotoImage(file='icons/annotate.png').subsample(15)
settings_icon = PhotoImage(file='icons/settings.png').subsample(15)
logout_icon = PhotoImage(file='icons/exit.png').subsample(15)


menu_bar_frame = Frame(root, bg=menu_bar_colour)
menu_bar_frame.config(width=60)
menu_bar_frame.pack(side=LEFT, fill=Y)
menu_bar_frame.pack_propagate(flag=False)


toggle_icon_label = Label(menu_bar_frame, image=toggle_icon, bg=menu_bar_colour)
toggle_icon_label.place(anchor='center', relx=0.5, rely=0.07)

dashboard_icon_btn = Button(menu_bar_frame, image=dashboard_icon, bg=menu_bar_colour, bd=4, cursor='hand2', activebackground=menu_bar_colour, command=lambda: switch(dashboard_icon_btn, dashboard))
dashboard_icon_btn.place(anchor='center', relx=0.5, rely=0.4)

annotation_icon_btn = Button(menu_bar_frame, image=annotation_icon, bg=menu_bar_colour, bd=4, cursor='hand2', activebackground=menu_bar_colour, command=lambda: switch(annotation_icon_btn, annotation))
annotation_icon_btn.place(anchor='center', relx=0.5, rely=0.5)

settings_icon_btn = Button(menu_bar_frame, image=settings_icon, bg=menu_bar_colour, bd=4, cursor='hand2', activebackground=menu_bar_colour, command=lambda: switch(settings_icon_btn, settings))
settings_icon_btn.place(anchor='center', relx=0.5, rely=0.85)

def logout():
    if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
        root.destroy()

logout_icon_btn = Button(menu_bar_frame, image=logout_icon, bg="red", bd=4, cursor='hand2', activebackground=menu_bar_colour, command=logout)
logout_icon_btn.place(anchor='center', relx=0.5, rely=0.95)

def dashboard():
    dashboard_frame = Frame(main_frame)
    dashboard_lb = Label(dashboard_frame, text="Dashboard", font=('arial', 20, 'bold'), bg='white', fg='black')
    dashboard_lb.pack(pady=20)
    dashboard_frame.pack(fill=BOTH, expand=True) 

def annotation():
    annotation_frame = Frame(main_frame)

    annotation_lb = Label(annotation_frame, text="Annotator", font=('arial', 20, 'bold'), bg='white', fg='black')
    def take_picture():
        # Code to take picture with webcam
        pass

    def select_file():
        file_path = filedialog.askopenfilename()
        # Code to handle selected file
        pass

    take_picture_btn = Button(annotation_frame, text="Take Picture", command=take_picture)

    select_file_btn = Button(annotation_frame, text="Select File", command=select_file)
    # take_picture_btn.pack(side=LEFT)
    # select_file_btn.pack(side=LEFT)
    take_picture_btn.pack(side=TOP, x=10)
    select_file_btn.pack(side=TOP, x=20)

    annotation_lb.pack(pady=20)
    annotation_frame.pack(fill=BOTH, expand=True)

def settings():
    settings_frame = Frame(main_frame)
    settings_lb = Label(settings_frame, text="Settings", font=('arial', 20, 'bold'), bg='white', fg='black')
    settings_lb.pack(pady=20)
    settings_frame.pack(fill=BOTH, expand=True)

def logout():
    root.destroy()

main_frame = Frame(root, bg="white")
main_frame.pack(side=LEFT, fill=BOTH, expand=True)

switch(annotation_icon_btn, annotation)
root.mainloop()