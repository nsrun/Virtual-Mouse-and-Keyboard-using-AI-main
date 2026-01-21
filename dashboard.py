import tkinter as tk
from tkinter import font as tkfont
import subprocess
import sys
import add_employee
import view_employee
import add_computer
import view_computeruser
from datetime import datetime


def run_script(script):
    subprocess.Popen([sys.executable, script])


class ModernButton(tk.Button):
    """Custom button with smooth hover effects and shadows"""

    def __init__(self, parent, **kwargs):
        self.default_bg = kwargs.pop('bg', '#6C5CE7')
        self.hover_bg = kwargs.pop('hover_bg', '#A29BFE')
        self.shadow_color = kwargs.pop('shadow_color', '#1a1a2e')
        super().__init__(parent, **kwargs)
        self.config(
            bg=self.default_bg,
            relief=tk.FLAT,
            cursor='hand2',
            borderwidth=0,
            padx=25,
            pady=15
        )
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)

    def on_enter(self, e):
        self.config(bg=self.hover_bg)

    def on_leave(self, e):
        self.config(bg=self.default_bg)


class GlowCard(tk.Frame):
    """Card with glowing border effect"""

    def __init__(self, parent, glow_color="#6C5CE7", **kwargs):
        super().__init__(parent, **kwargs)
        self.glow_color = glow_color
        self.config(
            bg=glow_color,
            padx=2,
            pady=2
        )


class AnimatedCard(tk.Frame):
    """Card with pulsing animation effect"""

    def __init__(self, parent, pulse_color="#6C5CE7", **kwargs):
        super().__init__(parent, **kwargs)
        self.pulse_color = pulse_color
        self.is_pulsing = False

    def start_pulse(self):
        if not self.is_pulsing:
            self.is_pulsing = True
            self._pulse()

    def _pulse(self):
        if self.is_pulsing:
            # Simple color alternation effect
            current = self.cget('bg')
            if current == self.pulse_color:
                self.config(bg='#2d2d44')
            else:
                self.config(bg=self.pulse_color)
            self.after(1000, self._pulse)


def create_stat_card(parent, title, value, icon, bg_color, glow_color):
    """Create a colorful statistics card with animations"""
    card_outer = GlowCard(parent, glow_color=glow_color, bg=glow_color)
    card_outer.pack(side=tk.LEFT, padx=15, pady=10)

    card_inner = tk.Frame(card_outer, bg="#2d2d44", width=200, height=130)
    card_inner.pack(padx=3, pady=3)
    card_inner.pack_propagate(False)

    # Icon with colored background and border
    icon_container = tk.Frame(card_inner, bg=glow_color, padx=2, pady=2)
    icon_container.place(x=15, y=15)

    icon_bg = tk.Frame(icon_container, bg=bg_color, width=50, height=50)
    icon_bg.pack()

    icon_label = tk.Label(
        icon_bg,
        text=icon,
        font=("Segoe UI", 24),
        bg=bg_color,
        fg="white"
    )
    icon_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # Value with animation
    value_label = tk.Label(
        card_inner,
        text=value,
        font=("Segoe UI", 22, "bold"),
        bg="#2d2d44",
        fg="white"
    )
    value_label.place(x=15, y=75)

    # Title
    tk.Label(
        card_inner,
        text=title,
        font=("Segoe UI", 10),
        bg="#2d2d44",
        fg="#B8B8D1"
    ).place(x=15, y=105)

    # Status indicator
    status_dot = tk.Frame(card_inner, bg=green, width=8, height=8)
    status_dot.place(x=180, y=20)


def create_activity_item(parent, icon, text, time, color):
    """Create an activity feed item"""
    item_frame = tk.Frame(parent, bg="#1a1a2e", height=60)
    item_frame.pack(fill=tk.X, pady=5)
    item_frame.pack_propagate(False)

    # Colored indicator line
    tk.Frame(item_frame, bg=color, width=4).pack(side=tk.LEFT, fill=tk.Y)

    content_frame = tk.Frame(item_frame, bg="#1a1a2e")
    content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=15, pady=10)

    # Icon
    tk.Label(
        content_frame,
        text=icon,
        font=("Segoe UI", 16),
        bg="#1a1a2e",
        fg=color
    ).pack(side=tk.LEFT, padx=(0, 10))

    # Text
    text_frame = tk.Frame(content_frame, bg="#1a1a2e")
    text_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    tk.Label(
        text_frame,
        text=text,
        font=("Segoe UI", 10, "bold"),
        bg="#1a1a2e",
        fg="white",
        anchor='w'
    ).pack(anchor='w')

    tk.Label(
        text_frame,
        text=time,
        font=("Segoe UI", 8),
        bg="#1a1a2e",
        fg="#B8B8D1",
        anchor='w'
    ).pack(anchor='w')


def create_quick_action(parent, icon, text, color, command):
    """Create a quick action button"""
    action_frame = GlowCard(parent, glow_color=color, bg="#1a1a2e")
    action_frame.pack(side=tk.LEFT, padx=10)

    inner = tk.Frame(action_frame, bg="#2d2d44", width=120, height=120)
    inner.pack(padx=3, pady=3)
    inner.pack_propagate(False)

    btn = tk.Button(
        inner,
        text=f"{icon}\n\n{text}",
        font=("Segoe UI", 10, "bold"),
        bg="#2d2d44",
        fg="white",
        relief=tk.FLAT,
        cursor='hand2',
        borderwidth=0,
        command=command
    )
    btn.pack(fill=tk.BOTH, expand=True)

    def on_enter(e):
        btn.config(bg=color)

    def on_leave(e):
        btn.config(bg="#2d2d44")

    btn.bind('<Enter>', on_enter)
    btn.bind('<Leave>', on_leave)


def open_dashboard(username, role):
    root = tk.Tk()
    root.title("AI Control Center")
    root.geometry("1600x900")
    root.resizable(False, False)

    # ===== VIBRANT COLOR SCHEME =====
    bg_dark = "#0f0f1e"
    bg_mid = "#1a1a2e"
    bg_card = "#16213e"

    # Global color definitions
    global purple, pink, blue, cyan, green, orange, yellow
    purple = "#9D4EDD"
    pink = "#F72585"
    blue = "#4CC9F0"
    cyan = "#4ECDC4"
    green = "#06FFA5"
    orange = "#FF6D00"
    yellow = "#FFD60A"

    text_white = "#FFFFFF"
    text_gray = "#B8B8D1"

    root.configure(bg=bg_mid)

    # ===== CUSTOM FONTS =====
    title_font = tkfont.Font(family="Segoe UI", size=32, weight="bold")
    subtitle_font = tkfont.Font(family="Segoe UI", size=12)
    button_font = tkfont.Font(family="Segoe UI", size=11, weight="bold")
    section_font = tkfont.Font(family="Segoe UI", size=16, weight="bold")

    # ===== TOP STATUS BAR =====
    status_bar = tk.Frame(root, bg="#0a0a14", height=35)
    status_bar.pack(fill=tk.X)
    status_bar.pack_propagate(False)

    # System status indicators
    status_items = [
        ("🟢", "All Systems Operational", green),
        ("📡", "Connected", blue),
        ("⚡", "High Performance", yellow)
    ]

    left_status = tk.Frame(status_bar, bg="#0a0a14")
    left_status.pack(side=tk.LEFT, padx=20)

    for icon, text, color in status_items:
        tk.Label(
            left_status,
            text=f"{icon} {text}",
            font=("Segoe UI", 9),
            bg="#0a0a14",
            fg=color
        ).pack(side=tk.LEFT, padx=15)

    # Clock
    clock_label = tk.Label(
        status_bar,
        text=datetime.now().strftime("%I:%M %p"),
        font=("Segoe UI", 10, "bold"),
        bg="#0a0a14",
        fg=text_white
    )
    clock_label.pack(side=tk.RIGHT, padx=20)

    def update_clock():
        clock_label.config(text=datetime.now().strftime("%I:%M %p"))
        clock_label.after(1000, update_clock)

    update_clock()

    # ===== ANIMATED HEADER =====
    header_frame = tk.Frame(root, bg=bg_dark, height=200)
    header_frame.pack(fill=tk.X)
    header_frame.pack_propagate(False)

    # Gradient layers
    gradient_colors = ["#1a1a2e", "#240046", "#3c096c", "#5a189a", "#7209b7"]
    for i, color in enumerate(gradient_colors):
        grad_frame = tk.Frame(header_frame, bg=color, height=200 - (i * 35))
        grad_frame.place(x=0, y=0, relwidth=1)

    # Sparkle decorations
    sparkle_positions = [(50, 30), (150, 60), (1500, 40), (1400, 70)]
    for x, y in sparkle_positions:
        tk.Label(
            header_frame,
            text="✨",
            font=("Segoe UI", 12),
            bg=bg_dark,
            fg=yellow
        ).place(x=x, y=y)

    # Main title with glow
    title_container = tk.Frame(header_frame, bg=bg_dark)
    title_container.place(relx=0.5, y=50, anchor=tk.CENTER)

    tk.Label(
        title_container,
        text="✨ AI CONTROL CENTER ✨",
        font=title_font,
        bg=bg_dark,
        fg=text_white
    ).pack()

    # Subtitle
    tk.Label(
        header_frame,
        text="Next-Generation AI Management System",
        font=("Segoe UI", 11, "italic"),
        bg=bg_dark,
        fg=purple
    ).place(relx=0.5, y=95, anchor=tk.CENTER)

    # Welcome section
    role_colors = {
        "admin": {"bg": pink, "glow": "#C51A5E"},
        "employee": {"bg": cyan, "glow": "#3DA39A"},
        "computer_user": {"bg": green, "glow": "#05CC84"}
    }

    welcome_container = tk.Frame(header_frame, bg=bg_dark)
    welcome_container.place(relx=0.5, y=130, anchor=tk.CENTER)

    tk.Label(
        welcome_container,
        text=f"Welcome back,",
        font=("Segoe UI", 12),
        bg=bg_dark,
        fg=text_gray
    ).pack(side=tk.LEFT, padx=5)

    tk.Label(
        welcome_container,
        text=f"{username}",
        font=("Segoe UI", 12, "bold"),
        bg=bg_dark,
        fg=text_white
    ).pack(side=tk.LEFT, padx=5)

    # Role badge
    role_color_set = role_colors.get(role, {"bg": purple, "glow": "#7B2FB8"})
    badge_glow = tk.Frame(welcome_container, bg=role_color_set["glow"], padx=2, pady=2)
    badge_glow.pack(side=tk.LEFT, padx=(15, 0))

    tk.Label(
        badge_glow,
        text=f" {role.upper()} ",
        font=("Segoe UI", 11, "bold"),
        bg=role_color_set["bg"],
        fg="white",
        padx=15,
        pady=6
    ).pack()

    # ===== STATS SECTION =====
    if role == "admin":
        stats_outer = tk.Frame(header_frame, bg=bg_dark)
        stats_outer.place(relx=0.5, y=175, anchor=tk.CENTER)

        create_stat_card(stats_outer, "Active Users", "24", "👥", purple, "#B57EFF")
        create_stat_card(stats_outer, "Systems Online", "12", "💻", blue, "#6FD7FF")
        create_stat_card(stats_outer, "AI Tasks Today", "48", "🤖", green, "#2BFFB8")
        create_stat_card(stats_outer, "Uptime", "99.9%", "⚡", orange, "#FFB366")

    # ===== MAIN CONTAINER =====
    main_container = tk.Frame(root, bg=bg_mid)
    main_container.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)

    # LEFT COLUMN (Controls)
    left_column = tk.Frame(main_container, bg=bg_mid, width=1000)
    left_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 15))

    # ===== ADMIN CONTROLS =====
    if role == "admin":
        admin_header = tk.Frame(left_column, bg=bg_mid)
        admin_header.pack(fill=tk.X, pady=(0, 20))

        tk.Frame(admin_header, bg=pink, width=5, height=30).pack(side=tk.LEFT)

        tk.Label(
            admin_header,
            text="⚡ ADMIN CONTROLS",
            font=section_font,
            bg=bg_mid,
            fg=text_white
        ).pack(side=tk.LEFT, padx=15)

        tk.Label(
            admin_header,
            text="Manage your organization",
            font=("Segoe UI", 9),
            bg=bg_mid,
            fg=text_gray
        ).pack(side=tk.LEFT, padx=10)

        # Admin buttons grid
        admin_grid = tk.Frame(left_column, bg=bg_mid)
        admin_grid.pack(fill=tk.X, pady=(0, 25))

        admin_buttons = [
            ("👤 Add Employee", add_employee.open_add_employee, purple, "#B87EFF"),
            ("📋 View Employees", view_employee.open_view_employee, pink, "#FF59A3"),
            ("💻 Add Computer User", add_computer.open_add_computer, blue, "#72D7FF"),
            ("🖥️ View Computer Users", view_computeruser.open_view_computeruser, cyan, "#6FE6DE")
        ]

        for i, (text, cmd, color, hover) in enumerate(admin_buttons):
            btn_container = GlowCard(admin_grid, glow_color=hover, bg=bg_mid)
            btn_container.grid(row=i // 2, column=i % 2, padx=12, pady=10, sticky='ew')

            ModernButton(
                btn_container,
                text=text,
                font=button_font,
                bg=color,
                hover_bg=hover,
                fg="white",
                activebackground=hover,
                activeforeground="white",
                command=cmd,
                width=40
            ).pack(padx=4, pady=4)

        admin_grid.columnconfigure(0, weight=1)
        admin_grid.columnconfigure(1, weight=1)

    # ===== AI CONTROLS =====
    ai_header = tk.Frame(left_column, bg=bg_mid)
    ai_header.pack(fill=tk.X, pady=(0, 20))

    tk.Frame(ai_header, bg=green, width=5, height=30).pack(side=tk.LEFT)

    tk.Label(
        ai_header,
        text="🚀 AI CONTROLS",
        font=section_font,
        bg=bg_mid,
        fg=text_white
    ).pack(side=tk.LEFT, padx=15)

    tk.Label(
        ai_header,
        text="Launch AI-powered tools",
        font=("Segoe UI", 9),
        bg=bg_mid,
        fg=text_gray
    ).pack(side=tk.LEFT, padx=10)

    # AI buttons
    ai_container = tk.Frame(left_column, bg=bg_mid)
    ai_container.pack(pady=10)

    ai_buttons_data = []

    if role != "employee":
        ai_buttons_data.append(("👆 Gesture Mouse", "Gesture_Controller.py", purple, "#B87EFF"))

    if role != "computer_user":
        ai_buttons_data.append(("⌨️ Virtual Keyboard", "keys.py", blue, "#72D7FF"))

    ai_buttons_data.append(("🎙️ Proton Assistant", "Proton.py", green, "#3BFFCA"))

    for text, script, color, hover in ai_buttons_data:
        btn_glow = GlowCard(ai_container, glow_color=hover, bg=bg_mid)
        btn_glow.pack(side=tk.LEFT, padx=15)

        ModernButton(
            btn_glow,
            text=text,
            font=button_font,
            bg=color,
            hover_bg=hover,
            fg="white",
            activebackground=hover,
            activeforeground="white",
            command=lambda s=script: run_script(s),
            width=20
        ).pack(padx=4, pady=4)

    # ===== QUICK ACTIONS =====
    if role == "admin":
        quick_header = tk.Frame(left_column, bg=bg_mid)
        quick_header.pack(fill=tk.X, pady=(25, 15))

        tk.Frame(quick_header, bg=orange, width=5, height=30).pack(side=tk.LEFT)

        tk.Label(
            quick_header,
            text="⚡ QUICK ACTIONS",
            font=section_font,
            bg=bg_mid,
            fg=text_white
        ).pack(side=tk.LEFT, padx=15)

        quick_container = tk.Frame(left_column, bg=bg_mid)
        quick_container.pack(pady=10)

        quick_actions = [
            ("📊", "Reports", blue, lambda: print("Reports")),
            ("⚙️", "Settings", purple, lambda: print("Settings")),
            ("🔔", "Alerts", orange, lambda: print("Alerts")),
            ("📈", "Analytics", green, lambda: print("Analytics"))
        ]

        for icon, text, color, cmd in quick_actions:
            create_quick_action(quick_container, icon, text, color, cmd)

    # ===== RIGHT SIDEBAR (Activity & Status) =====
    right_sidebar = tk.Frame(main_container, bg=bg_dark, width=400)
    right_sidebar.pack(side=tk.RIGHT, fill=tk.Y)
    right_sidebar.pack_propagate(False)

    # Activity Feed
    activity_header = tk.Frame(right_sidebar, bg=bg_dark)
    activity_header.pack(fill=tk.X, pady=20, padx=20)

    tk.Label(
        activity_header,
        text="📊 ACTIVITY FEED",
        font=("Segoe UI", 14, "bold"),
        bg=bg_dark,
        fg=text_white,
        anchor='w'
    ).pack(fill=tk.X)

    tk.Label(
        activity_header,
        text="Recent system events",
        font=("Segoe UI", 9),
        bg=bg_dark,
        fg=text_gray,
        anchor='w'
    ).pack(fill=tk.X, pady=(5, 0))

    # Activity items container
    activity_container = tk.Frame(right_sidebar, bg=bg_dark)
    activity_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(10, 20))

    activities = [
        ("👤", "New employee added", "2 min ago", purple),
        ("🤖", "AI task completed", "5 min ago", green),
        ("💻", "System update", "12 min ago", blue),
        ("⚡", "Performance optimized", "18 min ago", yellow),
        ("📊", "Report generated", "25 min ago", orange)
    ]

    for icon, text, time, color in activities:
        create_activity_item(activity_container, icon, text, time, color)

    # ===== FOOTER =====
    footer_frame = tk.Frame(root, bg=bg_dark, height=90)
    footer_frame.pack(side=tk.BOTTOM, fill=tk.X)
    footer_frame.pack_propagate(False)

    # Colorful gradient line
    gradient_line = tk.Frame(footer_frame, height=3)
    gradient_line.pack(fill=tk.X)

    for i, color in enumerate([purple, pink, blue, cyan, green, yellow, orange]):
        tk.Frame(gradient_line, bg=color, width=230).pack(side=tk.LEFT, fill=tk.Y)

    # Logout section
    logout_container = tk.Frame(footer_frame, bg=bg_dark)
    logout_container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    logout_glow = GlowCard(logout_container, glow_color="#FF8B8B", bg=bg_dark)
    logout_glow.pack()

    ModernButton(
        logout_glow,
        text="🚪 LOGOUT",
        font=button_font,
        bg=orange,
        hover_bg="#FF8E3C",
        fg="white",
        activebackground="#FF8E3C",
        activeforeground="white",
        command=root.destroy,
        width=25
    ).pack(padx=3, pady=3)

    # Version info
    tk.Label(
        footer_frame,
        text="AI Control Center v2.0 • Powered by Advanced AI",
        font=("Segoe UI", 8),
        bg=bg_dark,
        fg=text_gray
    ).place(relx=0.5, rely=0.85, anchor=tk.CENTER)

    root.mainloop()


# Test the dashboard
if __name__ == "__main__":
    # Mock functions for testing
    if 'add_employee' not in dir():
        class MockModule:
            @staticmethod
            def open_add_employee(): print("Add Employee")

            @staticmethod
            def open_view_employee(): print("View Employee")

            @staticmethod
            def open_add_computer(): print("Add Computer")

            @staticmethod
            def open_view_computeruser(): print("View Computer User")


        add_employee = view_employee = add_computer = view_computeruser = MockModule()

    open_dashboard("John Doe", "admin")