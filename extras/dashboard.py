# dashboard.py

import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import cv2
from PIL import Image, ImageTk
import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import requests

previous_occupied_spaces = None  # Initialize global variable to keep track of previous occupancy
is_video_paused = False  # Initialize global variable to keep track of pause/play state

def dashboard(main_frame, root):
    global previous_occupied_spaces, is_video_paused
    
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
        available_spots = []

        for coord in coordinates:
            points = coord["points"]
            box_id = coord["id"]
            polygon = np.array(points, np.int32)
            polygon = reshaped_polygon(polygon)

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
                available_spots.append(box_id)

            cv2.polylines(frame, [polygon], True, color, 2)
            # centroid = np.mean(polygon, axis=0).astype(int)
            # cv2.putText(frame, str(box_id), tuple(centroid), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        occupied_percentage = (occupied_spaces / len(coordinates)) * 100 if coordinates else 0

        if previous_occupied_spaces != occupied_spaces:
            update_pie_chart(occupied_spaces, len(coordinates) - occupied_spaces)
            previous_occupied_spaces = occupied_spaces

        # Send available_spots to the API
        if available_spots:
            send_to_api(available_spots)

    def reshaped_polygon(polygon):
        return polygon.reshape((-1, 1, 2))

    def update_pie_chart(occupied, available):
        labels = ['Occupied', 'Available']
        sizes = [occupied, available]
        colors = ['red', 'green']

        ax.clear()
        ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        ax.set_title('Occupied Spaces')  # Set the title for the pie chart
        pie_canvas.draw()

    def send_to_api(available_spots):
        url = "http://127.0.0.1:5000/api/receive-data"
        payload = json.dumps({"available_spots": available_spots})
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, data=payload, headers=headers)
        print(f"Sent data to API, response status: {response.status_code}")

    # Create the switch button and label
    on = ImageTk.PhotoImage(file="icons/on.png")
    off = ImageTk.PhotoImage(file="icons/off.png")
    on_button = tk.Button(realtime_tab, image=off, bd=0, command=switch_camera)
    on_button.pack(pady=20)

    camera_status_label = tk.Label(realtime_tab, text="The Camera is Off", font=("Helvetica", 14), fg="grey")
    camera_status_label.pack()

    # Create the video upload button
    upload_button = tk.Button(video_tab, text="Upload Video", command=upload_video)
    upload_button.pack(pady=10)

    video_canvas_upload = tk.Canvas(video_tab, width=800, height=480, bg='black')
    video_canvas_upload.pack()

    def toggle_video_pause():
        global is_video_paused
        is_video_paused = not is_video_paused
        pause_button.config(text="Play" if is_video_paused else "Pause")

    # Add a pause button to the video tab
    pause_button = tk.Button(video_tab, text="Pause", command=toggle_video_pause)
    pause_button.pack(pady=10)

    dashboard_frame.pack(fill=tk.BOTH, expand=True)
    return dashboard_frame
