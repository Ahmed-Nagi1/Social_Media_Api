from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from allauth.account.models import EmailAddress
from allauth.account.utils import send_email_confirmation
from django.contrib.auth import get_user_model
from allauth.account.views import ConfirmEmailView
from allauth.account.forms import ResetPasswordForm
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import PasswordResetForm


User = get_user_model()

class CustomConfirmEmailView(ConfirmEmailView):
    def get_template_names(self):
        return ["email/email.html"]

    def post(self, *args, **kwargs):
        response = super().post(*args, **kwargs)
        
        if self.object and self.object.email_address.verified:
            return JsonResponse({"status": "success", "message": "Email confirmed successfully."}, status=200)
        else:
            return JsonResponse({"status": "error", "message": "Email confirmation failed."}, status=400)


class PasswordResetAPIView(APIView):
    """
    API View to handle password reset requests.
    """

    def post(self, request, *args, **kwargs):
        # استخدم PasswordResetForm الخاص بـ Django
        form = PasswordResetForm(data=request.data)
        if form.is_valid():
            # حفظ البيانات وإرسال إيميل إعادة تعيين كلمة المرور
            form.save(
                request=request,
                use_https=request.is_secure(),
                from_email=None,  # يمكن تخصيص بريد الإرسال هنا
                email_template_name='registration/password_reset_email.html',  # تأكد من وجود القالب
            )
            return Response(
                {"detail": _("Password reset e-mail has been sent.")},
                status=status.HTTP_200_OK,
            )
        # إذا كانت البيانات غير صحيحة، أعد الأخطاء
        return Response(
            {"errors": form.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )



class ChangeEmailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        email = request.data.get("email")
        action = request.data.get("action")  # change or resend
        print(action)
        if not email:
            return Response({"error": "Email is required"}, status=400)

        if action == "change":
            # 
            user = request.user
            current_email = user.email

            # 
            if current_email == email:
                return Response({"error": "The new email address must be different from the current email"}, status=400)

            # 
            if User.objects.filter(email=email).exclude(id=user.id).exists():
                return Response({"error": "This email is already in use by another user"}, status=400)

            # 
            user.email = email
            user.save()

            # 
            send_email_confirmation(request, user)

            return Response({"message": "Email changed successfully. Please confirm your new email."})

        elif action == "resend":
            # 
            try:
                email_address = EmailAddress.objects.get(user=request.user, email=email)
                
                if email_address.verified:
                    return Response({"message": "This email is already verified"}, status=400)

                # 
                send_email_confirmation(request, request.user, email=email)
                return Response({"message": "Verification email resent successfully."})

            except EmailAddress.DoesNotExist:
                return Response({"error": "This email does not exist for the user"}, status=404)

        else:
            return Response({"error": "Invalid action. Valid actions are 'change' or 'resend'."}, status=400)



