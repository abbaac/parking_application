# from tkinter import *
# from tkinter import messagebox
# from tkinter import filedialog
# import cv2
# from PIL import Image, ImageTk
# import json

# import json

# def save_coordinates(coords):
#     with open("coordinates.json", "w") as file:
#         json.dump([coords], file, indent=4)



# root = Tk()
# # root.attributes('-fullscreen', True)
# root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth()-300, root.winfo_screenheight() - 100))
# root.title('Owcular Parking Lot Management System')

# menu_bar_colour = "#383838"

# def switch(button, page):
#     for btn in [dashboard_icon_btn, annotation_icon_btn, settings_icon_btn]:
#         btn.config(relief=RAISED, bg=menu_bar_colour)

#     for frame in main_frame.winfo_children():
#         frame.destroy()
#         root.update()

#     button.config(relief=SUNKEN, bg="yellow")

#     page()

# #icons
# toggle_icon = PhotoImage(file='icons/owl.png')
# dashboard_icon = PhotoImage(file='icons/dashboard.png').subsample(15)
# annotation_icon = PhotoImage(file='icons/annotate.png').subsample(15)
# settings_icon = PhotoImage(file='icons/settings.png').subsample(15)
# logout_icon = PhotoImage(file='icons/exit.png').subsample(15)

# menu_bar_frame = Frame(root, bg=menu_bar_colour)
# menu_bar_frame.config(width=60)
# menu_bar_frame.pack(side=LEFT, fill=Y)
# menu_bar_frame.pack_propagate(flag=False)

# toggle_icon_label = Label(menu_bar_frame, image=toggle_icon, bg=menu_bar_colour)
# toggle_icon_label.place(anchor='center', relx=0.5, rely=0.07)

# dashboard_icon_btn = Button(menu_bar_frame, image=dashboard_icon, bg=menu_bar_colour, bd=4, cursor='hand2', activebackground=menu_bar_colour, command=lambda: switch(dashboard_icon_btn, dashboard))
# dashboard_icon_btn.place(anchor='center', relx=0.5, rely=0.4)

# annotation_icon_btn = Button(menu_bar_frame, image=annotation_icon, bg=menu_bar_colour, bd=4, cursor='hand2', activebackground=menu_bar_colour, command=lambda: switch(annotation_icon_btn, annotation))
# annotation_icon_btn.place(anchor='center', relx=0.5, rely=0.5)

# settings_icon_btn = Button(menu_bar_frame, image=settings_icon, bg=menu_bar_colour, bd=4, cursor='hand2', activebackground=menu_bar_colour, command=lambda: switch(settings_icon_btn, settings))
# settings_icon_btn.place(anchor='center', relx=0.5, rely=0.85)

# def logout():
#     if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
#         root.destroy()

# logout_icon_btn = Button(menu_bar_frame, image=logout_icon, bg="red", bd=4, cursor='hand2', activebackground=menu_bar_colour, command=logout)
# logout_icon_btn.place(anchor='center', relx=0.5, rely=0.95)

# def dashboard():
#     dashboard_frame = Frame(main_frame)
#     dashboard_lb = Label(dashboard_frame, text="Dashboard", font=('arial', 20, 'bold'), bg='white', fg='black')
#     dashboard_lb.pack(pady=20)
#     dashboard_frame.pack(fill=BOTH, expand=True) 

# def annotation():
#     global annotation_canvas, annotation_box, annotation_frame
#     annotation_frame = Frame(main_frame)
#     annotation_frame.pack(fill=BOTH, expand=True)

#     annotation_canvas = Canvas(annotation_frame, width=800, height=480, bg="white")
#     annotation_canvas.pack()

#     annotation_lb = Label(annotation_frame, text="Annotator", font=('arial', 20, 'bold'), bg='white', fg='black')
#     annotation_lb.place(relx=0.5, rely=0.05, anchor='center')

#     start_x = None
#     start_y = None
#     end_x = None
#     end_y = None
#     current_rectangle = None

#     annotation_history = []  # List to keep track of annotations


#     def is_overlapping(new_coords):
#         for rect_id in annotation_history:
#             existing_coords = annotation_canvas.coords(rect_id)
#             if (new_coords[2] > existing_coords[0] and new_coords[0] < existing_coords[2] and
#                 new_coords[3] > existing_coords[1] and new_coords[1] < existing_coords[3]):
#                 return True
#         return False



#     def start_draw(event):
#         global start_x, start_y
#         start_x = event.x
#         start_y = event.y
#         # Fetch the width and height from the entry boxes, use default values if empty
#         try:
#             fixed_width = int(width_entry.get())
#         except ValueError:
#             fixed_width = 100  # Default width if entry is not a number
#         try:
#             fixed_height = int(height_entry.get())
#         except ValueError:
#             fixed_height = 50  # Default height if entry is not a number
        
#         new_coords = (start_x, start_y, start_x + fixed_width, start_y + fixed_height)
        
#         if not is_overlapping(new_coords):
#             annotation_id = annotation_canvas.create_rectangle(new_coords, outline="green", width=3)
#             annotation_history.append(annotation_id)  # Add this annotation to the history
#             print(annotation_history)
#             # Save only the top-left and bottom-right coordinates
#             save_coordinates({"top_left": (start_x, start_y), "bottom_right": (start_x + fixed_width, start_y + fixed_height)})
#         else:
#             messagebox.showwarning("Overlap", "This annotation overlaps with an existing one.")



#     def undo(event=None):
#         if annotation_history:  # Check if there are annotations to undo
#             last_annotation_id = annotation_history.pop()  # Remove the last annotation ID from the history
#             annotation_canvas.delete(last_annotation_id)  # Remove the last annotation from the canvas
#             print(annotation_history)

#     # Bind Ctrl+Z to the undo function
#     root.bind('<Control-z>', undo)  # Bind the undo function to the root window

#     def delete_annotation(event):
#         # Find the closest annotation to the right-click position
#         clicked_item = annotation_canvas.find_closest(event.x, event.y)
#         if clicked_item:  # If an item was found
#             annotation_canvas.delete(clicked_item)  # Delete the clicked annotation
#             # Also remove the item from the history if it's there
#             if clicked_item[0] in annotation_history:
#                 annotation_history.remove(clicked_item[0])

#     # Bind the right mouse click to remove an annotation
#     annotation_canvas.bind("<Button-3>", delete_annotation)

#     def show_image(file_path):
#         global start_x, start_y, annotation_canvas
#         img = Image.open(file_path)
#         img = img.resize((800, 480))  # Resize the image to match the window size
#         photo_img = ImageTk.PhotoImage(img)  # Convert to PhotoImage

#         # If the canvas exists, delete it and create a new one
#         if hasattr(annotation_box, 'canvas'):
#             annotation_box.canvas.destroy()

#         annotation_canvas = Canvas(annotation_box, width=800, height=480)
#         annotation_canvas.pack()
#         annotation_canvas.create_image(0, 0, anchor=NW, image=photo_img)
#         annotation_canvas.image = photo_img  # Prevent garbage collection

#         # Bind mouse events to the canvas
#         annotation_canvas.bind("<ButtonPress-1>", start_draw)

#     def open_webcam():
#         def capture_image():
#             ret, frame = cap.read()
#             if ret:
#                 img_name = "captured_image.jpg"
#                 cv2.imwrite(img_name, frame)
#                 show_image(img_name)
#                 cap.release()
#                 webcam_window.destroy()
#             else:
#                 print("Error: Could not capture image.")

#         webcam_window = Toplevel(main_frame)
#         webcam_window.title("Webcam Capture")
#         webcam_frame = Frame(webcam_window, width=800, height=480)
#         webcam_frame.pack()

#         cap = cv2.VideoCapture(0)
#         if not cap.isOpened():
#             print("Error: Could not open webcam.")
#             webcam_window.destroy()
#             return

#         lmain = Label(webcam_frame)
#         lmain.pack()

#         def show_frame():
#             _, frame = cap.read()
#             cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
#             img = Image.fromarray(cv2image)
#             imgtk = ImageTk.PhotoImage(image=img)
#             lmain.imgtk = imgtk
#             lmain.configure(image=imgtk)
#             lmain.after(10, show_frame)

#         show_frame()

#         capture_btn = Button(webcam_window, text="Capture", command=capture_image)
#         capture_btn.pack()

#         webcam_window.protocol("WM_DELETE_WINDOW", lambda: [cap.release(), webcam_window.destroy()])

#     def upload_image():
#         file_path = filedialog.askopenfilename()
#         if not file_path:  # Check if a file was selected
#             return
#         show_image(file_path)

#     take_picture_btn = Button(annotation_frame, text="Open Webcam", command=open_webcam, width=12)
#     upload_file_btn = Button(annotation_frame, text="Upload File", 
#                              width=12,
#                              command= upload_image)

#     take_picture_btn.place(relx=0.45, rely=0.15, anchor='center')    
#     upload_file_btn.place(relx=0.55, rely=0.15, anchor='center')

#     commentator = Label(annotation_frame, width=75, bg='yellow', text="No image data to annotate", fg='black')
#     commentator.place(relx=0.5, rely=0.25, anchor='center')

#     annotation_box = Frame(annotation_frame, width=800, height=480, bg="grey", pady="10")
#     annotation_box.place(relx=0.5, rely=0.6, anchor='center')

#     width_label = Label(annotation_frame, text="Width:", font=('arial', 12), bg='white')
#     width_label.place(relx=0.85, rely=0.35)
#     width_entry = Entry(annotation_frame, bd=2, width=4)
#     width_entry.place(relx=0.9, rely=0.35)

#     height_label = Label(annotation_frame, text="Height:", font=('arial', 12), bg='white')
#     height_label.place(relx=0.85, rely=0.3)
#     height_entry = Entry(annotation_frame, bd=2, width=4)
#     height_entry.place(relx=0.9, rely=0.3)

#     annotation_frame.pack(fill=BOTH, expand=True)

# def settings():
#     settings_frame = Frame(main_frame)
#     settings_lb = Label(settings_frame, text="Settings", font=('arial', 20, 'bold'), bg='white', fg='black')
#     settings_lb.pack(pady=20)
#     settings_frame.pack(fill=BOTH, expand=True)

# def logout():
#     root.destroy()

# main_frame = Frame(root, bg="white")
# main_frame.pack(side=LEFT, fill=BOTH, expand=True)

# switch(annotation_icon_btn, annotation)
# root.mainloop()

# main.py
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import cv2
from PIL import Image, ImageTk
import json
from annotation import create_annotation_page  # Import the function

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

annotation_icon_btn = Button(menu_bar_frame, image=annotation_icon, bg=menu_bar_colour, bd=4, cursor='hand2', activebackground=menu_bar_colour, command=lambda: switch(annotation_icon_btn, lambda: create_annotation_page(main_frame, root)))
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

def settings():
    settings_frame = Frame(main_frame)
    settings_lb = Label(settings_frame, text="Settings", font=('arial', 20, 'bold'), bg='white', fg='black')
    settings_lb.pack(pady=20)
    settings_frame.pack(fill=BOTH, expand=True)

def logout():
    root.destroy()

main_frame = Frame(root, bg="white")
main_frame.pack(side=LEFT, fill=BOTH, expand=True)

switch(annotation_icon_btn, lambda: create_annotation_page(main_frame, root))
root.mainloop()

