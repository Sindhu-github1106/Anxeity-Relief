import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
from datetime import datetime

# App setup
root = tk.Tk()
root.geometry("400x700")
root.title("Mindful Journal 🌿")
root.resizable(False, False)
if not os.path.exists("journals"):
    os.makedirs("journals")


def save_journal(month, content):
    """Save journal entry with timestamp in append mode"""
    if content.strip():
        timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]\n")
        with open(f"journals/{month}.txt", "a", encoding="utf-8") as f:
            f.write(f"{timestamp}{content}\n\n")


def open_journal(month):
    """Create journal window with flipbook-style interface (themed)"""
    journal_window = tk.Toplevel(root)
    journal_window.title(f"{month} Journal")
    journal_window.geometry("400x700")
    journal_window.configure(bg="#5c1305")  # dark background

    # Main container with parchment-like background
    main_frame = tk.Frame(journal_window, bg="#5c1305")
    main_frame.pack(fill="both", expand=True, padx=20, pady=10)

    # Header with month name
    header_frame = tk.Frame(main_frame, bg="#7e1d0a")
    header_frame.pack(fill="x", pady=(0, 10))
    tk.Label(header_frame, text=month, font=("Georgia", 18, "bold"),
             bg="#7e1d0a", fg="white").pack(pady=10)

    # Past entries display (read-only with scrollbar)
    entries_frame = tk.Frame(main_frame, bg="#5c1305")
    entries_frame.pack(fill="both", expand=True)

    scrollbar = ttk.Scrollbar(entries_frame)
    entries_text = tk.Text(entries_frame, wrap="word", font=("Georgia", 12),
                           bg="#fef0e1", fg="#5c1305", padx=15, pady=10,
                           relief="flat", spacing3=8, yscrollcommand=scrollbar.set)
    scrollbar.config(command=entries_text.yview)

    scrollbar.pack(side="right", fill="y")
    entries_text.pack(fill="both", expand=True)

    # Load existing entries in reverse chronological order
    filepath = f"journals/{month}.txt"
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            entries = [e.strip() for e in f.read().split("\n\n") if e.strip()]
            for entry in reversed(entries):
                entries_text.config(state="normal")
                entries_text.insert("end", entry + "\n\n")
                entries_text.config(state="disabled")

    entries_text.config(state="disabled")  # Make read-only

    # New entry section with save button
    new_entry_frame = tk.Frame(main_frame, bg="#5c1305")
    new_entry_frame.pack(fill="x", pady=(10, 0))

    tk.Label(new_entry_frame, text="New Entry:", font=("Georgia", 12, "bold"),
             bg="#5c1305", fg="#fef0e1").pack(anchor="w")

    new_entry = tk.Text(new_entry_frame, wrap="word", font=("Georgia", 12),
                        height=4, bg="#fef0e1", fg="#5c1305",
                        relief="flat", padx=10, pady=10)
    new_entry.pack(fill="x")

    def save_and_update():
        content = new_entry.get("1.0", "end-1c")
        if content.strip():
            save_journal(month, content)
            # Update display without reloading
            entries_text.config(state="normal")
            entries_text.insert("1.0", f"\n\n{datetime.now().strftime('[%Y-%m-%d %H:%M:%S]')}\n{content}")
            entries_text.config(state="disabled")
            new_entry.delete("1.0", "end")
            entries_text.yview_moveto(0)

    save_btn = tk.Button(new_entry_frame, text="✍️ Save Entry", command=save_and_update,
                         bg="#fe854f", fg="#7e1d0a", font=("Georgia", 12, "bold"),
                         activebackground="#7e1d0a", relief="flat")
    save_btn.pack(pady=10, ipadx=20)

# Custom colors to match the customtkinter version
bg_color = "#fef0e1"  # Light beige
container_color = "#e7c6b1"  # Light brown
button_color = "#5c1305"  # Dark brown
button_hover_color = "#b2422d"  # Lighter brown
text_color = "#5c1305"  # Dark brown

# Set background color
root.configure(bg=bg_color)

# Background frame
bg = tk.Frame(root, bg=bg_color)
bg.pack(fill="both", expand=True)

# --- HEADER ---
header_image_path = "assets/header.png"
if os.path.exists(header_image_path):
    header_img_raw = Image.open(header_image_path)
    header_img = ImageTk.PhotoImage(header_img_raw.resize((400, 220), Image.LANCZOS))
    header_label = tk.Label(bg, image=header_img, bg=bg_color)
    header_label.image = header_img  # Keep a reference
    header_label.place(x=0, y=-10)
else:
    header_label = tk.Label(bg, text="[Insert Header Image]",
                            font=("Georgia", 16), fg="#7e1d0a", bg=bg_color)
    header_label.place(x=0, y=0)


# --- Create a custom scrollable frame implementation ---
class ScrollableFrame(tk.Frame):
    def __init__(self, container, *args, **kwargs):
        bg_color = kwargs.pop('bg', container_color)
        self.canvas = tk.Canvas(container, bg=bg_color, highlightthickness=0)  # Removed fixed dimensions
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)

        self.scrollable_frame = tk.Frame(self.canvas, bg=bg_color)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas_frame = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.bind("<Configure>", self.resize_frame)

        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def resize_frame(self, event):
        self.canvas.itemconfig(self.canvas_frame, width=event.width)


# --- Month Container with rounded corners using a custom class ---
class RoundedFrame(tk.Frame):
    def __init__(self, parent, bg_color, corner_radius, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs, bg=bg_color)
        self.corner_radius = corner_radius

        # Create a canvas to draw the rounded rectangle
        self.canvas = tk.Canvas(self, bg=bg_color, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Draw the rounded rectangle on the canvas
        self.draw_rounded_rect()

        # Create a frame inside the canvas to hold content
        self.inner_frame = tk.Frame(self.canvas, bg=bg_color)
        self.inner_frame_id = self.canvas.create_window(0, 0, anchor="nw", window=self.inner_frame)

        # Bind canvas configure to adjust inner frame
        self.canvas.bind("<Configure>", self.on_canvas_configure)

    def on_canvas_configure(self, event):
        # Update the inner frame's size to match the canvas
        self.canvas.itemconfig(self.inner_frame_id, width=event.width, height=event.height)
        self.draw_rounded_rect()

    def draw_rounded_rect(self):
        self.canvas.delete("rounded_rect")
        width = self.winfo_width()
        height = self.winfo_height()

        if width > 1 and height > 1:
            # Draw rounded rectangle components
            self.canvas.create_rectangle(
                self.corner_radius, 0,
                width - self.corner_radius, height,
                fill=container_color, outline="", tags="rounded_rect"
            )
            self.canvas.create_rectangle(
                0, self.corner_radius,
                width, height - self.corner_radius,
                fill=container_color, outline="", tags="rounded_rect"
            )
            self.canvas.create_arc(
                0, 0,
                2 * self.corner_radius, 2 * self.corner_radius,
                start=90, extent=90, fill=container_color, outline="", tags="rounded_rect"
            )
            self.canvas.create_arc(
                width - 2 * self.corner_radius, 0,
                width, 2 * self.corner_radius,
                start=0, extent=90, fill=container_color, outline="", tags="rounded_rect"
            )
            self.canvas.create_arc(
                0, height - 2 * self.corner_radius,
                   2 * self.corner_radius, height,
                start=180, extent=90, fill=container_color, outline="", tags="rounded_rect"
            )
            self.canvas.create_arc(
                width - 2 * self.corner_radius, height - 2 * self.corner_radius,
                width, height,
                start=270, extent=90, fill=container_color, outline="", tags="rounded_rect"
            )


# Create the month container frame with rounded corners
month_frame_container = tk.Frame(bg, bg=bg_color)
month_frame_container.place(x=0, y=250, width=400, height=450)

# Create the rounded frame inside the container
rounded_frame = RoundedFrame(month_frame_container, bg_color=bg_color, corner_radius=40)
rounded_frame.pack(fill="both", expand=True)

# Add the scrollable frame inside the rounded frame
month_container = ScrollableFrame(rounded_frame.inner_frame)
month_container.canvas.pack(fill="both", expand=True)

# --- Greeting inside month container ---
greeting = tk.Label(month_container.scrollable_frame,
                    text="Hi 👋\nWrite mindful thoughts here",
                    font=("Georgia", 20, "bold"),
                    fg=text_color,
                    bg=container_color,
                    justify="left")
greeting.grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 10), sticky="w")

# --- Months Grid (Centered, Scrollable) ---
months = [
    "January", "February", "March", "April",
    "May", "June", "July", "August",
    "September", "October", "November", "December"
]


# Class for creating rounded buttons
class RoundedButton(tk.Canvas):
    def __init__(self, parent, text, command=None, width=120, height=120,
                 corner_radius=20, bg_color=button_color, hover_color=button_hover_color,
                 text_color="#7e1d0a", font=("Georgia", 14, "bold")):
        super().__init__(parent, width=width, height=height, bg=container_color,
                         highlightthickness=0)
        self.text = text
        self.command = command
        self.corner_radius = corner_radius
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.current_color = bg_color
        self.text_color = text_color
        self.font = font

        # Bind events
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click)

        # Draw initial button
        self.draw_rounded_rect()

    def draw_rounded_rect(self):
        self.delete("all")
        width, height = self.winfo_width(), self.winfo_height()

        if width < 2 or height < 2:
            width, height = 120, 120

        # Draw rounded rectangle components
        self.create_rectangle(
            self.corner_radius, 0,
            width - self.corner_radius, height,
            fill=self.current_color, outline=""
        )
        self.create_rectangle(
            0, self.corner_radius,
            width, height - self.corner_radius,
            fill=self.current_color, outline=""
        )
        self.create_arc(
            0, 0,
            2 * self.corner_radius, 2 * self.corner_radius,
            start=90, extent=90, fill=self.current_color, outline=""
        )
        self.create_arc(
            width - 2 * self.corner_radius, 0,
            width, 2 * self.corner_radius,
            start=0, extent=90, fill=self.current_color, outline=""
        )
        self.create_arc(
            0, height - 2 * self.corner_radius,
               2 * self.corner_radius, height,
            start=180, extent=90, fill=self.current_color, outline=""
        )
        self.create_arc(
            width - 2 * self.corner_radius, height - 2 * self.corner_radius,
            width, height,
            start=270, extent=90, fill=self.current_color, outline=""
        )
        self.create_text(width / 2, height / 2, text=self.text, fill=self.text_color, font=self.font)

    def on_enter(self, event):
        self.current_color = self.hover_color
        self.draw_rounded_rect()

    def on_leave(self, event):
        self.current_color = self.bg_color
        self.draw_rounded_rect()

    def on_click(self, event):
        if self.command:
            self.command()

def save_journal(month, content):
    with open(f"journals/{month}.txt", "w", encoding="utf-8") as f:
        f.write(content)

def open_journal(month):
    journal_window = tk.Toplevel(root)
    journal_window.title(f"{month} Journal")
    journal_window.geometry("400x700")
    journal_window.configure(bg="#fef0e1")

    label = tk.Label(journal_window, text=f"Your Journal for {month}", font=("Georgia", 18, "bold"), bg="#fef0e1", fg="#5c1305")
    label.pack(pady=20)

    text_box = tk.Text(journal_window, wrap="word", font=("Georgia", 14), bg="#fffaf5", fg="#5c1305", padx=10, pady=10, relief="flat")
    text_box.pack(expand=True, fill="both", padx=20, pady=10)

    # Load saved journal content if exists
    filepath = f"journals/{month}.txt"
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            text_box.insert("1.0", f.read())

    save_btn = tk.Button(journal_window, text="Save", font=("Georgia", 12, "bold"), bg="#5c1305", fg="#7e1d0a", command=lambda: save_journal(month, text_box.get("1.0", "end-1c")))
    save_btn.pack(pady=10)

months = [
    "January", "February", "March", "April",
    "May", "June", "July", "August",
    "September", "October", "November", "December"
]

current_month_index = datetime.now().month  # 1 to 12



# Replace the tk.Button code with this RoundedButton implementation
for i, m in enumerate(months):
    row = (i // 2) + 1
    col = i % 2
    is_future = (i + 1) > current_month_index


    def handle_click(month=m, future=is_future):
        if not future:
            open_journal(month)


    btn = RoundedButton(
        month_container.scrollable_frame,
        text=m,
        width=120,
        height=120,
        corner_radius=20,
        bg_color=button_color if not is_future else "#e27f6b",
        hover_color="#fe854f" if not is_future else "#c5482f",
        text_color="white" if not is_future else "#7e1d0a",
        font=("Georgia", 14, "bold"),
        command=lambda m=m, f=is_future: open_journal(m) if not f else None
    )

    if is_future:
        btn.unbind("<Button-1>")  # Optional if you want to *fully* disable it
    btn.grid(row=row, column=col, padx=20, pady=10, sticky="nsew")

# Configure grid weights to allow proper expansion
month_container.scrollable_frame.grid_columnconfigure(0, weight=1)
month_container.scrollable_frame.grid_columnconfigure(1, weight=1)
for i in range((len(months) // 2) + 2):
    month_container.scrollable_frame.grid_rowconfigure(i, weight=1)

root.mainloop()