from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth import authenticate


from quiz.models import Users, UserConfig


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Users
        fields = ['id', 'email', 'username', 'password']

    def create(self, validated_data):
        user = Users.objects.create(
            username=validated_data.get('username'),
            email=validated_data.get('email'),


        )
        user.set_password(validated_data.get('password'))
        user.save()
        user.create_verification_code()
        return user

    def to_representation(self, instance):
        user = super(UserSerializer, self).to_representation(instance)
        user.update(instance.token())
        return user


class ConfSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=4, write_only=True)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError("Username yoki parol noto'g'ri!")

        attrs['user'] = user
        return attrs
