from flask import Flask, render_template, request
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from werkzeug.utils import secure_filename
import os
from email.mime.base import MIMEBase
from email import encoders


app = Flask(__name__)
def send_email(body, filename):
    smtp_server = 'sandbox.smtp.mailtrap.io'
    smtp_port = 587
    smtp_user = 'username'
    smtp_password = 'password'


    msg = MIMEMultipart()
    msg['From'] = smtp_user
    msg['To'] = 'layilarinde2@gmail.com'
    msg['Subject'] = 'New Form Submission'

    with open('C:/email/' + filename, 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition',
            f'attachment; filename= {filename}',
        )
        msg.attach(part)

    # Email body
    msg.attach(MIMEText(body, 'html'))

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.send_message(msg)
        print("Email sent successfully!")

@app.route('/')
def home():
    return render_template('safeguardian.html')

@app.route('/email', methods=['POST'])
def post_data():
    
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    # Check if the post request has the file part
    if 'attachment' not in request.files:
        return 'No file part'
    file = request.files['attachment']
    if file.filename == '':
        return 'No selected file'
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join('C:/email/', filename))

    # Construct the email content
    body = f"<p>Name: {name}</p><p>Email: {email}</p><p>Message: {message}</p>"
    send_email(body, filename)
    # Send email logic here
    return 'Form submitted successfully!'
if __name__ == '__main__':
    app.run(debug=True)
