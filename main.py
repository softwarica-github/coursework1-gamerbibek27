import tkinter as tk
import subprocess

class OTPApp:
    def __init__(self, master):
        self.master = master
        master.title("Welcome to OTP Sender and Verifier")

        self.title_label = tk.Label(master, text="Welcome to OTP Sender and Verifier", font=("Arial", 16))
        self.title_label.pack(pady=20)

        # Customizing button colors
        self.generate_button = tk.Button(master, text="Generate OTP", command=self.open_ibek, bg="blue", fg="white")
        self.generate_button.pack()

    def open_ibek(self):
        subprocess.Popen(['python', 'ibek.py'])
        self.master.withdraw()  # Hide the main window

root = tk.Tk()
app = OTPApp(root)
root.mainloop()
