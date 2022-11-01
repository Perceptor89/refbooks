from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Element, Refbook


class RefbookSerializer(serializers.ModelSerializer):
    id = serializers.CharField(max_length=100)

    class Meta:
        model = Refbook
        fields = ['id', 'code', 'name']


class UserSerializer(serializers.ModelSerializer):
    refbooks = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Refbook.objects.all()
    )

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'refbooks']


class ElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Element
        fields = ['code', 'value']
