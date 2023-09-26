from rest_framework.views import APIView
from rest_framework import filters, status
from django_filters import rest_framework as django_filters
from rest_framework.response import Response
from datetime import datetime

from api.v1.filters import ShopsFilter
from api.v1.models import Store, Product, Sales, SalesForecast
from api.v1.serializers import CategoriesSerializer, SalesSerializer, StoreSerializer, SalesForecastSerializer


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


class SalesForecastView(APIView):
	def post(self, request):
		data = request.data.get("data")
		if data:
			for forecast_data in data:
				serializer = SalesForecastSerializer(data=forecast_data)
				if serializer.is_valid():
					serializer.save()
				else:
					return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
			return Response({"message": "Прогноз успешно сохранен"}, status=status.HTTP_201_CREATED)
		else:
			return Response({"message": "В запросе отсутствую данные"}, status=status.HTTP_400_BAD_REQUEST)

	def get(self, request):
		store_id = request.query_params.get('store_id')
		sku = request.query_params.get('sku')
		start_date_param = request.query_params.get('start_date')
		end_date_param = request.query_params.get('end_date')

		start_date = None
		end_date = None

		if start_date_param:
			start_date = datetime.strptime(start_date_param, "%Y-%m-%d")
		if end_date_param:
			end_date = datetime.strptime(end_date_param, "%Y-%m-%d")

		forecasts = SalesForecast.objects.all()

		if store_id:
			forecasts = forecasts.filter(store__st_id=store_id)
		if sku:
			forecasts = forecasts.filter(product__pr_sku_id=sku)

		if start_date and end_date:
			forecasts = forecasts.filter(forecast_date__gte=start_date, forecast_date__lte=end_date)

		serializer = SalesForecastSerializer(forecasts, many=True)
		return Response({"data": serializer.data})
