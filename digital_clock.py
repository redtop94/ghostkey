import tkinter as tk
from tkinter import font
from datetime import datetime
import pytz

class DigitalClock:
    def __init__(self, root):
        self.root = root
        self.root.title("Digital Clock - Multiple Time Zones")
        self.root.geometry("600x400")
        self.root.config(bg="#1a1a1a")
        
        # Time zones to display
        self.timezones = [
            ("UTC", "UTC"),
            ("EST", "America/New_York"),
            ("CST", "America/Chicago"),
            ("PST", "America/Los_Angeles"),
            ("GMT", "Europe/London"),
            ("IST", "Asia/Kolkata"),
            ("JST", "Asia/Tokyo"),
            ("AEST", "Australia/Sydney"),
        ]
        
        # Create labels for each timezone
        self.labels = {}
        self.setup_ui()
        self.update_time()
    
    def setup_ui(self):
        # Title
        title_font = font.Font(family="Helvetica", size=24, weight="bold")
        title = tk.Label(
            self.root,
            text="World Clock",
            font=title_font,
            bg="#1a1a1a",
            fg="#00ff00"
        )
        title.pack(pady=20)
        
        # Create frame for clocks
        clock_frame = tk.Frame(self.root, bg="#1a1a1a")
        clock_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Time font
        time_font = font.Font(family="Courier", size=16, weight="bold")
        label_font = font.Font(family="Helvetica", size=12)
        
        # Create labels for each timezone
        for i, (name, tz) in enumerate(self.timezones):
            row = i // 2
            col = i % 2
            
            # Frame for each clock
            frame = tk.Frame(clock_frame, bg="#2a2a2a", relief=tk.RAISED, bd=2)
            frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            
            # Timezone name
            tz_label = tk.Label(
                frame,
                text=name,
                font=label_font,
                bg="#2a2a2a",
                fg="#00ff00"
            )
            tz_label.pack(pady=(5, 2))
            
            # Time display
            time_label = tk.Label(
                frame,
                text="00:00:00",
                font=time_font,
                bg="#2a2a2a",
                fg="#00ff00"
            )
            time_label.pack(pady=(2, 5))
            
            self.labels[tz] = time_label
        
        # Configure grid weights
        for i in range(4):
            clock_frame.grid_rowconfigure(i, weight=1)
        for i in range(2):
            clock_frame.grid_columnconfigure(i, weight=1)
    
    def update_time(self):
        for name, tz in self.timezones:
            # Get current time in timezone
            timezone = pytz.timezone(tz)
            current_time = datetime.now(timezone)
            time_str = current_time.strftime("%H:%M:%S")
            
            # Update label
            self.labels[tz].config(text=time_str)
        
        # Schedule next update
        self.root.after(1000, self.update_time)

if __name__ == "__main__":
    root = tk.Tk()
    clock = DigitalClock(root)
    root.mainloop()
