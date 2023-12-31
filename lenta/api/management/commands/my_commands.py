import csv
import os
from random import randint, uniform, choice
import json

from django.core.management.base import BaseCommand
from api.v1.models import Store, Product, Sales, SalesForecast, ProductSubcategory, ProductCategory, ProductGroup, City
import random
from datetime import date, datetime
from django.utils import timezone

from lenta import settings


class Command(BaseCommand):
    help = 'Populate the database with sample data'

    def handle(self, *args, **kwargs):
        # Создаем 10 городов
        for city_id in range(1, 11):
            city = City(st_city_id=f"city_{city_id}")
            city.save()

        # Создаем 100 магазинов
        for store_id in range(100):
            city = City.objects.get(st_city_id=f"city_{randint(1, 10)}")
            store = Store(
                st_id=f"store_{store_id}",
                st_city_id=city,
                st_division_code=f"division_{randint(1, 5)}",
                st_type_format_id=randint(1, 3),
                st_type_loc_id=randint(1, 2),
                st_type_size_id=randint(1, 4),
                st_is_active=choice([True, False])
            )
            store.save()

        # Создаем 100 групп продуктов
        for group_id in range(1, 11):
            product_group = ProductGroup(pr_group_id=f"group_{group_id}")
            product_group.save()

        # Создаем 100 категорий продуктов с учетом зависимостей
        for cat_id in range(100):
            group = ProductGroup.objects.get(pr_group_id=f"group_{randint(1, 10)}")
            product_category = ProductCategory(
                pr_cat_id=f"cat_{cat_id}",
                pr_group_id=group
            )
            product_category.save()

        # Создаем 100 подкатегорий продуктов с учетом зависимостей
        for subcat_id in range(100):
            category = ProductCategory.objects.get(pr_cat_id=f"cat_{randint(1, 5)}")
            product_subcategory = ProductSubcategory(
                pr_subcat_id=f"subcat_{subcat_id}",
                pr_cat_id=category
            )
            product_subcategory.save()

        # Создаем 100 продуктов с учетом зависимостей
        for sku_id in range(100):
            subcategory = ProductSubcategory.objects.get(pr_subcat_id=f"subcat_{randint(1, 3)}")
            product = Product(
                pr_sku_id=f"sku_{sku_id}",
                pr_group=subcategory.pr_cat_id.pr_group_id,
                pr_category=subcategory.pr_cat_id,
                pr_subcategory=subcategory,
                pr_uom_id=randint(1, 5)
            )
            product.save()

        # Создаем 100 записей о продажах с учетом зависимостей
        for _ in range(100):
            store = Store.objects.get(st_id=f"store_{randint(0, 99)}")
            product = Product.objects.get(pr_sku_id=f"sku_{randint(0, 99)}")

            sales_date = date(randint(2020, 2022), randint(1, 12), randint(1, 28))
            sales = Sales(
                store=store,
                product=product,
                date=sales_date,
                pr_sales_type_id=randint(1, 4),
                pr_sales_in_units=randint(10, 100),
                pr_promo_sales_in_units=randint(0, 50),
                pr_sales_in_rub=uniform(100, 1000),
                pr_promo_sales_in_rub=uniform(0, 200)
            )
            sales.save()

        # Теперь добавляем данные для модели SalesForecast
        for _ in range(100):
            store = Store.objects.get(st_id=f"store_{randint(0, 99)}")
            product = Product.objects.get(pr_sku_id=f"sku_{randint(0, 99)}")

            forecast_date = date(randint(2022, 2024), randint(1, 12), randint(1, 28))
            forecast = [
                {
                    "date": str(forecast_date),
                    "sales_type": randint(1, 4),
                    "sales_units": randint(10, 100),
                    "sales_units_promo": randint(0, 50),
                    "sales_rub": uniform(100, 1000),
                    "sales_run_promo": uniform(0, 200)
                }
            ]

            forecast_json = json.dumps(forecast)

            sales_forecast = SalesForecast(
                store=store,
                product=product,
                forecast_date=forecast_date,
                forecast=forecast_json
            )
            sales_forecast.save()



# class Command(BaseCommand):
#     help = 'Populate the database with sample data'
#
#     def handle(self, *args, **kwargs):
#         for _ in range(100):
#             store = Store(
#                 st_id=f"store_{_}",
#                 st_city_id=f"city_{random.randint(1, 10)}",
#                 st_division_code=f"division_{random.randint(1, 5)}",
#                 st_type_format_id=random.randint(1, 3),
#                 st_type_loc_id=random.randint(1, 2),
#                 st_type_size_id=random.randint(1, 4),
#                 st_is_active=random.choice([True, False])
#             )
#             store.save()
#
#         # Создаем 100 объектов Product
#         for _ in range(100):
#             product = Product(
#                 pr_sku_id=f"sku_{_}",
#                 pr_group_id=f"group_{random.randint(1, 10)}",
#                 pr_cat_id=f"cat_{random.randint(1, 5)}",
#                 pr_subcat_id=f"subcat_{random.randint(1, 3)}",
#                 pr_uom_id=random.randint(1, 5)
#             )
#             product.save()
#
#         # Создаем 100 объектов Sales и SalesForecast с учетом зависимостей
#         for _ in range(100):
#             store = Store.objects.get(st_id=f"store_{random.randint(0, 99)}")
#             product = Product.objects.get(pr_sku_id=f"sku_{random.randint(0, 99)}")
#
#             sales_date = date(random.randint(2020, 2022), random.randint(1, 12), random.randint(1, 28))
#             sales = Sales(
#                 store=store,
#                 product=product,
#                 date=sales_date,
#                 pr_sales_type_id=random.randint(1, 4),
#                 pr_sales_in_units=random.randint(10, 100),
#                 pr_promo_sales_in_units=random.randint(0, 50),
#                 pr_sales_in_rub=random.uniform(100, 1000),
#                 pr_promo_sales_in_rub=random.uniform(0, 200)
#             )
#             sales.save()
#
#             forecast_date = sales_date + timezone.timedelta(days=random.randint(1, 30))
#             sales_forecast = SalesForecast(
#                 store=store,
#                 product=product,
#                 forecast_date=forecast_date,
#                 sales_units=[random.randint(5, 20) for _ in range(30)]
#             )
#             sales_forecast.save()
# class Command(BaseCommand):
#     help = 'Process and save data from CSV files'
#
#     def handle(self, *args, **options):
#         media_folder = settings.MEDIA_ROOT
#
#         pr_st_file_path = os.path.join(media_folder, 'st_df.csv')
#         pr_df_file_path = os.path.join(media_folder, 'pr_df.csv')
#         sales_df_file_path = os.path.join(media_folder, 'sales_df_train.csv')
#
#         self.process_and_save_pr_st_file(pr_st_file_path)
#         self.process_and_save_pr_df_file(pr_df_file_path)
#         self.process_and_save_sales_df_file(sales_df_file_path)
#
#
#     def process_and_save_pr_st_file(self, file_path):
#         with open(file_path, 'r') as file:
#             reader = csv.DictReader(file)
#
#             for row in reader:
#                 store, created = Store.objects.get_or_create(
#                     st_id=row['st_id'],
#                     defaults={
#                         'st_city_id': row['st_city_id'],
#                         'st_division_code': row['st_division_code'],
#                         'st_type_format_id': row['st_type_format_id'],
#                         'st_type_loc_id': row['st_type_loc_id'],
#                         'st_type_size_id': row['st_type_size_id'],
#                         'st_is_active': bool(int(row['st_is_active']))
#                     }
#                 )
#
#     def process_and_save_pr_df_file(self, file_path):
#         with open(file_path, 'r') as file:
#             reader = csv.DictReader(file)
#
#             for row in reader:
#                 product, created = Product.objects.get_or_create(
#                     pr_sku_id=row['pr_sku_id'],
#                     defaults={
#                         'pr_group_id': row['pr_group_id'],
#                         'pr_cat_id': row['pr_cat_id'],
#                         'pr_subcat_id': row['pr_subcat_id'],
#                         'pr_uom_id': row['pr_uom_id']
#                     }
#                 )
#
#     def process_and_save_sales_df_file(self, file_path):
#         with open(file_path, 'r') as file:
#             reader = csv.DictReader(file)
#
#             for row in reader:
#                 store_id, _ = Store.objects.get_or_create(st_id=row['st_id'])
#                 product_id, _ = Product.objects.get_or_create(pr_sku_id=row['pr_sku_id'])
#                 date = datetime.strptime(row['date'], '%Y-%m-%d')
#
#                 pr_sales_type_id = bool(
#                     int(row['pr_sales_type_id']))
#
#                 Sales.objects.create(
#                     store_id=store_id,
#                     product_id=product_id,
#                     date=date,
#                     pr_sales_type_id=pr_sales_type_id,
#                     pr_sales_in_units=float(row['pr_sales_in_units']),
#                     pr_promo_sales_in_units=float(row['pr_promo_sales_in_units']),
#                     pr_sales_in_rub=float(row['pr_sales_in_rub']),
#                     pr_promo_sales_in_rub=float(row['pr_promo_sales_in_rub'])
#                 )
