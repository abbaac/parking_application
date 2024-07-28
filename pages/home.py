import tkinter as tk
from .settings import settings
from .dashboard import dashboard
from .annotation import annotation
from tkinter import messagebox
import json
from . import globals

root = tk.Tk()
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth() - 300, root.winfo_screenheight() - 100))
root.title('Owcular Parking Lot Management System')

menu_bar_colour = "#383838"

main_frame = tk.Frame(root, bg="white")
main_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

home_icon = tk.PhotoImage(file='icons/owl.png')
dashboard_icon = tk.PhotoImage(file='icons/dashboard.png').subsample(15)
annotation_icon = tk.PhotoImage(file='icons/annotate.png').subsample(15)
dashboard_home_icon = tk.PhotoImage(file='icons/dashboard.png').subsample(5)
annotation_home_icon = tk.PhotoImage(file='icons/annotate.png').subsample(5)
settings_icon = tk.PhotoImage(file='icons/settings.png').subsample(15)
logout_icon = tk.PhotoImage(file='icons/exit.png').subsample(15)

menu_bar_frame = tk.Frame(root, bg=menu_bar_colour)
menu_bar_frame.config(width=60)
menu_bar_frame.pack(side=tk.LEFT, fill=tk.Y)
menu_bar_frame.pack_propagate(flag=False)

home_icon_btn = tk.Label(menu_bar_frame, image=home_icon, bg=menu_bar_colour)
home_icon_btn.place(anchor='center', relx=0.5, rely=0.07)

dashboard_icon_btn = tk.Button(menu_bar_frame, image=dashboard_icon, bg=menu_bar_colour, bd=4, cursor='hand2', activebackground=menu_bar_colour, command=lambda: switch(dashboard_icon_btn, dashboard))
dashboard_icon_btn.place(anchor='center', relx=0.5, rely=0.4)

annotation_icon_btn = tk.Button(menu_bar_frame, image=annotation_icon, bg=menu_bar_colour, bd=4, cursor='hand2', activebackground=menu_bar_colour, command=lambda: switch(annotation_icon_btn, annotation))
annotation_icon_btn.place(anchor='center', relx=0.5, rely=0.5)

settings_icon_btn = tk.Button(menu_bar_frame, image=settings_icon, bg=menu_bar_colour, bd=4, cursor='hand2', activebackground=menu_bar_colour, command=lambda: switch(settings_icon_btn, settings))
settings_icon_btn.place(anchor='center', relx=0.5, rely=0.85)

def home(main_frame, switch, dashboard_icon_btn, dashboard, annotation, dashboard_home_icon, annotation_home_icon, menu_bar_colour, annotation_icon_btn):
    home_frame = tk.Frame(main_frame)

    home_lb = tk.Label(home_frame, text=f"Welcome to the Owcular Dashboard, {globals.username}.", font=('arial', 20, 'bold'), bg='white', fg='black')
    home_lb_2 = tk.Label(home_frame, text="Select a use case.", font=('arial', 15, 'bold'), bg='white', fg='#F6BB42')

    dashboard_home_btn = tk.Button(home_frame, image=dashboard_home_icon, bg="red", bd=10, cursor='hand2', activebackground=menu_bar_colour, command=lambda: switch(dashboard_icon_btn, dashboard), width=250, height=250)
    dashboard_home_btn.place(anchor='center', relx=0.3, rely=0.45)
    dashboard_home_btn_lb = tk.Label(home_frame, text="View Real Time Analysis", font=('arial', 15, 'bold'), bg='white', fg='black')
    dashboard_home_btn_lb.place(anchor='center', relx=0.3, rely=0.68)

    annotation_home_btn = tk.Button(home_frame, image=annotation_home_icon, bg="yellow", bd=10, cursor='hand2', activebackground=menu_bar_colour, command=lambda: switch(annotation_icon_btn, annotation), width=250, height=250)
    annotation_home_btn.place(anchor='center', relx=0.7, rely=0.45)
    annotation_home_btn_lb = tk.Label(home_frame, text="Annotate your Parking Lot", font=('arial', 15, 'bold'), bg='white', fg='black')
    annotation_home_btn_lb.place(anchor='center', relx=0.7, rely=0.68)

    home_lb.pack(pady=20)
    home_lb_2.pack(pady=10)
    home_frame.pack(fill=tk.BOTH, expand=True)


def switch(button, page):
    for btn in [dashboard_icon_btn, annotation_icon_btn, settings_icon_btn]:
        btn.config(relief=tk.RAISED, bg=menu_bar_colour)

    for frame in main_frame.winfo_children():
        frame.destroy()
        root.update()

    button.config(relief=tk.SUNKEN, bg="yellow")
    page(main_frame, root)

def logout():
    if messagebox.askyesno("Logout", "Are you sure you want to logout?"):  
        occupancy_data = {
            'total_spaces': 0,
            'free_spaces': 0,
            'occupied_spaces': 0,
            'available_spots': 0
        }

        with open('occupancy_data.json', 'w') as file:
            json.dump(occupancy_data, file) 
        root.destroy()

logout_icon_btn = tk.Button(menu_bar_frame, image=logout_icon, bg="red", bd=4, cursor='hand2', activebackground=menu_bar_colour, command=logout)
logout_icon_btn.place(anchor='center', relx=0.5, rely=0.95)

home(main_frame, switch, dashboard_icon_btn, dashboard, annotation, dashboard_home_icon, annotation_home_icon, menu_bar_colour, annotation_icon_btn)
root.mainloop()
