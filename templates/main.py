from tkinter import *
from PIL import ImageTk, Image
from tkinter import simpledialog
from tkinter import messagebox
from tkinter import font
import random

def account():
    root.withdraw()
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
    
    bg = PhotoImage(file = "templates/account.png")
    label1 = Label( mywin, image = bg)
    label1.place(x = 0, y = 0)
    
    click_btn_= PhotoImage(file='templates/plus_btn.png')
    button1= Button(mywin, image=click_btn_,command= features,borderwidth=0)
    button1.place(x=180, y=640)
    
    click_btn2= PhotoImage(file='templates/home_btn.png')
    button2= Button(mywin, image=click_btn2,command= mainpg,borderwidth=0)
    button2.place(x=20, y=640)
    
    mywin.mainloop()
    
def box():
    root.withdraw()
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
    
    bg = PhotoImage(file = "templates/box.png")
    label1 = Label( mywin, image = bg)
    label1.place(x = 0, y = 0)
    
    click_btn0= PhotoImage(file='templates/back.png')
    button0= Button(mywin, image=click_btn0,command= features,borderwidth=0)
    button0.place(x=320, y=60)
    
    click_btn_= PhotoImage(file='templates/home_btn.png')
    button1= Button(mywin, image=click_btn_,command= mainpg,borderwidth=0)
    button1.place(x=20, y=640)
    
    click_btn2= PhotoImage(file='templates/account_btn.png')
    button2= Button(mywin, image=click_btn2,command= account,borderwidth=0)
    button2.place(x=320, y=638)
    
    click_btn3= PhotoImage(file='templates/plus_btn.png')
    button3= Button(mywin, image=click_btn3,command= features,borderwidth=0)
    button3.place(x=180, y=640)
    
    mywin.mainloop()

def features():
    root.withdraw()
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
    
    bg = PhotoImage(file = "templates/features.png")
    label1 = Label( mywin, image = bg)
    label1.place(x = 0, y = 0)
    
    click_btn_= PhotoImage(file='templates/home_btn.png')
    button1= Button(mywin, image=click_btn_,command= mainpg,borderwidth=0)
    button1.place(x=20, y=640)
    
    click_btn2= PhotoImage(file='templates/account_btn.png')
    button2= Button(mywin, image=click_btn2,command= account,borderwidth=0)
    button2.place(x=320, y=638)
    
    click_btn3= PhotoImage(file='templates/box_btn.png')
    button3= Button(mywin, image=click_btn3,command= box,borderwidth=0)
    button3.place(x=25, y=100)
    
    mywin.mainloop()

def mainpg():
    root.withdraw()
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
    
    bg = PhotoImage(file = "templates/mainpg.png")
    label1 = Label( mywin, image = bg)
    label1.place(x = 0, y = 0)
    
    # Create Canvas for ECG Line Animation
    canvas = Canvas(mywin, width=350, height=100, bg="white", highlightthickness=0)
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
    
    
    click_btn_= PhotoImage(file='templates/plus_btn.png')
    button1= Button(mywin, image=click_btn_,command= features,borderwidth=0)
    button1.place(x=180, y=640)
    
    click_btn2= PhotoImage(file='templates/account_btn.png')
    button2= Button(mywin, image=click_btn2,command= account,borderwidth=0)
    button2.place(x=320, y=638)
    
    mywin.mainloop()

def signup():
    root.withdraw()
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
    
    bg = PhotoImage(file = "templates/signup.png")
    label1 = Label( mywin, image = bg)
    label1.place(x = 0, y = 0)
    
    click_btn_= PhotoImage(file='templates/next.png')
    button1= Button(mywin, image=click_btn_,command= mainpg,borderwidth=0)
    button1.place(x=320, y=630)

    click_btn2= PhotoImage(file='templates/back.png')
    button2= Button(mywin, image=click_btn2,command= login,borderwidth=0)
    button2.place(x=20, y=630)
    
    mywin.mainloop()

def login():
    root.withdraw()
    mywin = Toplevel()
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

click_btn_= PhotoImage(file='templates/signup_button.png')
button2= Button(root, image=click_btn_,command= signup,borderwidth=0)
button2.place(x=100, y=380)

click_btn2= PhotoImage(file='templates/login_button.png')
button3= Button(root, image=click_btn2,command= login,borderwidth=0)
button3.place(x=100, y=560)


root.mainloop()