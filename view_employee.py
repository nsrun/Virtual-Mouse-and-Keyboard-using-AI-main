import tkinter as tk
from tkinter import font as tkfont
import sqlite3


class ModernButton(tk.Button):
    """Custom button with hover effects"""

    def __init__(self, parent, **kwargs):
        self.default_bg = kwargs.pop('bg', '#6C5CE7')
        self.hover_bg = kwargs.pop('hover_bg', '#A29BFE')
        super().__init__(parent, **kwargs)
        self.config(
            bg=self.default_bg,
            relief=tk.FLAT,
            cursor='hand2',
            borderwidth=0,
            padx=20,
            pady=12,
            font=("Segoe UI", 11, "bold")
        )
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)

    def on_enter(self, e):
        self.config(bg=self.hover_bg)

    def on_leave(self, e):
        self.config(bg=self.default_bg)


def open_view_employee():
    win = tk.Toplevel()
    win.title("View Employees")
    win.geometry("600x650")
    win.resizable(False, False)

    # Colors
    bg_dark = "#1a1a2e"
    bg_mid = "#2d2d44"
    cyan = "#4ECDC4"
    cyan_light = "#6FE6DE"
    blue = "#4CC9F0"
    blue_light = "#72D7FF"
    red = "#FF6D00"
    red_light = "#FF8E3C"
    text_white = "#FFFFFF"
    text_gray = "#B8B8D1"

    win.configure(bg=bg_dark)

    # ===== HEADER =====
    header_frame = tk.Frame(win, bg=cyan, height=100)
    header_frame.pack(fill=tk.X)
    header_frame.pack_propagate(False)

    tk.Label(
        header_frame,
        text="📋 Employee Directory",
        font=("Segoe UI", 20, "bold"),
        bg=cyan,
        fg=text_white
    ).pack(pady=(20, 5))

    # Employee count label (will be updated)
    count_label = tk.Label(
        header_frame,
        text="Loading employees...",
        font=("Segoe UI", 10),
        bg=cyan,
        fg="#1a1a2e"
    )
    count_label.pack()

    # ===== MAIN CONTAINER =====
    main_frame = tk.Frame(win, bg=bg_dark)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)

    # ===== LISTBOX CONTAINER WITH GLOW =====
    listbox_glow = tk.Frame(main_frame, bg=cyan_light, padx=3, pady=3)
    listbox_glow.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

    # Create a frame for listbox and scrollbar
    listbox_frame = tk.Frame(listbox_glow, bg=bg_mid)
    listbox_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

    # Scrollbar
    scrollbar = tk.Scrollbar(listbox_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Styled Listbox
    listbox = tk.Listbox(
        listbox_frame,
        bg=bg_mid,
        fg=text_white,
        selectbackground=cyan,
        selectforeground=text_white,
        font=("Segoe UI", 11),
        relief=tk.FLAT,
        borderwidth=0,
        highlightthickness=0,
        yscrollcommand=scrollbar.set
    )
    listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    scrollbar.config(command=listbox.yview)

    # ===== LOAD DATA FUNCTION =====
    def load_employees():
        listbox.delete(0, tk.END)

        try:
            conn = sqlite3.connect("company.db")
            cur = conn.cursor()

            cur.execute("SELECT username, role FROM users WHERE role='employee'")
            rows = cur.fetchall()
            conn.close()

            if not rows:
                listbox.insert(tk.END, "")
                listbox.insert(tk.END, "   🔍 No employees found")
                listbox.insert(tk.END, "")
                listbox.insert(tk.END, "   Add employees to see them here")
                count_label.config(text="0 employees in database")
            else:
                # Add header
                listbox.insert(tk.END, "")
                listbox.insert(tk.END, "  ┌─────────────────────────────────────────────────┐")
                listbox.insert(tk.END, "")

                for idx, row in enumerate(rows, 1):
                    # Add employee entry with icon
                    listbox.insert(tk.END, f"  👤  {row[0]}")
                    listbox.insert(tk.END, f"       Role: {row[1].upper()}")

                    # Add separator between entries
                    if idx < len(rows):
                        listbox.insert(tk.END, "  ├─────────────────────────────────────────────────┤")
                    listbox.insert(tk.END, "")

                listbox.insert(tk.END, "  └─────────────────────────────────────────────────┘")
                listbox.insert(tk.END, "")

                count_label.config(text=f"{len(rows)} employee{'s' if len(rows) != 1 else ''} found")

        except sqlite3.Error as e:
            listbox.insert(tk.END, "")
            listbox.insert(tk.END, f"   ⚠️ Database Error: {str(e)}")
            listbox.insert(tk.END, "")
            count_label.config(text="Error loading data")

    # Load initial data
    load_employees()

    # ===== BUTTONS =====
    buttons_frame = tk.Frame(main_frame, bg=bg_dark)
    buttons_frame.pack(fill=tk.X)

    button_container = tk.Frame(buttons_frame, bg=bg_dark)
    button_container.pack()

    ModernButton(
        button_container,
        text="🔄 Refresh",
        bg=blue,
        hover_bg=blue_light,
        fg="white",
        activebackground=blue_light,
        activeforeground="white",
        command=load_employees,
        width=18
    ).pack(side=tk.LEFT, padx=8)

    ModernButton(
        button_container,
        text="❌ Close",
        bg=red,
        hover_bg=red_light,
        fg="white",
        activebackground=red_light,
        activeforeground="white",
        command=win.destroy,
        width=18
    ).pack(side=tk.LEFT, padx=8)

    # Info label
    tk.Label(
        main_frame,
        text="💡 Tip: Click Refresh to update the list",
        font=("Segoe UI", 9, "italic"),
        bg=bg_dark,
        fg=text_gray
    ).pack(pady=(15, 0))


# Test the window
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    open_view_employee()
    root.mainloop()