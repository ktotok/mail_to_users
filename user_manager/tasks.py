from __future__ import absolute_import, unicode_literals

from celery import shared_task
from django.contrib.auth.models import User
from django.core.mail import send_mail


@shared_task
def send_email_to_user(user_id):
    user_obj = User.objects.filter(pk=user_id)
    if user_obj.exists():
        send_mail('Notification',
                  'This is a notification message for user "{name}"!'.format(name=user_obj.first().username),
                  'mail_sender@mail.host.com',
                  [f'{user_obj.first().email}'])

    return None
