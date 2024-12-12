from django_filters.rest_framework import FilterSet, filters

from quiz.models import (
    Test, Questions, Variants
)


class TestFilter(FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    degree = filters.CharFilter(field_name='degree', lookup_expr='icontains')
    abut = filters.CharFilter(field_name='about', lookup_expr='icontains')
    sciences = filters.CharFilter(field_name='sciences__name', lookup_expr='icontains')

    class Meta:
        model = Test
        fields = ['name', 'degree', 'abut', 'sciences']


class QuestionsFilter(FilterSet):
    about = filters.CharFilter(field_name='about', lookup_expr='icontains')
    test = filters.CharFilter(field_name='test__name', lookup_expr='icontains')

    class Meta:
        model = Questions
        fields = ['about', 'test']


class VariantsFilter(FilterSet):
    text = filters.CharFilter(field_name='text', lookup_expr='icontains')
    question = filters.CharFilter(field_name='question__about', lookup_expr='icontains')

    class Meta:
        model = Variants
        fields = ['text', 'question']
