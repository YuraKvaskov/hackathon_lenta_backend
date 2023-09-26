from django.core.management.base import BaseCommand
import csv
from django.conf import settings
from api.v1.models import Store, Product, Sales
from datetime import datetime
import os


class Command(BaseCommand):
    help = 'Process and save data from CSV files'

    def handle(self, *args, **options):
        media_folder = settings.MEDIA_ROOT

        pr_st_file_path = os.path.join(media_folder, 'st_df.csv')
        pr_df_file_path = os.path.join(media_folder, 'pr_df.csv')
        sales_df_file_path = os.path.join(media_folder, 'sales_df_train.csv')

        self.process_and_save_pr_st_file(pr_st_file_path)
        self.process_and_save_pr_df_file(pr_df_file_path)
        self.process_and_save_sales_df_file(sales_df_file_path)

    def process_and_save_pr_st_file(self, file_path):
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)

            for row in reader:
                store, created = Store.objects.get_or_create(
                    st_id=row['st_id'],
                    defaults={
                        'st_city_id': row['st_city_id'],
                        'st_division_code': row['st_division_code'],
                        'st_type_format_id': row['st_type_format_id'],
                        'st_type_loc_id': row['st_type_loc_id'],
                        'st_type_size_id': row['st_type_size_id'],
                        'st_is_active': bool(int(row['st_is_active']))
                    }
                )

    def process_and_save_pr_df_file(self, file_path):
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)

            for row in reader:
                product, created = Product.objects.get_or_create(
                    pr_sku_id=row['pr_sku_id'],
                    defaults={
                        'pr_group_id': row['pr_group_id'],
                        'pr_cat_id': row['pr_cat_id'],
                        'pr_subcat_id': row['pr_subcat_id'],
                        'pr_uom_id': row['pr_uom_id']
                    }
                )

    def process_and_save_sales_df_file(self, file_path):
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)

            for row in reader:
                store, _ = Store.objects.get_or_create(st_id=row['st_id'])
                product, _ = Product.objects.get_or_create(pr_sku_id=row['pr_sku_id'])
                date = datetime.strptime(row['date'], '%Y-%m-%d')

                pr_sales_type_id = bool(
                    int(row['pr_sales_type_id']))

                Sales.objects.create(
                    store=store,
                    product=product,
                    date=date,
                    pr_sales_type_id=pr_sales_type_id,
                    pr_sales_in_units=float(row['pr_sales_in_units']),
                    pr_promo_sales_in_units=float(row['pr_promo_sales_in_units']),
                    pr_sales_in_rub=float(row['pr_sales_in_rub']),
                    pr_promo_sales_in_rub=float(row['pr_promo_sales_in_rub'])
                )
