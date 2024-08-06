from django.conf import settings
from django.core.mail import send_mail


def send_verification_email(name, email, token):
    subject = 'Verify Your Jobfinity Account - Action Required'
    message = (
        f'Dear {name}, Welcome to Jobfinity! We are excited to have you on board and ready to help you find your dream job. To ensure the security of your account and start exploring our platform, we need to verify your email address.'
        f'Please click the verification link below to activate your Jobfinity account: http://127.0.0.1:8000/verify/{token}')
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
