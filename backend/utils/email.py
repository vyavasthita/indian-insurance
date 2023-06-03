
from flask_mail import Message
from apps import mail, configuration


def send_email(to, subject, template):
    try:
        msg = Message(
            subject,
            recipients=[to],
            html=template,
            sender=configuration.MAIL_DEFAULT_SENDER
        )
        mail.send(msg)
    except Exception as err:
        print(f"Failed to send email. To {to}, sender {configuration.MAIL_DEFAULT_SENDER}.")
        return False, "Failed to send email.", None
    
    return True, None, None