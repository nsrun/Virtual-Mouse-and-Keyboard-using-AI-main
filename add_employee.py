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

        # Add padding frame
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


def open_add_employee():
    win = tk.Toplevel()
    win.title("Add Employee")
    win.geometry("450x550")
    win.resizable(False, False)

    # Colors
    bg_dark = "#1a1a2e"
    bg_mid = "#2d2d44"
    purple = "#9D4EDD"
    purple_light = "#B87EFF"
    green = "#06FFA5"
    green_light = "#3BFFCA"
    red = "#FF6D00"
    red_light = "#FF8E3C"
    text_white = "#FFFFFF"
    text_gray = "#B8B8D1"

    win.configure(bg=bg_dark)

    # ===== HEADER =====
    header_frame = tk.Frame(win, bg=purple, height=80)
    header_frame.pack(fill=tk.X)
    header_frame.pack_propagate(False)

    tk.Label(
        header_frame,
        text="👤 Add New Employee",
        font=("Segoe UI", 18, "bold"),
        bg=purple,
        fg=text_white
    ).pack(pady=25)

    # ===== FORM CONTAINER =====
    form_frame = tk.Frame(win, bg=bg_dark)
    form_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=30)

    # -------- Username Field --------
    tk.Label(
        form_frame,
        text="Username",
        font=("Segoe UI", 10, "bold"),
        bg=bg_dark,
        fg=text_gray,
        anchor='w'
    ).pack(fill=tk.X, pady=(0, 5))

    username_container = tk.Frame(form_frame, bg=purple_light, padx=2, pady=2)
    username_container.pack(fill=tk.X, pady=(0, 20))

    username_entry = ModernEntry(username_container)
    username_entry.pack(fill=tk.X, padx=2, pady=2, ipady=8, ipadx=10)

    # -------- Password Field --------
    tk.Label(
        form_frame,
        text="Password",
        font=("Segoe UI", 10, "bold"),
        bg=bg_dark,
        fg=text_gray,
        anchor='w'
    ).pack(fill=tk.X, pady=(0, 5))

    password_container = tk.Frame(form_frame, bg=purple_light, padx=2, pady=2)
    password_container.pack(fill=tk.X, pady=(0, 20))

    password_entry = ModernEntry(password_container, show="●")
    password_entry.pack(fill=tk.X, padx=2, pady=2, ipady=8, ipadx=10)

    # -------- Role Field --------
    tk.Label(
        form_frame,
        text="Role",
        font=("Segoe UI", 10, "bold"),
        bg=bg_dark,
        fg=text_gray,
        anchor='w'
    ).pack(fill=tk.X, pady=(0, 5))

    role_container = tk.Frame(form_frame, bg=purple_light, padx=2, pady=2)
    role_container.pack(fill=tk.X, pady=(0, 30))

    role_entry = ModernEntry(role_container)
    role_entry.insert(0, "employee")
    role_entry.pack(fill=tk.X, padx=2, pady=2, ipady=8, ipadx=10)

    # -------- Save Function --------
    def save_employee():
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        role = role_entry.get().strip().lower()

        if not username or not password or not role:
            messagebox.showwarning("Input Error", "All fields are required")
            return

        try:
            conn = sqlite3.connect("company.db")
            cur = conn.cursor()

            cur.execute(
                "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                (username, password, role)
            )

            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Employee added successfully")
            win.destroy()

        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists")

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))

    # -------- Buttons --------
    buttons_frame = tk.Frame(form_frame, bg=bg_dark)
    buttons_frame.pack(fill=tk.X, pady=(10, 0))

    ModernButton(
        buttons_frame,
        text="💾 Save Employee",
        bg=green,
        hover_bg=green_light,
        fg="white",
        activebackground=green_light,
        activeforeground="white",
        command=save_employee,
        width=20
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
        width=20
    ).pack(pady=8)

    # Info label
    tk.Label(
        form_frame,
        text="All fields are required",
        font=("Segoe UI", 8, "italic"),
        bg=bg_dark,
        fg=text_gray
    ).pack(pady=(15, 0))


# Test the form
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    open_add_employee()
    root.mainloop()