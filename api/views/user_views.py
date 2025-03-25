
from django.contrib.auth.models import User
from rest_framework import generics

from rest_framework.decorators import action
from django.shortcuts import get_object_or_404


from ..serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny



class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
