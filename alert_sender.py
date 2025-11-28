import smtplib
import threading
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

load_dotenv('.env')
def send_detected_face_to_admin(face_img_dir):
    with open(face_img_dir, 'rb') as f:
        img = f.read()

    splitters = face_img_dir.split('!')
    print("Here ", splitters)
    face_id, time_string = splitters[-1].split('@')
    time_string = time_string[:-4]

    message = MIMEMultipart()
    fromEmail = os.environ.get("SOURCE_EMAIL")
    toEmail = os.environ.get("ADMIN_EMAIL")

    message['From'] = fromEmail
    message['To'] = toEmail
    message['Subject'] = f"Sending all the detected Faces with their IDs"

    text = MIMEText(f"Face Detection software detected these faces.")
    message.attach(text)

    image_attachment = MIMEImage(img, name=f"Detected Face {face_id} at {time_string}")
    message.attach(image_attachment)

    smtp_server = smtplib.SMTP("smtp.gmail.com", 587)
    smtp_server.ehlo()
    smtp_server.starttls()
    smtp_server.login(fromEmail, os.environ.get("SOURCE_PASSWORD"))
    smtp_server.sendmail(fromEmail, toEmail, message.as_string())
    smtp_server.quit()
    print("Detected Faces sent successfully")

def send_all_at_once():
    det_img_path = Path("detected_images")
    message = MIMEMultipart()
    fromEmail = os.environ.get("SOURCE_EMAIL")
    toEmail = os.environ.get("ADMIN_EMAIL")

    message['From'] = fromEmail
    message['To'] = toEmail
    message['Subject'] = f"Sending all the detected Faces with their IDs"

    text = MIMEText(f"Face Detection software detected these faces.")
    message.attach(text)

    img_list = det_img_path.glob("*.png")
    for idx, img_path in enumerate(img_list):
        with open(str(img_path), 'rb') as f:
            img = f.read()

        splitters = str(img_path).split('!')
        face_id, time_string = splitters[-1].split('@')
        time_string = time_string[:-4]
        print(time_string, face_id)

        image_attachment = MIMEImage(img, name=f"Detected Face {face_id} at {time_string}")
        image_attachment.add_header('Content-ID', f'<image{idx+1}>')
        message.attach(image_attachment)
    print("Starting attachment send")

    smtp_server = smtplib.SMTP("smtp.gmail.com", 587)
    smtp_server.ehlo()
    smtp_server.starttls()
    smtp_server.login(fromEmail, os.environ.get("SOURCE_PASSWORD"))
    smtp_server.sendmail(fromEmail, toEmail, message.as_string())
    smtp_server.quit()
    print("Detected Faces sent successfully")


def send_email_async(face_img_dir, time_string, face_id):
    """Threaded function to send email asynchronously"""
    # Create a new thread that will run the send_detected_face_to_admin function
    email_thread = threading.Thread(target=send_detected_face_to_admin)
    email_thread.start()  # Start the thread to run in the background

# send_detected_face_to_admin('Detected_ID1.png', '28/11/2025', 0)
