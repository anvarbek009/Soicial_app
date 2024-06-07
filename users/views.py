from django.shortcuts import render
from .models import User ,ConfirmUser
from .serializers import UserCreateSerializers
from rest_framework.generics import CreateAPIView
# Create your views here.



class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializers