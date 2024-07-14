import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
import cv2
from PIL import Image, ImageTk
import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from annotation import create_annotation_page  # Import the function

root = tk.Tk()
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth() - 300, root.winfo_screenheight() - 100))
root.title('Owcular Parking Lot Management System')

menu_bar_colour = "#383838"

previous_occupied_spaces = None  # Initialize global variable to keep track of previous occupancy
is_video_paused = False  # Initialize global variable to keep track of pause/play state

def switch(button, page):
    for btn in [dashboard_icon_btn, annotation_icon_btn, settings_icon_btn]:
        btn.config(relief=tk.RAISED, bg=menu_bar_colour)

    for frame in main_frame.winfo_children():
        frame.destroy()
        root.update()

    button.config(relief=tk.SUNKEN, bg="yellow")

    page()

# Icons
toggle_icon = tk.PhotoImage(file='icons/owl.png')
dashboard_icon = tk.PhotoImage(file='icons/dashboard.png').subsample(15)
annotation_icon = tk.PhotoImage(file='icons/annotate.png').subsample(15)
settings_icon = tk.PhotoImage(file='icons/settings.png').subsample(15)
logout_icon = tk.PhotoImage(file='icons/exit.png').subsample(15)

menu_bar_frame = tk.Frame(root, bg=menu_bar_colour)
menu_bar_frame.config(width=60)
menu_bar_frame.pack(side=tk.LEFT, fill=tk.Y)
menu_bar_frame.pack_propagate(flag=False)

toggle_icon_label = tk.Label(menu_bar_frame, image=toggle_icon, bg=menu_bar_colour)
toggle_icon_label.place(anchor='center', relx=0.5, rely=0.07)

dashboard_icon_btn = tk.Button(menu_bar_frame, image=dashboard_icon, bg=menu_bar_colour, bd=4, cursor='hand2', activebackground=menu_bar_colour, command=lambda: switch(dashboard_icon_btn, dashboard))
dashboard_icon_btn.place(anchor='center', relx=0.5, rely=0.4)

annotation_icon_btn = tk.Button(menu_bar_frame, image=annotation_icon, bg=menu_bar_colour, bd=4, cursor='hand2', activebackground=menu_bar_colour, command=lambda: switch(annotation_icon_btn, lambda: create_annotation_page(main_frame, root)))
annotation_icon_btn.place(anchor='center', relx=0.5, rely=0.5)

settings_icon_btn = tk.Button(menu_bar_frame, image=settings_icon, bg=menu_bar_colour, bd=4, cursor='hand2', activebackground=menu_bar_colour, command=lambda: switch(settings_icon_btn, settings))
settings_icon_btn.place(anchor='center', relx=0.5, rely=0.85)

def logout():
    if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
        root.destroy()

logout_icon_btn = tk.Button(menu_bar_frame, image=logout_icon, bg="red", bd=4, cursor='hand2', activebackground=menu_bar_colour, command=logout)
logout_icon_btn.place(anchor='center', relx=0.5, rely=0.95)

def dashboard():
    dashboard_frame = tk.Frame(main_frame, bg="#DEDDE3")
    dashboard_lb = tk.Label(dashboard_frame, text="Dashboard", font=('arial', 20, 'bold'), bg="#DEDDE3", fg='black')
    dashboard_lb.pack(pady=20)

    # Create frames for the notebook and pie chart
    notebook_frame = tk.Frame(dashboard_frame, width=int(root.winfo_width() * 0.75), bg="#DEDDE3")
    pie_chart_frame = tk.Frame(dashboard_frame, width=int(root.winfo_width() * 0.25), bg="#DEDDE3")

    notebook_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    pie_chart_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    notebook = ttk.Notebook(notebook_frame)
    notebook.pack(fill=tk.BOTH, expand=True)

    realtime_tab = tk.Frame(notebook)
    video_tab = tk.Frame(notebook)
    
    notebook.add(realtime_tab, text="Real-Time View")
    notebook.add(video_tab, text="Video")

    # Real-Time View
    video_canvas = tk.Canvas(realtime_tab, width=800, height=480, bg='black')
    video_canvas.pack()

    cap = None  # Initialize the video capture object

    # Read coordinates from the annotation frame
    try:
        with open("coordinates.json", "r") as file:
            coordinates = json.load(file)
    except FileNotFoundError:
        coordinates = []

    # Initialize the pie chart figure and canvas
    fig, ax = plt.subplots()
    ax.pie([1], labels=['Loading'], colors=['gray'], autopct='%1.1f%%', shadow=True, startangle=140)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    ax.set_title('Occupied Spaces')  # Set the title for the pie chart
    pie_canvas = FigureCanvasTkAgg(fig, master=pie_chart_frame)
    
    pie_chart_width = int(root.winfo_width() * 0.7)
    pie_chart_height = int(root.winfo_height() * 0.4)
    
    pie_canvas.get_tk_widget().place(relx=0.5, rely=0.2, anchor=tk.CENTER, width=pie_chart_width, height=pie_chart_height)
    pie_canvas.draw()

    # Create a frame for the virtual view of the lot with a border and title
    virtual_view_frame = tk.Frame(pie_chart_frame, bd=2, relief="solid")
    virtual_view_frame.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

    virtual_view_title = tk.Label(pie_chart_frame, text="Virtual View", font=('arial', 12, 'bold'))
    virtual_view_title.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

    # Keep track of the button state on/off
    global is_on
    is_on = False

    def switch_camera():
        nonlocal cap
        global is_on
        
        if is_on:
            # Turn off the camera
            is_on = False
            on_button.config(image=off)
            camera_status_label.config(text="The Camera is Off", fg="grey")
            if cap is not None and cap.isOpened():
                cap.release()
                video_canvas.delete("all")  # Clear the canvas
        else:
            # Turn on the camera
            is_on = True
            on_button.config(image=on)
            camera_status_label.config(text="The Camera is On", fg="green")
            cap = cv2.VideoCapture(0)  # Initialize the video capture
            process_frame()  # Start processing frames

    def process_frame():
        if is_on:
            ret, frame = cap.read()
            if ret:
                # Resize the frame once
                frame_resized = cv2.resize(frame, (800, 480))

                # Apply image processing
                gray_frame = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2GRAY)
                blurred_frame = cv2.GaussianBlur(gray_frame, (3, 3), 1)
                threshold_frame = cv2.adaptiveThreshold(blurred_frame, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
                frame_median = cv2.medianBlur(threshold_frame, 5)
                kernel = np.ones((5, 5), np.uint8)
                dilated_frame = cv2.dilate(frame_median, kernel, iterations=1)

                # Check parking space occupancy
                check_parking_space(dilated_frame, frame_resized)

                # Convert the processed frame to a format suitable for Tkinter
                img = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
                imgtk = ImageTk.PhotoImage(image=Image.fromarray(img))

                # Update the canvas with the new frame
                video_canvas.create_image(0, 0, anchor=tk.NW, image=imgtk)
                video_canvas.image = imgtk  # Keep a reference to avoid garbage collection

            # Call this function again after 10 milliseconds
            dashboard_frame.after(10, process_frame)

    # Video Upload and Display
    upload_cap = None  # Variable to hold the video capture object for uploaded videos

    def upload_video():
        nonlocal upload_cap
        file_path = filedialog.askopenfilename()
        if not file_path:
            return
        if upload_cap is not None:
            upload_cap.release()  # Release the previous video capture object if it exists

        upload_cap = cv2.VideoCapture(file_path)  # Open the new video file
        video_canvas_upload.delete("all")  # Clear the canvas for the new video

        def process_uploaded_video():
            if not is_video_paused:
                ret, frame = upload_cap.read()
                if ret:
                    # Resize the frame once
                    frame_resized = cv2.resize(frame, (800, 480))

                    # Apply image processing
                    gray_frame = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2GRAY)
                    blurred_frame = cv2.GaussianBlur(gray_frame, (3, 3), 1)
                    threshold_frame = cv2.adaptiveThreshold(blurred_frame, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
                    frame_median = cv2.medianBlur(threshold_frame, 5)
                    kernel = np.ones((5, 5), np.uint8)
                    dilated_frame = cv2.dilate(frame_median, kernel, iterations=1)

                    # Check parking space occupancy
                    check_parking_space(dilated_frame, frame_resized)

                    # Convert the processed frame to a format suitable for Tkinter
                    img = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
                    imgtk = ImageTk.PhotoImage(image=Image.fromarray(img))

                    # Update the canvas with the new frame
                    video_canvas_upload.create_image(0, 0, anchor=tk.NW, image=imgtk)
                    video_canvas_upload.image = imgtk  # Keep a reference to avoid garbage collection

                    # Call this function again after 30 milliseconds
                    video_tab.after(30, process_uploaded_video)
                else:
                    upload_cap.release()
            else:
                video_tab.after(30, process_uploaded_video)

        process_uploaded_video()

    def check_parking_space(dilated_frame, frame):
        global previous_occupied_spaces
        occupied_spaces = 0

        for coord in coordinates:
            points = coord["points"]
            polygon = np.array(points, np.int32)
            polygon = polygon.reshape((-1, 1, 2))

            mask = np.zeros(dilated_frame.shape, dtype=np.uint8)
            cv2.fillPoly(mask, [polygon], 255)
            img_crop = cv2.bitwise_and(dilated_frame, mask)
            total_area = cv2.countNonZero(mask)
            occupied_area = cv2.countNonZero(img_crop)

            if occupied_area >= (total_area * 0.75) / 2:
                occupied_spaces += 1
                color = (0, 0, 255)
            else:
                color = (0, 255, 0)

            cv2.polylines(frame, [polygon], isClosed=True, color=color, thickness=1)
            cv2.putText(frame, str(occupied_area), (points[0][0], points[0][1] - 5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.5, color, 1)

        total_spaces = len(coordinates)
        free_spaces = total_spaces - occupied_spaces
        cv2.putText(frame, f'{occupied_spaces} / {total_spaces}', (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 255), 3)

        # Update pie chart only if there is a change in occupancy
        if previous_occupied_spaces is None or previous_occupied_spaces != occupied_spaces:
            update_pie_chart(free_spaces, occupied_spaces, dilated_frame)
            previous_occupied_spaces = occupied_spaces

    def update_pie_chart(free_spaces, occupied_spaces, dilated_frame):
        labels = 'Free', 'Occupied'
        sizes = [free_spaces, occupied_spaces]
        colors = ['green', 'red']
        explode = (0, 0.1)  # only "explode" the 2nd slice (i.e. 'Occupied')

        ax.clear()
        ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        ax.set_title('Occupied Spaces')  # Set the title for the pie chart

        pie_canvas.draw()

        # Clear the previous virtual view boxes
        for widget in virtual_view_frame.winfo_children():
            widget.destroy()

        # Create the virtual view boxes
        for coord in coordinates:
            points = coord["points"]
            box_id = coord["id"]
            occupied = is_occupied(coord, dilated_frame)
            color = "red" if occupied else "green"
            box = tk.Label(virtual_view_frame, text=str(box_id), bg=color, fg="white", width=5, height=2)
            box.pack(side=tk.LEFT, padx=5, pady=5)

    def is_occupied(coord, dilated_frame):
        points = coord["points"]
        polygon = np.array(points, np.int32)
        polygon = polygon.reshape((-1, 1, 2))

        mask = np.zeros(dilated_frame.shape, dtype=np.uint8)
        cv2.fillPoly(mask, [polygon], 255)
        img_crop = cv2.bitwise_and(dilated_frame, mask)
        total_area = cv2.countNonZero(mask)
        occupied_area = cv2.countNonZero(img_crop)

        return occupied_area >= (total_area * 0.75) / 2

    # Define Our Images
    on = tk.PhotoImage(file="icons/on.png")
    off = tk.PhotoImage(file="icons/off.png")

    # Create a Label for camera status
    camera_status_label = tk.Label(realtime_tab, text="The Camera is Off", fg="grey", font=("Helvetica", 32))
    camera_status_label.pack(pady=20)

    # Create A Button for the switch
    on_button = tk.Button(realtime_tab, image=off, bd=0, command=switch_camera)
    on_button.pack(pady=20)

    video_canvas_upload = tk.Canvas(video_tab, width=800, height=480, bg='black')
    video_canvas_upload.pack()

    upload_button = tk.Button(video_tab, text="Upload Video", command=upload_video)
    upload_button.pack(pady=20)

    dashboard_frame.pack(fill=tk.BOTH, expand=True)

def settings():
    settings_frame = tk.Frame(main_frame)
    settings_lb = tk.Label(settings_frame, text="Settings", font=('arial', 20, 'bold'), bg='white', fg='black')
    settings_lb.pack(pady=20)
    settings_frame.pack(fill=tk.BOTH, expand=True)

def logout():
    root.destroy()

main_frame = tk.Frame(root, bg="white")
main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

switch(annotation_icon_btn, lambda: create_annotation_page(main_frame, root))
root.mainloop()
