from rest_framework.views import APIView
from rest_framework import filters
from django_filters import rest_framework as django_filters
from rest_framework.response import Response

from api.v1.filters import ShopsFilter
from api.v1.models import Store, Product, Sales
from api.v1.serializers import CategoriesSerializer, SalesSerializer, StoreSerializer


class SalesView(APIView):
	def get(self, request):
		product_id = request.query_params.get('product_id')
		store_id = request.query_params.get('store_id')

		if product_id and store_id:
			sales = Sales.objects.filter(product__pr_sku_id=product_id, store__st_id=store_id)
		else:
			sales = Sales.objects.all()

		serializer = SalesSerializer(sales, many=True)
		return Response({"data": serializer.data})


class CategoriesView(APIView):
	def get(self, request):
		categories = Product.objects.all()
		serializer = CategoriesSerializer(categories, many=True)
		return Response({"data": serializer.data})


class ShopsView(APIView):
	filter_backends = [filters.OrderingFilter, django_filters.DjangoFilterBackend]
	filterset_class = ShopsFilter
	ordering_fields = '__all__'

	def filter_queryset(self, queryset):
		return self.filterset_class(self.request.GET, queryset=queryset).qs

	def get(self, request):
		queryset = Store.objects.all()
		queryset = self.filter_queryset(queryset)
		serializer = StoreSerializer(queryset, many=True)
		return Response({"data": serializer.data})
