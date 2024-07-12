from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk
import json
import cv2
import os
import numpy as np

def create_annotation_page(main_frame, root):
    global annotation_canvas, annotation_frame, annotation_history, commentator, next_id, uploaded_image
    annotation_frame = Frame(main_frame)
    annotation_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

    annotation_frame.config(bd=2, relief="solid")  # Adding border to annotation_frame

    annotation_canvas = Canvas(annotation_frame, width=800, height=480, bg="white")
    annotation_canvas.pack()

    annotation_lb = Label(annotation_frame, text="Annotator", font=('arial', 20, 'bold'), bg='white', fg='black')
    annotation_lb.place(relx=0.5, rely=0.05, anchor='center')

    start_x = None
    start_y = None
    end_x = None
    current_rectangle = None
    next_id = 1  # Initialize the next ID

    annotation_history = []  # List to keep track of annotations
    uploaded_image = None  # Global variable to keep the image in memory

    def update_commentator(message):
        commentator.config(text=message)

    def is_overlapping(new_coords):
        for rect_id, _, _ in annotation_history:
            existing_coords = annotation_canvas.coords(rect_id)
            if (new_coords[2] > existing_coords[0] and new_coords[0] < existing_coords[2] and
                new_coords[3] > existing_coords[1] and new_coords[1] < existing_coords[3]):
                return True
        return False

    def save_all_annotations():
        all_annotations = []
        for rect_id, rect_id_num, text_id in annotation_history:
            coords = annotation_canvas.coords(rect_id)
            all_annotations.append({
                "id": rect_id_num,
                "top_left": (coords[0], coords[1]),
                "bottom_right": (coords[2], coords[3])
            })
        
        with open("coordinates.json", "w") as file:
            json.dump(all_annotations, file, indent=4)
        
        update_commentator("All annotations saved.")

    def start_draw(event):
        global start_x, start_y, next_id
        start_x = event.x
        start_y = event.y
        # Fetch the width and height from the entry boxes, use default values if empty
        try:
            fixed_width = int(width_entry.get())
        except ValueError:
            fixed_width = 100  # Default width if entry is not a number
        try:
            fixed_height = int(height_entry.get())
        except ValueError:
            fixed_height = 50  # Default height if entry is not a number
        
        new_coords = (start_x, start_y, start_x + fixed_width, start_y + fixed_height)
        
        if not is_overlapping(new_coords):
            annotation_id = annotation_canvas.create_rectangle(new_coords, outline="green", width=3)
            text_id = annotation_canvas.create_text(start_x + fixed_width / 2, start_y + fixed_height / 2, text=str(next_id), fill="black")
            annotation_history.append((annotation_id, next_id, text_id))  # Add this annotation and text ID to the history
            update_commentator(f"Parking space {next_id} drawn from ({start_x}, {start_y}) to ({start_x + fixed_width}, {start_y + fixed_height})")
            next_id += 1
        else:
            update_commentator("This annotation overlaps with an existing one.")

    def renumber_annotations():
        for i, (rect_id, _, text_id) in enumerate(annotation_history):
            new_id = i + 1
            annotation_canvas.itemconfig(text_id, text=str(new_id))
            annotation_history[i] = (rect_id, new_id, text_id)

    def undo(event=None):
        global next_id
        if annotation_history:  # Check if there are annotations to undo
            last_annotation_id, last_annotation_num, last_text_id = annotation_history.pop()  # Remove the last annotation and text ID from the history
            annotation_canvas.delete(last_annotation_id)  # Remove the last annotation from the canvas
            annotation_canvas.delete(last_text_id)  # Remove the corresponding text from the canvas
            next_id -= 1
            renumber_annotations()
            update_commentator(f"Annotation {last_annotation_num} undone.")
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
        global start_x, start_y, annotation_canvas, uploaded_image
        img = Image.open(file_path)
        img = img.resize((800, 480))  # Resize the image to match the window size
        uploaded_image = ImageTk.PhotoImage(img)  # Convert to PhotoImage

        annotation_canvas.create_image(0, 0, anchor=NW, image=uploaded_image)
        annotation_canvas.image = img  # Store the PIL Image

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

    def detect_cars():
        update_commentator("Detecting cars...")
        # Load pre-trained YOLO model
        net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
        layer_names = net.getLayerNames()
        try:
            output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
        except TypeError:
            output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
        
        # Load image from canvas
        canvas_img = annotation_canvas.image
        if canvas_img is None:
            update_commentator("No image data to detect cars.")
            return
        
        # Convert PIL Image to OpenCV format
        img = np.array(canvas_img)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        
        height, width = img.shape[:2]
        
        # Create blob from image
        blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        net.setInput(blob)
        outs = net.forward(output_layers)
        
        class_ids = []
        confidences = []
        boxes = []
        
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.2 and class_id == 2:  # class_id 2 corresponds to 'car' in COCO dataset
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    boxes.append([x, y, w, h])
                    print([x,y,w,h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)
        
        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        
        if len(indexes) > 0:
            for i in indexes.flatten():
                x, y, w, h = boxes[i]
                new_coords = (x, y, x + w, y + h)
                if not is_overlapping(new_coords):
                    annotation_id = annotation_canvas.create_rectangle(new_coords, outline="green", width=3)
                    text_id = annotation_canvas.create_text(x + w / 2, y + h / 2, text=str(next_id), fill="black")
                    annotation_history.append((annotation_id, next_id, text_id))  # Add this annotation and text ID to the history
                    next_id += 1
        update_commentator("Car detection completed.")

    take_picture_btn = Button(annotation_frame, text="Open Webcam", command=open_webcam, width=12)
    upload_file_btn = Button(annotation_frame, text="Upload File", 
                             width=12,
                             command= upload_image)
    detect_cars_btn = Button(annotation_frame, text="Detect Cars", command=detect_cars, width=12)

    take_picture_btn.place(relx=0.35, rely=0.15, anchor='center')    
    upload_file_btn.place(relx=0.45, rely=0.15, anchor='center')
    detect_cars_btn.place(relx=0.55, rely=0.15, anchor='center')

    commentator = Label(annotation_frame, width=75, bg='yellow', text="No image data to annotate", fg='black')
    commentator.place(relx=0.5, rely=0.25, anchor='center')

    width_label = Label(annotation_frame, text="Width:", font=('arial', 12), bg='white')
    width_label.place(relx=0.85, rely=0.35)
    width_entry = Entry(annotation_frame, bd=2, width=4)
    width_entry.place(relx=0.9, rely=0.35)

    height_label = Label(annotation_frame, text="Height:", font=('arial', 12), bg='white')
    height_label.place(relx=0.85, rely=0.3)
    height_entry = Entry(annotation_frame, bd=2, width=4)
    height_entry.place(relx=0.9, rely=0.3)

    save_btn = Button(annotation_frame, text="Save Annotations", command=save_all_annotations, width=15)
    save_btn.place(relx=0.85, rely=0.4)

    annotation_frame.pack(fill=BOTH, expand=True)
