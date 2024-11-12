import smtplib
import schedule
import time
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def send_email(content_msg):
    smtp_host = "smtp.gmail.com"
    smtp_port = 587
    email = "patara1929@gmail.com"
    password = "hnoy gqhk trmx bhyn" 
    
    to_email = "64011224@kmitl.ac.th"
    subject = "สัญญาญซื้อขายหุ้น"
    body = content_msg
    
    message = MIMEMultipart()
    message['From'] = email
    message['To'] = to_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))
    try:
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(email, password)
            server.sendmail(email, to_email, message.as_string())
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")


# schedule.every().monday.at("05.00").do(send_email)
# schedule.every().tuesday.at("05.00").do(send_email)
# schedule.every().wednesday.at("05.00").do(send_email)
# schedule.every().thursday.at("05.00").do(send_email)
# schedule.every().friday.at("05.00").do(send_email)

# # Run the schedule
# while True:
#     schedule.run_pending()
#     time.sleep(1)


content_msg = "ตอนนี้ได้เวลาซ์้อขายหุ้นแล้วนะครับ"
send_email(content_msg)