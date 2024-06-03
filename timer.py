import tkinter as tk
from tkinter import messagebox
import time

class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Timer and Stopwatch")
        
        # Variables
        self.running = False
        self.paused = False
        self.reset = False
        self.time_left = 0
        self.start_time = 0
        self.pause_time = 0

        # Display Label
        self.label = tk.Label(root, text="00:00:00", font=("Helvetica", 48))
        self.label.pack(pady=20)

        # Entry for countdown duration
        self.entry_label = tk.Label(root, text="Set countdown (min):")
        self.entry_label.pack(pady=5)
        self.entry = tk.Entry(root)
        self.entry.pack(pady=5)

        # Buttons
        self.start_button = tk.Button(root, text="Start Countdown", command=self.start_countdown)
        self.start_button.pack(side="left", padx=10)
        
        self.stopwatch_button = tk.Button(root, text="Start Stopwatch", command=self.start_stopwatch)
        self.stopwatch_button.pack(side="left", padx=10)
        
        self.pause_button = tk.Button(root, text="Pause", command=self.pause_resume)
        self.pause_button.pack(side="left", padx=10)
        
        self.stop_button = tk.Button(root, text="Stop", command=self.stop_timer)
        self.stop_button.pack(side="left", padx=10)
        
        self.reset_button = tk.Button(root, text="Reset", command=self.reset_timer)
        self.reset_button.pack(side="left", padx=10)

    def start_countdown(self):
        try:
            minutes = int(self.entry.get())
            self.time_left = minutes * 60  # Convert minutes to seconds
            self.running = True
            self.paused = False
            self.reset = False
            self.update_timer()
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter a valid number of minutes.")

    def start_stopwatch(self):
        self.running = True
        self.paused = False
        self.reset = False
        self.start_time = time.time()
        self.update_stopwatch()

    def update_timer(self):
        if self.reset:
            self.label.config(text="00:00:00")
            return

        if self.paused:
            return
        
        if self.time_left > 0 and self.running:
            mins, secs = divmod(self.time_left, 60)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            self.label.config(text=timeformat)
            self.time_left -= 1
            self.root.after(1000, self.update_timer)
        elif self.time_left == 0 and self.running:
            self.label.config(text="Time's up!")
            messagebox.showinfo("Timer", "Time's up!")

    def update_stopwatch(self):
        if self.reset:
            self.label.config(text="00:00:00")
            return

        if self.paused:
            return

        if self.running:
            elapsed_time = int(time.time() - self.start_time)
            mins, secs = divmod(elapsed_time, 60)
            hours, mins = divmod(mins, 60)
            timeformat = '{:02d}:{:02d}:{:02d}'.format(hours, mins, secs)
            self.label.config(text=timeformat)
            self.root.after(1000, self.update_stopwatch)

    def pause_resume(self):
        if self.running:
            if self.paused:
                # Resume
                self.paused = False
                self.pause_button.config(text="Pause")
                if self.time_left > 0:
                    self.update_timer()
                else:
                    self.start_time = time.time() - (self.pause_time - self.start_time)
                    self.update_stopwatch()
            else:
                # Pause
                self.paused = True
                self.pause_time = time.time()
                self.pause_button.config(text="Resume")

    def stop_timer(self):
        self.running = False
        self.paused = False
        self.pause_button.config(text="Pause")

    def reset_timer(self):
        self.reset = True
        self.paused = False
        self.running = False
        self.label.config(text="00:00:00")
        self.pause_button.config(text="Pause")

if __name__ == "__main__":
    root = tk.Tk()
    app = TimerApp(root)
    root.mainloop()