from tkinter import *
import ttkbootstrap as ttk
from texts import *

from frames.diet_optimizer import DietOptimizerPage

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("CMSC 150 Project")
        self.root.geometry("880x620")
        # self.root.geometry("780x270")
    
        self.frames = []
        self.initialize_frames()
    
    def initialize_frames(self):
        self.main_frame = self.generate_main_frame()
        self.main_frame.pack()

        self.generate_project_details()
        self.generate_diet_solver_content()

        self.diet_optimizer_frame = DietOptimizerPage(self.root, self.send_to, self.main_frame)

        self.frames.append(self.main_frame)
        self.frames.append(self.diet_optimizer_frame)
        
    def generate_main_frame(self):
        main_frame = ttk.Frame(self.root)
        return main_frame
    
    def generate_project_details(self):
        self.project_frame = ttk.Frame(self.main_frame)

        project_title_label = ttk.Label(self.project_frame, text=project_title, font=("Arial Black", 28))
        project_title_label.pack(side="top", anchor="w", pady=15)

        self.project_frame.pack(padx=130, pady=10, fill="both", expand=True)

    def generate_diet_solver_content(self):
        self.diet_solver_content_frame = ttk.Frame(self.main_frame)

        diet_solver_description_label = ttk.Label(self.diet_solver_content_frame, text=diet_solver_description, font=("Bahnschrift Light", 11), wraplength=500, justify="left")
        diet_solver_description_label.pack(side="top", anchor="w")

        diet_solver_button = ttk.Button(self.diet_solver_content_frame, text=diet_solver_button_text, bootstyle="outline.light", command=lambda: self.send_to(self.diet_optimizer_frame))
        diet_solver_button.pack(side="top", anchor="w", pady=10,)

        self.diet_solver_content_frame.pack(padx=130, pady=10, fill="both", expand=True)

    def send_to(self, page_to_show):
        for frame in self.frames:
            if frame == page_to_show:
                page_to_show.pack()
            else:
                frame.pack_forget()