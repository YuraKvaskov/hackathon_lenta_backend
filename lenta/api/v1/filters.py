from django_filters import rest_framework as django_filters
from api.v1.models import Store


class ShopsFilter(django_filters.FilterSet):
    class Meta:
        model = Store
        fields = {
            'st_id': ['exact'],
            'st_division_code': ['exact'],
            'st_type_format_id': ['exact'],
            'st_type_loc_id': ['exact'],
            'st_type_size_id': ['exact'],
            'st_is_active': ['exact'],
            'st_city_id': ['exact'],  # Поле st_city_id присутствует в модели Store
        }