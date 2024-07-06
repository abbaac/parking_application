from tkinter import *
import cv2 
from PIL import Image, ImageTk
import os

class WebcamApp:
    def __init__(self, window):
        self.window = window
        self.window.title('Webcam App')

        self.video_capture = cv2.VideoCapture(0)
        self.current_image = None

        self.canvas = Canvas(window, width=640, height=480)
        self.canvas.pack() 

        self.download_button = Button(window, text="Capture", command=self.download_image)
        self.download_button.pack()

        self.update_webcam()

    def update_webcam(self):
        ret, frame = self.video_capture.read()
        if ret:
            self.current_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            self.photo = ImageTk.PhotoImage(self.current_image)
            self.canvas.create_image(0, 0, image=self.photo, anchor=NW)
        self.window.after(10, self.update_webcam)

    def download_image(self):
        if self.current_image is not None:
            folder_path = os.path.join(os.getcwd(), "captures")
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            file_path = os.path.join(folder_path, "webcam_capture.png")
            self.current_image.save(file_path)
            # os.startfile(file_path)

            # self.current_image.save(file_path)
            # os.startfile(file_path)

root = Tk()

app = WebcamApp(root)

root.mainloop()

    
