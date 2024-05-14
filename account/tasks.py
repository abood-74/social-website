from celery import shared_task
from datetime import datetime, timedelta
from django.core.mail import send_mail

from django.conf import settings
from .models import CustomUser
from images.models import Image

@shared_task
def send_inactive_users_email():
    try:
        thirty_days_ago = datetime.now() - timedelta(days=30)
        active_users = Image.objects.filter(created__gte=thirty_days_ago).values_list('user', flat=True)
        inactive_users = CustomUser.objects.exclude(id__in=active_users)
        for user in inactive_users:
            send_mail(
                'Your Inactivity on Our Platform',
                f"Dear {user.username},\n\nYour inactivity is causing a decrease in popularity on our platform. Consider creating a new post to engage with your followers.",
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )

        print(f"Inactive user emails sent: {len(inactive_users)}")
    except Exception as e:
        print(f"Error sending inactive user emails: {e}")
        
        
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings    

@shared_task
def send_congratulatory_email(user):
    try:
        message = f"Your Account Creation was successful! Welcome to our platform, {user['username']}!"

        # Send the email
        send_mail(
            "Account Creation Successful!",
            message,
            settings.EMAIL_HOST_USER,  
            [user["email"],],  
            fail_silently=False,
        )

        print(f"Congratulatory email sent to {user['username']}")
    except Exception as e:
        print(f"Error sending congratulatory email to {user['username']}: {e}")