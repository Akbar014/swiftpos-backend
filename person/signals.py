# signals.py
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail
from django.dispatch import receiver
from django.conf import settings

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Handles password reset tokens
    """
    confirm_link = f"http://127.0.0.1:5501/new_pass.html?token={reset_password_token.key}"
    
    email_plaintext_message = f"Your password reset link is: {confirm_link}" 

   
    send_mail(
        # subject:
        "Password Reset for {title}".format(title="Your App Name"),
        # message:
        email_plaintext_message,
        # from email:
        settings.DEFAULT_FROM_EMAIL,
        # recipient list:
        [reset_password_token.user.email]
    )
 