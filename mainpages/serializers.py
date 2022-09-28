from rest_framework import serializers
from .models import SpentModel


class UserFromTelegramSer(serializers.Serializer):
    username = serializers.CharField(max_length=50)
    usertgid = serializers.CharField(max_length=50)


class RequestFromTelegramSer(serializers.Serializer):
    usertgid = serializers.CharField(max_length=50)


class GetUserSpentSer(serializers.ModelSerializer):
    class Meta:
        model = SpentModel
        fields = ('title', 'amount', 'price_for_unit', 'category', 'comment')

