import random
import sqlite3
import tkinter as tk
import win32com.client as win32
import re

# Function to generate OTP
def generate_otp():
    return ''.join(random.choices('0123456789', k=6))

# Function to save OTP to database
def save_otp_to_db(otp):
    try:
        with sqlite3.connect('otp.db') as conn:
            c = conn.cursor()
            c.execute("CREATE TABLE IF NOT EXISTS otps (otp TEXT)")
            c.execute("INSERT INTO otps (otp) VALUES (?)", (otp,))
    except sqlite3.Error as e:
        print("Error occurred while saving OTP to database:", e)

# Function to get the most recent OTP from database
def get_recent_otp_from_db():
    try:
        with sqlite3.connect('otp.db') as conn:
            c = conn.cursor()
            c.execute("SELECT otp FROM otps ORDER BY ROWID DESC LIMIT 1")
            result = c.fetchone()
            return result[0] if result else None
    except sqlite3.Error as e:
        print("Error occurred while fetching OTP from database:", e)
        return None

# Function to send OTP via email
def send_otp_email(email, otp):
    try:
        outlook = win32.Dispatch('outlook.application')
        mail = outlook.CreateItem(0)
        mail.To = email
        mail.Subject = "Your OTP"
        mail.Body = f"Your OTP is: {otp}"
        mail.Send()
        print("OTP sent successfully!")
    except Exception as e:
        print("Error occurred while sending OTP email:", e)

# Function to verify OTP
def verify_otp(entered_otp):
    recent_otp = get_recent_otp_from_db()
    if recent_otp and recent_otp == entered_otp:
        return True
    else:
        return False

# GUI
def send_otp_gui():
    email = email_entry.get()
    if re.match(r"[^@]+@[^@]+\.[^@]+", email):
        otp = generate_otp()
        save_otp_to_db(otp)
        send_otp_email(email, otp)
        status_label.config(text="OTP sent successfully!")
    else:
        status_label.config(text="Invalid email format!")

def verify_otp_gui():
    entered_otp = otp_entry.get()
    if verify_otp(entered_otp):
        status_label.config(text="OTP is valid!")
    else:
        status_label.config(text="Invalid OTP!")

root = tk.Tk()
root.title("OTP Verification")
root.geometry("400x300")  # Set initial size of the window

title_label = tk.Label(root, text="Start Generating OTP", font=("Arial", 20))
title_label.pack(pady=20)

email_label = tk.Label(root, text="Enter your email:", font=("Arial", 12))
email_label.pack()
email_entry = tk.Entry(root, font=("Arial", 12))
email_entry.pack()

send_otp_button = tk.Button(root, text="Send OTP", command=send_otp_gui, font=("Arial", 14), bg="blue", fg="white")
send_otp_button.pack(pady=10)

otp_label = tk.Label(root, text="Enter OTP received:", font=("Arial", 12))
otp_label.pack()
otp_entry = tk.Entry(root, font=("Arial", 12))
otp_entry.pack()

verify_otp_button = tk.Button(root, text="Verify OTP", command=verify_otp_gui, font=("Arial", 14), bg="green", fg="white")
verify_otp_button.pack(pady=10)

status_label = tk.Label(root, text="", font=("Arial", 12))
status_label.pack()

root.mainloop()
