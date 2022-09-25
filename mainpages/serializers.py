from rest_framework import serializers


class UserFromTelegramSer(serializers.Serializer):
    username = serializers.CharField(max_length=50)
    usertgid = serializers.CharField(max_length=50)
