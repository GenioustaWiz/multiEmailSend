import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import tkinter as tk
from tkinter import filedialog

# Gmail account credentials
sender_email = "cm0215557@gmail.com"
sender_password = "**********"

# Function to send the email
def send_email():
    # Get recipients, subject, and message text from the GUI
    recipients = recipient_entry.get().split(',')
    subject = subject_entry.get()
    message_text = message_text_entry.get("1.0", "end-1c")

    # Create the email message
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = ", ".join(recipients)
    msg["Subject"] = subject

    # Attach the message text
    msg.attach(MIMEText(message_text, "plain"))

    # Connect to the SMTP server (Gmail's SMTP server)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)

        # Send the email
        server.sendmail(sender_email, recipients, msg.as_string())
        status_label.config(text="Email sent successfully!")

    except Exception as e:
        status_label.config(text="Error: Unable to send email.")
        print(e)

    finally:
        # Close the SMTP server connection
        server.quit()

# Function to add recipients to the list
def add_recipients():
    recipients_list = recipient_entry.get().split(',')
    with open("recipients.txt", "a") as file:
        for recipient in recipients_list:
            file.write(recipient.strip() + "\n")
    recipient_entry.delete(0, tk.END)
    status_label.config(text="Recipients added and saved!")

# Function to load recipients from a file
def load_recipients():
    recipients = []
    try:
        with open("recipients.txt", "r") as file:
            recipients = file.read().splitlines()
        recipient_entry.delete(0, tk.END)
        recipient_entry.insert(0, ", ".join(recipients))
        status_label.config(text="Recipients loaded from file!")

    except FileNotFoundError:
        status_label.config(text="No recipients file found.")

# Create a tkinter window
window = tk.Tk()
window.title("Email Sender")

# Recipients Entry
recipient_label = tk.Label(window, text="Recipients (comma-separated):")
recipient_label.pack()
recipient_entry = tk.Entry(window, width=40)
recipient_entry.pack()

# Load and Save Buttons
load_button = tk.Button(window, text="Load Recipients", command=load_recipients)
load_button.pack()
save_button = tk.Button(window, text="Add and Save Recipients", command=add_recipients)
save_button.pack()

# Subject Entry
subject_label = tk.Label(window, text="Subject:")
subject_label.pack()
subject_entry = tk.Entry(window, width=40)
subject_entry.pack()

# Message Text Entry
message_text_label = tk.Label(window, text="Message Text:")
message_text_label.pack()
message_text_entry = tk.Text(window, height=5, width=40)
message_text_entry.pack()

# Send Button
send_button = tk.Button(window, text="Send Email", command=send_email)
send_button.pack()

# Status Label
status_label = tk.Label(window, text="")
status_label.pack()

# Start the tkinter main loop
window.mainloop()
