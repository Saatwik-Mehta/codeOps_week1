import logging
import os
import smtplib
from email.message import EmailMessage
import credentials

logging.basicConfig(filename='logging_email.log', level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s')


temp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), './Generated_reports/GhibliStudio/')

EMAIL_ADDRESS = os.getenv('EMAIL')
EMAIL_PASSWORD = os.getenv('PASSWORD')

msg = EmailMessage()
msg['Subject'] = 'Museum API Reports'
msg['From'] = EMAIL_ADDRESS
msg['To'] = 'saatwikmehta@gmail.com'
msg.set_content('Hi Dear, \n\nHere I have attached the museum api reports zip file. Kindly '
                'check it for your reference. \n\nThanks & Regards,\nAnkita L')

files = ['Ghibli_reports_ankitacode.zip']
for file in files:
    try:
        with open(file, 'rb') as f:
            file_data = f.read()
            file_name = f.name
        msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)
    except FileNotFoundError as fnf_err:
        logging.exception('check the correct path %s', fnf_err)


def mail_send():
    """function opens smtp server with context manager
        and uses smtp builtin functions to send the email"""
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)


if __name__ == '__main__':
    mail_send()