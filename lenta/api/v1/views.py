from io import BytesIO
import pandas as pd

from rest_framework.views import APIView
from rest_framework import filters, status
from django_filters import rest_framework as django_filters
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponse

from rest_framework.response import Response
from datetime import datetime, timedelta
from rest_framework import permissions
from rest_framework.decorators import action, permission_classes


from api.v1.filters import ShopsFilter
from api.v1.models import Store, Product, Sales, SalesForecast, FilterTemplate
from api.v1.serializers import CategoriesSerializer, SalesSerializer, StoreSerializer, SalesForecastSerializer, \
    InfoHeaderSerializer, FilterTemplateSerializer


class SaveFilterTemplateView(APIView):
    def get(self, request):
        user = request.user
        templates = FilterTemplate.objects.filter(user=user)
        serializer = FilterTemplateSerializer(templates, many=True)
        return Response(serializer.data)

    def post(self, request):
        user = request.user
        data = request.data
        template_name = data.get('template_name')
        st_city_id = data.get('st_city_id')
        store_id = data.get('store_id')
        pr_group_id = data.get('pr_group_id')
        pr_cat_id = data.get('pr_cat_id')
        pr_subcat_id = data.get('pr_subcat_id')
        selected_interval = int(data.get('selected_interval', 14))

        filter_template, created = FilterTemplate.objects.get_or_create(
            user=user,
            name=template_name,
        )
        filter_template.st_city_id = st_city_id
        filter_template.store_id = store_id
        filter_template.pr_group_id = pr_group_id
        filter_template.pr_cat_id = pr_cat_id
        filter_template.pr_subcat_id = pr_subcat_id
        filter_template.selected_interval = selected_interval
        filter_template.save()

        return Response({'message': 'Шаблон успешно сохранен'}, status=status.HTTP_201_CREATED)

    def delete(self, request, template_id):
        try:
            user = request.user
            template = FilterTemplate.objects.get(user=user, id=template_id)
            template.delete()
            return Response({'message': 'Шаблон успешно удален'}, status=status.HTTP_204_NO_CONTENT)
        except FilterTemplate.DoesNotExist:
            return Response({'message': 'Шаблон не найден'}, status=status.HTTP_404_NOT_FOUND)


class InfoHeaderView(APIView):
    def get(self, request):
        user = request.user
        serializer = InfoHeaderSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


# @permission_classes([permissions.IsAuthenticated])  # как будет отбращаться ML?
class SalesView(APIView):
    """
    Возвращает временной ряд с информацией о количестве проданных товаров.
    Обязательные входные параметры запроса: id товара, id ТЦ.\n
    Образец запроса
    /?store_id=<store_id>&product_id=<product_id>
    """
    serializer_class = SalesSerializer

    def get(self, request):
        product_id = request.query_params.get('product_id')
        store_id = request.query_params.get('store_id')
        if product_id and store_id:
            sales = Sales.objects.filter(product__pr_sku_id=product_id, store__st_id=store_id)
        serialized_sales = self.serializer_class(sales, many=True).data
        response_data = {"data": [
            {
                "store_id": store_id,
                "product_id": product_id,
                "fact": serialized_sales
            }
        ]}
        return Response(response_data)


# @permission_classes([permissions.IsAuthenticated])
class CategoriesView(APIView):
    serializer_class = CategoriesSerializer

    def get(self, request):
        categories = Product.objects.all()
        serializer = self.serializer_class(categories, many=True)
        return Response({"data": serializer.data})


# @permission_classes([permissions.IsAuthenticated])
class ShopsView(APIView):
    serializer_class = StoreSerializer

    filter_backends = [filters.OrderingFilter, django_filters.DjangoFilterBackend]
    filterset_class = ShopsFilter
    ordering_fields = '__all__'

    def filter_queryset(self, queryset):
        return self.filterset_class(self.request.GET, queryset=queryset).qs

    def get(self, request):
        queryset = Store.objects.all()
        queryset = self.filter_queryset(queryset)
        serializer = self.serializer_class(queryset, many=True)
        return Response({"data": serializer.data})


# @permission_classes([permissions.IsAuthenticated])
class SalesForecastView(APIView):
    serializer_class = SalesForecastSerializer

    def post(self, request):
        data = request.data.get("data")
        if data:
            for forecast_data in data:
                serializer = self.serializer_class(data=forecast_data)
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({"message": "Прогноз успешно сохранен"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "В запросе отсутствуют данные"}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):

        st_city_id = request.query_params.get('st_city_id')
        store_id = request.query_params.get('store_id')
        pr_group_id = request.query_params.get('pr_group_id')
        pr_cat_id = request.query_params.get('pr_cat_id')
        pr_subcat_id = request.query_params.get('pr_subcat_id')
        selected_interval = int(request.query_params.get('selected_interval', 14))

        start_date = datetime.now().date() + timedelta(days=1)
        end_date = start_date + timedelta(days=selected_interval)

        filters = {}
        if st_city_id:
            filters['store__st_city_id'] = st_city_id
        if store_id:
            filters['store__st_id'] = store_id
        if pr_group_id:
            filters['product__pr_group_id'] = pr_group_id
        if pr_cat_id:
            filters['product__pr_cat_id'] = pr_cat_id
        if pr_subcat_id:
            filters['product__pr_subcat_id'] = pr_subcat_id
        try:
            forecasts = SalesForecast.objects.filter(
                forecast_date__gte=start_date,
                forecast_date__lte=end_date,
                **filters
            )
        except ObjectDoesNotExist:
            return JsonResponse({'data': []})

        serializer = self.serializer_class(forecasts, many=True)
        return JsonResponse({'data': serializer.data})


class ExportSelectedForecastsToExcelView(APIView):
    def post(self, request):
        data = request.data.get("data")
        if data:
            selected_forecasts = [item for item in data if item.get('selected')]
            if selected_forecasts:
                df_data = {
                    'forecast_date': [],
                    'store': [],
                    'product': [],
                    'forecast': [],
                }
                for forecast in selected_forecasts:
                    df_data['forecast_date'].append(forecast['forecast_date'])
                    df_data['store'].append(forecast['store'])
                    df_data['product'].append(forecast['product'])
                    df_data['forecast'].append(forecast['forecast'])
                df = pd.DataFrame(df_data)

                output = BytesIO()
                writer = pd.ExcelWriter(output, engine='xlsxwriter')
                df.to_excel(writer, sheet_name='Selected Forecasts', index=False)
                writer.save()

                response = HttpResponse(output.getvalue(),
                                        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = 'attachment; filename=selected_forecasts.xlsx'

                return response
        return Response({"message": "Нет выбранных строк для выгрузки"}, status=status.HTTP_400_BAD_REQUEST)