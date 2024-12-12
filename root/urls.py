"""
URL configuration for root project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from quiz.views import (
    UserCreateAPIView, UserConfirmationView, UserLoginAPIView,
    ShopListAPIView, ShopCreateAPIView, SciencesCreateAPIView,
    SciencesListAPIView, TestCreateAPIView, TestListAPIView,
    QuestionsListAPIView, QuestionsCreateAPIView, VariantsListAPIView,
    VariantsCreateAPIView, SciencesDetailAPIView, ShopSotibolishAPIView
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('user-create/', UserCreateAPIView.as_view(), name='user_create'),
    path('user-confirm/', UserConfirmationView.as_view(), name='user_confirm'),
    path('user-login/', UserLoginAPIView.as_view(), name='user_login'),
    path('shop-list/', ShopListAPIView.as_view(), name='shop_list'),
    path('shop-create/', ShopCreateAPIView.as_view(), name='shop_create'),
    path('science-create/', SciencesCreateAPIView.as_view(), name='science_create'),
    path('science-list/', SciencesListAPIView.as_view(), name='science_list'),
    path('test-create/', TestCreateAPIView.as_view(), name='test_create'),
    path('test-list/', TestListAPIView.as_view(), name='test_list'),
    path('question-create/', QuestionsCreateAPIView.as_view(), name='question_create'),
    path('question-list/', QuestionsListAPIView.as_view(), name='question_list'),
    path('variant-list/', VariantsListAPIView.as_view(), name='variant_list'),
    path('variant-create/', VariantsCreateAPIView.as_view(), name='variant_create'),
    path('quis/<int:pk>/', SciencesDetailAPIView.as_view(), name='variant_create'),
    path('shop-olish', ShopSotibolishAPIView.as_view())

]
