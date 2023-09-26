from rest_framework import serializers
from .models import Store, Product, Sales


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
        fields = '__all__'