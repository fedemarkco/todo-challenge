from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Task


def required(value):
    if value is None:
        raise serializers.ValidationError('This field is required')


class TaskSerializers(serializers.ModelSerializer):
    title = serializers.CharField(validators=[required])
    description = serializers.CharField(validators=[required])

    class Meta:
        model = Task
        fields = ['title', 'description', 'completed']

    def create(self, validated_data):
        return Task.objects.create(**validated_data)


class UserLoginSerializers(serializers.Serializer):
    email = serializers.EmailField(validators=[required])
    password = serializers.CharField(validators=[required])

    def validate(self, data):
        user = User.objects.filter(
            email=data['email'],
            password=data['password']
        )
        if user:
            return user.first()
        raise serializers.ValidationError('Incorrect Credentials Passed.')


class UserSignupSerializers(serializers.Serializer):
    email = serializers.EmailField(validators=[required])
    password = serializers.CharField(validators=[required])

    def validate(self, validated_data):
        email = User.objects.filter(email=validated_data['email'])
        if email:
            raise serializers.ValidationError('User exist!')
        user = User.objects.filter(
            email=validated_data['email'],
            password=validated_data['password']
        )
        if user:
            raise serializers.ValidationError('User exist!')
        return validated_data

    def create(self, validated_data):
        validated_data['username'] = validated_data['email']
        user = User.objects.create(**validated_data)
        return user
