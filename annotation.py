from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk
import json
import cv2
import os

def create_annotation_page(main_frame, root):
    global annotation_canvas, annotation_frame, annotation_history, commentator, next_id, polygon_points
    annotation_frame = Frame(main_frame)
    annotation_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

    annotation_frame.config(bd=2, relief="solid")  # Adding border to annotation_frame

    annotation_canvas = Canvas(annotation_frame, width=800, height=480, bg="white", bd=2, relief="solid")
    annotation_canvas.place(relx=0.5, rely=0.6, anchor='center')

    annotation_lb = Label(annotation_frame, text="Annotator", font=('arial', 20, 'bold'), bg='white', fg='black')
    annotation_lb.place(relx=0.5, rely=0.05, anchor='center')

    polygon_points = []
    next_id = 1  # Initialize the next ID

    annotation_history = []  # List to keep track of annotations

    def update_commentator(message):
        commentator.config(text=message)

    def save_all_annotations():
        all_annotations = []
        for poly_id, poly_id_num, text_id, points in annotation_history:
            coords = annotation_canvas.coords(poly_id)
            all_annotations.append({
                "id": poly_id_num,
                "points": points
            })
        
        with open("coordinates.json", "w") as file:
            json.dump(all_annotations, file, indent=4)
        
        update_commentator("All annotations saved.")

    def start_draw(event):
        global polygon_points, next_id
        polygon_points.append((event.x, event.y))
        annotation_canvas.create_oval(event.x-2, event.y-2, event.x+2, event.y+2, fill='red')

        if len(polygon_points) == 4:
            poly_id = annotation_canvas.create_polygon(polygon_points, outline="green", width=3, fill="")
            text_x = sum([point[0] for point in polygon_points]) / len(polygon_points)
            text_y = sum([point[1] for point in polygon_points]) / len(polygon_points)
            text_id = annotation_canvas.create_text(text_x, text_y, text=str(next_id), fill="black")
            annotation_history.append((poly_id, next_id, text_id, polygon_points.copy()))
            update_commentator(f"Polygon {next_id} drawn.")
            next_id += 1
            polygon_points = []

    def renumber_annotations():
        for i, (poly_id, _, text_id, points) in enumerate(annotation_history):
            new_id = i + 1
            annotation_canvas.itemconfig(text_id, text=str(new_id))
            annotation_history[i] = (poly_id, new_id, text_id, points)

    def undo(event=None):
        global next_id
        if annotation_history:  # Check if there are annotations to undo
            last_poly_id, last_poly_num, last_text_id, _ = annotation_history.pop()  # Remove the last annotation and text ID from the history
            annotation_canvas.delete(last_poly_id)  # Remove the last annotation from the canvas
            annotation_canvas.delete(last_text_id)  # Remove the corresponding text from the canvas
            next_id -= 1
            renumber_annotations()
            update_commentator(f"Annotation {last_poly_num} undone.")
            print(annotation_history)

    # Bind Ctrl+Z to the undo function
    root.bind('<Control-z>', undo)  # Bind the undo function to the root window

    def delete_annotation(event):
        global next_id
        # Find the closest annotation to the right-click position
        clicked_item = annotation_canvas.find_closest(event.x, event.y)
        if clicked_item:  # If an item was found
            for item in annotation_history:
                if item[0] == clicked_item[0] or item[2] == clicked_item[0]:
                    annotation_canvas.delete(item[0])  # Delete the clicked annotation
                    annotation_canvas.delete(item[2])  # Delete the corresponding text
                    annotation_history.remove(item)
                    next_id -= 1
                    renumber_annotations()
                    update_commentator(f"Annotation {item[1]} deleted.")
                    break

    # Bind the right mouse click to remove an annotation
    annotation_canvas.bind("<Button-3>", delete_annotation)

    def show_image(file_path):
        global start_x, start_y, annotation_canvas
        img = Image.open(file_path)
        img = img.resize((800, 480))  # Resize the image to match the window size
        photo_img = ImageTk.PhotoImage(img)  # Convert to PhotoImage

        annotation_canvas.create_image(0, 0, anchor=NW, image=photo_img)
        annotation_canvas.image = photo_img  # Prevent garbage collection

        # Bind mouse events to the canvas
        annotation_canvas.bind("<ButtonPress-1>", start_draw)

    def open_webcam():
        def capture_image():
            ret, frame = cap.read()
            if ret:
                img_name = "captured_image.jpg"
                cv2.imwrite(img_name, frame)
                show_image(img_name)
                cap.release()
                webcam_window.destroy()
            else:
                update_commentator("Error: Could not capture image.")

        webcam_window = Toplevel(main_frame)
        webcam_window.title("Webcam Capture")
        webcam_frame = Frame(webcam_window, width=800, height=480)
        webcam_frame.pack()

        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            update_commentator("Error: Could not open webcam.")
            webcam_window.destroy()
            return

        lmain = Label(webcam_frame)
        lmain.pack()

        def show_frame():
            _, frame = cap.read()
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            lmain.imgtk = imgtk
            lmain.configure(image=imgtk)
            lmain.after(10, show_frame)

        show_frame()

        capture_btn = Button(webcam_window, text="Capture", command=capture_image)
        capture_btn.pack()

        webcam_window.protocol("WM_DELETE_WINDOW", lambda: [cap.release(), webcam_window.destroy()])

    def upload_image():
        file_path = filedialog.askopenfilename()
        if not file_path:  # Check if a file was selected
            return
        show_image(file_path)

    take_picture_btn = Button(annotation_frame, text="Open Webcam", command=open_webcam, width=12)
    upload_file_btn = Button(annotation_frame, text="Upload File", 
                             width=12,
                             command= upload_image)

    take_picture_btn.place(relx=0.45, rely=0.15, anchor='center')    
    upload_file_btn.place(relx=0.55, rely=0.15, anchor='center')

    commentator = Label(annotation_frame, width=75, bg='yellow', text="No image data to annotate", fg='black')
    commentator.place(relx=0.5, rely=0.25, anchor='center')

    save_btn = Button(annotation_frame, text="Save Annotations", command=save_all_annotations, width=15)
    save_btn.place(relx=0.85, rely=0.3)

    annotation_frame.pack(fill=BOTH, expand=True)
