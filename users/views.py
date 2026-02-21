from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import PasswordResetCode
from .serializers import (
    PasswordResetRequestSerializer,
    PasswordResetVerifySerializer,
    PasswordResetConfirmSerializer
)
from django.core.mail import send_mail
from django.conf import settings

class PasswordResetRequestView(generics.GenericAPIView):
    serializer_class = PasswordResetRequestSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"detail": "Пользователь не найден"}, status=404)
        code = PasswordResetCode.generate_code()
        PasswordResetCode.objects.create(user=user, code=code)
        send_mail(
            subject='Код для сброса пароля',
            message=f'Ваш код для сброса пароля: {code}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
        )
        return Response({"detail": "Код отправлен на почту"})


class PasswordResetVerifyView(generics.GenericAPIView):
    serializer_class = PasswordResetVerifySerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        code = serializer.validated_data['code']
        try:
            user = User.objects.get(email=email)
            reset_code = PasswordResetCode.objects.filter(user=user, code=code, is_used=False).last()
        except User.DoesNotExist:
            return Response({"detail": "Неверные данные"}, status=400)
        if not reset_code or reset_code.is_expired():
            return Response({"detail": "Код недействителен или истёк"}, status=400)
        return Response({"detail": "Код подтверждён"})


class PasswordResetConfirmView(generics.GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        code = serializer.validated_data['code']
        new_password = serializer.validated_data['new_password']
        try:
            user = User.objects.get(email=email)
            reset_code = PasswordResetCode.objects.filter(user=user, code=code, is_used=False).last()
        except User.DoesNotExist:
            return Response({"detail": "Неверные данные"}, status=400)
        if not reset_code or reset_code.is_expired():
            return Response({"detail": "Код недействителен или истёк"}, status=400)
        user.set_password(new_password)
        user.save()
        reset_code.is_used = True
        reset_code.save()
        return Response({"detail": "Пароль успешно изменён"})