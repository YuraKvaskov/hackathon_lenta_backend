from rest_framework import serializers
from api.v1.models import Store, Product, Sales, SalesForecast


class SalesForecastSerializer(serializers.ModelSerializer):
    forecast = serializers.JSONField()  # Здесь предполагается, что поле "forecast" будет JSON-строкой

    class Meta:
        model = SalesForecast
        fields = ('store', 'product', 'forecast_date', 'forecast')

    def to_representation(self, instance):
        # Преобразуйте даты из формата datetime в строку "год-месяц-день"
        instance.forecast_date = instance.forecast_date.strftime("%Y-%m-%d")
        return super().to_representation(instance)


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'


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