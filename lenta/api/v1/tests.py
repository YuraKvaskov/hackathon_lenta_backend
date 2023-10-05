import json

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Store, Product, SalesForecast
from datetime import date


class ExportSelectedForecastsToExcelViewTestCase(TestCase):
	"""
	Здесь мы тестируем работу функции по формированию Excel файла
	"""

	def setUp(self):
		self.user = User.objects.create_user(username='testuser', password='testpass')
		self.store = Store.objects.create(
			st_id='test_store_id',
			st_city_id='test_city_id',
			st_division_code='test_division',
			st_type_format_id=1,
			st_type_loc_id=2,
			st_type_size_id=3,
			st_is_active=True
		)
		self.product = Product.objects.create(
			pr_sku_id='test_sku',
			pr_group_id='test_group',
			pr_cat_id='test_category',
			pr_subcat_id='test_subcategory',
			pr_uom_id=1
		)
		self.forecast1 = SalesForecast.objects.create(
			store=self.store,
			product=self.product,
			forecast_date=date.today(),
			sales_units={"key1": "value1", "key2": "value2"}
		)

	def test_export_selected_forecasts(self):
		factory = APIRequestFactory()
		url = reverse('export_selected_forecasts')
		data = {
			"data": [
				{"id": 1, "selected": True},
			]
		}

		data_json = json.dumps(data)

		self.client.force_login(self.user)
		response = self.client.post(url, data_json, content_type='application/json')

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response['Content-Type'], 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')