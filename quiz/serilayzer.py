from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth import authenticate


from quiz.models import Users, UserConfig, Shop, Sciences, Test, Questions, Variants


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


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ['name', 'abut', 'amount', 'coin', 'is_active', 'sale']


class ShopListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ['name', 'abut', 'amount', 'coin', 'is_active', 'sale', 'sale_price']


class SciencesSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Sciences
        fields = ['id', 'name']


class TestSerializer(serializers.ModelSerializer):
    sciences = serializers.SlugRelatedField(
        queryset=Sciences.objects.all(),
        slug_field='slug'
    )
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Test
        fields = ['id', 'name', 'degree', 'about', 'sciences']


class QuestionsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    test = serializers.CharField(source='test.name', read_only=True)

    class Meta:
        model = Questions
        fields = ['id', 'about', 'test']


class VariantsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    question = serializers.CharField(source='question.about', read_only=True)

    class Meta:
        model = Variants
        fields = ['id', 'text', 'is_true', 'question']
