from rest_framework import serializers

class ChangeEmailSerializer(serializers.Serializer):
    current_email = serializers.EmailField()
    new_email = serializers.EmailField()

    def validate_new_email(self, value):
        from allauth.account.models import EmailAddress
        if EmailAddress.objects.filter(email=value).exists():
            raise serializers.ValidationError("البريد الإلكتروني مستخدم بالفعل.")
        return value
