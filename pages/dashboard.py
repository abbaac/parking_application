import tkinter as tk
from tkinter import filedialog, Label
import cv2
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import json
from tkinter import filedialog, messagebox
import numpy as np


camera_on = False
cap = None
loaded_coords = []


def update_pie_chart(pie_ax, data, labels):
    pie_ax.clear()
    colors = ['red', 'green']  # Define colors for the pie chart
    wedges, texts, autotexts = pie_ax.pie(data, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
    
    # Customize text inside the pie chart
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(10)

    occupied_spaces = data[0]
    free_spaces = data[1]

    if free_spaces == 1000:
        free_spaces = 0


    # Define background properties
    bbox_props_free = dict(boxstyle="round,pad=0.3", edgecolor='none', facecolor='lightgreen')
    bbox_props_occupied = dict(boxstyle="round,pad=0.3", edgecolor='none', facecolor='lightcoral')
    
    # Add "free" text in green
    pie_ax.text(-0.3, -1.5, f"{free_spaces} Free", ha='right', va='baseline', fontsize=12, color='green', bbox=bbox_props_free)
    
    # Add "occupied" text in red
    pie_ax.text(0.3, -1.5, f"{occupied_spaces} Occupied", ha='left', va='baseline', fontsize=12, color='red', bbox=bbox_props_occupied)
    
    pie_ax.set_position([0.1, 0.15, 0.8, 0.8])  # [left, bottom, width, height]
    
    pie_ax.figure.canvas.draw()


def load_coordinates(canvas, pie_ax, pie_labels, virtual_view_canvas):
    global loaded_coords
    file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if file_path:
        with open(file_path, 'r') as file:
            loaded_coords = json.load(file)
        # Clear the canvas (video frame will be redrawn by show_video)
        canvas.delete("all")
        # Call show_video to ensure coordinates are drawn on top of the video
        if cap:
            show_video(cap, canvas, loaded_coords, pie_ax, pie_labels)
        
        update_virtual_view(virtual_view_canvas, loaded_coords)


def start_camera(canvas):
    global cap
    cap = cv2.VideoCapture(0)  # 0 is the default camera
    show_video(cap, canvas)

def upload_video(canvas, camera_btn, upload_btn, pie_ax, pie_labels):
    global camera_on, cap
    if upload_btn['text'] == "Remove Video":
        canvas.delete("all")
        if cap:
            cap.release()
            cap = None
        upload_btn.config(text="Upload Video")
        return

    file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi")])
    if file_path:
        if camera_on:
            toggle_camera(camera_btn, canvas, upload_btn)  # Toggle camera off if it is on
        if cap:
            cap.release()
        cap = cv2.VideoCapture(file_path)
        show_video(cap, canvas, loaded_coords, pie_ax, pie_labels)
        upload_btn.config(text="Remove Video")

def toggle_camera(camera_btn, canvas, upload_btn, pie_ax, pie_labels):
    global camera_on, cap
    if camera_on:
        camera_on = False
        camera_btn.config(text="Start Camera Stream")
        if cap:
            cap.release()
            cap = None
        canvas.delete("all")  # Clear the canvas when stopping the camera stream
    else:
        if upload_btn['text'] == "Remove Video":
            canvas.delete("all")
            if cap:
                cap.release()
                cap = None
            upload_btn.config(text="Upload Video")
        camera_on = True
        camera_btn.config(text="Stop Camera Stream")
        cap = cv2.VideoCapture(0)
        show_video(cap, canvas, loaded_coords, pie_ax, pie_labels)


def show_video(cap, canvas, coords=[], pie_ax=None, pie_labels=None):
    if cap.isOpened():
        ret, frame = cap.read()
        if ret:
            # Resize the frame
            frame_resized = cv2.resize(frame, (800, 480))

            # Apply image processing
            gray_frame = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2GRAY)
            blurred_frame = cv2.GaussianBlur(gray_frame, (3, 3), 1)
            threshold_frame = cv2.adaptiveThreshold(blurred_frame, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
            frame_median = cv2.medianBlur(threshold_frame, 5)
            kernel = np.ones((5, 5), np.uint8)
            dilated_frame = cv2.dilate(frame_median, kernel, iterations=1)

            occupied_spaces = 0
            available_spots = []

            # Draw coordinates on top of the video frame
            for coord in coords:
                points = coord["points"]
                polygon = np.array(points, np.int32).reshape((-1, 1, 2))
                
                mask = np.zeros(dilated_frame.shape, dtype=np.uint8)
                cv2.fillPoly(mask, [polygon], 255)
                img_crop = cv2.bitwise_and(dilated_frame, mask)
                total_area = cv2.countNonZero(mask)
                occupied_area = cv2.countNonZero(img_crop)

                if occupied_area >= (total_area * 0.75) / 2:
                    coord["occupied"] = True  # Mark as occupied
                    occupied_spaces += 1
                    color = (0, 0, 255)
                else:
                    coord["occupied"] = False  # Mark as free
                    color = (0, 255, 0)
                    available_spots.append(coord["id"])

                cv2.polylines(frame_resized, [polygon], isClosed=True, color=color, thickness=1)
                cv2.putText(frame_resized, str(occupied_area), (points[0][0], points[0][1] - 5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.5, color, 1)

            # Calculate free spaces
            total_spaces = len(coords)
            free_spaces = total_spaces - occupied_spaces

            # Update the pie chart
            if pie_ax and pie_labels:
                data = [occupied_spaces, free_spaces]
                update_pie_chart(pie_ax, data, pie_labels)

            # Convert the processed frame to a format suitable for Tkinter
            img = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
            imgtk = ImageTk.PhotoImage(image=Image.fromarray(img))
            canvas.imgtk = imgtk
            canvas.create_image(0, 0, anchor=tk.NW, image=imgtk)
        
        canvas.after(10, show_video, cap, canvas, coords, pie_ax, pie_labels)


def update_virtual_view(canvas, coords):
    # Clear previous content
    canvas.delete("all")

    if not coords:
        print("No coordinates loaded.")
        return

    # Set dimensions and colors
    rect_width = 50
    rect_height = 30
    occupied_color = '#FF0000'  # Red for occupied
    free_color = '#00FF00'  # Green for free

    # Draw rectangles for each parking space
    for idx, coord in enumerate(coords):
        x = (idx % 6) * (rect_width + 10) + 10  # X position
        y = (idx // 6) * (rect_height + 10) + 10  # Y position
        
        # Determine color based on occupancy status
        color = occupied_color if coord.get("occupied", False) else free_color
        
        # Draw rectangle
        canvas.create_rectangle(x, y, x + rect_width, y + rect_height, fill=color, outline='black')
        # Draw text (ID) inside the rectangle
        canvas.create_text(x + rect_width / 2, y + rect_height / 2, text=str(coord["id"]), fill='white')

    # Schedule the next update
    canvas.after(1000, update_virtual_view, canvas, coords)  # Update every second




def dashboard(main_frame, root):
    dashboard_frame = tk.Frame(main_frame, bg="#DEDDE3")

    dashboard_lb = tk.Label(dashboard_frame, text="Dashboard", font=('arial', 20, 'bold'), bg="#DEDDE3", fg='black')
    dashboard_lb.pack(pady=((20, 40)))

    video_frame = tk.Frame(dashboard_frame, bg="#DEDDE3", border=2, relief=tk.SOLID)
    video_frame.pack_propagate(False)
    video_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    analytics_frame = tk.Frame(dashboard_frame, bg="#DEDDE3", border=2, relief=tk.SOLID)
    analytics_frame.pack_propagate(False)
    analytics_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    root.update_idletasks()  # Ensure the root is updated to get the correct dimensions

    video_frame.config(width=int(root.winfo_width() * 0.6))
    analytics_frame.config(width=int(root.winfo_width() * 0.3))

    ##############################Video Frame############################################

    video_lb = tk.Label(video_frame, text="Video Feed", font=('arial', 15, 'bold'), bg="black", fg='white')
    video_lb.pack(pady=((20, 5)))

    # Placeholder for video display with fixed dimensions
    video_canvas = tk.Canvas(video_frame, bg="black", width=800, height=480)
    video_canvas.pack(pady=5)

    # Buttons for uploading video and starting camera stream
    upload_btn = tk.Button(video_frame, text="Upload Video", command=lambda: upload_video(video_canvas, camera_btn, upload_btn, pie_ax, labels))
    upload_btn.place(relx=0.2, rely=0.8, anchor='center')

    # Toggle button for camera stream
    camera_btn = tk.Button(video_frame, text="Start Camera Stream", command=lambda: toggle_camera(camera_btn, video_canvas, upload_btn, pie_ax, labels))
    camera_btn.place(relx=0.35, rely=0.8, anchor='center')

    load_coords_btn = tk.Button(video_frame, text="Load Coordinates", command=lambda: load_coordinates(video_canvas, pie_ax, labels, virtual_view_canvas))
    load_coords_btn.place(relx=0.8, rely=0.8, anchor='center')


    video_frame_instructions = Label(video_frame, text="Dashboard Instructions", font=('arial', 15, 'bold'), fg='black')
    video_frame_instructions = Label(video_frame, text="1. Upload a video or begin camera stream for real-time analysis of a parking lot.\n 2. Load corresponding coordinates for parking space occupancy detection.\n3. View analytics and share link for remote access on occupancy.", font=('arial', 10, ''), bg='#D5B895', fg='black')
    video_frame_instructions.place(relx=0.5, rely=0.9, anchor='center')
    video_frame_instructions.place(relx=0.5, rely=0.9, anchor='center')

    ##############################Analytics Frame############################################

    analytics_lb = tk.Label(analytics_frame, text="Occupancy Chart", font=('arial', 15, 'bold'), bg="black", fg='white')
    analytics_lb.pack(pady=20)

    # Create a matplotlib figure and axis for the pie chart
    fig = Figure(figsize=(3, 3), dpi=100)
    pie_ax = fig.add_subplot(111)

    # Initial data for the pie chart
    data = [0, 1000]
    labels = ['Occupied Spaces', 'Free Spaces']

    # Create the initial pie chart
    update_pie_chart(pie_ax, data, labels)

    # Embed the figure in a tkinter canvas
    canvas = FigureCanvasTkAgg(fig, master=analytics_frame)
    canvas.draw()
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(padx=20, pady=20)  # Remove fill and expand to control the size manually

    # Set the width and height of the canvas
    canvas_widget.config(width=400, height=300, bg="red")  # Adjust width and height as needed

    analytics_lb = tk.Label(analytics_frame, text="Virtual View", font=('arial', 15, 'bold'), bg="black", fg='white')
    analytics_lb.pack(pady=20)

    # Add a Canvas for the virtual view
    virtual_view_canvas = tk.Canvas(analytics_frame, bg='#DEDDE3', width=400, height=300)
    virtual_view_canvas.pack(padx=20, pady=10, side=tk.BOTTOM)  # Adjust position as needed

    # Start showing video with the pie chart updates
    if cap:
        show_video(cap, video_canvas, loaded_coords, pie_ax, labels)

    update_virtual_view(virtual_view_canvas, loaded_coords)

    dashboard_frame.pack(fill=tk.BOTH, expand=True)

    


# # Main function to initialize and run the tkinter application
# def main():
#     root = tk.Tk()
#     root.title('Owcular Parking Lot Management System')

#     # Make the window fullscreen
#     root.state('zoomed')

#     main_frame = tk.Frame(root)
#     main_frame.pack(fill=tk.BOTH, expand=True)

#     dashboard(main_frame, root)

#     def on_closing():
#         global cap
#         if cap:
#             cap.release()
#         root.destroy()  # Close the Tkinter window
#         root.quit()  # Ensure the Tkinter main loop stops

#     root.protocol("WM_DELETE_WINDOW", on_closing)

#     root.mainloop()

# # if __name__ == '__main__':
# #     main()

# Main function to initialize and run the tkinter application
def main():
    root = tk.Tk()
    root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth() - 300, root.winfo_screenheight() - 100))
    root.title('Owcular Parking Lot Management System')

    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True)

    dashboard(main_frame, root)

    root.mainloop()

if __name__ == "__main__":
    main()