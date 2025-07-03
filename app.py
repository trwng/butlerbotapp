import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from PIL import Image, ImageTk
from PIL import ImageDraw, ImageOps
import cv2

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("ButlerBot")
        self.root.geometry("1000x600")
        self.root.configure(bg="white")
        #custom_font = tkFont.Font(family="Arial", size=14, weight="bold", slant="italic")

        self.cap = cv2.VideoCapture(0)

        # Left sidebar
        sidebar = tk.Frame(root, bg="white", width=200)
        sidebar.pack(side="left", fill="y", pady=51, padx=20)

        self.title_label = tk.Label(self.root, text="ButlerBot", bg="white", font=("Inter-Normal", 13, "bold"))
        self.title_label.place(x=10, y=10)

        
        for option in ["Camera", "Sensor Data", "Music"]:
            b = tk.Button(sidebar, text=option, bg="white", font=("Inter Regular", 10), bd=0, anchor="w", padx=20)
            b.pack(fill="x", pady=3)

        tk.Label(sidebar, bg="white").pack(expand=True, fill="both")
        tk.Button(sidebar, text="Settings", bg="white", bd=0, anchor="w", padx=20).pack(side="bottom", pady=10)


        topbar = tk.Frame(root, bg="white", height=10)
        topbar.pack(side="top", fill="x", padx=140, pady=20)

        button_style = {
            "bg": "white",
            "relief": "flat",
            "borderwidth": 0,
            "highlightthickness": 0
        }

        for t in ["Camera", "Tab", "Tab"]:
            tk.Button(topbar, text=t, **button_style, font=("Inter Regular", 10)).pack(side="left", padx=1, pady=5)

        tk.Button(topbar, text="Shutdown", bg="#8B0000", fg="white",
                relief="flat", borderwidth=0, highlightthickness=0).pack(side="right", padx=5, pady=5)




        self.canvas = tk.Label(root, bg="white")
        self.canvas.pack(expand=True, fill="both", padx=140, pady=10)

        self.update_frame()

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Get label (canvas) dimensions
            label_width = self.canvas.winfo_width()
            label_height = self.canvas.winfo_height()

            if label_width > 1 and label_height > 1:
                # Resize the frame to match label size
                frame = cv2.resize(frame, (label_width, label_height))
                img = Image.fromarray(frame)

                # Rounded corners mask
                radius = 25
                mask = Image.new("L", img.size, 0)
                draw = ImageDraw.Draw(mask)
                draw.rounded_rectangle((0, 0, img.size[0], img.size[1]), radius=radius, fill=255)

                # Background color matches the window (white)
                background = Image.new("RGB", img.size, color="white")
                background.paste(img, mask=mask)

                imgtk = ImageTk.PhotoImage(image=background)
                self.canvas.imgtk = imgtk
                self.canvas.configure(image=imgtk)

        self.root.after(20, self.update_frame)



    def on_close(self):
        self.cap.release()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
