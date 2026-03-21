import os
import sys
import threading
import tkinter as tk
from tkinter import ttk, messagebox

import customtkinter as ctk
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

from src.file_handler import FileHandler
from src.file_handler_mysql import FileHandlerMySQL
from src.grade_manager import GradeManager
from src.analytics import Analytics
from src.predictor import GradePredictor

# ─────────────────────────────────────────────────────────────────────────────
# THEME
# ─────────────────────────────────────────────────────────────────────────────
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

BG_ROOT    = "#0F1117"
BG_SIDEBAR = "#16181F"
BG_CARD    = "#1E2130"
BG_CARD2   = "#252840"
ACCENT     = "#6C63FF"
ACCENT2    = "#A78BFA"
GREEN      = "#22C55E"
ORANGE     = "#F59E0B"
RED        = "#EF4444"
TEXT_MAIN  = "#F1F5F9"
TEXT_DIM   = "#94A3B8"

FONT_TITLE = ("Trebuchet MS", 22, "bold")
FONT_HEAD  = ("Trebuchet MS", 13, "bold")
FONT_BODY  = ("Calibri", 12)
FONT_SMALL = ("Calibri", 10)
FONT_MONO  = ("Courier New", 11)


# ─────────────────────────────────────────────────────────────────────────────
# APP
# ─────────────────────────────────────────────────────────────────────────────
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Student Habits & Performance Analytics")
        self.geometry("1280x780")
        self.minsize(1100, 680)
        self.configure(fg_color=BG_ROOT)

        self.manager   = None
        self.analytics = None
        self.predictor = None
        self.students  = []

        self._build_layout()
        self._load_data()

    # ── Layout ────────────────────────────────────────────────────────────────
    def _build_layout(self):
        self.sidebar = ctk.CTkFrame(self, width=230, fg_color=BG_SIDEBAR,
                                    corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        logo = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        logo.pack(fill="x", padx=16, pady=(20, 8))
        ctk.CTkLabel(logo, text="", font=("Segoe UI Emoji", 28)).pack(anchor="w")
        ctk.CTkLabel(logo, text="Student\nAnalytics",
                     font=("Trebuchet MS", 16, "bold"),
                     text_color=TEXT_MAIN).pack(anchor="w")
        ctk.CTkLabel(logo, text="Habits & Performance",
                     font=FONT_SMALL, text_color=TEXT_DIM).pack(anchor="w")

        ctk.CTkFrame(self.sidebar, height=1, fg_color=BG_CARD2).pack(
            fill="x", padx=12, pady=10)

        self._nav_buttons = []
        sections = [
            ("ANALYTICS", [
                ("All Students",       self.view_all_students),
                ("Top 5 Students",     self.view_top_students),
                ("At-Risk Students",   self.view_at_risk),
                ("Dropout Risk",       self.view_dropout),
                ("Score Distribution", self.view_distribution),
                ("Semester Averages",  self.view_semester_avg),
                ("Major Ranking",      self.view_major_ranking),
                ("Export Report",      self.view_export),
            ]),
            ("PREDICTION  (RF)", [
                ("Manual Predict",      self.view_predict_manual),
                ("Predict by ID",       self.view_predict_student),
                ("Actual vs Predicted", self.view_actual_vs_pred),
                ("Feature Importance",  self.view_feature_importance),
                ("Model Summary",       self.view_model_summary),
            ]),
        ]

        for section_label, items in sections:
            ctk.CTkLabel(self.sidebar, text=section_label,
                         font=("Trebuchet MS", 9, "bold"),
                         text_color=ACCENT2).pack(anchor="w", padx=20, pady=(8, 2))
            for label, cmd in items:
                btn = ctk.CTkButton(
                    self.sidebar, text=label, anchor="w",
                    fg_color="transparent", hover_color=BG_CARD2,
                    text_color=TEXT_DIM, font=FONT_BODY,
                    height=34, corner_radius=8,
                    command=lambda c=cmd: self._nav_click(c)
                )
                btn.pack(fill="x", padx=10, pady=1)
                self._nav_buttons.append((btn, cmd))

        ctk.CTkFrame(self.sidebar, height=1, fg_color=BG_CARD2).pack(
            fill="x", padx=12, pady=10, side="bottom")
        self.status_label = ctk.CTkLabel(
            self.sidebar, text="Loading...",
            font=FONT_SMALL, text_color=TEXT_DIM,
            wraplength=200, justify="left")
        self.status_label.pack(side="bottom", padx=16, pady=8, anchor="w")

        self.content = ctk.CTkFrame(self, fg_color=BG_ROOT, corner_radius=0)
        self.content.pack(side="left", fill="both", expand=True)

    def _nav_click(self, cmd):
        for btn, c in self._nav_buttons:
            if c == cmd:
                btn.configure(fg_color=ACCENT, text_color=TEXT_MAIN)
            else:
                btn.configure(fg_color="transparent", text_color=TEXT_DIM)
        cmd()

    def _set_status(self, msg, color=TEXT_DIM):
        self.status_label.configure(text=msg, text_color=color)

    def _clear_content(self):
        for w in self.content.winfo_children():
            w.destroy()

    def _page_header(self, title, subtitle=""):
        hdr = ctk.CTkFrame(self.content, fg_color="transparent")
        hdr.pack(fill="x", padx=28, pady=(22, 6))
        ctk.CTkLabel(hdr, text=title, font=FONT_TITLE,
                     text_color=TEXT_MAIN).pack(anchor="w")
        if subtitle:
            ctk.CTkLabel(hdr, text=subtitle, font=FONT_BODY,
                         text_color=TEXT_DIM).pack(anchor="w")
        ctk.CTkFrame(self.content, height=1,
                     fg_color=BG_CARD2).pack(fill="x", padx=28, pady=(0, 14))

    def _stat_card(self, parent, label, value, color=ACCENT):
        card = ctk.CTkFrame(parent, fg_color=BG_CARD, corner_radius=12)
        card.pack(side="left", padx=6, pady=6, fill="both", expand=True)
        ctk.CTkLabel(card, text=value,
                     font=("Trebuchet MS", 26, "bold"),
                     text_color=color).pack(padx=16, pady=(14, 2))
        ctk.CTkLabel(card, text=label, font=FONT_SMALL,
                     text_color=TEXT_DIM).pack(padx=16, pady=(0, 14))

    def _embed_chart(self, parent, fig):
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        plt.close(fig)

    def _table(self, parent, columns, rows, col_widths=None):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("H.Treeview",
            background=BG_CARD, foreground=TEXT_MAIN,
            fieldbackground=BG_CARD, rowheight=28,
            font=FONT_MONO, borderwidth=0)
        style.configure("H.Treeview.Heading",
            background=BG_SIDEBAR, foreground=ACCENT,
            font=("Trebuchet MS", 11, "bold"), relief="flat")
        style.map("H.Treeview", background=[("selected", ACCENT)])

        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=20, pady=8)

        tree = ttk.Treeview(frame, columns=columns, show="headings",
                            style="H.Treeview", selectmode="browse")
        for i, col in enumerate(columns):
            w = col_widths[i] if col_widths else 120
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=w)

        for row in rows:
            tree.insert("", "end", values=row)

        sb_y = ttk.Scrollbar(frame, orient="vertical",   command=tree.yview)
        sb_x = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=sb_y.set, xscrollcommand=sb_x.set)
        tree.pack(side="left", fill="both", expand=True)
        sb_y.pack(side="right",  fill="y")
        sb_x.pack(side="bottom", fill="x")

    # ── Data Loading ──────────────────────────────────────────────────────────
    def _load_data(self):
        # Ask user which data source to use before loading
        choice = messagebox.askquestion(
            "Select Data Source",
            "Load from MySQL database?\n\nYes  →  MySQL (student_1000)\nNo   →  CSV file"
        )

        def task():
            try:
                if choice == "yes":
                    self._set_status("Connecting to MySQL...", ORANGE)
                    fh = FileHandlerMySQL(
                        host="127.0.0.1",
                        port=8889,
                        user="root",
                        password="root",
                        database="students_1000"
                    )
                    fh.connect()
                else:
                    fh = FileHandler("data/students_habits.csv")

                records = fh.load_csv()
                self.manager = GradeManager()
                self.manager.load_from_records(records)
                self.students  = self.manager.get_all_students()
                self.analytics = Analytics(self.students)

                source = "MySQL" if choice == "yes" else "CSV"
                self._set_status(f" {len(self.students)} students\n Source: {source}", GREEN)
                self.after(0, self.view_all_students)

                self.predictor = GradePredictor()
                self.predictor.train(self.students)
                self._set_status(
                    f" {len(self.students)} students\n RF R²: {self.predictor.r2}", GREEN)

            except Exception as e:
                self._set_status(f"❌ {e}", RED)
                messagebox.showerror("Load Error", str(e))

        threading.Thread(target=task, daemon=True).start()

    # ─────────────────────────────────────────────────────────────────────────
    # ANALYTICS VIEWS
    # ─────────────────────────────────────────────────────────────────────────
    def view_all_students(self):
        self._clear_content()
        self._page_header("All Students",
                          f"{len(self.students)} total — Sem 1–4 Undergrad  |  Sem 5–8 Graduate")

        stats = ctk.CTkFrame(self.content, fg_color="transparent")
        stats.pack(fill="x", padx=22, pady=(0, 10))
        undergrad = sum(1 for s in self.students if s.semester <= 4)
        avg_score = round(sum(s.exam_score for s in self.students) / len(self.students), 1)
        at_risk   = sum(1 for s in self.students if s.exam_score < 60)
        self._stat_card(stats, "Total",        str(len(self.students)), ACCENT)
        self._stat_card(stats, "Undergraduate", str(undergrad),          "#3B82F6")
        self._stat_card(stats, "Graduate",      str(len(self.students) - undergrad), ACCENT2)
        self._stat_card(stats, "Avg Score",     str(avg_score),          GREEN)
        self._stat_card(stats, "At-Risk",       str(at_risk),            RED)

        cols = ["ID","Major","Type","Sem","GPA","Score",
                "Study Hrs","Attend%","Sleep","Stress","Dropout"]
        rows = [(
            s.student_id, s.major, s.type, s.semester,
            f"{s.previous_gpa:.2f}", f"{s.exam_score:.1f}",
            f"{s.study_hours_per_day:.1f}", f"{s.attendance_percentage:.1f}",
            f"{s.sleep_hours:.1f}", f"{s.stress_level:.1f}", s.dropout_risk
        ) for s in self.students]
        self._table(self.content, cols, rows,
                    [50,130,110,45,55,60,75,70,55,55,65])

    def view_top_students(self):
        self._clear_content()
        top = self.manager.get_top_students(10)
        self._page_header("Top 10 Students", "Ranked by exam score")

        card = ctk.CTkFrame(self.content, fg_color=BG_CARD, corner_radius=12)
        card.pack(fill="x", padx=22, pady=6)
        cols = ["Rank","ID","Major","Type","Sem","GPA","Score","Study Hrs","Attend%"]
        rows = [(i, s.student_id, s.major, s.type, s.semester,
                 f"{s.previous_gpa:.2f}", f"{s.exam_score:.1f}",
                 f"{s.study_hours_per_day:.1f}", f"{s.attendance_percentage:.1f}")
                for i, s in enumerate(top, 1)]
        self._table(card, cols, rows, [50,60,140,110,50,65,65,85,70])

        fig, ax = plt.subplots(figsize=(9, 2.8), facecolor=BG_CARD)
        ax.set_facecolor(BG_CARD)
        ids    = [str(s.student_id) for s in top]
        scores = [s.exam_score for s in top]
        bars   = ax.barh(ids[::-1], scores[::-1], color=ACCENT, height=0.6)
        for bar, val in zip(bars, scores[::-1]):
            ax.text(bar.get_width()+0.4, bar.get_y()+bar.get_height()/2,
                    f"{val:.0f}", va="center", color=TEXT_MAIN, fontsize=9)
        ax.set_xlim(0, 115); ax.set_xlabel("Exam Score", color=TEXT_DIM)
        ax.tick_params(colors=TEXT_DIM)
        for sp in ax.spines.values(): sp.set_color(BG_CARD2)
        ax.set_title("Top 10 by Exam Score", color=TEXT_MAIN, fontweight="bold")
        fig.tight_layout()
        chart = ctk.CTkFrame(self.content, fg_color=BG_CARD, corner_radius=12)
        chart.pack(fill="x", padx=22, pady=6)
        self._embed_chart(chart, fig)

    def view_at_risk(self):
        self._clear_content()
        at_risk = self.manager.get_at_risk_students()
        self._page_header("At-Risk Students",
                          f"{len(at_risk)} students with exam score < 60")
        if not at_risk:
            ctk.CTkLabel(self.content, text="[OK] No at-risk students found.",
                         font=FONT_HEAD, text_color=GREEN).pack(pady=40)
            return
        cols = ["ID","Major","Type","Sem","Score","Study Hrs",
                "Attend%","Sleep","Stress","Mental Health","Dropout"]
        rows = [(s.student_id, s.major, s.type, s.semester,
                 f"{s.exam_score:.1f}", f"{s.study_hours_per_day:.1f}",
                 f"{s.attendance_percentage:.1f}", f"{s.sleep_hours:.1f}",
                 f"{s.stress_level:.1f}", f"{s.mental_health_rating:.1f}",
                 s.dropout_risk) for s in at_risk]
        card = ctk.CTkFrame(self.content, fg_color=BG_CARD, corner_radius=12)
        card.pack(fill="both", expand=True, padx=22, pady=6)
        self._table(card, cols, rows, [50,130,110,45,60,75,70,55,55,95,65])

    def view_dropout(self):
        self._clear_content()
        dropout = [s for s in self.students if s.dropout_risk == "Yes"]
        self._page_header("Dropout Risk Students",
                          f"{len(dropout)} students flagged  "
                          f"({round(len(dropout)/len(self.students)*100,1)}% of total)")
        if not dropout:
            ctk.CTkLabel(self.content, text="[OK] No dropout-risk students found.",
                         font=FONT_HEAD, text_color=GREEN).pack(pady=40)
            return
        cols = ["ID","Major","Sem","Score","Stress","Attend%","Study Hrs","Sleep","Mental Health"]
        rows = [(s.student_id, s.major, s.semester,
                 f"{s.exam_score:.1f}", f"{s.stress_level:.1f}",
                 f"{s.attendance_percentage:.1f}", f"{s.study_hours_per_day:.1f}",
                 f"{s.sleep_hours:.1f}", f"{s.mental_health_rating:.1f}") for s in dropout]
        card = ctk.CTkFrame(self.content, fg_color=BG_CARD, corner_radius=12)
        card.pack(fill="both", expand=True, padx=22, pady=6)
        self._table(card, cols, rows, [55,140,45,60,60,75,80,55,95])

    def view_distribution(self):
        self._clear_content()
        self._page_header("Exam Score Distribution",
                          "Grade band breakdown across all students")
        dist   = self.analytics.grade_distribution()
        labels = list(dist.keys())
        values = list(dist.values())
        colors = ["#22C55E","#3B82F6","#F59E0B","#EF4444","#6B7280"]

        stats = ctk.CTkFrame(self.content, fg_color="transparent")
        stats.pack(fill="x", padx=22, pady=(0,10))
        for lbl, val, col in zip(labels, values, colors):
            self._stat_card(stats, lbl, str(val), col)

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10,4), facecolor=BG_ROOT)
        for ax in (ax1, ax2): ax.set_facecolor(BG_CARD)

        bars = ax1.bar(labels, values, color=colors, width=0.6,
                       edgecolor=BG_ROOT, linewidth=1.5)
        for bar, val in zip(bars, values):
            ax1.text(bar.get_x()+bar.get_width()/2, bar.get_height()+1,
                     str(val), ha="center", color=TEXT_MAIN, fontsize=10, fontweight="bold")
        ax1.set_ylim(0, max(values)*1.2)
        ax1.tick_params(colors=TEXT_DIM)
        ax1.set_title("Count by Grade Band", color=TEXT_MAIN, fontweight="bold")
        for sp in ax1.spines.values(): sp.set_color(BG_CARD2)

        wedges, texts, autos = ax2.pie(values, labels=labels, colors=colors,
            autopct="%1.1f%%", startangle=90,
            wedgeprops=dict(edgecolor=BG_ROOT, linewidth=2))
        for t in texts: t.set_color(TEXT_DIM)
        for t in autos: t.set_color(TEXT_MAIN); t.set_fontweight("bold")
        ax2.set_title("Percentage Share", color=TEXT_MAIN, fontweight="bold")

        fig.tight_layout(pad=2)
        card = ctk.CTkFrame(self.content, fg_color=BG_CARD, corner_radius=12)
        card.pack(fill="both", expand=True, padx=22, pady=6)
        self._embed_chart(card, fig)

    def view_semester_avg(self):
        self._clear_content()
        self._page_header("Average Score by Semester",
                          "Blue = Undergraduate (1–4)   |   Purple = Graduate (5–8)")
        avgs   = self.analytics.class_average_per_subject("semester")
        labels = list(avgs.keys())
        values = list(avgs.values())
        colors = ["#3B82F6" if int(l)<=4 else ACCENT2 for l in labels]

        fig, ax = plt.subplots(figsize=(9,4), facecolor=BG_ROOT)
        ax.set_facecolor(BG_CARD)
        bars = ax.bar(labels, values, color=colors, width=0.6,
                      edgecolor=BG_ROOT, linewidth=1.5)
        for bar, val in zip(bars, values):
            ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.3,
                    f"{val:.1f}", ha="center", color=TEXT_MAIN, fontsize=10, fontweight="bold")
        overall = sum(values)/len(values)
        ax.axhline(overall, color=GREEN, linestyle="--", linewidth=1.2, alpha=0.7,
                   label=f"Overall avg: {overall:.1f}")
        ax.set_ylim(0,110); ax.set_xlabel("Semester",color=TEXT_DIM)
        ax.set_ylabel("Avg Exam Score",color=TEXT_DIM)
        ax.tick_params(colors=TEXT_DIM)
        ax.set_title("Average Exam Score by Semester",color=TEXT_MAIN,fontweight="bold")
        ax.legend(facecolor=BG_CARD,labelcolor=TEXT_MAIN,edgecolor=BG_CARD2)
        for sp in ax.spines.values(): sp.set_color(BG_CARD2)
        fig.tight_layout()
        card = ctk.CTkFrame(self.content, fg_color=BG_CARD, corner_radius=12)
        card.pack(fill="both", expand=True, padx=22, pady=6)
        self._embed_chart(card, fig)

    def view_major_ranking(self):
        self._clear_content()
        self._page_header("Major Ranking",
                          "Average exam score per major — sorted lowest to highest")
        ranking = self.analytics.subject_difficulty_ranking()
        labels  = list(ranking.keys())
        values  = list(ranking.values())
        norm    = plt.Normalize(min(values), max(values))
        colors  = [plt.cm.RdYlGn(norm(v)) for v in values]

        fig, ax = plt.subplots(figsize=(9, max(3.5, len(labels)*0.55)), facecolor=BG_ROOT)
        ax.set_facecolor(BG_CARD)
        bars = ax.barh(labels, values, color=colors, height=0.6)
        for bar, val in zip(bars, values):
            ax.text(bar.get_width()+0.3, bar.get_y()+bar.get_height()/2,
                    f"{val:.1f}", va="center", color=TEXT_MAIN, fontsize=10)
        ax.set_xlim(0, max(values)*1.18)
        ax.set_xlabel("Average Exam Score", color=TEXT_DIM)
        ax.tick_params(colors=TEXT_DIM)
        ax.set_title("Major Ranking by Avg Exam Score",color=TEXT_MAIN,fontweight="bold")
        for sp in ax.spines.values(): sp.set_color(BG_CARD2)
        fig.tight_layout()
        card = ctk.CTkFrame(self.content, fg_color=BG_CARD, corner_radius=12)
        card.pack(fill="both", expand=True, padx=22, pady=6)
        self._embed_chart(card, fig)

    def view_export(self):
        self._clear_content()
        self._page_header("Export Student Report",
                          "Enter a student ID to view and export their full profile")
        card = ctk.CTkFrame(self.content, fg_color=BG_CARD, corner_radius=12)
        card.pack(fill="x", padx=22, pady=8)
        row = ctk.CTkFrame(card, fg_color="transparent")
        row.pack(padx=20, pady=16)

        ctk.CTkLabel(row, text="Student ID:", font=FONT_HEAD,
                     text_color=TEXT_MAIN).pack(side="left", padx=(0,10))
        sid_entry = ctk.CTkEntry(row, width=180, placeholder_text="e.g.  42")
        sid_entry.pack(side="left")

        out = ctk.CTkTextbox(self.content, font=FONT_MONO, fg_color=BG_CARD,
                             text_color=TEXT_MAIN, height=460, corner_radius=12)
        out.pack(fill="both", expand=True, padx=22, pady=6)

        def do_export():
            sid = sid_entry.get().strip()
            student = self.manager.get_student_by_id(sid)
            if not student:
                messagebox.showerror("Not Found", f"No student with ID: {sid}")
                return
            report = student.generate_report()
            out.configure(state="normal")
            out.delete("0.0","end")
            out.insert("0.0", report)
            fh = FileHandler("data/students_habits.csv")
            fh.export_report(report, f"report_{sid}.txt")
            messagebox.showinfo("Exported", f"Saved → data/reports/report_{sid}.txt")

        ctk.CTkButton(row, text="Load & Export", fg_color=ACCENT,
                      hover_color=ACCENT2, font=FONT_HEAD,
                      command=do_export).pack(side="left", padx=10)

    # ─────────────────────────────────────────────────────────────────────────
    # PREDICTION VIEWS
    # ─────────────────────────────────────────────────────────────────────────
    def _pred_not_ready(self):
        if not self.predictor or not self.predictor.is_trained:
            ctk.CTkLabel(self.content,
                         text="Model still training — please wait a moment...",
                         font=FONT_HEAD, text_color=ORANGE).pack(pady=40)
            return True
        return False

    def view_predict_manual(self):
        self._clear_content()
        self._page_header("Manual Prediction",
                          "Enter a behavioral profile to predict exam score")
        if self._pred_not_ready(): return

        scroll = ctk.CTkScrollableFrame(self.content, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=22, pady=4)

        left  = ctk.CTkFrame(scroll, fg_color=BG_CARD, corner_radius=12)
        right = ctk.CTkFrame(scroll, fg_color=BG_CARD, corner_radius=12)
        left.pack(side="left", fill="both", expand=True, padx=(0,6), pady=4)
        right.pack(side="left", fill="both", expand=True, padx=(6,0), pady=4)

        entries = {}

        def field(parent, label, key, default, row_i, options=None):
            ctk.CTkLabel(parent, text=label, font=FONT_SMALL,
                         text_color=TEXT_DIM).grid(
                row=row_i, column=0, sticky="w", padx=16, pady=5)
            if options:
                var = ctk.StringVar(value=default)
                ctk.CTkOptionMenu(parent, values=options, variable=var,
                                  width=180, fg_color=BG_CARD2,
                                  button_color=ACCENT, font=FONT_BODY).grid(
                    row=row_i, column=1, padx=12, pady=5, sticky="w")
                entries[key] = var
            else:
                w = ctk.CTkEntry(parent, width=180, font=FONT_BODY)
                w.insert(0, str(default))
                w.grid(row=row_i, column=1, padx=12, pady=5, sticky="w")
                entries[key] = w

        # Left column
        ctk.CTkLabel(left, text="Study & Academic", font=FONT_HEAD,
                     text_color=ACCENT).grid(row=0,columnspan=2,padx=16,pady=(14,4),sticky="w")
        field(left,"Study Hours/Day (0–12)",    "study_hours_per_day",     5.0, 1)
        field(left,"Attendance % (40–100)",      "attendance_percentage",   80.0, 2)
        field(left,"Previous GPA (0.0–4.0)",    "previous_gpa",            3.0, 3)
        field(left,"Time Management (1–10)",     "time_management_score",   5.0, 4)
        field(left,"Study Environment",          "study_environment",        "Library", 5,
              ["Library","Dorm","Quiet Room","Cafe","Co-Learning Group"])
        field(left,"Access to Tutoring",         "access_to_tutoring",       "No", 6, ["Yes","No"])

        ctk.CTkLabel(left, text="Health", font=FONT_HEAD,
                     text_color=ACCENT).grid(row=7,columnspan=2,padx=16,pady=(14,4),sticky="w")
        field(left,"Sleep Hours (4–12)",         "sleep_hours",             7.0, 8)
        field(left,"Exercise Days/Week (0–7)",   "exercise_frequency",      3.0, 9)
        field(left,"Mental Health (1–10)",       "mental_health_rating",    6.0, 10)
        field(left,"Stress Level (1–10)",        "stress_level",            5.0, 11)
        field(left,"Exam Anxiety (1–10)",        "exam_anxiety_score",      6.0, 12)
        field(left,"Diet Quality",               "diet_quality",             "Fair", 13,
              ["Poor","Fair","Good"])

        # Right column
        ctk.CTkLabel(right, text="Screen & Leisure", font=FONT_HEAD,
                     text_color=ACCENT2).grid(row=0,columnspan=2,padx=16,pady=(14,4),sticky="w")
        field(right,"Social Media Hrs/Day (0–5)", "social_media_hours",    2.0, 1)
        field(right,"Netflix Hrs/Day (0–4)",       "netflix_hours",         1.0, 2)
        field(right,"Total Screen Time Hrs/Day",   "screen_time",           5.0, 3)

        ctk.CTkLabel(right, text="Socio-economic", font=FONT_HEAD,
                     text_color=ACCENT2).grid(row=4,columnspan=2,padx=16,pady=(14,4),sticky="w")
        field(right,"Parental Support (1–10)",    "parental_support_level", 5,   5)
        field(right,"Parent Education",           "parental_education_level","Bachelor",6,
              ["High School","Some College","Bachelor","Master","PhD"])
        field(right,"Family Income",              "family_income_range",    "Medium",7,
              ["Low","Medium","High"])
        field(right,"Internet Quality",           "internet_quality",       "Medium",8,
              ["Low","Medium","High"])
        field(right,"Part-time Job",              "part_time_job",          "No",9,["Yes","No"])

        ctk.CTkLabel(right, text="Engagement", font=FONT_HEAD,
                     text_color=ACCENT2).grid(row=10,columnspan=2,padx=16,pady=(14,4),sticky="w")
        field(right,"Motivation (1–10)",          "motivation_level",       6.0, 11)
        field(right,"Extracurricular",            "extracurricular_participation","No",12,["Yes","No"])
        field(right,"Learning Style",             "learning_style",         "Reading",13,
              ["Reading","Visual","Auditory","Kinesthetic"])
        field(right,"Gender",                     "gender",                 "Male",14,
              ["Male","Female","Other"])

        result_var = ctk.StringVar(value="")
        ctk.CTkLabel(scroll, textvariable=result_var,
                     font=("Trebuchet MS", 18, "bold"),
                     text_color=GREEN).pack(pady=10)

        def predict():
            try:
                def gv(k):
                    v = entries[k]
                    return v.get() if isinstance(v, ctk.StringVar) else v.get()
                score = self.predictor.predict_exam_score(
                    float(gv("study_hours_per_day")), float(gv("attendance_percentage")),
                    float(gv("sleep_hours")), float(gv("exercise_frequency")),
                    float(gv("mental_health_rating")), float(gv("previous_gpa")),
                    float(gv("stress_level")), float(gv("social_media_hours")),
                    float(gv("netflix_hours")), float(gv("screen_time")),
                    float(gv("exam_anxiety_score")), float(gv("time_management_score")),
                    float(gv("motivation_level")), int(float(gv("parental_support_level"))),
                    gv("gender"), gv("diet_quality"), gv("part_time_job"),
                    gv("parental_education_level"), gv("internet_quality"),
                    gv("extracurricular_participation"), gv("access_to_tutoring"),
                    gv("family_income_range"), gv("learning_style"), gv("study_environment"),
                )
                letter = "A" if score>=90 else "B" if score>=80 else \
                         "C" if score>=70 else "D" if score>=60 else "F"
                result_var.set(f"Predicted Exam Score:  {score:.1f} / 100  ({letter})")
            except Exception as e:
                messagebox.showerror("Input Error", str(e))

        ctk.CTkButton(scroll, text="Predict Exam Score",
                      fg_color=ACCENT, hover_color=ACCENT2,
                      font=("Trebuchet MS", 14, "bold"), height=42,
                      command=predict).pack(pady=12)

    def view_predict_student(self):
        self._clear_content()
        self._page_header("Predict by Student ID",
                          "Auto-reads behavioral profile and predicts exam score")
        if self._pred_not_ready(): return

        top_card = ctk.CTkFrame(self.content, fg_color=BG_CARD, corner_radius=12)
        top_card.pack(fill="x", padx=22, pady=8)
        row = ctk.CTkFrame(top_card, fg_color="transparent")
        row.pack(padx=20, pady=16)
        ctk.CTkLabel(row, text="Student ID:", font=FONT_HEAD,
                     text_color=TEXT_MAIN).pack(side="left", padx=(0,10))
        sid_entry = ctk.CTkEntry(row, width=180, placeholder_text="e.g.  42")
        sid_entry.pack(side="left")
        ctk.CTkButton(row, text="Predict", fg_color=ACCENT, hover_color=ACCENT2,
                      font=FONT_HEAD,
                      command=lambda: do_predict()).pack(side="left", padx=10)

        result_card = ctk.CTkFrame(self.content, fg_color=BG_CARD, corner_radius=12)
        result_card.pack(fill="both", expand=True, padx=22, pady=6)

        def do_predict():
            sid = sid_entry.get().strip()
            student = self.manager.get_student_by_id(sid)
            if not student:
                messagebox.showerror("Not Found", f"No student with ID: {sid}")
                return
            for w in result_card.winfo_children(): w.destroy()

            predicted = self.predictor.predict_for_student(student)
            actual    = student.exam_score
            letter    = "A" if predicted>=90 else "B" if predicted>=80 else \
                        "C" if predicted>=70 else "D" if predicted>=60 else "F"

            info = ctk.CTkFrame(result_card, fg_color="transparent")
            info.pack(fill="x", padx=20, pady=14)

            fields = [
                ("ID",               student.student_id),
                ("Major",            student.major),
                ("Type",             student.type),
                ("Semester",         student.semester),
                ("Study Hrs/Day",    f"{student.study_hours_per_day:.1f}"),
                ("Attendance",       f"{student.attendance_percentage:.1f}%"),
                ("Sleep Hours",      f"{student.sleep_hours:.1f}"),
                ("Stress Level",     f"{student.stress_level:.1f}"),
                ("Mental Health",    f"{student.mental_health_rating:.1f}"),
                ("Motivation",       f"{student.motivation_level:.1f}"),
                ("Exam Anxiety",     f"{student.exam_anxiety_score:.1f}"),
                ("Time Management",  f"{student.time_management_score:.1f}"),
                ("Previous GPA",     f"{student.previous_gpa:.2f}"),
                ("Dropout Risk",     student.dropout_risk),
            ]
            for i, (lbl, val) in enumerate(fields):
                col, row_i = divmod(i, 7)
                ctk.CTkLabel(info, text=f"{lbl}:", font=FONT_SMALL,
                             text_color=TEXT_DIM).grid(
                    row=row_i, column=col*2, sticky="w", padx=(12,4), pady=3)
                ctk.CTkLabel(info, text=str(val), font=FONT_BODY,
                             text_color=TEXT_MAIN).grid(
                    row=row_i, column=col*2+1, sticky="w", padx=(0,20), pady=3)

            ctk.CTkFrame(result_card, height=1, fg_color=BG_CARD2).pack(fill="x",padx=20,pady=6)

            out = ctk.CTkFrame(result_card, fg_color="transparent")
            out.pack(pady=12)
            ctk.CTkLabel(out, text=f"Actual Score:     {actual:.1f}",
                         font=FONT_HEAD, text_color=TEXT_DIM).pack()
            ctk.CTkLabel(out,
                         text=f"Predicted Score:  {predicted:.1f} / 100  ({letter})",
                         font=("Trebuchet MS", 18, "bold"), text_color=GREEN).pack()
            diff  = predicted - actual
            color = GREEN if abs(diff)<5 else ORANGE if abs(diff)<10 else RED
            ctk.CTkLabel(out, text=f"Difference:  {diff:+.1f} pts",
                         font=FONT_HEAD, text_color=color).pack()

    def view_actual_vs_pred(self):
        self._clear_content()
        r2  = self.predictor.r2  if self.predictor else "..."
        mae = self.predictor.mae if self.predictor else "..."
        self._page_header("Actual vs Predicted",
                          f"R² = {r2}   |   MAE = ±{mae} pts")
        if self._pred_not_ready(): return

        yt = self.predictor.y_test
        yp = self.predictor.y_pred

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11,4.5), facecolor=BG_ROOT)
        for ax in (ax1, ax2): ax.set_facecolor(BG_CARD)

        ax1.scatter(yt, yp, color=ACCENT, alpha=0.55, s=40, edgecolors="none")
        mn, mx = min(yt.min(),yp.min())-3, max(yt.max(),yp.max())+3
        ax1.plot([mn,mx],[mn,mx], color=RED, linestyle="--", linewidth=1.5,
                 label="Perfect prediction")
        ax1.set_xlabel("Actual Score",    color=TEXT_DIM)
        ax1.set_ylabel("Predicted Score", color=TEXT_DIM)
        ax1.tick_params(colors=TEXT_DIM)
        ax1.set_title("Scatter: Actual vs Predicted",color=TEXT_MAIN,fontweight="bold")
        ax1.legend(facecolor=BG_CARD,labelcolor=TEXT_DIM,edgecolor=BG_CARD2)
        for sp in ax1.spines.values(): sp.set_color(BG_CARD2)

        residuals = yp - yt
        ax2.hist(residuals, bins=30, color=ACCENT2, edgecolor=BG_ROOT, linewidth=0.6)
        ax2.axvline(0, color=RED, linestyle="--", linewidth=1.5)
        ax2.set_xlabel("Prediction Error", color=TEXT_DIM)
        ax2.set_ylabel("Count", color=TEXT_DIM)
        ax2.tick_params(colors=TEXT_DIM)
        ax2.set_title("Residuals Distribution",color=TEXT_MAIN,fontweight="bold")
        for sp in ax2.spines.values(): sp.set_color(BG_CARD2)

        fig.tight_layout(pad=2)
        card = ctk.CTkFrame(self.content, fg_color=BG_CARD, corner_radius=12)
        card.pack(fill="both", expand=True, padx=22, pady=6)
        self._embed_chart(card, fig)

        stats = ctk.CTkFrame(self.content, fg_color="transparent")
        stats.pack(fill="x", padx=22, pady=4)
        self._stat_card(stats, "R² Score",    str(r2),       GREEN)
        self._stat_card(stats, "MAE (pts)",   f"±{mae}",     ORANGE)
        self._stat_card(stats, "Test Samples",str(len(yt)),  ACCENT)
        label = ("Excellent" if self.predictor.r2>=0.9 else
                 "Good" if self.predictor.r2>=0.7 else "Acceptable")
        self._stat_card(stats, "Accuracy", label, ACCENT2)

    def view_feature_importance(self):
        self._clear_content()
        self._page_header("Feature Importance",
                          "Which behavioral habit predicts exam score the most?")
        if self._pred_not_ready(): return

        pairs  = self.predictor.get_feature_importances()
        labels = [p[0] for p in pairs]
        values = [p[1] for p in pairs]
        norm   = plt.Normalize(min(values), max(values))
        colors = [plt.cm.plasma(norm(v)) for v in values]

        fig, ax = plt.subplots(figsize=(9, max(4, len(labels)*0.42)), facecolor=BG_ROOT)
        ax.set_facecolor(BG_CARD)
        bars = ax.barh(labels[::-1], values[::-1], color=colors[::-1], height=0.65)
        for bar, val in zip(bars, values[::-1]):
            ax.text(bar.get_width()+0.003, bar.get_y()+bar.get_height()/2,
                    f"{val:.1%}", va="center", color=TEXT_MAIN, fontsize=9)
        ax.set_xlim(0, max(values)*1.22)
        ax.set_xlabel("Importance Score", color=TEXT_DIM)
        ax.tick_params(colors=TEXT_DIM)
        ax.set_title("Feature Importance — Random Forest (24 features)",
                     color=TEXT_MAIN, fontweight="bold")
        for sp in ax.spines.values(): sp.set_color(BG_CARD2)
        fig.tight_layout()
        card = ctk.CTkFrame(self.content, fg_color=BG_CARD, corner_radius=12)
        card.pack(fill="both", expand=True, padx=22, pady=6)
        self._embed_chart(card, fig)

        tbl = ctk.CTkFrame(self.content, fg_color=BG_CARD, corner_radius=12)
        tbl.pack(fill="x", padx=22, pady=6)
        rows = [(i, lbl, f"{val:.2%}",
                ("***" if val>0.05 else "**" if val>0.01 else "*"))
                for i, (lbl, val) in enumerate(pairs, 1)]
        self._table(tbl, ["Rank","Feature","Importance","Impact"],
                    rows, [50,200,100,70])

    def view_model_summary(self):
        self._clear_content()
        self._page_header("Model Summary",
                          "Random Forest Regressor — Behavioral Prediction")
        if self._pred_not_ready(): return

        stats = ctk.CTkFrame(self.content, fg_color="transparent")
        stats.pack(fill="x", padx=22, pady=(0,10))
        self._stat_card(stats, "Algorithm",  "Random Forest",           ACCENT)
        self._stat_card(stats, "Trees",      "200 estimators",          ACCENT2)
        self._stat_card(stats, "Features",   "24",                      "#3B82F6")
        self._stat_card(stats, "R² Score",   str(self.predictor.r2),    GREEN)
        self._stat_card(stats, "MAE",        f"±{self.predictor.mae}",  ORANGE)

        txt = ctk.CTkTextbox(self.content, font=FONT_MONO, fg_color=BG_CARD,
                             text_color=TEXT_MAIN, corner_radius=12)
        txt.pack(fill="both", expand=True, padx=22, pady=6)
        txt.insert("0.0", self.predictor.get_model_summary())
        txt.configure(state="disabled")


# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    app = App()
    app.mainloop()
