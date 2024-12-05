from django.contrib import admin

from quiz.models import Users, Shop, Variants, Test, Sciences, UserConfig, Questions


# Register your models here.

@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('username', 'id',  'email', 'roles', 'degree')
    list_filter = ('roles', 'degree', 'id', 'email')


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('name', 'abut', 'amount', 'coin', 'sale')
    list_filter = ('name', 'abut', 'amount', 'coin', 'sale')


@admin.register(Variants)
class VariantsAdmin(admin.ModelAdmin):
    list_display = ('text', 'is_true', 'question')


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('name', 'degree', 'about', 'sciences')
    list_filter = ('name', 'degree')


@admin.register(Questions)
class QuestionsAdmin(admin.ModelAdmin):
    list_display = ('about', 'test')

@admin.register(Sciences)
class SciencesAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(UserConfig)
class UserConfigAdmin(admin.ModelAdmin):
    list_display = ('user', 'code', 'expire_time', 'is_confirm')
