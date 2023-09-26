from rest_framework import filters
from django_filters import rest_framework as django_filters
from .models import Store


class ShopsFilter(django_filters.FilterSet):
    class Meta:
        model = Store
        fields = {
            'st_id': ['exact', 'contains'],
            'st_city_id': ['exact', 'contains'],
            'st_division_code': ['exact', 'contains'],
            'st_type_format_id': ['exact'],
            'st_type_loc_id': ['exact'],
            'st_type_size_id': ['exact'],
            'st_is_active': ['exact'],
        }