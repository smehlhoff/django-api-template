from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .utils import email_token_generator

from_email = settings.EMAIL_FROM


def send_reset_password_email(user):
    context = {
        'username': user.username,
        'site_name': settings.SITE_NAME,
        'site_url': settings.SITE_URL,
        'uid': urlsafe_base64_encode(force_bytes(user.id)).decode(),
        'token': default_token_generator.make_token(user),
    }

    subject = loader.render_to_string(
        'registration/email/password_reset_subject.txt', context)
    subject = ''.join(subject.splitlines())
    body = loader.render_to_string(
        'registration/email/password_reset.html', context)

    email_message = EmailMultiAlternatives(
        subject, body, from_email, [user.email])
    email_message.send()


def send_password_changed_email(user):
    context = {
        'username': user.username,
        'site_name': settings.SITE_NAME,
        'site_url': settings.SITE_URL,
    }

    subject = loader.render_to_string(
        'registration/email/password_changed_subject.txt', context)
    subject = ''.join(subject.splitlines())
    body = loader.render_to_string(
        'registration/email/password_changed.html', context)

    email_message = EmailMultiAlternatives(
        subject, body, from_email, [user.email])
    email_message.send()


def send_email_verification(user):
    context = {
        'username': user.username,
        'site_name': settings.SITE_NAME,
        'site_url': settings.SITE_URL,
        'uid': urlsafe_base64_encode(force_bytes(user.id)).decode(),
        'token': email_token_generator.make_token(user),
    }

    subject = loader.render_to_string(
        'registration/email/email_verification_subject.txt', context)
    subject = ''.join(subject.splitlines())
    body = loader.render_to_string(
        'registration/email/email_verification.html', context)

    email_message = EmailMultiAlternatives(
        subject, body, from_email, [user.email])
    email_message.send()
