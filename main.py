import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from src import * # This imports your visualizer functions and team classes

class StudentAnalyticsApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Config
        self.title("Student Grade Analytics System")
        self.geometry("1200x720")
        ctk.set_appearance_mode("dark")

        # Layout Setup
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar Navigation
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        # Display Area
        self.display_frame = ctk.CTkFrame(self, fg_color="#1a1a1a")
        self.display_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        self._build_sidebar()

    def _build_sidebar(self):
        """Creates the 16-button navigation menu"""
        ctk.CTkLabel(self.sidebar, text="ANALYTICS", font=("Arial", 16, "bold")).pack(pady=20)
        
        # Testing your Visualizer functions
        ctk.CTkButton(self.sidebar, text="📊 Grade Distribution", 
                      command=self.view_grade_dist).pack(pady=10, padx=20)
        
        ctk.CTkButton(self.sidebar, text="🏆 Top Students", 
                      command=self.view_top_students).pack(pady=10, padx=20)

    def _render_chart(self, plot_func, *args):
        """Helper to clear the screen and embed a Matplotlib chart"""
        for widget in self.display_frame.winfo_children():
            widget.destroy()

        # Create the figure and axis
        fig, ax = plt.subplots(figsize=(8, 5), dpi=100)
        
        # Call the specific function from your visualizer.py
        plot_func(ax, *args)
        
        # Embed the chart into CustomTkinter
        canvas = FigureCanvasTkAgg(fig, master=self.display_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    # --- View Methods (Connecting to Visualizer) ---

    def view_grade_dist(self):
        # Mock data for distribution
        data = {'A': 5, 'B': 10, 'C': 15, 'D': 5, 'F': 2}
        self._render_chart(plot_grade_distribution_embedded, data)

    def view_top_students(self):
        # Mocking student objects for testing
        class MockStudent:
            def __init__(self, name, gpa):
                self.name, self.gpa = name, gpa
            def get_gpa(self): return self.gpa

        students = [MockStudent("Yin", 95), MockStudent("Sreylenn", 88), MockStudent("Sambath", 92)]
        self._render_chart(plot_top_students_embedded, students)

if __name__ == "__main__":
    app = StudentAnalyticsApp()
    app.mainloop()