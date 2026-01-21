import tkinter as tk
from tkinter import messagebox
from tkinter import font as tkfont
import sqlite3


class ModernEntry(tk.Entry):
    """Custom styled entry field"""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.config(
            bg="#2d2d44",
            fg="white",
            insertbackground="white",
            relief=tk.FLAT,
            borderwidth=0,
            font=("Segoe UI", 11)
        )

        self.bind('<FocusIn>', self.on_focus_in)
        self.bind('<FocusOut>', self.on_focus_out)

    def on_focus_in(self, e):
        self.config(bg="#3d3d5c")

    def on_focus_out(self, e):
        self.config(bg="#2d2d44")


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


def open_add_computer():
    win = tk.Toplevel()
    win.title("Add Computer User")
    win.geometry("500x600")
    win.resizable(False, False)

    # Colors - Blue Tech Theme
    bg_dark = "#1a1a2e"
    bg_mid = "#2d2d44"
    blue = "#4CC9F0"
    blue_light = "#72D7FF"
    green = "#06FFA5"
    green_light = "#3BFFCA"
    red = "#FF6D00"
    red_light = "#FF8E3C"
    text_white = "#FFFFFF"
    text_gray = "#B8B8D1"

    win.configure(bg=bg_dark)

    # ===== HEADER =====
    header_frame = tk.Frame(win, bg=blue, height=100)
    header_frame.pack(fill=tk.X)
    header_frame.pack_propagate(False)

    # Header icon and title container
    header_content = tk.Frame(header_frame, bg=blue)
    header_content.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    tk.Label(
        header_content,
        text="💻",
        font=("Segoe UI", 32),
        bg=blue,
        fg=text_white
    ).pack()

    tk.Label(
        header_content,
        text="Add Computer User",
        font=("Segoe UI", 18, "bold"),
        bg=blue,
        fg=text_white
    ).pack(pady=(5, 0))

    # ===== FORM CONTAINER =====
    form_frame = tk.Frame(win, bg=bg_dark)
    form_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=40)

    # -------- Username Field --------
    tk.Label(
        form_frame,
        text="👤 User Name",
        font=("Segoe UI", 10, "bold"),
        bg=bg_dark,
        fg=text_gray,
        anchor='w'
    ).pack(fill=tk.X, pady=(0, 5))

    username_container = tk.Frame(form_frame, bg=blue_light, padx=2, pady=2)
    username_container.pack(fill=tk.X, pady=(0, 20))

    username_entry = ModernEntry(username_container)
    username_entry.pack(fill=tk.X, padx=2, pady=2, ipady=10, ipadx=10)

    # -------- System ID Field --------
    tk.Label(
        form_frame,
        text="🔑 System ID",
        font=("Segoe UI", 10, "bold"),
        bg=bg_dark,
        fg=text_gray,
        anchor='w'
    ).pack(fill=tk.X, pady=(0, 5))

    tk.Label(
        form_frame,
        text="Enter unique system identifier",
        font=("Segoe UI", 8, "italic"),
        bg=bg_dark,
        fg=text_gray,
        anchor='w'
    ).pack(fill=tk.X, pady=(0, 5))

    sid_container = tk.Frame(form_frame, bg=blue_light, padx=2, pady=2)
    sid_container.pack(fill=tk.X, pady=(0, 20))

    sid_entry = ModernEntry(sid_container)
    sid_entry.pack(fill=tk.X, padx=2, pady=2, ipady=10, ipadx=10)

    # -------- Password Field --------
    tk.Label(
        form_frame,
        text="🔒 Password",
        font=("Segoe UI", 10, "bold"),
        bg=bg_dark,
        fg=text_gray,
        anchor='w'
    ).pack(fill=tk.X, pady=(0, 5))

    pwd_container = tk.Frame(form_frame, bg=blue_light, padx=2, pady=2)
    pwd_container.pack(fill=tk.X, pady=(0, 30))

    pwd_entry = ModernEntry(pwd_container, show="●")
    pwd_entry.pack(fill=tk.X, padx=2, pady=2, ipady=10, ipadx=10)

    # -------- Save Function --------
    def save():
        username = username_entry.get().strip()
        system_id = sid_entry.get().strip()
        password = pwd_entry.get().strip()

        if not username or not system_id or not password:
            messagebox.showerror("Error", "All fields required")
            return

        try:
            conn = sqlite3.connect("company.db")
            cur = conn.cursor()

            cur.execute(
                "INSERT INTO computer_users (username, system_id, password) VALUES (?, ?, ?)",
                (username, system_id, password)
            )

            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Computer user added successfully!")
            win.destroy()

        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    # -------- Buttons --------
    buttons_frame = tk.Frame(form_frame, bg=bg_dark)
    buttons_frame.pack(fill=tk.X, pady=(10, 0))

    ModernButton(
        buttons_frame,
        text="💾 Save Computer User",
        bg=green,
        hover_bg=green_light,
        fg="white",
        activebackground=green_light,
        activeforeground="white",
        command=save,
        width=24
    ).pack(pady=8)

    ModernButton(
        buttons_frame,
        text="❌ Close",
        bg=red,
        hover_bg=red_light,
        fg="white",
        activebackground=red_light,
        activeforeground="white",
        command=win.destroy,
        width=24
    ).pack(pady=8)

    # Info box at bottom
    info_frame = tk.Frame(form_frame, bg="#2d2d44", padx=2, pady=2)
    info_frame.pack(fill=tk.X, pady=(20, 0))

    info_inner = tk.Frame(info_frame, bg="#3d3d5c")
    info_inner.pack(fill=tk.X, padx=2, pady=2)

    tk.Label(
        info_inner,
        text="ℹ️ Info",
        font=("Segoe UI", 9, "bold"),
        bg="#3d3d5c",
        fg=blue,
        anchor='w'
    ).pack(fill=tk.X, padx=15, pady=(10, 5))

    tk.Label(
        info_inner,
        text="• System ID must be unique for each computer\n• Password is encrypted for security\n• All fields are mandatory",
        font=("Segoe UI", 9),
        bg="#3d3d5c",
        fg=text_gray,
        anchor='w',
        justify=tk.LEFT
    ).pack(fill=tk.X, padx=15, pady=(0, 10))


# Test the form
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    open_add_computer()
    root.mainloop()