
from flask_mail import Message
from apps import mail, configuration


def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=configuration.MAIL_DEFAULT_SENDER
    )
    mail.send(msg)