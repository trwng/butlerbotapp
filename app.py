import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cv2

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("ButlerBot")
        self.root.geometry("1000x600")
        self.root.configure(bg="white")

        self.cap = cv2.VideoCapture(0)

        # Left sidebar
        sidebar = tk.Frame(root, bg="white", width=200)
        sidebar.pack(side="left", fill="y")

        tk.Label(sidebar, text="ButlerBot", bg="white", font=("Arial", 16, "bold")).pack(pady=10)
        
        for option in ["Camera", "Sensor Data", "Music"]:
            b = tk.Button(sidebar, text=option, bg="white", bd=0, anchor="w", padx=20)
            b.pack(fill="x", pady=5)

        # Spacer
        tk.Label(sidebar, bg="white").pack(expand=True, fill="both")
        tk.Button(sidebar, text="Settings", bg="white", bd=0, anchor="w", padx=20).pack(side="bottom", pady=10)

        # Top bar
        topbar = tk.Frame(root, bg="white", height=40)
        topbar.pack(side="top", fill="x")

        for t in ["Camera", "Tab", "Tab"]:
            tk.Button(topbar, text=t, bg="white").pack(side="left", padx=5, pady=5)

        tk.Button(topbar, text="Shutdown", bg="#8B0000", fg="white").pack(side="right", padx=5, pady=5)

        # Main camera area
        self.canvas = tk.Label(root, bg="black")
        self.canvas.pack(expand=True, fill="both", padx=10, pady=10)

        self.update_frame()

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (800, 500))
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
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
