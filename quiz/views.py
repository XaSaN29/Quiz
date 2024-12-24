from datetime import datetime

from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from drf_spectacular.utils import extend_schema
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework import status
from rest_framework import filters

from quiz.filter import (
    TestFilter, QuestionsFilter, VariantsFilter
)
from quiz.models import (
    Users, Shop, Sciences, Test,
    Questions, Variants
)
from quiz.serilayzer import (
    UserSerializer, ConfSerializer, LoginSerializer, ShopSerializer,
    ShopListSerializer, SciencesSerializer, TestSerializer,
    QuestionsSerializer, VariantsSerializer, ShopSotibolishSerializer, UserShopSerializer, ResultSerializer,
    ResultItmSerializer
)
from responses.models import Result, ResultItm


class UserCreateAPIView(CreateAPIView):
    queryset = Users.objects.all()
    serializer_class = UserSerializer


class UserConfirmationView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        request=ConfSerializer
    )
    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = ConfSerializer(data=request.data)
        if serializer.is_valid():
            self.verify_codee(user, serializer.validated_data.get("code"))
            data = {
                'status': 'Success',
                'message': f'Confirmation code {serializer.validated_data["code"]}',
            }
        else:
            data = {
                'status': 'Fail',
                'message': serializer.errors
            }
        return Response(data)

    @staticmethod
    def verify_codee(user, code):
        verification = user.code.filter(
            code=code,
            is_confirm=False,
            expire_time__gte=datetime.now()
        )
        if not verification.exists():
            data = {
                'status': 'Fail',
                'message': 'Code xato yokida eskirgan'
            }
            raise ValidationError(data)
        verification.update(is_confirm=True)
        user.is_verified = True
        user.save()

        return True


class UserLoginAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        request=LoginSerializer
    )
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']

            return Response({
                'access_token': user.token()['access_token'],
                'refresh_token': user.token()['refresh_token']
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ShopListAPIView(ListAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopListSerializer


class ShopCreateAPIView(CreateAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer


class SciencesCreateAPIView(CreateAPIView):
    queryset = Sciences.objects.all()
    serializer_class = SciencesSerializer


class SciencesListAPIView(ListAPIView):
    queryset = Sciences.objects.all()
    serializer_class = SciencesSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class TestListAPIView(ListAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TestFilter


class TestCreateAPIView(CreateAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerializer


class QuestionsListAPIView(ListAPIView):
    queryset = Questions.objects.all()
    serializer_class = QuestionsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = QuestionsFilter


class QuestionsCreateAPIView(CreateAPIView):
    queryset = Questions.objects.all()
    serializer_class = QuestionsSerializer


class VariantsListAPIView(ListAPIView):
    queryset = Variants.objects.all()
    serializer_class = VariantsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = VariantsFilter


class VariantsCreateAPIView(CreateAPIView):
    queryset = Variants.objects.all()
    serializer_class = VariantsSerializer


class SciencesDetailAPIView(APIView):
    def get(self, request, pk):
        try:
            tests = Test.objects.get(pk=pk)
        except tests.DoesNotExist:
            raise NotFound("Bu ID ga tegishli fan topilmadi.")

        serializer = TestSerializer(tests)
        return Response(serializer.data)


class ShopSotibolishAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        request=ShopSotibolishSerializer
    )
    def post(self, request):
        serializer = ShopSotibolishSerializer(data=request.data)
        if serializer.is_valid():
            shop_id = serializer.validated_data['shop_id']
            amount = serializer.validated_data['amount']
            user = request.user

            shop = Shop.objects.get(id=shop_id)
            total_price = serializer.validated_data['sale_price']
            if user.ball >= total_price:
                user.ball -= total_price
                user.save()
                shop.amount -= amount
                shop.save()

                return Response({'message': 'Tovarni sotib oldingiz'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'Coin yetarli emas'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserShopAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserShopSerializer(user)
        return Response(serializer.data)


class ResultAPIView(CreateAPIView):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer
    permission_classes = [permissions.IsAuthenticated]


class ResultItemAPIView(CreateAPIView):
    queryset = ResultItm.objects.all()
    serializer_class = ResultItmSerializer
    permission_classes = [permissions.IsAuthenticated]

