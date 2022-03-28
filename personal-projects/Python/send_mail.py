from cgitb import html
import smtplib
from email.mime.text import MIMEText

def send_mail(customer, restaurant, rating, comments):
    port = 2525
    smpt_server = 'smtp.mailtrap.io'
    login = '4ffb606ffc8ac7'
    password = 'e2bdb3fcb5ee01'
    message = f"<h3>New Feedback Submission</h3><ul><li>Customer: {customer}</li><li>Restaurant: {restaurant}</li><li>Rating: {rating}</li><li>Comments: {comments}</li></ul>"
    

    
    sender_email = 'customer@example.com'
    receiver_email = 'owner@example.com'
    msg = MIMEText(message, 'html')
    msg['Subject'] = 'Barbeque Feedback'
    msg['From'] = sender_email
    msg['To'] = receiver_email
    
    # Send Email
    with smtplib.SMTP(smpt_server, port) as server:
        server.login(login, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())