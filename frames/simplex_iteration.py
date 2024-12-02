from tkinter import *
import ttkbootstrap as ttk

from util.matrix_display_util import MatrixDisplay
from texts import *

class SimplexIteration(ttk.Frame):
    def __init__(self, root, simplex_iteration, selected_foods, optimized_solution_frame):
        super().__init__(root)
        self.simplex_iteration = simplex_iteration
        self.selected_foods = selected_foods
        self.optimized_solution_frame = optimized_solution_frame

        self.initialize_frames()

    def initialize_frames(self):
        self.simplex_iteration_details_frame = ttk.Frame(self)
        self.simplex_iteration_details_frame.pack(pady=10)

        self.functions_frame = ttk.Frame(self)
        self.functions_frame.pack(pady=10)

        self.matrix_display = None

        self.generate_simplex_iteration_details()
        self.generate_functions()

    def generate_simplex_iteration_details(self):
        simplex_iteration_title_label = ttk.Label(self.simplex_iteration_details_frame, text="Simplex Iterations", font=("Arial Black", 28))
        simplex_iteration_title_label.pack(pady=15, anchor="w")

        simplex_iteration_description_label = ttk.Label(self.simplex_iteration_details_frame, text=simplex_iteration_text, font=("Bahnschrift Light", 10), wraplength=800, justify="left")
        simplex_iteration_description_label.pack(pady=5, anchor="w")

    def generate_functions(self):
        back_button = ttk.Button(self.functions_frame, text="Back", bootstyle="light-outline", command=lambda: self.send_to_optimized_solution_frame())
        back_button.pack(side="left", anchor="w", padx=10)

        generate_iteration_button = ttk.Button(self.functions_frame, text="Generate Iteration", bootstyle="light-outline", command=lambda: self.generate_simplex_iteration())
        generate_iteration_button.pack(side="left", anchor="w", padx=5)

        self.iteration_count_spinbox = ttk.Spinbox(self.functions_frame, from_=0, to=len(self.simplex_iteration)-1, style="secondary.TSpinbox")
        self.iteration_count_spinbox.pack(side="left", anchor="w", padx=5)

        self.success_promt = ttk.Label(self, text="")
        self.success_promt.pack()

    def generate_simplex_iteration(self):
        self.success_promt.config(text="")

        if self.iteration_count_spinbox.get() == "":
            self.success_promt.config(text="Select iteration count first", bootstyle="danger")
            return

        try:
            iteration_count = int(self.iteration_count_spinbox.get())
        except:
            self.success_promt.config(text="Invalid iteration count", bootstyle="danger")
            return

        if int(self.iteration_count_spinbox.get()) > len(self.simplex_iteration)-1:
            self.success_promt.config(text="Invalid iteration count", bootstyle="danger")
            return

        if self.matrix_display is not None:
            self.matrix_display.destroy()

        if iteration_count == len(self.simplex_iteration)-1:
            self.matrix_display = MatrixDisplay(self, self.simplex_iteration[iteration_count], self.selected_foods, True)
        else:
            self.matrix_display = MatrixDisplay(self, self.simplex_iteration[iteration_count], self.selected_foods, False)

        self.matrix_display.pack(pady=10)


    def send_to_optimized_solution_frame(self):
        self.optimized_solution_frame.pack()
        self.pack_forget()
