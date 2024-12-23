from allauth.account.views import ConfirmEmailView
from django.http import JsonResponse

from dj_rest_auth.views import LoginView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from datetime import timedelta



class CustomLoginView(LoginView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200 and 'key' in response.data:
            token = response.data['key']
            response.set_cookie(
                key='auth_token',
                value=token,
                # httponly=True, 
                secure=False,   
                samesite='Lax' 
            )
            # del response.data['key']
        return response



class CustomConfirmEmailView(ConfirmEmailView):
    def get_template_names(self):
        return ["email/email.html"]

    def post(self, *args, **kwargs):
        response = super().post(*args, **kwargs)
        
        if self.object and self.object.email_address.verified:
            return JsonResponse({"status": "success", "message": "Email confirmed successfully."}, status=200)
        else:
            return JsonResponse({"status": "error", "message": "Email confirmation failed."}, status=400)
