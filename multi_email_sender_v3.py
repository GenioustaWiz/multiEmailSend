import tkinter as tk
from tkinter import filedialog
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import base64
import pickle

# Function to send the email using Gmail API
def send_email():
    # Get recipients, subject, and message text from the GUI
    recipients = recipient_entry.get().split(',')
    subject = subject_entry.get()
    message_text = message_text_entry.get("1.0", "end-1c")

    try:
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

# Get Gmail API service using the second authentication method
SCOPES = ['https://www.googleapis.com/auth/gmail.send'] #['https://mail.google.com/']
service = None

def authenticate_gmail():
    global service
    creds = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
    service = build('gmail', 'v1', credentials=creds)

# Call the authentication function to initialize the Gmail API service
authenticate_gmail()

# Start the tkinter main loop
window.mainloop()
