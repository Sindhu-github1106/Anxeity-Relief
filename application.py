import customtkinter as ctk
from PIL import Image
from tkinter import simpledialog, messagebox
import random

# Set appearance mode and color theme
ctk.set_appearance_mode("light")  # or "dark"
ctk.set_default_color_theme("blue")

def account():
    root.withdraw()
    mywin = ctk.CTkToplevel(root)
    
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
    
    bg_image = ctk.CTkImage(Image.open("templates/account.png"), size=(400, 700))
    bg_label = ctk.CTkLabel(mywin, image=bg_image, text="")
    bg_label.place(x=0, y=0)
    
    click_btn = ctk.CTkImage(Image.open("templates/plus_btn.png"))
    button1 = ctk.CTkButton(mywin, image=click_btn, command=features, text="", fg_color="transparent", hover=False)
    button1.place(x=180, y=640)
    
    click_btn2 = ctk.CTkImage(Image.open("templates/home_btn.png"))
    button2 = ctk.CTkButton(mywin, image=click_btn2, command=mainpg, text="", fg_color="transparent", hover=False)
    button2.place(x=20, y=640)
    
def box():
    root.withdraw()
    mywin = ctk.CTkToplevel(root)
    
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
    
    bg_image = ctk.CTkImage(Image.open("templates/box.png"), size=(400, 700))
    label1 = ctk.CTkLabel(mywin, image=bg_image, text="")
    label1.place(x=0, y=0)
    
    click_btn0 = ctk.CTkImage(Image.open("templates/back.png"))
    button0 = ctk.CTkButton(mywin, image=click_btn0, command=features, text="", fg_color="transparent", hover=False)
    button0.place(x=320, y=60)
    
    click_btn = ctk.CTkImage(Image.open("templates/home_btn.png"))
    button1 = ctk.CTkButton(mywin, image=click_btn, command=mainpg, text="", fg_color="transparent", hover=False)
    button1.place(x=20, y=640)
    
    click_btn2 = ctk.CTkImage(Image.open("templates/account_btn.png"))
    button2 = ctk.CTkButton(mywin, image=click_btn2, command=account, text="", fg_color="transparent", hover=False)
    button2.place(x=320, y=638)
    
    click_btn3 = ctk.CTkImage(Image.open("templates/plus_btn.png"))
    button3 = ctk.CTkButton(mywin, image=click_btn3, command=features, text="", fg_color="transparent", hover=False)
    button3.place(x=180, y=640)
    
def features():
    root.withdraw()
    mywin = ctk.CTkToplevel(root)
    
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
    
    bg_image = ctk.CTkImage(Image.open("templates/features.png"), size=(400, 700))
    label1 = ctk.CTkLabel(mywin, image=bg_image, text="")
    label1.place(x=0, y=0)
    
    click_btn = ctk.CTkImage(Image.open("templates/home_btn.png"))
    button1 = ctk.CTkButton(mywin, image=click_btn, command=mainpg, text="", fg_color="transparent", hover=False)
    button1.place(x=20, y=640)
    
    click_btn2 = ctk.CTkImage(Image.open("templates/account_btn.png"))
    button2 = ctk.CTkButton(mywin, image=click_btn2, command=account, text="", fg_color="transparent", hover=False)
    button2.place(x=320, y=638)
    
    click_btn3 = ctk.CTkImage(Image.open("templates/box_btn.png"))
    button3 = ctk.CTkButton(mywin, image=click_btn3, command=box, text="", fg_color="transparent", hover=False)
    button3.place(x=25, y=100)
    
def mainpg():
    root.withdraw()
    mywin = ctk.CTkToplevel(root)
    
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
    
    bg_image = ctk.CTkImage(Image.open("templates/mainpg.png"), size=(400, 700))
    label1 = ctk.CTkLabel(mywin, image=bg_image, text="")
    label1.place(x=0, y=0)
    
    # Create Canvas for ECG Line Animation
    canvas = ctk.CTkCanvas(mywin, width=350, height=100, bg="white", highlightthickness=0)
    canvas.place(x=30, y=30)  # Adjust position

    # ECG pattern function
    def generate_ecg_pattern():
        """Generate a repeating ECG wave pattern."""
        pattern = []
        x = 0
        while x < 350:
            pattern.append((x, 75))  # Baseline
            x += 10
            if x < 350:
                pattern.append((x, random.randint(70, 80)))  # Small variation
                x += 10
            if x < 350:
                pattern.append((x, 40))  # Sharp peak (heartbeat)
                x += 10
            if x < 350:
                pattern.append((x, 90))  # Sharp drop
                x += 10
            if x < 350:
                pattern.append((x, 75))  # Return to baseline
                x += 10
        return pattern

    # Initialize ECG line
    line_points = generate_ecg_pattern()
    line = canvas.create_line(*[coord for point in line_points for coord in point], fill="red", width=2)

    def update_ecg():
        """Animate ECG wave by shifting points left and adding new beats."""
        nonlocal line_points
        line_points = line_points[1:] + [(350, random.randint(70, 80))]  # Shift left
        for i in range(len(line_points)):  # Keep the heartbeat peaks
            if i % 15 == 0 and 50 < line_points[i][0] < 300:
                line_points[i] = (line_points[i][0], random.choice([40, 90]))  # Simulate beat
        canvas.coords(line, *[coord for point in line_points for coord in point])  # Update line
        mywin.after(100, update_ecg)  # Refresh every 100ms

    # Start ECG Animation
    update_ecg()
    
    click_btn = ctk.CTkImage(Image.open("templates/plus_btn.png"))
    button1 = ctk.CTkButton(mywin, image=click_btn, command=features, text="", fg_color="transparent", hover=False)
    button1.place(x=180, y=640)
    
    click_btn2 = ctk.CTkImage(Image.open("templates/account_btn.png"))
    button2 = ctk.CTkButton(mywin, image=click_btn2, command=account, text="", fg_color="transparent", hover=False)
    button2.place(x=320, y=638)
    
def signup():
    root.withdraw()
    mywin = ctk.CTkToplevel(root)
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
    
    bg_image = ctk.CTkImage(Image.open("templates/signup.png"), size=(400, 700))
    label1 = ctk.CTkLabel(mywin, image=bg_image, text="")
    label1.place(x=0, y=0)
    
    click_btn = ctk.CTkImage(Image.open("templates/next.png"))
    button1 = ctk.CTkButton(mywin, image=click_btn, command=mainpg, text="", fg_color="transparent", hover=False)
    button1.place(x=320, y=630)

    click_btn2 = ctk.CTkImage(Image.open("templates/back.png"))
    button2 = ctk.CTkButton(mywin, image=click_btn2, command=login, text="", fg_color="transparent", hover=False)
    button2.place(x=20, y=630)
    
def login():
    root.withdraw()
    mywin = ctk.CTkToplevel(root)
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
    
    mywin.mainloop()

# Main application
root = ctk.CTk()
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

bg_image = ctk.CTkImage(Image.open("templates/welcome.png"), size=(400, 700))
label1 = ctk.CTkLabel(root, image=bg_image, text="")
label1.place(x=0, y=0)

click_btn = ctk.CTkImage(Image.open("templates/signup_button.png"))
button2 = ctk.CTkButton(root, image=click_btn, command=signup, text="", fg_color="transparent", hover=False)
button2.place(x=100, y=380)

click_btn2 = ctk.CTkImage(Image.open("templates/login_button.png"))
button3 = ctk.CTkButton(root, image=click_btn2, command=login, text="", fg_color="transparent", hover=False)
button3.place(x=100, y=560)

root.mainloop()