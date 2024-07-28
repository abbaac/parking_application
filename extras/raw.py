import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import cv2
from PIL import Image, ImageTk
import json
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import requests
import os
from tkinter import messagebox

previous_occupied_spaces = None  # Initialize global variable to keep track of previous occupancy
is_video_paused = False  # Initialize global variable to keep track of pause/play state
camera_on = False
cap = None
update_id = None

def dashboard(main_frame, root):
    dashboard_frame = tk.Frame(main_frame, bg="#DEDDE3")
    dashboard_lb = tk.Label(dashboard_frame, text="Dashboard", font=('arial', 20, 'bold'), bg="#DEDDE3", fg='black')
    dashboard_lb.pack(pady=20)

    # Create frames for the notebook and pie chart
    video_feed_frame = tk.Frame(dashboard_frame, width=int(root.winfo_width() * 0.75), bg="#DEDDE3")
    analytical_frame = tk.Frame(dashboard_frame, width=int(root.winfo_width() * 0.25), bg="#DEDDE3")

    video_feed_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    analytical_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    notebook = ttk.Notebook(video_feed_frame)
    notebook.pack(fill=tk.BOTH, expand=True)

    realtime_tab = tk.Frame(notebook)
    video_tab = tk.Frame(notebook)
    
    notebook.add(realtime_tab, text="Real-Time View")
    notebook.add(video_tab, text="Video")

    # cap = None  # Initialize the video capture object

    # Initialize the pie chart figure and canvas
    fig, ax = plt.subplots()
    ax.pie([1], labels=['Loading'], colors=['gray'], autopct='%1.1f%%', shadow=True, startangle=140)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    ax.set_title('Occupied Spaces')  # Set the title for the pie chart
    pie_canvas = FigureCanvasTkAgg(fig, master=analytical_frame)
    
    pie_chart_width = int(root.winfo_width() * 0.7)
    pie_chart_height = int(root.winfo_height() * 0.4)
    
    pie_canvas.get_tk_widget().place(relx=0.5, rely=0.2, anchor=tk.CENTER, width=pie_chart_width, height=pie_chart_height)
    pie_canvas.draw()

    # Create a frame for the virtual view of the lot with a border and title
    virtual_view_frame = tk.Frame(analytical_frame, bd=2, relief="solid")
    virtual_view_frame.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

    virtual_view_title = tk.Label(analytical_frame, text="Virtual View", font=('arial', 12, 'bold'))
    virtual_view_title.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

    # # Keep track of the button state on/off
    # global is_on
    # is_on = False

    def load_coordinates():
        coordinates_dir = "local/coordinates"
        if not os.path.exists(coordinates_dir):
            os.makedirs(coordinates_dir)

        # Ask user to select a JSON file from the 'coordinates' directory
        file_path = filedialog.askopenfilename(initialdir=coordinates_dir, filetypes=[("JSON files", "*.json")])
        if not file_path:
            return
        try:
            with open(file_path, "r") as file:
                loaded_coordinates = json.load(file)
                # return coordinates
                # Check parking space occupancy
                check_parking_space(dilated_frame, frame_resized, loaded_coordinates)
                # process_frame(video_canvas)
        except Exception as e:
            print(f"Error loading coordinates: {e}")
            return None


    def toggle_camera(tab_canvas):
        def inner_toggle():
            global camera_on, cap, update_id
            if camera_on:
                camera_on = False
                on_button.config(text="Turn on camera feed")
                if cap is not None and cap.isOpened():
                    cap.release()
                    tab_canvas.delete("all")
                if update_id is not None:
                    tab_canvas.after_cancel(update_id)
            else:
                camera_on = True
                on_button.config(text="Turn off camera feed")
                cap = cv2.VideoCapture(0)
                process_frame(real_time_canvas)
        return inner_toggle

    def process_frame(canvas_video):
        global cap, update_id, dilated_frame, frame_resized
        if camera_on and cap is not None:
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

                # Convert the processed frame to a format suitable for Tkinter
                img = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
                imgtk = ImageTk.PhotoImage(image=Image.fromarray(img))

                # Update the canvas with the new frame
                canvas_video.create_image(0, 0, anchor=tk.NW, image=imgtk)
                canvas_video.image = imgtk  # Keep a reference to avoid garbage collection

            # Call this function again after 10 milliseconds
            update_id = canvas_video.after(10, process_frame, canvas_video)

    # Video Upload and Display
    upload_cap = None  # Variable to hold the video capture object for uploaded videos

    def upload_video():
        nonlocal upload_cap
        file_path = filedialog.askopenfilename()
        if not file_path:
            return
        if upload_cap is not None:
            upload_cap.release()  # Release the previous video capture object if it exists
            process_frame(video_canvas_upload)  # Start processing the new video

        upload_cap = cv2.VideoCapture(file_path)  # Open the new video file
        video_canvas_upload.delete("all")  # Clear the canvas for the new video

    def check_parking_space(dilated_frame, frame, coordinates):
        global previous_occupied_spaces
        occupied_spaces = 0
        available_spots = []
        for coord in coordinates:
            points = coord["points"]
            box_id = coord["id"]
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
                available_spots.append(box_id)

            cv2.polylines(frame, [polygon], isClosed=True, color=color, thickness=1)
            cv2.putText(frame, str(occupied_area), (points[0][0], points[0][1] - 5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.5, color, 1)
        
        total_spaces = len(coordinates)
        print(coordinates)
        # free_spaces = total_spaces - occupied_spaces
        cv2.putText(frame, f'{occupied_spaces} / {total_spaces}', (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 255), 3)


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

    # Real-Time View
    real_time_canvas = tk.Canvas(realtime_tab, width=800, height=480, bg='black')
    real_time_canvas.pack()

    # Create A Button for the switch
    on_button = tk.Button(realtime_tab, text="Turn on camera feed", command=toggle_camera(real_time_canvas))
    on_button.pack(pady=10)

    load_coordinates_real_time = tk.Button(realtime_tab, text="Load Coordinates", command=load_coordinates)
    load_coordinates_real_time.pack(pady=10)


    # Video View
    video_canvas_upload = tk.Canvas(video_tab, width=800, height=480, bg='black')
    video_canvas_upload.pack()
    
    upload_button = tk.Button(video_tab, text="Upload Video", command=upload_video)
    upload_button.pack(pady=10)

    load_coordinates_video = tk.Button(video_tab, text="Load Coordinates", command=load_coordinates)
    load_coordinates_video.pack(pady=10)

    

    dashboard_frame.pack(fill=tk.BOTH, expand=True)



# Main function to initialize and run the tkinter application
def main():
    root = tk.Tk()
    root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth() - 300, root.winfo_screenheight() - 100))
    root.title('Owcular Parking Lot Management System')

    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True)

    dashboard(main_frame, root)

    def on_closing():
        global cap
        if cap is not None and cap.isOpened():
            cap.release()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()