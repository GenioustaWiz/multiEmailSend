import tkinter as tk
from tkinter import filedialog
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account
from google.auth.transport.requests import Request
import os
import base64

# Function to send the email using Gmail API
def send_email():
    # Define the SCOPES and the path to your JSON credentials file
    SCOPES = ['https://www.googleapis.com/auth/gmail.send'] #['https://mail.google.com/']
    our_email = 'cm0215557@gmail.com'
    CREDENTIALS_FILE = 'credentials.json'

    try:
        # Load the credentials
        creds = None
        if os.path.exists('token.json'):
            creds = service_account.Credentials.from_service_account_file(
                CREDENTIALS_FILE, scopes=SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                raise Exception("Failed to acquire valid credentials")

        # Create the Gmail API service
        service = build('gmail', 'v1', credentials=creds)

        # Get recipients, subject, and message text from the GUI
        recipients = recipient_entry.get().split(',')
        subject = subject_entry.get()
        message_text = message_text_entry.get("1.0", "end-1c")

        # Create the email message
        message = MIMEText(message_text)
        message['to'] = ", ".join(recipients)
        message['subject'] = subject

        # Send the email using the Gmail API
        raw_message = base64.urlsafe_b64encode(message.as_string().encode("utf-8")).decode("utf-8")
        body = {"raw": raw_message}
        service.users().messages().send(userId="me", body=body).execute()
        status_label.config(text="Email sent successfully!")

    except HttpError as error:
        status_label.config(text=f"Error: {str(error)}")
    except Exception as e:
        status_label.config(text="Error: Unable to send email.")
        print(e)

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
window.geometry("1000x550+200+50") 
window.config(bg="skyblue")

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

