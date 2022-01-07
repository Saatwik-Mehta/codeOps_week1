import credentials
import smtplib
import os
from email.message import EmailMessage

EMAIL_ADDRESS = credentials.os.getenv('EMAIL')
EMAIL_PASSWORD = credentials.os.getenv('PASSWORD')


# # EMAIL_ADDRESS = os.getenv('EMAIL')
# # EMAIL_PASSWORD = os.getenv('PASSWORD')

def send_mail(smtp_host='smtp.gmail.com', smtp_port=587, smtp_user_mail=None,
              smtp_user_password=None, sender_mail=None, receiver_mail=None,
              mail_body="Mail Body", mail_subject="Mail Subject", files_to_send: list = None):
    """

    :param smtp_host:
    :param smtp_port:
    :param smtp_user_mail:
    :param smtp_user_password:
    :param sender_mail:
    :param receiver_mail:
    :param mail_body:
    :param mail_subject:
    :param files_to_send:
    :return:
    """
    msg = EmailMessage()
    msg['Subject'] = mail_subject
    msg['From'] = sender_mail
    msg['To'] = receiver_mail
    msg.set_content(mail_body)
    for file in files_to_send:
        with open(file, 'rb') as file_obj:
            file_data = file_obj.read()
            file_name = os.path.split(file_obj.name)[1]
        msg.add_attachment(file_data, maintype='application',
                           subtype='octet-stream', filename=file_name)

    with smtplib.SMTP(smtp_host, smtp_port) as smtp:
        smtp.starttls()
        smtp.ehlo()
        smtp.login(smtp_user_mail, smtp_user_password)
        smtp.send_message(msg=msg)


if __name__ == '__main__':
    mail_body = "Hi Sir,\n" \
                "I have Generated the Reports for the Json data provided to me.\n" \
                "Please find attached the zip file that " \
                "contains the generated reports from my code.\n\n" \
                "Thank You\n" \
                "Saatwik Mehta\n" \
                "+91-9560-298-378\n" \
                "saatwik@codeops.tech\n"

    mail_subject = "Reports generated from JSON data"
    RECEIVER_MAIL = 'cprone846@gmail.com'

    send_mail(smtp_user_mail=EMAIL_ADDRESS, smtp_user_password=EMAIL_PASSWORD,
              sender_mail=EMAIL_ADDRESS, receiver_mail=RECEIVER_MAIL,
              files_to_send=['reports.zip', r'..\Generated_reports\GhibliStudio\ghibliStudioApi_csv.csv'],
              mail_body=mail_body, mail_subject=mail_subject)
