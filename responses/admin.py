from django.contrib import admin

from responses.models import Result, ResultItm


# Register your models here.


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'test', 'balls', 'start_time', 'end_time', 'time')


@admin.register(ResultItm)
class ResultItmAdmin(admin.ModelAdmin):
    list_display = ('result', 'question', 'answer')
    