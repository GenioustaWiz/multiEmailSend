import tkinter as tk
from tkinter import filedialog, messagebox
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import base64
import pickle
# from PIL import ImageTk

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
        print(error)
    except Exception as e:
        status_label.config(text="Error: Unable to send email.")
        print(e)

# Function to add recipients to the list
def add_recipients():
    recipients_list = recipient_entry.get().split(',')
    
    # Load existing recipients from the file
    existing_recipients = set()
    try:
        with open("recipients2.txt", "r") as file:
            existing_recipients = set(file.read().splitlines())

    except FileNotFoundError:
        pass  # File doesn't exist, so no need to check
    
    new_recipients = []

    for recipient in recipients_list:
        recipient = recipient.strip()  # Remove leading/trailing spaces

        # Check if the recipient is not already in the file
        if recipient and recipient not in existing_recipients:
            new_recipients.append(recipient)
            existing_recipients.add(recipient)  # Add it to the set for future checks
    
    if new_recipients:
        with open("recipients2.txt", "a") as file:
            file.write("\n".join(new_recipients) + "\n")
    
        recipient_entry.delete(0, tk.END)
        status_label.config(text="Recipients added and saved!")
    else:
        recipient_entry.delete(0, tk.END)
        status_label.config(text="Recipients Email Exists!")

# ...


# Function to load recipients from a file
def load_recipients():
    recipients = []
    try:
        with open("recipients2.txt", "r") as file:
            recipients = file.read().splitlines()
        
        # Count the number of recipients
        recipient_count = len(recipients)
        
        recipient_entry.delete(0, tk.END)
        recipient_entry.insert(0, ", ".join(recipients))
        
        # Display the total count on the GUI
        total_label.config(text=f"Total Recipients: {recipient_count}")
        status_label.config(text="Recipients loaded from file!")

    except FileNotFoundError:
        status_label.config(text="No recipients file found.")
        total_label.config(text="Total Recipients: 0")  # Set the count to 0 if file not found

# Function to clear the recipient_entry
def clear_recipient_entry():
    recipient_entry.delete(0, tk.END)
    # Display the total count on the GUI
    total_label.config(text="")
    status_label.config(text="")

# Create a tkinter window
window = tk.Tk()
window.title("Email Sender")
window.geometry("1000x550+200+50")
window.config(bg="skyblue")

# Total Recipients Label
total_label = tk.Label(window, text="", font=("times new roman", 14, "bold"), bg="skyblue", fg="black")
total_label.place(x=600, y=500)

# ...
# Recipients Entry
recipient_label = tk.Label(window, text="Recipients (comma-separated):", font=("times new roman", 14, "bold"), bg="skyblue", fg="black")
recipient_label.place(x=50, y=150)
recipient_entry = tk.Entry(window, width=40, font=("times new roman", 14), bg="lightyellow")
recipient_entry.place(x=340, y=150)

# Clear Button
clear_button = tk.Button(window, text="Clear", command=clear_recipient_entry, font=("times new roman", 12), bg="red", fg="white")
clear_button.place(x=740, y=148)

# Load and Save Buttons
load_button = tk.Button(window, text="Load Recipients", command=load_recipients, font=("times new roman", 16), bg="black", fg="white")
load_button.place(x=50, y=200)
save_button = tk.Button(window, text="Add and Save Recipients", command=add_recipients, font=("times new roman", 16), bg="#ffcccb", fg="black")
save_button.place(x=340, y=200)

# Subject Entry
subject_label = tk.Label(window, text="Subject:", font=("times new roman", 18, "bold"), bg="skyblue", fg="black")
subject_label.place(x=50, y=250)
subject_entry = tk.Entry(window, width=40, font=("times new roman", 14), bg="lightyellow")
subject_entry.place(x=340, y=250)

# Message Text Entry
message_text_label = tk.Label(window, text="Message Text:", font=("times new roman", 14, "bold"), bg="skyblue", fg="black")
message_text_label.place(x=50, y=300)
message_text_entry = tk.Text(window, height=5, width=40, font=("times new roman", 14), bg="lightyellow")
message_text_entry.place(x=340, y=300)

# Send Button
send_button = tk.Button(window, text="Send Email", command=send_email, font=("times new roman", 20, "bold"), bg="black", fg="white")
send_button.place(x=400, y=450)

# Status Label
status_label = tk.Label(window, text="", font=("times new roman", 10, "bold"), bg="skyblue", fg="black")
status_label.place(x=50, y=500)

# Get Gmail API service using the second authentication method
SCOPES =  ['https://www.googleapis.com/auth/gmail.send'] #['https://mail.google.com/'] #
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
            flow = InstalledAppFlow.from_client_secrets_file('credentials2.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
    service = build('gmail', 'v1', credentials=creds)

# Call the authentication function to initialize the Gmail API service
authenticate_gmail()

# Start the tkinter main loop
window.mainloop()
