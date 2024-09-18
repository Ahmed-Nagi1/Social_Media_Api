from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from rest_framework.views import APIView
from django_rest_passwordreset.signals import reset_password_token_created
from django.urls import reverse
from django.dispatch import receiver
from rest_framework_simplejwt.tokens import RefreshToken


from .serializers import (RegisterSerializer,
                        ChangePasswordSerializer,
)



class RegisterViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    if request.method == 'POST':
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if user.check_password(serializer.data.get('old_password')):
                user.set_password(serializer.data.get('new_password'))
                user.save()
                update_session_auth_hash(request, user)  # To update session after password change
                return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)
            return Response({'error': 'Incorrect old password.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    context = {
        'current_user': reset_password_token.user,
        'username': reset_password_token.user.username,
        'email': reset_password_token.user.email,
        'reset_password_url': "{}?token={}".format(
            instance.request.build_absolute_uri(reverse('password_reset:reset-password-confirm')),
            reset_password_token.key)
    }

    # render email text
    email_html_message = render_to_string('email/password_reset_email.html', context)
    email_plaintext_message = render_to_string('email/password_reset_email.txt', context)

    msg = EmailMultiAlternatives(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()
