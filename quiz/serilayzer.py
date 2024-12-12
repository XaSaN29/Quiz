from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth import authenticate


from quiz.models import (
    Users, Shop, Sciences, Test,
    Questions, Variants
)


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
        fields = ['id', 'name', 'slug']


class TestSerializer(serializers.ModelSerializer):
    sciences = serializers.SlugRelatedField(
        queryset=Sciences.objects.all(),
        slug_field='slug'
    )
    id = serializers.IntegerField(read_only=True)
    questions = serializers.SerializerMethodField()

    class Meta:
        model = Test
        fields = ['id', 'name', 'degree', 'about', 'sciences', 'questions']

    def get_questions(self, obj):
        questions = obj.questions.all()
        return QuestionsSerializer(questions, many=True).data


class QuestionsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    test = serializers.CharField(source='test.name', read_only=True)
    variants = serializers.SerializerMethodField()

    class Meta:
        model = Questions
        fields = ['id', 'about', 'test', 'variants']

    def get_variants(self, obj):
        variants = obj.variants.all()
        return VariantsSerializer(variants, many=True).data


class VariantsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    question = serializers.CharField(source='question.about', read_only=True)

    class Meta:
        model = Variants
        fields = ['id', 'text', 'is_true', 'question']


class ShopSotibolishSerializer(serializers.ModelSerializer):
    shop_id = serializers.IntegerField(write_only=True)
    amount = serializers.IntegerField(write_only=True)
    sale_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Shop
        fields = ['shop_id', 'amount', 'sale_price']
        read_only_fields = ['sale_price']

    def validate(self, data):
        shop_id = data.get('shop_id')
        amount = data.get('amount')
        try:
            shop = Shop.objects.get(id=shop_id, is_active=True)
        except Shop.DoesNotExist:
            raise serializers.ValidationError({'shop_id': 'Bunday faol mahsulot mavjud emas.'})

        if shop.amount < amount:
            raise serializers.ValidationError({'amount': 'Mahsulotning yetarli miqdori mavjud emas.'})

        data['sale_price'] = (shop.coin - (shop.coin * shop.sale / 100)) * amount
        return data

