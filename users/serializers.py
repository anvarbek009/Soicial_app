from .models import User
from rest_framework import serializers

class UserCreateSerializers(serializers.ModelSerial):
    id = serializers.UUIDField(read_only=True)
    auth_type = serializers.CharField(read_only=True, max_length=50)