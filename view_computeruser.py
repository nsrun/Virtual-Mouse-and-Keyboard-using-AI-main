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


def open_view_computeruser():
    win = tk.Toplevel()
    win.title("View Computer Users")
    win.geometry("700x650")
    win.resizable(False, False)

    # Colors - Blue/Tech Theme
    bg_dark = "#1a1a2e"
    bg_mid = "#2d2d44"
    blue = "#4CC9F0"
    blue_light = "#72D7FF"
    purple = "#9D4EDD"
    purple_light = "#B87EFF"
    red = "#FF6D00"
    red_light = "#FF8E3C"
    text_white = "#FFFFFF"
    text_gray = "#B8B8D1"

    win.configure(bg=bg_dark)

    # ===== HEADER =====
    header_frame = tk.Frame(win, bg=blue, height=100)
    header_frame.pack(fill=tk.X)
    header_frame.pack_propagate(False)

    tk.Label(
        header_frame,
        text="🖥️ Computer Users Registry",
        font=("Segoe UI", 20, "bold"),
        bg=blue,
        fg=text_white
    ).pack(pady=(20, 5))

    # User count label
    count_label = tk.Label(
        header_frame,
        text="Loading computer users...",
        font=("Segoe UI", 10),
        bg=blue,
        fg="#1a1a2e"
    )
    count_label.pack()

    # ===== MAIN CONTAINER =====
    main_frame = tk.Frame(win, bg=bg_dark)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)

    # ===== SCROLLABLE FRAME FOR CARDS =====
    # Canvas for scrolling
    canvas_glow = tk.Frame(main_frame, bg=blue_light, padx=3, pady=3)
    canvas_glow.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

    canvas_container = tk.Frame(canvas_glow, bg=bg_mid)
    canvas_container.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

    canvas = tk.Canvas(
        canvas_container,
        bg=bg_mid,
        highlightthickness=0,
        relief=tk.FLAT
    )

    scrollbar = tk.Scrollbar(canvas_container, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg=bg_mid)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
    scrollbar.pack(side="right", fill="y")

    # Mouse wheel scrolling
    def on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    canvas.bind_all("<MouseWheel>", on_mousewheel)

    # ===== LOAD DATA FUNCTION =====
    def load_computer_users():
        # Clear existing widgets
        for widget in scrollable_frame.winfo_children():
            widget.destroy()

        try:
            conn = sqlite3.connect("company.db")
            cur = conn.cursor()

            cur.execute("SELECT username, system_id FROM computer_users")
            rows = cur.fetchall()
            conn.close()

            if not rows:
                # Empty state
                empty_frame = tk.Frame(scrollable_frame, bg=bg_mid)
                empty_frame.pack(fill=tk.BOTH, expand=True, pady=100)

                tk.Label(
                    empty_frame,
                    text="🔍",
                    font=("Segoe UI", 48),
                    bg=bg_mid,
                    fg=text_gray
                ).pack()

                tk.Label(
                    empty_frame,
                    text="No Computer Users Found",
                    font=("Segoe UI", 14, "bold"),
                    bg=bg_mid,
                    fg=text_white
                ).pack(pady=(10, 5))

                tk.Label(
                    empty_frame,
                    text="Add computer users to see them here",
                    font=("Segoe UI", 10),
                    bg=bg_mid,
                    fg=text_gray
                ).pack()

                count_label.config(text="0 computer users in database")
            else:
                # Add spacing at top
                tk.Frame(scrollable_frame, bg=bg_mid, height=10).pack()

                # Create user cards
                for idx, (username, system_id) in enumerate(rows, 1):
                    # Card with glow effect
                    card_glow = tk.Frame(scrollable_frame, bg=purple_light, padx=2, pady=2)
                    card_glow.pack(fill=tk.X, padx=20, pady=8)

                    card = tk.Frame(card_glow, bg="#3d3d5c")
                    card.pack(fill=tk.X, padx=2, pady=2)

                    # Card content
                    content_frame = tk.Frame(card, bg="#3d3d5c")
                    content_frame.pack(fill=tk.X, padx=20, pady=15)

                    # Left side - Icon and Number
                    left_frame = tk.Frame(content_frame, bg="#3d3d5c")
                    left_frame.pack(side=tk.LEFT)

                    # User number badge
                    number_frame = tk.Frame(left_frame, bg=blue, padx=2, pady=2)
                    number_frame.pack(side=tk.LEFT)

                    tk.Label(
                        number_frame,
                        text=f"#{idx}",
                        font=("Segoe UI", 10, "bold"),
                        bg=purple,
                        fg=text_white,
                        padx=12,
                        pady=8
                    ).pack()

                    # Computer icon
                    tk.Label(
                        left_frame,
                        text="💻",
                        font=("Segoe UI", 28),
                        bg="#3d3d5c"
                    ).pack(side=tk.LEFT, padx=(15, 20))

                    # Right side - User info
                    info_frame = tk.Frame(content_frame, bg="#3d3d5c")
                    info_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)

                    # Username
                    tk.Label(
                        info_frame,
                        text=username,
                        font=("Segoe UI", 14, "bold"),
                        bg="#3d3d5c",
                        fg=text_white,
                        anchor='w'
                    ).pack(fill=tk.X)

                    # System ID with icon
                    system_frame = tk.Frame(info_frame, bg="#3d3d5c")
                    system_frame.pack(fill=tk.X, pady=(5, 0))

                    tk.Label(
                        system_frame,
                        text="🔑",
                        font=("Segoe UI", 10),
                        bg="#3d3d5c",
                        fg=blue
                    ).pack(side=tk.LEFT, padx=(0, 5))

                    tk.Label(
                        system_frame,
                        text=f"System ID: {system_id}",
                        font=("Segoe UI", 11),
                        bg="#3d3d5c",
                        fg=text_gray,
                        anchor='w'
                    ).pack(side=tk.LEFT)

                    # Status indicator
                    status_frame = tk.Frame(content_frame, bg="#3d3d5c")
                    status_frame.pack(side=tk.RIGHT, padx=(10, 0))

                    tk.Label(
                        status_frame,
                        text="🟢",
                        font=("Segoe UI", 12),
                        bg="#3d3d5c"
                    ).pack()

                    tk.Label(
                        status_frame,
                        text="Active",
                        font=("Segoe UI", 8),
                        bg="#3d3d5c",
                        fg=text_gray
                    ).pack()

                # Add spacing at bottom
                tk.Frame(scrollable_frame, bg=bg_mid, height=10).pack()

                count_label.config(text=f"{len(rows)} computer user{'s' if len(rows) != 1 else ''} found")

        except sqlite3.Error as e:
            error_frame = tk.Frame(scrollable_frame, bg=bg_mid)
            error_frame.pack(fill=tk.BOTH, expand=True, pady=100)

            tk.Label(
                error_frame,
                text="⚠️",
                font=("Segoe UI", 48),
                bg=bg_mid,
                fg=red
            ).pack()

            tk.Label(
                error_frame,
                text="Database Error",
                font=("Segoe UI", 14, "bold"),
                bg=bg_mid,
                fg=text_white
            ).pack(pady=(10, 5))

            tk.Label(
                error_frame,
                text=str(e),
                font=("Segoe UI", 10),
                bg=bg_mid,
                fg=text_gray
            ).pack()

            count_label.config(text="Error loading data")

    # Load initial data
    load_computer_users()

    # ===== BUTTONS =====
    buttons_frame = tk.Frame(main_frame, bg=bg_dark)
    buttons_frame.pack(fill=tk.X)

    button_container = tk.Frame(buttons_frame, bg=bg_dark)
    button_container.pack()

    ModernButton(
        button_container,
        text="🔄 Refresh",
        bg=purple,
        hover_bg=purple_light,
        fg="white",
        activebackground=purple_light,
        activeforeground="white",
        command=load_computer_users,
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
        text="💡 Tip: Computer users are identified by their unique system IDs",
        font=("Segoe UI", 9, "italic"),
        bg=bg_dark,
        fg=text_gray
    ).pack(pady=(15, 0))


# Test the window
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    open_view_computeruser()
    root.mainloop()