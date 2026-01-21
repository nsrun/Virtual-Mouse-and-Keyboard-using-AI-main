import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
from database import authenticate


def start_login(open_dashboard):
    window = tk.Tk()
    window.title("Login")
    window.geometry("1000x600")  # Increased size
    window.resizable(False, False)

    # ===== SAFE IMAGE PATH =====
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    img_path = os.path.join(BASE_DIR, "image", "bg_forest.png")

    # ===== Load Background Image =====
    bg_image = Image.open(img_path)
    bg_image = bg_image.resize((1000, 600))
    bg_photo = ImageTk.PhotoImage(bg_image)

    # IMPORTANT: keep reference
    window.bg_photo = bg_photo

    canvas = tk.Canvas(window, width=1000, height=600, highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=bg_photo, anchor="nw")

    # ===== Glass Card Shadow =====
    shadow = tk.Frame(window, bg="#cbbcff")
    shadow.place(relx=0.5, rely=0.5, anchor="center", width=420, height=440)

    # ===== Glass Card =====
    card = tk.Frame(
        window,
        bg="#f7f4ff",
        highlightbackground="#e0d7ff",
        highlightthickness=1,
        bd=0,
        relief="flat"
    )
    card.place(relx=0.5, rely=0.5, anchor="center", width=400, height=420)

    # ===== Title =====
    tk.Label(
        card,
        text="Login",
        font=("Segoe UI", 28, "bold"),
        fg="#5b2dbf",
        bg="#f7f4ff"
    ).pack(pady=(30, 15))

    # ===== Username =====
    tk.Label(
        card,
        text="Username",
        font=("Segoe UI", 12),
        fg="#555555",
        bg="#f7f4ff"
    ).pack(anchor="w", padx=50)

    username_entry = tk.Entry(
        card,
        font=("Segoe UI", 13),
        bg="#ffffff",
        relief="flat"
    )
    username_entry.pack(fill="x", padx=50, pady=6, ipady=8)

    # ===== Password =====
    tk.Label(
        card,
        text="Password",
        font=("Segoe UI", 12),
        fg="#555555",
        bg="#f7f4ff"
    ).pack(anchor="w", padx=50, pady=(15, 0))

    password_entry = tk.Entry(
        card,
        font=("Segoe UI", 13),
        show="*",
        bg="#ffffff",
        relief="flat"
    )
    password_entry.pack(fill="x", padx=50, pady=6, ipady=8)

    # ===== Button Styles =====
    def on_enter(e):
        login_button.config(bg="#5a1fd1")
    def on_leave(e):
        login_button.config(bg="#7b3ff2")

    # ===== Login Function =====
    def do_login():
        username = username_entry.get()
        password = password_entry.get()

        success, user, role = authenticate(username, password)

        if success:
            window.destroy()
            open_dashboard(user, role)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    # ===== Login Button =====
    login_button = tk.Button(
        card,
        text="Login",
        font=("Segoe UI", 14, "bold"),
        bg="#7b3ff2",
        fg="white",
        activebackground="#5a1fd1",
        relief="flat",
        cursor="hand2",
        command=do_login
    )
    # Hover effect
    login_button.bind("<Enter>", on_enter)
    login_button.bind("<Leave>", on_leave)

    login_button.pack(pady=(25, 15), ipadx=30, ipady=10)

    # Optional: Add a "Forgot Password" or "Register" link
    def on_click_link():
        messagebox.showinfo("Info", "Feature coming soon!")

    link_label = tk.Label(
        card,
        text="Forgot Password?",
        font=("Segoe UI", 10, "underline"),
        fg="#555555",
        bg="#f7f4ff",
        cursor="hand2"
    )
    link_label.pack()
    link_label.bind("<Button-1>", lambda e: on_click_link())

    window.mainloop()