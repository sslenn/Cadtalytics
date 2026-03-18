import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class StudentAnalyticsApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # 1. Base Configuration 
        self.title("Student Grade Analytics System | CADT")
        self.geometry("1200x720")
        ctk.set_appearance_mode("dark")
        
        # 2. Grid Layout (Sidebar vs Content) 
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self._build_sidebar()
        
        # Main Content Area
        self.content_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#1a1c23")
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        # Show initial dashboard 
        self.view_dashboard()

    def _build_sidebar(self):
        """Builds the 220px sidebar seen in your reference image """
        self.sidebar = ctk.CTkScrollableFrame(self, width=220, corner_radius=0, fg_color="#11131a")
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        # Logo Area
        self.logo = ctk.CTkLabel(self.sidebar, text="📊 Grade Analytics", font=("Arial", 18, "bold"))
        self.logo.pack(pady=30)
        
        # Section: Analytics 
        ctk.CTkLabel(self.sidebar, text="ANALYTICS", text_color="gray", font=("Arial", 11, "bold")).pack(anchor="w", padx=20)
        self._add_sidebar_btn("👥 All Students", self.view_all_students)
        self._add_sidebar_btn("🏆 Top 5", self.view_top_students)
        # ... (Add remaining 7 Analytics buttons)
        
        # Section: Prediction 
        ctk.CTkLabel(self.sidebar, text="PREDICTION (ML)", text_color="gray", font=("Arial", 11, "bold")).pack(anchor="w", padx=20, pady=(20, 0))
        self._add_sidebar_btn("🔮 Manual G4", self.view_predict_manual)
        # ... (Add remaining 6 Prediction buttons)

    def view_dashboard(self):
        """Renders the 4-card layout from your image """
        self._clear_content()
        
        # Setup 2x2 Grid for Cards
        self.content_frame.grid_columnconfigure((0, 1), weight=1)
        self.content_frame.grid_rowconfigure((0, 1), weight=1)
        
        # Top Left: Analytics Card (Blue)
        self._create_card(0, 0, "Analytics Section", "9 views: student tables, 4 chart types...", "#3b82f6")
        
        # Top Right: Prediction Card (Yellow)
        self._create_card(0, 1, "Prediction Section", "7 views: manual input, trend chart...", "#eab308")
        
        # Bottom Left: Embedded Charts (Green)
        self._create_card(1, 0, "Embedded Charts", "All Matplotlib charts render inside...", "#22c55e")
        
        # Bottom Right: Dark Theme (Purple)
        self._create_card(1, 1, "Dark Theme GUI", "CustomTkinter dark mode with sidebar...", "#8b5cf6")

    def _create_card(self, r, c, title, desc, accent_color):
        """Helper to build the card style from your image """
        card = ctk.CTkFrame(self.content_frame, fg_color="#23262f", corner_radius=10)
        card.grid(row=r, column=c, padx=15, pady=15, sticky="nsew")
        
        # Accent Border/Line
        accent = ctk.CTkFrame(card, width=5, fg_color=accent_color)
        accent.pack(side="left", fill="y", padx=(0, 15))
        
        # Content
        ctk.CTkLabel(card, text=title, font=("Arial", 18, "bold"), text_color=accent_color).pack(anchor="w", pady=(20, 5))
        ctk.CTkLabel(card, text=desc, font=("Arial", 13), wraplength=300, justify="left").pack(anchor="w")

    def _clear_content(self):
        """Standard Sousdey-role helper to switch views """
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def _add_sidebar_btn(self, txt, cmd):
        btn = ctk.CTkButton(self.sidebar, text=txt, command=cmd, fg_color="transparent", anchor="w", hover_color="#2d2f39")
        btn.pack(fill="x", padx=10, pady=2)

    # Placeholder view methods for your 16 total views
    def view_all_students(self): self._clear_content()
    def view_top_students(self): self._clear_content()
    def view_predict_manual(self): self._clear_content()

if __name__ == "__main__":
    app = StudentAnalyticsApp()
    app.mainloop()