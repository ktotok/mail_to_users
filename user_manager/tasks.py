from __future__ import absolute_import, unicode_literals

from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_email():
    send_mail('Celery Task Worked!',
              'This is proof the task worked!',
              'support@prettyprinted.com',
              ['lopiteh471@officemalaga.com'])

    return None