from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk
import json
import cv2
import os
import uuid  # Import the uuid module
from datetime import datetime
from PIL import Image
from PIL import Image, ImageOps



def annotation(main_frame, root):

    global annotation_canvas, annotation_frame, annotation_history, commentator, next_id, polygon_points, image_loaded
    image_loaded = False
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

    def load_annotations():
        # Check if the 'coordinates' directory exists; create if it doesn't
        coordinates_dir = "local/coordinates"
        if not os.path.exists(coordinates_dir):
            os.makedirs(coordinates_dir)

        # Ask user to select a JSON file from the 'coordinates' directory
        file_path = filedialog.askopenfilename(initialdir=coordinates_dir, filetypes=[("JSON files", "*.json")])
        if not file_path:
            return

        try:
            with open(file_path, "r") as file:
                all_annotations = json.load(file)

            # Clear existing annotations
            annotation_canvas.delete("all")
            annotation_history.clear()
            global next_id
            next_id = 1  # Reset the next ID

            # Check if there is an image loaded
            if annotation_canvas.image:
                # Show the existing image
                annotation_canvas.create_image(0, 0, anchor=NW, image=annotation_canvas.image)

            # Load annotations onto the canvas
            for annotation in all_annotations:
                points = annotation["points"]
                poly_id = annotation_canvas.create_polygon(points, outline="green", width=3, fill="")
                text_x = sum([point[0] for point in points]) / len(points)
                text_y = sum([point[1] for point in points]) / len(points)
                text_id = annotation_canvas.create_text(text_x, text_y, text=str(next_id), fill="black")
                annotation_history.append((poly_id, next_id, text_id, points))
                next_id += 1

            update_commentator("Annotations loaded successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load annotations: {str(e)}")
            update_commentator("Failed to load annotations.")

    def save_all_annotations():
        global annotation_canvas

        if not hasattr(annotation_canvas, "image_path") or not annotation_canvas.image_path:
            messagebox.showerror("Error", "No image data to save annotations.")
            return

        # Get the original image path and filename
        img_path = annotation_canvas.image_path
        img_name = os.path.basename(img_path)

        # Generate unique filename using UUID and current datetime
        unique_id = uuid.uuid4().hex[:8]  # Generate UUID
        current_time = datetime.now().strftime("%Y_%m_%d___%H_%M_%S")  # Current date and time
        img_name_with_time = f"{img_name}_{current_time}_{unique_id}.jpg"
        # img_name_with_time = "yooy"

        # Save the image to the 'uploads' directory
        upload_dir = "local/recent_uploads"
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)

        img_dest_path = os.path.join(upload_dir, img_name_with_time)
        try:
            with Image.open(img_path) as pil_image:
                # Convert RGBA image to RGB if it has an alpha channel
                if pil_image.mode == 'RGBA':
                    pil_image = pil_image.convert('RGB')
                
                # Save the image
                pil_image.save(img_dest_path)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save image: {str(e)}")
            return

        # Save annotations
        all_annotations = []
        for poly_id, poly_id_num, text_id, points in annotation_history:
            coords = annotation_canvas.coords(poly_id)
            all_annotations.append({
                "id": poly_id_num,
                "points": points
            })

        coordinates_dir = "local/coordinates"
        if not os.path.exists(coordinates_dir):
            os.makedirs(coordinates_dir)
        coordinates_file = filedialog.asksaveasfilename(
            initialdir=coordinates_dir,
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")],
            initialfile=f"{img_name}_{current_time}_{unique_id}.json",
            title="Save Annotations"
        )

        if coordinates_file:
            # Save the annotations to the selected file
            with open(coordinates_file, "w") as file:
                json.dump(all_annotations, file, indent=4)
            
            update_commentator("Annotations and image saved.")
            messagebox.showinfo("Annotations Saved", "Annotations and image have been saved successfully.")
        else:
            messagebox.showwarning("Save Cancelled", "No file was selected. Annotations were not saved.")


    def clear_annotations(event=None):
        global next_id
        for poly_id, _, text_id, points in annotation_history:
            annotation_canvas.delete(poly_id)  # Delete the polygon
            annotation_canvas.delete(text_id)  # Delete the corresponding text
            for point in points:
                x, y = point
                # Find all items within a small bounding box around the point
                item_ids = annotation_canvas.find_overlapping(x-3, y-3, x+3, y+3)
                for item_id in item_ids:
                    item_type = annotation_canvas.type(item_id)
                    if item_type == 'oval':  # Check if it's a point marker
                        annotation_canvas.delete(item_id)  # Delete the point marker
        annotation_history.clear()  # Clear the annotation history
        next_id = 1  # Reset the next ID
        update_commentator("Annotations cleared.")



    # Bind 'c' key to clear_annotations function
    root.bind('c', clear_annotations)

    def start_draw(event):
        global polygon_points, next_id
        polygon_points.append((event.x, event.y))
        annotation_canvas.create_oval(event.x-2, event.y-2, event.x+2, event.y+2, fill='red')

        if len(polygon_points) == 4:  # Change this condition according to your polygon requirements
            poly_id = annotation_canvas.create_polygon(polygon_points, outline="green", width=3, fill="")
            text_x = sum([point[0] for point in polygon_points]) / len(polygon_points)
            text_y = sum([point[1] for point in polygon_points]) / len(polygon_points)
            text_id = annotation_canvas.create_text(text_x, text_y, text=str(next_id), fill="black")
            annotation_history.append((poly_id, next_id, text_id, polygon_points.copy()))
            update_commentator(f"Polygon {next_id} drawn.")
            next_id += 1
            polygon_points = []  # Clear polygon_points after drawing the polygon


    def renumber_annotations():
        for i, (poly_id, _, text_id, points) in enumerate(annotation_history):
            new_id = i + 1
            annotation_canvas.itemconfig(text_id, text=str(new_id))
            annotation_history[i] = (poly_id, new_id, text_id, points)

    def undo(event=None):
        global next_id
        if annotation_history:  # Check if there are annotations to undo
            last_poly_id, last_poly_num, last_text_id, points = annotation_history.pop()  # Remove the last annotation from history
            annotation_canvas.delete(last_poly_id)  # Remove the last polygon from the canvas
            annotation_canvas.delete(last_text_id)  # Remove the corresponding text label
            for point in points:
                x, y = point
                # Find all items within a small bounding box around the point
                item_ids = annotation_canvas.find_overlapping(x-3, y-3, x+3, y+3)
                for item_id in item_ids:
                    item_type = annotation_canvas.type(item_id)
                    if item_type == 'oval':  # Check if it's a point marker
                        annotation_canvas.delete(item_id)  # Delete the point marker
            next_id -= 1
            renumber_annotations()
            update_commentator(f"Annotation {last_poly_num} undone.")


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
        global annotation_canvas
        img = Image.open(file_path)
        img = img.resize((800, 480))  # Resize the image to match the canvas size
        photo_img = ImageTk.PhotoImage(img)  # Convert to PhotoImage

        annotation_canvas.create_image(0, 0, anchor=NW, image=photo_img)
        annotation_canvas.image = photo_img  # Store PhotoImage in canvas
        annotation_canvas.image_path = file_path  # Store the image file path

        # Bind mouse events to the canvas
        annotation_canvas.bind("<ButtonPress-1>", start_draw)

        update_commentator("Image loaded successfully.")

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
        # Check if the 'uploads' directory exists; create if it doesn't
        uploads_dir = "local/recent_uploads"
        if not os.path.exists(uploads_dir):
            os.makedirs(uploads_dir)

        # Check if the 'uploads' directory is empty
        if not os.listdir(uploads_dir):  # Check if directory is empty
            file_path = filedialog.askopenfilename(initialdir="~/Pictures", filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
        else:
            file_path = filedialog.askopenfilename(initialdir=uploads_dir, filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])

        if not file_path:  # Check if a file was selected
            return
        
        # Check if the selected file has a valid image extension
        valid_extensions = ('.jpg', '.jpeg', '.png')
        if not file_path.lower().endswith(valid_extensions):
            messagebox.showerror("Error", "Selected file is not a valid image file (JPEG, JPG, PNG).")
            return
        
        # Proceed to show the image if it passed the validation
        show_image(file_path)




    upload_instruction = Label(annotation_frame, text="Annotation Instructions", font=('arial', 15, 'bold'), fg='black')
    upload_instruction_text = Label(annotation_frame, text=".1. Upload or capture a visible image of your parking lot.\n 2. Click on 4 consecutive points to mark out parking spaces.\n3. You can load previous annotations for editing.\n4. Save annotations to be used for real-time detection.", font=('arial', 10, ''), bg='#D5B895', fg='black')
    upload_instruction.place(relx=0.2, rely=0.08, anchor='center')
    upload_instruction_text.place(relx=0.2, rely=0.15, anchor='center')

    annotate_instruction = Label(annotation_frame, text="Canvas commands", font=('arial', 15, 'bold'), fg='black')
    annotate_instruction.place(relx=0.8, rely=0.08, anchor='center')
    annotate_instruction_text = Label(annotation_frame, text="Mouse Right Click :- Add point for polygon\n'CTRL+Z' :- Undo\n'C' key :- Clear Annotations", font=('arial', 10, ''), bg='#D5B895', fg='black')
    annotate_instruction_text.place(relx=0.8, rely=0.14, anchor='center')

    take_picture_btn = Button(annotation_frame, text="Open Webcam", command=open_webcam, width=12)
    upload_file_btn = Button(annotation_frame, text="Upload File", 
                             width=12,
                             command= upload_image)

    take_picture_btn.place(relx=0.45, rely=0.15, anchor='center')    
    upload_file_btn.place(relx=0.55, rely=0.15, anchor='center')

    commentator = Label(annotation_frame, width=75, bg='yellow', text="No image data to annotate", fg='black')
    commentator.place(relx=0.5, rely=0.25, anchor='center')

    load_btn = Button(annotation_frame, text="Load Annotations", command=load_annotations, width=15)
    load_btn.place(relx=0.88, rely=0.55)

    save_btn = Button(annotation_frame, text="Save Annotations", command=save_all_annotations, width=15)
    save_btn.place(relx=0.88, rely=0.6)

    annotation_frame.pack(fill=BOTH, expand=True)

# Main function to initialize and run the tkinter application
def main():
    root = Tk()
    root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth() - 300, root.winfo_screenheight() - 100))
    root.title('Owcular Parking Lot Management System')

    main_frame = Frame(root)
    main_frame.pack(fill=BOTH, expand=True)

    annotation(main_frame, root)

    root.mainloop()

if __name__ == "__main__":
    main()