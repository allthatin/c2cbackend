
from django.template.loader import render_to_string
from config import celery_app
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from django.core.mail import EmailMessage
from django.conf import settings
from analytics.models import View
from alert.models import AlertHistory
from cs.models import Inquiry

User = get_user_model()

def send_email_as_html(receiver, title, html, params):

    # if settings.ENV != 'prod':
    #     return

    from_email = settings.EMAIL_FROM_EMAIL
    body = render_to_string(html, params)
    try:
        email = EmailMessage(
            title,  # subject
            body,  # message
            from_email,  # from email
            [receiver],  # to email
        )
        email.content_subtype = 'html'  # set content type to html
        email.send()

    except Exception as e:
        print(e)

    finally:
        print('email sent')

@celery_app.task(bind=True)
def register_confirmation_email(_, user_id):
    user = User.objects.get(id=user_id)
    greetings = "Good Morning!" if 6 <= now().hour < 12 else "Good Afternoon!" if 12 <= now().hour < 18 else "Good Evening!"
    params = {
        'greetings': greetings,
        'span1': '날라날라 대표 이정호 입니다.',
        'span2': '번거로운 가구 거래 편리하게 할 수 있도록 도와드리겠습니다.',
    }

    send_email_as_html(
        user.email, 
        '[날라날라] 가입해주셔서 감사합니다', 
        'email/welcome_template.html', 
        params)

@celery_app.task(bind=True)
def send_email_by_viewmodel(_, view_id, alert_id):
    view = View.objects.get(id=view_id)
    alerthistory = AlertHistory.objects.get(id=alert_id)
    content_object = view.content_object
    author = content_object.user

    greetings = "Good Morning!" if 6 <= now().hour < 12 else "Good Afternoon!" if 12 <= now().hour < 18 else "Good Evening!"
    title = alerthistory.title
    content = alerthistory.content

    params = {
        'greetings': greetings,
        'span1': title,
        'span2': content,
    }

    send_email_as_html(
        author.email, 
        f'[날라날라] {content}', 
        'email/visitor_alert_template.html', 
        params)
    
@celery_app.task(bind=True)
def send_cs_alert_email(_, alert_id):
    alerthistory = AlertHistory.objects.get(id=alert_id)
    user = alerthistory.user
    title = alerthistory.title
    content = alerthistory.content

    params = {
        'greetings': 'Good Morning!',
        'span1': title,
        'span2': content,
    }

    send_email_as_html(
        user.email, 
        f'[날라날라] {title}', 
        'email/visitor_alert_template.html', 
        params)