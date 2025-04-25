from tkinter import *
from PIL import ImageTk, Image
from tkinter import simpledialog
from tkinter import messagebox
from tkinter import font
import tkinter as tk
from tkinter import ttk
from pygame import mixer
import random
import time
import os
import threading
import serial
from datetime import datetime
import cv2
from PIL import Image, ImageTk, ImageDraw

from tkinter import font as tkfont, simpledialog, messagebox, filedialog

simulate_anxiety=False

cap = cv2.VideoCapture("videos/meditate.mp4")

 # Custom colors to match the customtkinter version
bg_color = "#fef0e1"  # Light beige
container_color = "#e7c6b1"  # Light brown
button_color = "#5c1305"  # Dark brown
button_hover_color = "#b2422d"  # Lighter brown
text_color = "#5c1305"  # Dark brown

current_bpm = "---"



def read_serial():
    global current_bpm
    arduino_port = 'COM9'  # Change to your Arduino port
    baud_rate = 9600
    
    try:
        ser = serial.Serial(arduino_port, baud_rate)
        print("Connected to Arduino!")

        while True:
            line = ser.readline().decode('utf-8').strip()
            if "BPM" in line:
                current_bpm = ''.join([c for c in line if c.isdigit()])
                # Update the BPM label if it exists
                if 'bpm_label' in globals():
                    bpm_label.config(text=f"   {current_bpm}")

    except serial.SerialException:
        print("Could not connect to Arduino. Check the port.")
    except KeyboardInterrupt:
        print("Stopped.")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()

# Start serial reading in a separate thread
serial_thread = threading.Thread(target=read_serial, daemon=True)
serial_thread.start()

def rounded_rect_image(width, height, radius, color):
    img = Image.new("RGBA", (width, height), (255, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle((0, 0, width, height), radius, fill=color)
    return ImageTk.PhotoImage(img)


def get_greeting():
    current_hour = time.localtime().tm_hour
    if 5 <= current_hour < 12:
        return "Good Morning"
    elif 12 <= current_hour < 17:
        return "Good Afternoon"
    else:
        return "Good Evening"


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
    screen_width = journal_window.winfo_screenwidth()
    screen_height = journal_window.winfo_screenheight()

    # Set window size
    window_width = 400
    window_height = 700

    # Calculate position to center the window
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2

    # Set geometry to center the window
    journal_window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
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


    


########



def journal():
    
    
    mywin = Toplevel()
    screen_width = mywin.winfo_screenwidth()
    screen_height = mywin.winfo_screenheight()

    # Set window size
    window_width = 400
    window_height = 700

    # Calculate position to center the window
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2

    # Set geometry to center the window
    mywin.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
    mywin.title("Mindful Journal 🌿")
    mywin.resizable(False, False)
    
    if not os.path.exists("journals"):
        os.makedirs("journals")
    
   

    # Set background color
    mywin.configure(bg=bg_color)

    # Background frame
    bg = tk.Frame(mywin, bg=bg_color)
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
    
    # Create the month container frame with rounded corners
    month_frame_container = tk.Frame(bg, bg=bg_color)
    month_frame_container.place(x=0, y=250, width=400, height=450)
    
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
    greeting.grid(row=0, column=0, columnspan=2, sticky="w")

    # --- Months Grid (Centered, Scrollable) ---
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
    
    month_container.scrollable_frame.grid_columnconfigure(0, weight=1)
    month_container.scrollable_frame.grid_columnconfigure(1, weight=1)
    for i in range((len(months) // 2) + 2):
        month_container.scrollable_frame.grid_rowconfigure(i, weight=1)

    # Handle window closing properly
    def on_close():
        mywin.destroy()
        mainpg()

    mywin.protocol("WM_DELETE_WINDOW", on_close)
    
    mywin.mainloop()

def account():
    mywin = tk.Toplevel()
    creen_width = mywin.winfo_screenwidth()
    screen_height = mywin.winfo_screenheight()

    # Set window size
    window_width = 400
    window_height = 700

    # Calculate position to center the window
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2

    # Set geometry to center the window
    mywin.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
    mywin.title("Meditation Profile")
    mywin.configure(bg="#fef0e1")

    # Fonts
    title_font = tkfont.Font(family="Helvetica", size=22, weight="bold")
    section_font = tkfont.Font(family="Helvetica", size=16, weight="bold")
    normal_font = tkfont.Font(family="Helvetica", size=12)

    # ---- Title with Greeting ----
    greeting = get_greeting()
    tk.Label(mywin, text=f"{greeting}, Sophia!", font=title_font, fg="#b2422d", bg="#fef0e1").pack(pady=20)

    # ---- Profile Card ----
    card_width, card_height = 340, 200
    rounded_card_img = rounded_rect_image(card_width, card_height, 25, "#e58572")
    card_canvas = tk.Canvas(mywin, width=card_width + 20, height=card_height + 20, bg="#fef0e1", highlightthickness=0)
    card_canvas.create_image(10, 10, image=rounded_card_img, anchor="nw")
    card_canvas.pack(pady=20)

    # ---- Functions to Upload Photo and Edit Name ----
    def upload_photo():
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg")])
        if file_path:
            try:
                img = Image.open(file_path).resize((100, 100))
                new_photo = ImageTk.PhotoImage(img)
                avatar.configure(image=new_photo)
                avatar.image = new_photo
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {e}")

    def edit_name(event=None):
        new_name = simpledialog.askstring("Edit Name", "Enter new name:")
        if new_name:
            name.config(text=new_name)

    # Profile Picture
    try:
        profile_img = Image.open("profile_picture.jpg").resize((100, 100))
        profile_photo = ImageTk.PhotoImage(profile_img)
    except FileNotFoundError:
        profile_photo = ImageTk.PhotoImage(Image.new("RGB", (100, 100), "#fef0e1"))

    avatar = tk.Label(mywin, image=profile_photo, bg="#e58572", cursor="hand2")
    avatar.bind("<Button-1>", lambda e: upload_photo())
    card_canvas.create_window(card_width // 2 + 10, 60, window=avatar)

    name = tk.Label(mywin, text="Sophia", font=title_font, fg="#b2422d", bg="#e58572", cursor="xterm")
    name.bind("<Button-1>", edit_name)
    card_canvas.create_window(card_width // 2 + 10, 120, window=name)

    uid = tk.Label(mywin, text="Calm ID: 12934", font=normal_font, fg="#3E3E3E", bg="#e58572")
    card_canvas.create_window(card_width // 2 + 10, 150, window=uid)

    # ---- Rounded Button Factory ----
    def rounded_button(master, text, bg_color, command=None):
        width, height = 140, 40
        radius = 20
        img = rounded_rect_image(width, height, radius, bg_color)
        canvas = tk.Canvas(master, width=width, height=height, bg="#fef0e1", highlightthickness=0)
        canvas.create_image(0, 0, image=img, anchor="nw")
        btn = tk.Button(canvas, text=text, bg=bg_color, fg="white", font=normal_font, bd=0,
                        activebackground=bg_color, command=command)
        canvas.create_window(width // 2, height // 2, window=btn)
        canvas.image = img
        return canvas

    # ---- Connected Devices Card ----
    device_card_height = 240
    device_card_img = rounded_rect_image(card_width, device_card_height, 25, "#e58572")
    device_canvas = tk.Canvas(mywin, width=card_width + 20, height=device_card_height + 20, bg="#fef0e1",
                              highlightthickness=0)
    device_canvas.create_image(10, 10, image=device_card_img, anchor="nw")
    device_canvas.pack(pady=10)

    # Section Title
    title_label = tk.Label(mywin, text="Connected Devices", font=section_font, fg="#b2422d", bg="#e58572")
    device_canvas.create_window(card_width // 2 + 10, 20, window=title_label)

    device_list_frame = tk.Frame(mywin, bg="#e58572")
    device_canvas.create_window(card_width // 2 + 10, 110, window=device_list_frame)

    devices = ["iPhone 16 Pro Max", "Air Pods Pro 3", "iPad Mini"]

    def create_device_row(name):
        row = tk.Frame(device_list_frame, bg="#e58572")
        row.pack(fill="x", pady=5, padx=10)
        dev_label = tk.Label(row, text=name, font=normal_font, bg="#e58572", fg="#3E3E3E")
        dev_label.pack(side=tk.LEFT)
        rename_btn = tk.Button(row, text="Rename", font=("Arial", 8), bg="#e58572", fg="#fef0e1", relief="flat",
                               command=lambda name=name: rename_device(name))
        rename_btn.pack(side=tk.RIGHT, padx=5)
        remove_btn = tk.Button(row, text="Remove", font=("Arial", 8), bg="#e58572", fg="#fef0e1", relief="flat",
                               command=lambda name=name: remove_device(name))
        remove_btn.pack(side=tk.RIGHT, padx=5)

    def rename_device(device_name):
        new_name = simpledialog.askstring("Rename Device", f"Enter new name for {device_name}:")
        if new_name:
            update_device_list(device_name, new_name)

    def remove_device(device_name):
        if messagebox.askyesno("Remove Device", f"Are you sure you want to remove '{device_name}'?"):
            devices.remove(device_name)
            update_device_list()

    def update_device_list(old_name=None, new_name=None):
        for widget in device_list_frame.winfo_children():
            widget.destroy()
        if old_name and new_name:
            devices[devices.index(old_name)] = new_name
        for device in devices:
            create_device_row(device)

    def add_device():
        new_device_name = simpledialog.askstring("Add Device", "Enter the name of the new device:")
        if new_device_name:
            devices.append(new_device_name)
            update_device_list()

    # Populate initial device list
    for device in devices:
        create_device_row(device)

    # Add Device Button
    add_button = rounded_button(mywin, "➕ Add Device", "#b2422d", add_device)
    add_button.pack(pady=25)

    mywin.mainloop()
    
def breathe():
    mywin = Toplevel()
    
    screen_width = mywin.winfo_screenwidth()
    screen_height = mywin.winfo_screenheight()

    # Set window size
    window_width = 400
    window_height = 700

    # Calculate position to center the window
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2

    # Set geometry to center the window
    mywin.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
    
    bg = PhotoImage(file = "templates/breathing.png")
    label1 = Label( mywin, image = bg)
    label1.place(x = 0, y = 0)
    
    back_btn0= PhotoImage(file='templates/back.png')
    button0= Button(mywin, image=back_btn0, command=mainpg, borderwidth=0)
    button0.place(x=25, y=25)
    
    click_btn2 = PhotoImage(file='templates/account_btn.png')
    button2 = Button(mywin, image=click_btn2, command=account, borderwidth=0)
    button2.place(x=310, y=20)
    
    click_btn_= PhotoImage(file='templates/breathing_start.png')
    button1= Button(mywin, image=click_btn_,command= techniques,borderwidth=0)
    button1.place(x=50, y=600)
    
    
    
    mywin.mainloop()
    
def box():
    
    def update_timer_and_instruction(elapsed):
        nonlocal current_phase  # Declare nonlocal first
        
        remaining = max(0, 16 - elapsed)
        timer_label.config(text=f"{int(remaining//60)}:{int(remaining%60):02d}")
        
        # Update breathing instruction based on phase
        phase_time = elapsed % 16  # Within current 16-second cycle
        if phase_time < 4:
            new_phase = "Inhale"
        elif phase_time < 8:
            new_phase = "Hold"
        elif phase_time < 12:
            new_phase = "Exhale"
        else:
            new_phase = "Hold"
        
        if new_phase != current_phase:
            instruction_label.config(text=new_phase)
            current_phase = new_phase
    
    def animate():
        nonlocal is_paused, start_time, total_paused, anim_id
        
        if is_paused:
            return
            
        current_time = time.time()
        elapsed = current_time - start_time - total_paused
        progress = min(elapsed / 16, 1.0)
        angle = progress * 360
        
        canvas.itemconfig(arc, extent=-angle)  # Negative for clockwise
        update_timer_and_instruction(elapsed)
        
        if progress < 1.0:
            anim_id = mywin.after(16, animate)
        else:
            reset_animation()
            start_animation()
    
    def start_animation():
        nonlocal is_paused, start_time, total_paused, current_phase
        if is_paused:
            total_paused += time.time() - pause_time
            is_paused = False
            toggle_btn.config(image=pause_img)
            instruction_label.config(text="Inhale")
            current_phase = "Inhale"
            animate()
    
    def pause_animation():
        nonlocal is_paused, pause_time, current_phase
        if not is_paused:
            is_paused = True
            pause_time = time.time()
            toggle_btn.config(image=resume_img)
            instruction_label.config(text="Paused")
            current_phase = "Paused"
    
    def reset_animation():
        nonlocal is_paused, start_time, total_paused, current_phase
        canvas.itemconfig(arc, extent=0)
        start_time = time.time()
        total_paused = 0
        current_phase = "Ready"
        timer_label.config(text="0:16")
        instruction_label.config(text="Press Resume to begin")
        if not is_paused:
            pause_animation()
    
    def toggle_animation():
        if is_paused:
            start_animation()
        else:
            pause_animation()
    
    
    mywin = Toplevel()
    
    # Window setup
    screen_width = mywin.winfo_screenwidth()
    screen_height = mywin.winfo_screenheight()
    window_width, window_height = 400, 700
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2
    mywin.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
    
    # Background
    bg = PhotoImage(file="templates/breathe.png")
    label1 = Label(mywin, image=bg)
    label1.place(x=0, y=0)
    
    # Navigation buttons
    back_btn0 = PhotoImage(file='templates/back.png')
    button0 = Button(mywin, image=back_btn0, command=techniques, 
                    borderwidth=0, highlightthickness=0, relief='flat')
    button0.place(x=25, y=25)
    
    account_btn = PhotoImage(file='templates/account_btn.png')
    button2 = Button(mywin, image=account_btn, command=account, 
                    borderwidth=0, highlightthickness=0, relief='flat')
    button2.place(x=310, y=20)
    
    # Animation control variables
    is_paused = True  # Start paused
    start_time = 0
    pause_time = 0
    total_paused = 0
    anim_id = None
    current_phase = "Ready"  # Track breathing phase
    
    # Animation canvas
    canvas = Canvas(mywin, width=300, height=300, bg="#fef0e1", highlightthickness=0)
    canvas.place(x=50, y=150)
    arc = canvas.create_arc(50, 50, 250, 250, start=90, extent=0,
                          outline="#be685d", style="arc", width=8)
    
    # Timer display
    timer_label = Label(mywin, text="0:16", font=("Arial", 24), bg="#fef0e1", fg="#be685d")
    timer_label.place(x=180, y=120, anchor="center")
    
    # Breathing instruction
    instruction_label = Label(mywin, text="Press Resume to begin", font=("Arial", 16), 
                            bg="#fef0e1", fg="#be685d")
    instruction_label.place(x=200, y=470, anchor="center")
    
    # Button images
    pause_img = PhotoImage(file='templates/pause.png')
    resume_img = PhotoImage(file='templates/resume.png')
    reset_img = PhotoImage(file='templates/reset.png')
    
    # Control buttons frame
    control_frame = Frame(mywin, bg='#fef0e1')
    control_frame.place(x=30, y=550, width=400, height=100)
    
    # Toggle button
    toggle_btn = Button(control_frame, image=pause_img, command=lambda: toggle_animation(),
                       borderwidth=0, highlightthickness=0, relief='flat')
    toggle_btn.pack(side=LEFT, padx=20)
    
    # Reset button
    reset_btn = Button(control_frame, image=reset_img, command=reset_animation,
                      borderwidth=0, highlightthickness=0, relief='flat')
    reset_btn.pack(side=LEFT, padx=20)
    
    
    
    # Start with animation paused (showing resume button)
    toggle_btn.config(image=resume_img)
    
    mywin.mainloop()
    
def b446():
    
    
    def update_timer_and_instruction(elapsed):
        nonlocal current_phase
        
        remaining = max(0, TOTAL_DURATION - elapsed)
        timer_label.config(text=f"0:{int(remaining):02d}")
        
        # Update breathing instruction based on phase
        if elapsed < INHALE_DURATION:
            new_phase = "Inhale"
            progress = elapsed / INHALE_DURATION
        elif elapsed < INHALE_DURATION + HOLD_DURATION:
            new_phase = "Hold"
            progress = (elapsed - INHALE_DURATION) / HOLD_DURATION
        else:
            new_phase = "Exhale"
            progress = (elapsed - INHALE_DURATION - HOLD_DURATION) / EXHALE_DURATION
        
        # Update arc based on current phase
        if new_phase == "Inhale":
            angle = progress * 360  # Clockwise for inhale
            canvas.itemconfig(arc, extent=-angle)
        elif new_phase == "Hold":
            canvas.itemconfig(arc, extent=-360)  # Full circle during hold
        else:  # Exhale
            angle = progress * 360  # Clockwise for exhale
            canvas.itemconfig(arc, extent=angle)  # Counter-clockwise animation
        
        if new_phase != current_phase:
            instruction_label.config(text=new_phase)
            current_phase = new_phase
    
    def animate():
        nonlocal is_paused, start_time, total_paused, anim_id
        
        if is_paused:
            return
            
        current_time = time.time()
        elapsed = current_time - start_time - total_paused
        progress = min(elapsed / TOTAL_DURATION, 1.0)
        
        update_timer_and_instruction(elapsed)
        
        if progress < 1.0:
            anim_id = mywin.after(16, animate)
        else:
            reset_animation()
            start_animation()
    
    def start_animation():
        nonlocal is_paused, start_time, total_paused, current_phase
        if is_paused:
            total_paused += time.time() - pause_time
            is_paused = False
            toggle_btn.config(image=pause_img)
            instruction_label.config(text="Inhale")
            current_phase = "Inhale"
            animate()
    
    def pause_animation():
        nonlocal is_paused, pause_time, current_phase
        if not is_paused:
            is_paused = True
            pause_time = time.time()
            toggle_btn.config(image=resume_img)
            instruction_label.config(text="Paused")
            current_phase = "Paused"
    
    def reset_animation():
        nonlocal is_paused, start_time, total_paused, current_phase
        canvas.itemconfig(arc, extent=0)
        start_time = time.time()
        total_paused = 0
        current_phase = "Ready"
        timer_label.config(text=f"0:{TOTAL_DURATION:02d}")
        instruction_label.config(text="Press Resume to begin")
        if not is_paused:
            pause_animation()
    
    def toggle_animation():
        if is_paused:
            start_animation()
        else:
            pause_animation()
    
    
    
    mywin = Toplevel()
    
    # Window setup
    screen_width = mywin.winfo_screenwidth()
    screen_height = mywin.winfo_screenheight()
    window_width, window_height = 400, 700
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2
    mywin.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
    
    # Background
    bg = PhotoImage(file="templates/breathe.png")
    label1 = Label(mywin, image=bg)
    label1.place(x=0, y=0)
    
    # Navigation buttons
    back_btn0 = PhotoImage(file='templates/back.png')
    button0 = Button(mywin, image=back_btn0, command=techniques, 
                    borderwidth=0, highlightthickness=0, relief='flat')
    button0.place(x=25, y=25)
    
    account_btn = PhotoImage(file='templates/account_btn.png')
    button2 = Button(mywin, image=account_btn, command=account, 
                    borderwidth=0, highlightthickness=0, relief='flat')
    button2.place(x=310, y=20)
    
    # Breathing pattern configuration
    INHALE_DURATION = 4
    HOLD_DURATION = 4
    EXHALE_DURATION = 6
    TOTAL_DURATION = INHALE_DURATION + HOLD_DURATION + EXHALE_DURATION
    
    # Animation control variables
    is_paused = True  # Start paused
    start_time = 0
    pause_time = 0
    total_paused = 0
    anim_id = None
    current_phase = "Ready"  # Track breathing phase
    
    # Animation canvas
    canvas = Canvas(mywin, width=300, height=300, bg="#fef0e1", highlightthickness=0)
    canvas.place(x=50, y=150)
    arc = canvas.create_arc(50, 50, 250, 250, start=90, extent=0,
                          outline="#be685d", style="arc", width=8)
    
    # Timer display
    timer_label = Label(mywin, text=f"0:{TOTAL_DURATION:02d}", font=("Arial", 24), bg="#fef0e1", fg="#be685d")
    timer_label.place(x=180, y=120, anchor="center")
    
    # Breathing instruction
    instruction_label = Label(mywin, text="Press Resume to begin", font=("Arial", 16), 
                            bg="#fef0e1", fg="#be685d")
    instruction_label.place(x=200, y=470, anchor="center")
    
    # Button images
    pause_img = PhotoImage(file='templates/pause.png')
    resume_img = PhotoImage(file='templates/resume.png')
    reset_img = PhotoImage(file='templates/reset.png')
    
    # Control buttons frame
    control_frame = Frame(mywin, bg='#fef0e1')
    control_frame.place(x=30, y=550, width=400, height=100)
    
    # Toggle button
    toggle_btn = Button(control_frame, image=pause_img, command=lambda: toggle_animation(),
                       borderwidth=0, highlightthickness=0, relief='flat')
    toggle_btn.pack(side=LEFT, padx=20)
    
    # Reset button
    reset_btn = Button(control_frame, image=reset_img, command=reset_animation,
                      borderwidth=0, highlightthickness=0, relief='flat')
    reset_btn.pack(side=LEFT, padx=20)
    
    
    
    # Start with animation paused (showing resume button)
    toggle_btn.config(image=resume_img)
    
    mywin.mainloop()

def techniques():
    mywin = Toplevel()
    
    screen_width = mywin.winfo_screenwidth()
    screen_height = mywin.winfo_screenheight()

    # Set window size
    window_width = 400
    window_height = 700

    # Calculate position to center the window
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2

    # Set geometry to center the window
    mywin.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
    
    bg = PhotoImage(file = "templates/techniques.png")
    label1 = Label( mywin, image = bg)
    label1.place(x = 0, y = 0)
    
    back_btn0= PhotoImage(file='templates/back.png')
    button0= Button(mywin, image=back_btn0, command=breathe, borderwidth=0,highlightthickness=0, relief='flat')
    button0.place(x=25, y=25)
    
    click_btn2 = PhotoImage(file='templates/account_btn.png')
    button2 = Button(mywin, image=click_btn2, command=account, borderwidth=0,highlightthickness=0, relief='flat')
    button2.place(x=310, y=20)
    
    click_btn_= PhotoImage(file='templates/startbox.png')
    button1= Button(mywin, image=click_btn_,command= box,borderwidth=0,highlightthickness=0, relief='flat')
    button1.place(x=45, y=540)
    
    click_btn3= PhotoImage(file='templates/start446.png')
    button3= Button(mywin, image=click_btn3,command= b446,borderwidth=0,highlightthickness=0, relief='flat')
    button3.place(x=230, y=540)
    
    if simulate_anxiety==True:
        rec = PhotoImage(file = "templates/box_rec.png")
        label2 = Label( mywin, image = rec)
        label2.place(x = 220, y = 600)
        
    elif current_bpm!="---":
        if int(current_bpm)>100:
            rec = PhotoImage(file = "templates/box_rec.png")
            label2 = Label( mywin, image = rec,borderwidth=0,highlightthickness=0, relief='flat')
            label2.place(x = 220, y = 618)
    else:
        rec = PhotoImage(file = "templates/any_rec.png")
        label2 = Label( mywin, image = rec,borderwidth=0,highlightthickness=0, relief='flat')
        label2.place(x = 220, y = 618)
    
    mywin.mainloop()



def sounds():
    
    
    
    mywin = Toplevel()

    # Initialize pygame mixer
    mixer.init()
    
    # Window dimensions and positioning
    screen_width = mywin.winfo_screenwidth()
    screen_height = mywin.winfo_screenheight()
    window_width = 400
    window_height = 700
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2
    mywin.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
    
    # Background image
    bg = PhotoImage(file="templates/sounds.png")
    label1 = Label(mywin, image=bg)
    label1.place(x=0, y=0)
    
    # Top buttons (unchanged)
    back_btn0 = PhotoImage(file='templates/echoback.png')
    button0 = Button(mywin, image=back_btn0, command=mainpg, borderwidth=0, highlightthickness=0, relief='flat')
    button0.place(x=25, y=25)
    
    click_btn2 = PhotoImage(file='templates/echo_profile.png')
    button2 = Button(mywin, image=click_btn2, command=account, borderwidth=0, highlightthickness=0, relief='flat')
    button2.place(x=310, y=20)
    
    meditate = PhotoImage(file='templates/meditate.png')
    button3 = Button(mywin, image=meditate, command=None, borderwidth=0, highlightthickness=0, relief='flat')
    button3.place(x=60, y=110)

    # --- Volume Control (without label) ---
    volume_frame = Frame(mywin, bg='#9f4a35')
    volume_frame.place(x=50, y=520, width=300, height=50)  # Reduced height
    
    volume_slider = tk.Scale(volume_frame, from_=0, to=100, orient=tk.HORIZONTAL, 
                            bg='#9f4a35', fg='white', highlightthickness=0,
                            command=lambda val: mixer.music.set_volume(float(val)/100))
    volume_slider.set(70)  # Default volume
    volume_slider.pack(fill='x', padx=20, pady=5)  # Adjusted padding
    
    # Set initial volume
    mixer.music.set_volume(0.7)

    # --- Create horizontal scrollable area for sound buttons ---
    scroll_frame = Frame(mywin, bg='#9f4a35')
    scroll_frame.place(x=0, y=580, width=400, height=120)

    canvas = Canvas(scroll_frame, bg='#9f4a35', height=120, width=400, highlightthickness=0)
    h_scroll = Scrollbar(scroll_frame, orient="horizontal", command=canvas.xview)
    canvas.configure(xscrollcommand=h_scroll.set)

    h_scroll.pack(side="bottom", fill="x")
    canvas.pack(side="top", fill="both", expand=True)

    inner_frame = Frame(canvas, bg='#9f4a35')
    canvas.create_window((0, 0), window=inner_frame, anchor="nw")

    # Function to play sounds
    def play_sound(sound_file):
        mixer.music.stop()
        mixer.music.load(f"sounds/{sound_file}")
        mixer.music.play()

    # Load button images and create sound buttons
    btn_images = [
        ('rain.png', 'rain.mp3'),
        ('fireplace.png', 'fireplace.mp3'),
        ('ocean.png', 'ocean.mp3'),
        ('piano.png', 'piano.mp3')
    ]

    inner_frame.btn_images = []
    for img_file, sound_file in btn_images:
        btn_img = PhotoImage(file=f'templates/{img_file}')
        inner_frame.btn_images.append(btn_img)  # Keep reference
        
        btn = Button(inner_frame, image=btn_img, 
                    command=lambda sf=sound_file: play_sound(sf),
                    borderwidth=0, highlightthickness=0, relief='flat')
        btn.pack(side="left", padx=20, pady=20)

    # Update scroll region when inner frame changes
    def update_scroll_region(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    inner_frame.bind("<Configure>", update_scroll_region)

    def on_close():
        mixer.music.stop()
        mywin.destroy()
        root.deiconify()

    mywin.protocol("WM_DELETE_WINDOW", on_close)
    
    mywin.mainloop()

def echo():
    mywin = Toplevel()

    screen_width = mywin.winfo_screenwidth()
    screen_height = mywin.winfo_screenheight()

    # Set window size
    window_width = 400
    window_height = 700

    # Calculate position to center the window
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2

    # Set geometry to center the window
    mywin.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
    
    bg = PhotoImage(file = "templates/echo.png")
    label1 = Label( mywin, image = bg)
    label1.place(x = 0, y = 0)
    
    back_btn0= PhotoImage(file='templates/echo_next.png')
    button0= Button(mywin, image=back_btn0, command=sounds, borderwidth=0, highlightthickness=0, relief='flat')
    button0.place(x=300, y=600)
    
    
    mywin.mainloop()
    

def detected():
    mywin = Toplevel()

    # Initialize pygame mixer and play background music
    mixer.init()
    try:
        mixer.music.load("sounds/bgmanxiety.mp3")  # Path to your MP3 file
        mixer.music.set_volume(0.5)  # 50% volume (adjust as needed)
        mixer.music.play(-1)  # -1 makes it loop indefinitely
    except:
        print("Could not load background music")

    screen_width = mywin.winfo_screenwidth()
    screen_height = mywin.winfo_screenheight()

    # Set window size and position
    window_width = 400
    window_height = 700
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2
    mywin.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
    
    # Background image
    bg = PhotoImage(file="templates/detected.png")
    label1 = Label(mywin, image=bg)
    label1.place(x=0, y=0)
    
    # Navigation buttons
    back_btn0 = PhotoImage(file='templates/exit.png')
    Button(mywin, image=back_btn0, command=lambda: [mixer.music.stop(), mainpg()], 
          borderwidth=0, highlightthickness=0, relief='flat').place(x=50, y=600)
    
    # Stop music when window is closed
    def on_close():
        mixer.music.stop()
        mywin.destroy()
    
    mywin.protocol("WM_DELETE_WINDOW", on_close)
    mywin.mainloop()

def mainpg():
    mywin = Toplevel()

    screen_width = mywin.winfo_screenwidth()
    screen_height = mywin.winfo_screenheight()

    # Set window size and position
    window_width = 400
    window_height = 700
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2
    mywin.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
    
    # Background image
    bg = PhotoImage(file="templates/mainpg.png")
    label1 = Label(mywin, image=bg)
    label1.place(x=0, y=0)
    
    # Navigation buttons
    back_btn0 = PhotoImage(file='templates/back.png')
    Button(mywin, image=back_btn0, command=mywin.withdraw, borderwidth=0).place(x=25, y=25)
    
    account_btn = PhotoImage(file='templates/account_btn.png')
    Button(mywin, image=account_btn, command=account, borderwidth=0).place(x=310, y=20)

    # Centered pulse animation with BPM display
    center_frame = Frame(mywin, width=250, height=250, bg="#fef0e1")
    center_frame.place(x=75, y=200)  # Adjusted x position for better centering

    canvas = Canvas(center_frame, width=250, height=250, bg="#fef0e1", highlightthickness=0)
    canvas.pack()

    center_x = 125  # Centered in the 250x250 canvas
    center_y = 60
    base_radius = 60
    pulse_range = 3
    pulse_speed = 50
    
    # BPM display label (global so serial thread can update it)
    global bpm_label, simulate_anxiety
    
    if simulate_anxiety==True:
        simulate_anxiety=False
        mywin.withdraw()
        detected()
    if current_bpm!="---":
        if int(current_bpm)>100 :
            detected()
    bpm_label = Label(canvas, text=f"   {current_bpm} ", font=("Arial", 24, "bold"), 
                     bg="#ff9999", fg="#5c1305")
    bpm_label.place(x=center_x-50, y=center_y-15)  # Centered on the circle

    state = {
        "radius": base_radius,
        "growing": True,
        "circle": canvas.create_oval(center_x - base_radius, center_y - base_radius,
                                   center_x + base_radius, center_y + base_radius,
                                   fill="#ff9999", outline="")
    }

    def animate():
        canvas.delete(state["circle"])

        if state["growing"]:
            state["radius"] += 0.5
            if state["radius"] >= base_radius + pulse_range:
                state["growing"] = False
        else:
            state["radius"] -= 0.5
            if state["radius"] <= base_radius - pulse_range:
                state["growing"] = True

        r = state["radius"]
        state["circle"] = canvas.create_oval(center_x - r, center_y - r,
                                           center_x + r, center_y + r,
                                           fill="#ff9999", outline="")

        mywin.after(pulse_speed, animate)

    animate()

    # Scrollable button section (unchanged from your original code)
    bottom_frame = Frame(mywin, width=400, height=300, bg="#fef0e1")
    bottom_frame.place(x=0, y=360)

    button_canvas = Canvas(bottom_frame, width=400, height=300, bg="#fef0e1", highlightthickness=0)
    button_canvas.pack(side="top", fill="x")

    h_scroll = Scrollbar(bottom_frame, orient="horizontal", command=button_canvas.xview)
    h_scroll.pack(side="bottom", fill="x")
    button_canvas.configure(xscrollcommand=h_scroll.set)

    inner_frame = Frame(button_canvas, bg="#fef0e1")
    button_canvas.create_window((0, 0), window=inner_frame, anchor="nw")

    # Load button images
    image1 = Image.open("templates/journal_btn.png")
    image2 = Image.open("templates/echo_btn.png")
    image3 = Image.open("templates/breathe_btn.png")
    img1 = ImageTk.PhotoImage(image1)
    img2 = ImageTk.PhotoImage(image2)
    img3 = ImageTk.PhotoImage(image3)

    inner_frame.imgs = [img1, img2, img3]

    Button(inner_frame, image=img1, command=journal, borderwidth=0).pack(side="left", padx=10)
    Button(inner_frame, image=img2, command=echo, borderwidth=0).pack(side="left", padx=10)
    Button(inner_frame, image=img3, command=breathe, borderwidth=0).pack(side="left", padx=10)

    inner_frame.update_idletasks()
    button_canvas.config(scrollregion=button_canvas.bbox("all"))

    mywin.mainloop()



root = Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set window size
window_width = 400
window_height = 700

# Calculate position to center the window
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2

# Set geometry to center the window
root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
bg = PhotoImage(file = "templates/welcome.png")
label1 = Label( root, image = bg)
label1.place(x = 0, y = 0)

click_btn_= PhotoImage(file='templates/arrow.png')
button2= Button(root, image=click_btn_,command= mainpg,borderwidth=0, highlightthickness=0, relief='flat')
button2.place(x=250, y=630)

root.mainloop()
