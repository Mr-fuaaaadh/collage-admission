from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_contact_email(subject, message, from_email):
    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=['muhammadfuhad3@gmail.com'],
        fail_silently=False,
    )