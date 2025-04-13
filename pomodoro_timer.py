import tkinter as tk
import pygame

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"

# Pomodoro timing settings (standard technique cycle)
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20

# Global variables for session tracking
timer_started = False
is_paused = False
timer = ""
time_left = 0
reps = 1  # Tracks session progress
checkmark = "✔ "
session_checkmarks = ""  # Stores completed Pomodoro cycles visually
stage = ""  # Current session stage (Work / Break)

# Initializes the Pygame mixer module for playing audio files.
pygame.mixer.init()


# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    """Handles pausing and resetting the Pomodoro timer."""
    global timer_started, is_paused, reps

    if timer_started:
        is_paused = True
        timer_started = False
        root.title("Paused")
        lbl_title.config(text="Paused", fg=RED)
        root.after_cancel(timer)  # Stop active countdown
        btn_reset.config(text="Reset", bg=RED)
        btn_start.config(text="Resume")

    elif is_paused:  # Full reset
        root.title("Pomodoro Timer")
        lbl_title.config(text="Timer", fg=GREEN)
        canvas.itemconfig(timer_text, text="00:00")
        btn_reset.config(text="Pause", bg=PINK)
        btn_start.config(text="Start")
        lbl_green_checkmarks.config(text="")  # Clear checkmarks
        is_paused = False
        reps = 1


# ---------------------------- TIMER MECHANISM ------------------------------- #
def play_countdown_sound():
    """Plays a short alert sound for the countdown from 5 to 1."""
    pygame.mixer.music.load("./media/countdown_beep.wav")
    pygame.mixer.music.play()

def play_end_cycle_sound():
    """Plays an alert sound when the cycle ends."""
    pygame.mixer.music.load("./media/countdown_completed.wav")
    pygame.mixer.music.play()


def start_button_press():
    """Triggers timer start if not already running."""
    global timer_started
    if not timer_started:
        timer_started = True
        start_timer()


def start_timer():
    """Determines the current Pomodoro session stage and starts countdown."""
    global reps, is_paused, session_checkmarks, stage, timer_started

    if is_paused:
        # Resume countdown
        timer_started = True
        is_paused = False
        btn_reset.config(text="Pause", bg=PINK)
        btn_start.config(text="Start")
        lbl_title.config(text=stage, fg=GREEN if stage == "Work" else PINK)
        count_down(time_left)

    elif reps in [1, 3, 5, 7]:  # Work cycles
        stage = "Work"
        lbl_title.config(text=stage, fg=GREEN)
        count_down(WORK_MIN * 60)

    elif reps in [2, 4, 6]:  # Short breaks
        stage = "Break"
        lbl_title.config(text=stage, fg=PINK)
        count_down(SHORT_BREAK_MIN * 60)

    elif reps == 8:  # Long break (full Pomodoro cycle)
        stage = "Break"
        lbl_title.config(text=stage, fg=RED)
        reps = 0
        count_down(LONG_BREAK_MIN * 60)
        session_checkmarks += checkmark  # Add session completion marker
        lbl_red_checkmarks.config(text=session_checkmarks)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    """Manages the timer countdown and updates UI dynamically."""
    global reps, checkmark, timer, time_left

    minutes = f"{count // 60:02d}"
    seconds = f"{count % 60:02d}"
    canvas.itemconfig(timer_text, text=f"{minutes}:{seconds}")
    root.title(f"{minutes}:{seconds} {stage}")  # Display timer in title bar

    if count == 3:
        root.deiconify()
        center_window()  # Ensure visibility

    if 3 >= count > 0:  # Countdown sounds for 5 to 1
        play_countdown_sound()
    elif count == 0:  # End-of-cycle sound when timer hits 0
        play_end_cycle_sound()

    if count > 0:
        timer = root.after(1000, count_down, count - 1)  # Recursive countdown
        time_left = count
    else:
        reps += 1
        lbl_green_checkmarks.config(text=(checkmark * (reps // 2)))  # Add cycle checkmark
        start_timer()  # Move to next session


# ---------------------------- WINDOW MECHANISM ------------------------------- #
def center_window(win_width=416, win_height=410):
    """Centers the application window on screen."""
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width / 2) - (win_width / 2)
    y = (screen_height / 2) - (win_height / 2)

    root.geometry(f"{win_width}x{win_height}+{int(x)}+{int(y)}")


def collapse_window():
    """Shrinks the window to display only the title bar."""
    root.geometry("235x0")


def restore_window():
    """Restores the window size after maximize click."""
    root.state('normal')
    root.update_idletasks()
    center_window(416, 410)


def on_window_event(event):
    """Overrides maximize behavior and maintains the correct window size."""
    if root.state() == 'zoomed':
        root.update_idletasks()
        restore_window()


# ---------------------------- UI SETUP ------------------------------- #
root = tk.Tk()
center_window()
root.title("Pomodoro Timer")
root.maxsize(width=416, height=410)
root.attributes('-topmost', True)
root.iconbitmap(default="./media/tomato.ico")
root.bind("<Configure>", on_window_event)

# ------- Main Frame ------- #
frame = tk.Frame(root, bg=YELLOW, padx=30, pady=20)
frame.pack(fill="both", expand=True)

# ------- Timer Display ------- #
canvas = tk.Canvas(frame, width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = tk.PhotoImage(file="./media/tomato.png")
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 132, text="00:00", fill="white", font=(FONT_NAME, 26, "bold"))
canvas.grid(column=1, row=1, padx=10, pady=6)

# ------- Labels ------- #
lbl_title = tk.Label(frame, text="Timer", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 30, "bold"))
lbl_title.grid(column=1, row=0)

lbl_green_checkmarks = tk.Label(frame, text="", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 14))
lbl_green_checkmarks.grid(column=1, row=2, pady=10)

lbl_red_checkmarks = tk.Label(frame, text=session_checkmarks, fg=RED, bg=YELLOW, font=(FONT_NAME, 14))
lbl_red_checkmarks.grid(column=1, row=3, pady=4)

# ------- Buttons ------- #
btn_start = tk.Button(frame, width=6, height=1, text="Start", font=(FONT_NAME, 13, "bold"), bg=GREEN,
                      highlightthickness=0, command=start_button_press)
btn_start.grid(column=0, row=2)

btn_reset = tk.Button(frame, width=6, height=1, text="Pause", font=(FONT_NAME, 13, "bold"), bg=PINK,
                      highlightthickness=0, command=reset_timer)
btn_reset.grid(column=2, row=2)

btn_collapse = tk.Button(text="Collapse", bg=YELLOW, borderwidth=0, font=(FONT_NAME, 10, "bold", "underline"),
                         command=collapse_window)
btn_collapse.place(x=342, y=0)


root.mainloop()
