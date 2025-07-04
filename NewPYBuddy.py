import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import cv2
from PIL import Image, ImageTk
import time
import requests
import json
import pyttsx3

APP_ID = "d1b56ee3"
API_KEY = "1952289073a5f8e6f532f465abf99951"

HEADERS = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY
}

SEARCH_URL = "https://trackapi.nutritionix.com/v2/search/instant"
ITEM_URL = "https://trackapi.nutritionix.com/v2/search/item"


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
        self.nutrition_tab = tk.Frame(self.tabs, bg="white")
        self.music_tab = tk.Frame(self.tabs, bg="white")
        self.sensor_tab = tk.Frame(self.tabs, bg="white")

        self.tabs.add(self.camera_tab, text="Camera")
        self.tabs.add(self.nutrition_tab, text="Nutrition")
        self.tabs.add(self.music_tab, text="Music")
        self.tabs.add(self.sensor_tab, text="Sensor Data")

        # Left side (input and search button)
        left_frame = tk.Frame(self.nutrition_tab, bg="white", padx=20, pady=20)
        left_frame.pack(side="left", fill="y")

        tk.Label(left_frame, text="Enter branded food name:", bg="white", font=("Arial", 12)).pack(anchor="w")
        self.food_entry = tk.Entry(left_frame, font=("Arial", 12), width=30)
        self.food_entry.pack(pady=5, anchor="w")

        search_btn = tk.Button(left_frame, text="Search", command=self.fetch_nutrition, font=("Arial", 12))
        search_btn.pack(anchor="w")

        # Right side (facts window)
        self.facts_window = tk.Frame(self.nutrition_tab, bg="black")
        self.facts_window.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        self.fact_labels = {}
        for fact in ["Brand", "Serving", "Calories", "Total Fat", "Sugar", "Cholesterol", "Sodium", "Carbohydrates", "Protein"]:
            label = tk.Label(self.facts_window, text=f"{fact}: N/A", bg="black", fg="white", font=("Arial", 12), anchor="w")
            label.pack(anchor="w", pady=5, padx=10)
            self.fact_labels[fact] = label

        self.tabs.pack(fill="both", expand=True, padx=20, pady=10)

        shutdown_btn = tk.Button(self.main_area, text="Shutdown", bg="#8B2E2E", fg="white",
                         font=("Arial", 12, "bold"), command=self.destroy)
        shutdown_btn.place(relx=0.96, rely=0.04, anchor="ne")

    def fetch_nutrition(self):
        food_input = self.food_entry.get()
        if not food_input:
            messagebox.showwarning("Input Error", "Please enter a food name.")
            return

        try:
            search_params = {
                "query": food_input,
                "branded": True
            }
            search_response = requests.get(SEARCH_URL, headers=HEADERS, params=search_params)
            search_response.raise_for_status()
            search_result = search_response.json()

            if not search_result['branded']:
                messagebox.showinfo("Not Found", f"No branded item found for '{food_input}'.")
                return

            branded_item = search_result['branded'][0]
            item_id = branded_item['nix_item_id']

            item_response = requests.get(ITEM_URL, headers=HEADERS, params={"nix_item_id": item_id})
            item_response.raise_for_status()
            item = item_response.json()['foods'][0]

            self.fact_labels["Brand"].config(text=f"Brand: {item.get('brand_name', 'N/A')}")
            self.fact_labels["Serving"].config(text=f"Serving: {item['serving_qty']} {item['serving_unit']} ({item.get('serving_weight_grams', 'N/A')} g)")
            self.fact_labels["Calories"].config(text=f"Calories: {item.get('nf_calories', 'N/A')} kcal")
            self.fact_labels["Total Fat"].config(text=f"Total Fat: {item.get('nf_total_fat', 'N/A')} g")
            self.fact_labels["Sugar"].config(text=f"Sugar: {item.get('nf_sugars', 'N/A')} g")
            self.fact_labels["Cholesterol"].config(text=f"Cholesterol: {item.get('nf_cholesterol', 'N/A')} mg")
            self.fact_labels["Sodium"].config(text=f"Sodium: {item.get('nf_sodium', 'N/A')} mg")
            self.fact_labels["Carbohydrates"].config(text=f"Carbohydrates: {item.get('nf_total_carbohydrate', 'N/A')} g")
            self.fact_labels["Protein"].config(text=f"Protein: {item.get('nf_protein', 'N/A')} g")

        except requests.exceptions.RequestException as e:
            messagebox.showerror("Network Error", str(e))
        except (KeyError, IndexError) as e:
            messagebox.showerror("Data Error", "Unexpected response or missing data.")

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






