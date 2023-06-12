from rest_framework.response import Response
from api_user.models import Account, User
from rest_framework import status
from django.core.mail import EmailMessage
from django.template.loader import get_template
import secrets
import string
from django.core.mail import send_mail
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)


@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def forgot_password(request):
    data = request.data
    email = data.get('email')
    account = Account.objects.filter(email=email)
    if account.exists():
        account = account.first()
        password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(6))
        account.set_password(password)
        account.save()
        user = User.objects.get(account_id=account.id)
        mail_subject = 'Reset your password'
        # current_site = get_current_site(self.context['request'])
        message = get_template('password_reset_email.html').render(
            {
                'user': user.full_name,
                'title': "Read News By Topic",
                'password': password,
            }
        )
        email = EmailMessage(mail_subject, message, to=[account.email])
        email.content_subtype = 'html'
        email.send(fail_silently=False)

    else:
        return Response({'Error': 'Your email not exists!'}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'success': 'We have sent you a link to reset your password.'}, status=status.HTTP_200_OK)
