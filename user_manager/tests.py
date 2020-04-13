import pytest
from unittest.mock import patch

from django.contrib.auth.models import User
from django.core import mail
from user_manager.tasks import send_email_to_user


@pytest.fixture(autouse=True)
def email_backend_setup(settings):
    settings.EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'


@pytest.mark.django_db
def test_send():
    user_name = 'dummy_user'
    user_pass = 'uT3%zO8UWhp0'
    user_email = 'dummy@mail.com'
    email_content = 'This is a notification message for user "{name}"!'

    user_obj = User.objects.filter(username=user_name)
    if not user_obj.exists():
        new_user = User(username=user_name, email=user_email)
        new_user.set_password(user_pass)
        new_user.save()

    send_email_to_user(user_obj.first().id)

    assert len(mail.outbox) == 1
    assert mail.outbox[0].body == email_content.format(name=user_name)
    assert user_email in mail.outbox[0].to
