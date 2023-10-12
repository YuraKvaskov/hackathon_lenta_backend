from rest_framework import serializers
from api.v1.models import Store, Product, Sales, SalesForecast, FilterTemplate, ProductSubcategory, ProductCategory, \
    ProductGroup, City
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


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['pr_sku_id']

class ProductSubcategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = ProductSubcategory
        fields = ['pr_subcat_id', 'products']

class ProductCategorySerializer(serializers.ModelSerializer):
    subcategories = ProductSubcategorySerializer(many=True)

    class Meta:
        model = ProductCategory
        fields = ['pr_cat_id', 'subcategories']

class ProductGroupSerializer(serializers.ModelSerializer):
    categories = ProductCategorySerializer(many=True)

    class Meta:
        model = ProductGroup
        fields = ['pr_group_id', 'categories']

class StoreSerializer(serializers.ModelSerializer):
    st_city_id = CitySerializer()

    class Meta:
        model = Store
        fields = '__all__'

class SalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sales
        fields = '__all__'

# class SalesForecastSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = SalesForecast
#         fields = '__all__'
#
#     def to_representation(self, instance):
#         # Преобразуйте даты из формата datetime в строку "год-месяц-день"
#         instance.forecast_date = instance.forecast_date.strftime("%Y-%m-%d")
#         return super().to_representation(instance)

class SalesForecastSerializer(serializers.ModelSerializer):
    forecast  = serializers.JSONField()
    class Meta:
        model = SalesForecast
        fields = ('store', 'product', 'forecast_date', 'forecast')

     # Здесь предполагается, что поле "forecast" будет JSON-строкой
    # selected = serializers.BooleanField(default=False)


    def to_representation(self, instance):
        # Преобразуйте даты из формата datetime в строку "год-месяц-день"
        instance.forecast_date = instance.forecast_date.strftime("%Y-%m-%d")
        return super().to_representation(instance)

#
# class StoreSerializer(serializers.ModelSerializer):
#     st_is_active = serializers.SerializerMethodField()
#
#     class Meta:
#         model = Store
#         fields = '__all__'
#
#     def get_st_is_active(self, obj):
#         return int(obj.st_is_active)
#
#
# class CategoriesSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = '__all__'
#
#
# class SalesSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Sales
#         fields = [
#             'date',
#             'pr_sales_type_id',
#             'pr_sales_in_units',
#             'pr_promo_sales_in_units',
#             'pr_sales_in_rub',
#             'pr_promo_sales_in_rub'
#         ]