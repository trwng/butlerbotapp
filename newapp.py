import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import cv2
from PIL import Image, ImageTk

class ButlerBotApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ButlerBot")
        self.geometry("1000x700")
        self.configure(bg="white")

        self.sidebar = tk.Frame(self, bg="white", width=200)
        self.sidebar.pack(side="left", fill="y")

        self.main_area = tk.Frame(self, bg="white")
        self.main_area.pack(side="right", fill="both", expand=True)

        self.init_sidebar()
        self.init_main_area()
        self.show_camera()

    def init_sidebar(self):
        title = tk.Label(self.sidebar, text="ButlerBot", font=("Arial", 20, "bold"), bg="white", fg="black", anchor="w")
        title.pack(pady=(20, 15), padx=10, anchor="w")

        self.menu_buttons = {}
        for text, command in [
            ("Camera", self.show_camera),
            ("Sensor Data", self.show_sensor_data),
            ("Music", self.show_music)
        ]:
            btn = tk.Button(self.sidebar, text=text, font=("Arial", 14),
                bg="white", fg="black", bd=0, relief="flat", anchor="w",
                highlightthickness=0, highlightbackground="white", highlightcolor="white",
                command=command)

            btn.pack(fill="x", pady=2, padx=10)
            self.menu_buttons[text] = btn

        tk.Label(self.sidebar, text="", bg="white").pack(expand=True, fill="y")
        tk.Button(self.sidebar, text="Settings", font=("Arial", 12),
          bg="white", bd=0,
          highlightthickness=0, highlightbackground="white", highlightcolor="white"
          ).pack(side="bottom", pady=8)

    def init_main_area(self):
        style = ttk.Style()
        style.theme_use("default")
        style.configure("TNotebook", background="white", borderwidth=0)
        style.configure("TNotebook.Tab", background="white", foreground="black")
        style.map("TNotebook.Tab", background=[("selected", "white")])

        self.tabs = ttk.Notebook(self.main_area)
        self.camera_tab = tk.Frame(self.tabs, bg="white")
        self.sensor_tab = tk.Frame(self.tabs, bg="white")
        self.music_tab = tk.Frame(self.tabs, bg="white")

        self.tabs.add(self.camera_tab, text="Camera")
        self.tabs.add(self.sensor_tab, text="Sensor Data")
        self.tabs.add(self.music_tab, text="Music")
        self.tabs.pack(fill="both", expand=True, padx=20, pady=10)

        shutdown_btn = tk.Button(self.main_area, text="Shutdown", bg="#8B2E2E", fg="white",
                         font=("Arial", 12, "bold"), command=self.destroy,
                         highlightthickness=0, highlightbackground="#8B2E2E", highlightcolor="#8B2E2E")
        shutdown_btn.place(relx=0.96, rely=0.04, anchor="ne")

    def show_camera(self):
        self.tabs.select(self.camera_tab)
        for widget in self.camera_tab.winfo_children():
            widget.destroy()

        cam_frame = tk.Frame(self.camera_tab, bg="white", width=640, height=480)
        cam_frame.pack(pady=30)
        cam_frame.pack_propagate(False)

        self.cam_label = tk.Label(cam_frame, bg="white")
        self.cam_label.pack()

        snap_btn = tk.Button(self.camera_tab, text="📷", font=("Arial", 16), command=self.capture_image, bg="white", fg="black")
        snap_btn.pack(pady=10)

        self.cap = cv2.VideoCapture(0)
        self.update_camera()

    def update_camera(self):
        if hasattr(self, "cap") and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(cv2image)
                img = img.resize((640, 480))
                imgtk = ImageTk.PhotoImage(image=img)
                self.cam_label.imgtk = imgtk
                self.cam_label.configure(image=imgtk)
            self.after(20, self.update_camera)

    def capture_image(self):
        if hasattr(self, "cap") and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                cv2.imwrite("captured_image.png", frame)
                messagebox.showinfo("Image Captured", "Captured and saved as captured_image.png!")

    def show_sensor_data(self):
        self.tabs.select(self.sensor_tab)
        for widget in self.sensor_tab.winfo_children():
            widget.destroy()
        tk.Label(self.sensor_tab, text="Sensor Data", bg="white", fg="black", font=("Arial", 16)).pack(pady=40)

    def show_music(self):
        self.tabs.select(self.music_tab)
        for widget in self.music_tab.winfo_children():
            widget.destroy()
        tk.Label(self.music_tab, text="Music", bg="white", fg="black", font=("Arial", 16)).pack(pady=40)

    def on_closing(self):
        if hasattr(self, "cap") and self.cap.isOpened():
            self.cap.release()
        self.destroy()

if __name__ == "__main__":
    app = ButlerBotApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
