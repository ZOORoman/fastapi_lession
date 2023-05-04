import smtplib
from email.message import EmailMessage

from celery import Celery

from config import SMTP_PASSWORD, SMTP_FROM, SMTP_TO

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465

celery = Celery('tasks', broker='redis://localhost:6379')


def get_email_template_dashboard(username: str):
    email = EmailMessage()
    email['Subject'] = 'WakeMeTrip'
    email['From'] = SMTP_FROM
    email['To'] = SMTP_TO

    email.set_content(
        '<div>'
        f'<h1 style="color: red;">Хэй, {username}! Твое путешествие оформлено 🚀</h1>'
        '<img src="https://sun2-20.userapi.com/impf/c858328/v858328568/5d637/'
        'gR9sxyFFJNk.jpg?size=1280x960&quality=96&sign=b59948f73f7105ced320168f936bbfb2&type=album"'
        ' width="600">'
        '</div>',
        subtype='html'
    )
    return email


@celery.task
def send_email_report_dashboard(username: str):
    email = get_email_template_dashboard(username)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_FROM, SMTP_PASSWORD)
        server.send_message(email)