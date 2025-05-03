import django_filters
from .models import Exercise
from django_filters import rest_framework as filters

class CommaSeparatedListFilter(filters.BaseInFilter, filters.CharFilter):
    def filter(self, qs, value):
        if value:
            if isinstance(value, str):
                value = [v.strip() for v in value.split(',')]
        return super().filter(qs, value)
class ExerciseFilter(filters.FilterSet):
    tags = CommaSeparatedListFilter(field_name='tags__name', lookup_expr='in')
    muscle_groups = CommaSeparatedListFilter(field_name='muscle_groups__name', lookup_expr='in')
    difficulty = CommaSeparatedListFilter(field_name='difficulty', lookup_expr='in')
    equipments = CommaSeparatedListFilter(field_name='equipments__name', lookup_expr='in')

    class Meta:
        model = Exercise
        fields = ['tags', 'muscle_groups', 'difficulty', 'equipments']