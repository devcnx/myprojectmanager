from celery import shared_task
from django.core.mail import send_mail
from django.contrib.auth.models import User


@shared_task
def send_email():
    users = User.objects.all()
    user_count = users.count()

    subject = f'Test Email for Celery - {user_count} Users'
    message = 'Here is a list of Users : \n\n'
    for user in users:
        message += f'{user.username} - {user.email}\n'
    from_email = 'automations@upandcs.com'
    recipient_list = ['brittaney@upandcs.com']

    send_mail(subject, message, from_email, recipient_list)
