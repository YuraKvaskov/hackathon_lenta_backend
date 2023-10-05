from rest_framework import serializers
from api.v1.models import Store, Product, Sales, SalesForecast, FilterTemplate
from django.contrib.auth import get_user_model
from datetime import datetime

from users.models import UserStore

User = get_user_model()


class FilterTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FilterTemplate
        fields = '__all__'


class InfoHeaderSerializer(serializers.ModelSerializer):
    current_date = serializers.SerializerMethodField()
    store_ids = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'store_ids', 'current_date')

    def get_current_date(self, obj):
        current_date = datetime.now().strftime('%d %B %Y')
        return current_date

    def get_store_ids(self, obj):
        user_stores = UserStore.objects.filter(user=obj)
        store_ids = [store.store.st_id for store in user_stores]
        return store_ids


class SalesForecastSerializer(serializers.ModelSerializer):
    forecast = serializers.JSONField()  # Здесь предполагается, что поле "forecast" будет JSON-строкой
    selected = serializers.BooleanField(default=False)

    class Meta:
        model = SalesForecast
        fields = ('selected', 'store', 'product', 'forecast_date', 'forecast')

    def to_representation(self, instance):
        # Преобразуйте даты из формата datetime в строку "год-месяц-день"
        instance.forecast_date = instance.forecast_date.strftime("%Y-%m-%d")
        return super().to_representation(instance)


class StoreSerializer(serializers.ModelSerializer):
    st_is_active = serializers.SerializerMethodField()
    
    class Meta:
        model = Store
        fields = '__all__'
        
    def get_st_is_active(self, obj):
        return int(obj.st_is_active)


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class SalesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sales
        fields = [
            'date',
            'pr_sales_type_id',
            'pr_sales_in_units',
            'pr_promo_sales_in_units',
            'pr_sales_in_rub',
            'pr_promo_sales_in_rub'
        ]