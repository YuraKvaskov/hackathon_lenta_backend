from io import BytesIO
import pandas as pd
from django.db.models import Q

from rest_framework.views import APIView
from rest_framework import filters, status
from django_filters import rest_framework as django_filters
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponse

from rest_framework.response import Response
from datetime import datetime, timedelta
from rest_framework import permissions
from rest_framework.decorators import action, permission_classes


# from api.v1.filters import ShopsFilter
from api.v1.models import Store, Product, Sales, SalesForecast, FilterTemplate, ProductSubcategory, ProductCategory, \
    ProductGroup
from api.v1.serializers import SalesSerializer, StoreSerializer, SalesForecastSerializer, \
    InfoHeaderSerializer, FilterTemplateSerializer, ProductSerializer, ProductCategorySerializer, \
    ProductGroupSerializer, ProductSubcategorySerializer


# class SaveFilterTemplateView(APIView):
#     """
#     Представление для сохранения и управления шаблонами фильтров.
#         - `get`: Получить список всех сохраненных шаблонов для текущего пользователя.
#         - `post`: Создать новый шаблон фильтра.
#         - `delete`: Удалить шаблон фильтра по его идентификатору.
#     """
#     serializer_class = None
#
#     def get(self, request):
#         user = request.user
#         templates = FilterTemplate.objects.filter(user=user)
#         serializer = FilterTemplateSerializer(templates, many=True)
#         return Response(serializer.data)
#
#     def post(self, request):
#         user = request.user
#         data = request.data
#         template_name = data.get('template_name')
#         st_city_id = data.get('st_city_id')
#         store_id = data.get('store_id')
#         pr_group_id = data.get('pr_group_id')
#         pr_cat_id = data.get('pr_cat_id')
#         pr_subcat_id = data.get('pr_subcat_id')
#         selected_interval = int(data.get('selected_interval', 14))
#
#         filter_template, created = FilterTemplate.objects.get_or_create(
#             user=user,
#             name=template_name,
#         )
#         filter_template.st_city_id = st_city_id
#         filter_template.store_id = store_id
#         filter_template.pr_group_id = pr_group_id
#         filter_template.pr_cat_id = pr_cat_id
#         filter_template.pr_subcat_id = pr_subcat_id
#         filter_template.selected_interval = selected_interval
#         filter_template.save()
#
#         return Response({'message': 'Шаблон успешно сохранен'}, status=status.HTTP_201_CREATED)
#
#     def delete(self, request, template_id):
#         try:
#             user = request.user
#             template = FilterTemplate.objects.get(user=user, id=template_id)
#             template.delete()
#             return Response({'message': 'Шаблон успешно удален'}, status=status.HTTP_204_NO_CONTENT)
#         except FilterTemplate.DoesNotExist:
#             return Response({'message': 'Шаблон не найден'}, status=status.HTTP_404_NOT_FOUND)


class InfoHeaderView(APIView):
    """
    Представление для получения информации о пользователе и его магазинах в хеддере.
    """
    serializer_class = InfoHeaderSerializer

    def get(self, request):
        user = request.user
        if user.is_authenticated:
            serializer = InfoHeaderSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class SalesView(APIView):
    serializer_class = SalesSerializer

    def get(self, request):
        product_id = request.query_params.get('product_id')
        store_id = request.query_params.get('store_id')
        if product_id and store_id:
            sales = Sales.objects.filter(product__pr_sku_id=product_id, store__st_id=store_id)

            serialized_sales = self.serializer_class(sales, many=True).data

            response_data = {
                "data": [
                    {
                        "store": store_id,
                        "sku": product_id,
                        "fact": serialized_sales
                    }
                ]
            }

            return Response(response_data)
        else:
            return Response({"message": "Отсутствуют параметры product_id и store_id"}, status=status.HTTP_400_BAD_REQUEST)


# class CategoriesView(APIView):
#     def get(self, request):
#         product_groups = ProductGroup.objects.all()
#         data = []
#
#         for group in product_groups:
#             group_data = ProductGroupSerializer(group).data
#             group_data['categories'] = []
#
#             # Используйте правильное поле для фильтрации
#             categories = ProductCategory.objects.filter(pr_group_id=group)
#
#             for category in categories:
#                 category_data = ProductCategorySerializer(category).data
#                 category_data['subcategories'] = []
#                 subcategories = ProductSubcategory.objects.filter(pr_cat_id=category)
#
#                 for subcategory in subcategories:
#                     subcategory_data = ProductSubcategorySerializer(subcategory).data
#                     subcategory_data['products'] = []
#                     products = Product.objects.filter(pr_subcategory=subcategory)
#
#                     for product in products:
#                         product_data = ProductSerializer(product).data
#                         subcategory_data['products'].append(product_data)
#
#                     category_data['subcategories'].append(subcategory_data)
#
#                 group_data['categories'].append(category_data)
#
#             data.append(group_data)
#
#         return Response(data)

class CategoriesView(APIView):
    def get(self, request):
        product_groups = ProductGroup.objects.all()
        data = ProductGroupSerializer(product_groups, many=True).data
        return Response(data)

class ShopsView(APIView):
    serializer_class = StoreSerializer

    def get(self, request):
        queryset = Store.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response({"data": serializer.data})


class SalesForecastView(APIView):
    serializer_class = SalesForecastSerializer

    def get(self, request):
        st_city_id = request.query_params.get('st_city_id')
        store_id = request.query_params.get('store_id')
        pr_group_id = request.query_params.get('pr_group_id')
        pr_cat_id = request.query_params.get('pr_cat_id')
        pr_subcat_id = request.query_params.get('pr_subcat_id')
        pr_sku_id = request.query_params.get('pr_sku_id')
        selected_interval = int(request.query_params.get('selected_interval', 14))

        start_date = datetime.now().date() + timedelta(days=1)
        end_date = start_date + timedelta(days=selected_interval)

        filters = Q()
        if st_city_id:
            filters &= Q(store__st_city_id=st_city_id)
        if store_id:
            filters &= Q(store__st_id=store_id)
        if pr_group_id:
            filters &= Q(product__pr_group_id=pr_group_id)
        if pr_cat_id:
            filters &= Q(product__pr_cat_id=pr_cat_id)
        if pr_subcat_id:
            filters &= Q(product__pr_subcat_id=pr_subcat_id)
        if pr_sku_id:
            filters &= Q(product__pr_sku_id=pr_sku_id)

        forecasts = SalesForecast.objects.filter(filters)

        # Используйте сериализаторы для преобразования объектов в списки ID
        product_ids = ProductSerializer(forecasts, many=True).data
        category_ids = ProductCategorySerializer(forecasts, many=True).data
        group_ids = ProductGroupSerializer(forecasts, many=True).data
        subcategory_ids = ProductSubcategorySerializer(forecasts, many=True).data

        # Возвращайте списки ID вместе с другими данными
        return Response({'data': {'products': product_ids, 'categories': category_ids, 'groups': group_ids,
                                  'subcategories': subcategory_ids}})

        # forecasts = SalesForecast.objects.filter(
        #     forecast_date__gte=start_date,
        #     forecast_date__lte=end_date
        # ).filter(filters)
        #
        # serializer = self.serializer_class(forecasts, many=True)
        # return Response({'data': serializer.data})

# class SalesForecastView(APIView):
#     serializer_class = SalesForecastSerializer
#
#     def post(self, request):
#         data = request.data.get("data")
#         if data:
#             for forecast_data in data:
#                 serializer = self.serializer_class(data=forecast_data)
#                 if serializer.is_valid():
#                     serializer.save()
#                 else:
#                     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#             return Response({"message": "Прогноз успешно сохранен"}, status=status.HTTP_201_CREATED)
#         else:
#             return Response({"message": "В запросе отсутствуют данные"}, status=status.HTTP_400_BAD_REQUEST)
#
#     def get(self, request):
#         st_city_id = request.query_params.get('st_city_id')
#         store_id = request.query_params.get('store_id')
#         pr_group_id = request.query_params.get('pr_group_id')
#         pr_cat_id = request.query_params.get('pr_cat_id')
#         pr_subcat_id = request.query_params.get('pr_subcat_id')
#         pr_sku_id = request.query_params.get('pr_sku_id')  # Добавляем параметр для фильтрации по pr_sku_id
#         selected_interval = int(request.query_params.get('selected_interval', 14))
#         start_date = datetime.now().date() + timedelta(days=1)
#         end_date = start_date + timedelta(days=selected_interval)
#
#         filters = {}
#         if st_city_id:
#             filters['store__st_city_id'] = st_city_id
#         if store_id:
#             filters['store__st_id'] = store_id
#         if pr_group_id:
#             filters['product__pr_group_id'] = pr_group_id
#         if pr_cat_id:
#             filters['product__pr_cat_id'] = pr_cat_id
#         if pr_subcat_id:
#             filters['product__pr_subcat_id'] = pr_subcat_id
#         if pr_sku_id:
#             filters['product__pr_sku_id'] = pr_sku_id
#
#         try:
#             forecasts = SalesForecast.objects.filter(
#                 forecast_date__gte=start_date,
#                 forecast_date__lte=end_date,
#                 **filters
#             )
#         except ObjectDoesNotExist:
#             return JsonResponse({'data': []})
#
#         serializer = self.serializer_class(forecasts, many=True)
#         return JsonResponse({'data': serializer.data})

class ExportSelectedForecastsToExcelView(APIView):
    def post(self, request):
        data = request.data.get("data")
        if data:
            selected_forecast_ids = [item['id'] for item in data if item.get('selected')]
            if selected_forecast_ids:
                forecasts = SalesForecast.objects.filter(id__in=selected_forecast_ids)

                df_data = {
                    'forecast_date': [],
                    'store': [],
                    'product': [],
                    'sales_units': [],
                }
                for forecast in forecasts:
                    df_data['forecast_date'].append(forecast.forecast_date)
                    df_data['store'].append(forecast.store.st_id)
                    df_data['product'].append(forecast.product.pr_sku_id)
                    df_data['sales_units'].append(forecast.sales_units)
                df = pd.DataFrame(df_data)

                output = BytesIO()

                writer = pd.ExcelWriter(output, engine='xlsxwriter')
                df.to_excel(writer, sheet_name='Selected Forecasts', index=False)

                response = HttpResponse(output.getvalue(),
                                        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = 'attachment; filename=selected_forecasts.xlsx'

                return response
        return Response({"message": "Нет выбранных строк для выгрузки"}, status=status.HTTP_400_BAD_REQUEST)


# @permission_classes([permissions.IsAuthenticated])  # как будет отбращаться ML?
# class SalesView(APIView):
#     """
#     Возвращает временной ряд с информацией о количестве проданных товаров.
#     Обязательные входные параметры запроса: id товара, id ТЦ.\n
#     Образец запроса
#     /?store_id=<store_id>&product_id=<product_id>
#     """
#     serializer_class = SalesSerializer
#
#     def get(self, request):
#         product_id = request.query_params.get('product_id')
#         store_id = request.query_params.get('store_id')
#         if product_id and store_id:
#             sales = Sales.objects.filter(product__pr_sku_id=product_id, store__st_id=store_id)
#         serialized_sales = self.serializer_class(sales, many=True).data
#         response_data = {"data": [
#             {
#                 "store_id": store_id,
#                 "product_id": product_id,
#                 "fact": serialized_sales
#             }
#         ]}
#         return Response(response_data)
#
#
# # @permission_classes([permissions.IsAuthenticated])
# class CategoriesView(APIView):
#     """
#     Представление для получения списка категорий продуктов.
#     """
#     serializer_class = CategoriesSerializer
#
#     def get(self, request):
#         categories = Product.objects.all()
#         serializer = self.serializer_class(categories, many=True)
#         return Response({"data": serializer.data})
#
#
# # @permission_classes([permissions.IsAuthenticated])
# class ShopsView(APIView):
#     """
#     Представление для получения списка магазинов.
#     Поддерживает фильтрацию и сортировку.
#     Фильтры:
#     - st_city_id: ID города
#     - store_id: ID магазина
#     - pr_group_id: ID группы продуктов
#     - pr_cat_id: ID категории продуктов
#     - pr_subcat_id: ID подкатегории продуктов
#     - ordering: Поле для сортировки (по умолчанию сортировка по ID)
#
#     Ожидаемый ответ:
#     {
#         "data": [список магазинов]
#     }
#     """
#     serializer_class = StoreSerializer
#     filter_backends = [filters.OrderingFilter, django_filters.DjangoFilterBackend]
#     filterset_class = ShopsFilter
#     ordering_fields = '__all__'
#
#     def filter_queryset(self, queryset):
#         return self.filterset_class(self.request.GET, queryset=queryset).qs
#
#     def get(self, request):
#         queryset = Store.objects.all()
#         queryset = self.filter_queryset(queryset)
#         serializer = self.serializer_class(queryset, many=True)
#         return Response({"data": serializer.data})
#
#
# # @permission_classes([permissions.IsAuthenticated])
# class SalesForecastView(APIView):
#     """
#     Представление для работы с прогнозами продаж.
#     - `post`: Принимает прогнозы продаж от ML.
#     - `get`: Получить прогнозы продаж с фильтрацией по параметрам.
#
#     Параметры запроса:
#     - st_city_id: ID города
#     - store_id: ID магазина
#     - pr_group_id: ID группы продуктов
#     - pr_cat_id: ID категории продуктов
#     - pr_subcat_id: ID подкатегории продуктов
#     - selected_interval: Выбранный интервал дней (по умолчанию 14 дней)
#     Ожидаемый ответ:
#     {
#         "data": [список прогнозов продаж]
#     }
#     """
#     serializer_class = SalesForecastSerializer
#
#     def post(self, request):
#         data = request.data.get("data")
#         if data:
#             for forecast_data in data:
#                 serializer = self.serializer_class(data=forecast_data)
#                 if serializer.is_valid():
#                     serializer.save()
#                 else:
#                     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#             return Response({"message": "Прогноз успешно сохранен"}, status=status.HTTP_201_CREATED)
#         else:
#             return Response({"message": "В запросе отсутствуют данные"}, status=status.HTTP_400_BAD_REQUEST)
#
#     def get(self, request):
#         """
#         Получить прогнозы продаж с фильтрацией по параметрам.
#
#         Ожидаемые параметры запроса:
#         - st_city_id: ID города
#         - store_id: ID магазина
#         - pr_group_id: ID группы продуктов
#         - pr_cat_id: ID категории продуктов
#         - pr_subcat_id: ID подкатегории продуктов
#         - selected_interval: Выбранный интервал дней (по умолчанию 14 дней)
#
#         Успешный ответ:
#         {
#             "data": [список прогнозов продаж]
#         }
#         """
#         st_city_id = request.query_params.get('st_city_id')
#         store_id = request.query_params.get('store_id')
#         pr_group_id = request.query_params.get('pr_group_id')
#         pr_cat_id = request.query_params.get('pr_cat_id')
#         pr_subcat_id = request.query_params.get('pr_subcat_id')
#         pr_sku_id = request.query_params.get('pr_sku_id')  # Добавляем параметр для фильтрации по pr_sku_id
#         selected_interval = int(request.query_params.get('selected_interval', 14))
#         start_date = datetime.now().date() + timedelta(days=1)
#         end_date = start_date + timedelta(days=selected_interval)
#
#         filters = {}
#         if st_city_id:
#             filters['store__st_city_id'] = st_city_id
#         if store_id:
#             filters['store__st_id'] = store_id
#         if pr_group_id:
#             filters['product__pr_group_id'] = pr_group_id
#         if pr_cat_id:
#             filters['product__pr_cat_id'] = pr_cat_id
#         if pr_subcat_id:
#             filters['product__pr_subcat_id'] = pr_subcat_id
#         if pr_sku_id:
#             filters['product__pr_sku_id'] = pr_sku_id
#
#         try:
#             forecasts = SalesForecast.objects.filter(
#                 forecast_date__gte=start_date,
#                 forecast_date__lte=end_date,
#                 **filters
#             )
#         except ObjectDoesNotExist:
#             return JsonResponse({'data': []})
#
#         serializer = self.serializer_class(forecasts, many=True)
#         return JsonResponse({'data': serializer.data})
#
#
# class ExportSelectedForecastsToExcelView(APIView):
#     """
#     Представление для экспорта выбранных прогнозов продаж в формате Excel.
#
#     - `post`: Экспортировать выбранные прогнозы в Excel.
#     """
#
#     def post(self, request):
#         data = request.data.get("data")
#         if data:
#             selected_forecast_ids = [item['id'] for item in data if item.get('selected')]
#             if selected_forecast_ids:
#                 forecasts = SalesForecast.objects.filter(id__in=selected_forecast_ids)
#
#                 df_data = {
#                     'forecast_date': [],
#                     'store': [],
#                     'product': [],
#                     'sales_units': [],
#                 }
#                 for forecast in forecasts:
#                     df_data['forecast_date'].append(forecast.forecast_date)
#                     df_data['store'].append(forecast.store.st_id)
#                     df_data['product'].append(forecast.product.pr_sku_id)
#                     df_data['sales_units'].append(forecast.sales_units)
#                 df = pd.DataFrame(df_data)
#
#                 output = BytesIO()
#
#                 writer = pd.ExcelWriter(output, engine='xlsxwriter')
#                 df.to_excel(writer, sheet_name='Selected Forecasts', index=False)
#
#                 response = HttpResponse(output.getvalue(),
#                                         content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
#                 response['Content-Disposition'] = 'attachment; filename=selected_forecasts.xlsx'
#
#                 return response
#         return Response({"message": "Нет выбранных строк для выгрузки"}, status=status.HTTP_400_BAD_REQUEST)
