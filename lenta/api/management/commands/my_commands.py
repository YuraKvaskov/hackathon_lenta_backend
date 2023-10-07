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

            for index, row in enumerate(reader):
                if index >= 100:
                    break

                store, created = Store.objects.get_or_create(
                    st_id=row['st_id'],
                    defaults={
                        'st_city_id': row.get('st_city_id', 'City Default Value'),
                        'st_division_code': row.get('st_division_code', 'Division Code Default Value'),
                        'st_type_format_id': int(row.get('st_type_format_id', 1)),
                        'st_type_loc_id': int(row.get('st_type_loc_id', 1)),
                        'st_type_size_id': int(row.get('st_type_size_id', 1)),
                        'st_is_active': bool(int(row.get('st_is_active', 1)))
                    }
                )

    def process_and_save_pr_df_file(self, file_path):
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)

            for index, row in enumerate(reader):
                if index >= 100:
                    break

                pr_uom_id = int(float(row.get('pr_uom_id', 1)))

                product, created = Product.objects.get_or_create(
                    pr_sku_id=row['pr_sku_id'],
                    defaults={
                        'pr_group_id': row.get('pr_group_id', 'Group Default Value'),
                        'pr_cat_id': row.get('pr_cat_id', 'Category Default Value'),
                        'pr_subcat_id': row.get('pr_subcat_id', 'Subcategory Default Value'),
                        'pr_uom_id': pr_uom_id
                    }
                )

    def process_and_save_sales_df_file(self, file_path):
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)

            for index, row in enumerate(reader):
                if index >= 100:
                    break

                store_id, _ = Store.objects.get_or_create(st_id=row['st_id'])
                product_id, _ = Product.objects.get_or_create(pr_sku_id=row['pr_sku_id'])
                date = datetime.strptime(row['date'], '%Y-%m-%d')

                try:
                    pr_sales_in_units = int(float(row.get('pr_sales_in_units')))
                except (ValueError, TypeError):
                    pr_sales_in_units = 1

                try:
                    pr_promo_sales_in_units = int(float(row.get('pr_promo_sales_in_units')))
                except (ValueError, TypeError):
                    pr_promo_sales_in_units = 1

                try:
                    pr_sales_in_rub = float(row.get('pr_sales_in_rub'))
                except (ValueError, TypeError):
                    pr_sales_in_rub = 0.0

                try:
                    pr_promo_sales_in_rub = float(row.get('pr_promo_sales_in_rub'))
                except (ValueError, TypeError):
                    pr_promo_sales_in_rub = 0.0

                Sales.objects.create(
                    store_id=store_id,
                    product_id=product_id,
                    date=date,
                    pr_sales_type_id=int(row.get('pr_sales_type_id', 1)),
                    pr_sales_in_units=pr_sales_in_units,
                    pr_promo_sales_in_units=pr_promo_sales_in_units,
                    pr_sales_in_rub=pr_sales_in_rub,
                    pr_promo_sales_in_rub=pr_promo_sales_in_rub
                )


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


    # def process_and_save_pr_st_file(self, file_path):
    #     with open(file_path, 'r') as file:
    #         reader = csv.DictReader(file)
    #
    #         for row in reader:
    #             store, created = Store.objects.get_or_create(
    #                 st_id=row['st_id'],
    #                 defaults={
    #                     'st_city_id': row['st_city_id'],
    #                     'st_division_code': row['st_division_code'],
    #                     'st_type_format_id': row['st_type_format_id'],
    #                     'st_type_loc_id': row['st_type_loc_id'],
    #                     'st_type_size_id': row['st_type_size_id'],
    #                     'st_is_active': bool(int(row['st_is_active']))
    #                 }
    #             )
    #
    # def process_and_save_pr_df_file(self, file_path):
    #     with open(file_path, 'r') as file:
    #         reader = csv.DictReader(file)
    #
    #         for row in reader:
    #             product, created = Product.objects.get_or_create(
    #                 pr_sku_id=row['pr_sku_id'],
    #                 defaults={
    #                     'pr_group_id': row['pr_group_id'],
    #                     'pr_cat_id': row['pr_cat_id'],
    #                     'pr_subcat_id': row['pr_subcat_id'],
    #                     'pr_uom_id': row['pr_uom_id']
    #                 }
    #             )
    #
    # def process_and_save_sales_df_file(self, file_path):
    #     with open(file_path, 'r') as file:
    #         reader = csv.DictReader(file)
    #
    #         for row in reader:
    #             store_id, _ = Store.objects.get_or_create(st_id=row['st_id'])
    #             product_id, _ = Product.objects.get_or_create(pr_sku_id=row['pr_sku_id'])
    #             date = datetime.strptime(row['date'], '%Y-%m-%d')
    #
    #             pr_sales_type_id = bool(
    #                 int(row['pr_sales_type_id']))
    #
    #             Sales.objects.create(
    #                 store_id=store_id,
    #                 product_id=product_id,
    #                 date=date,
    #                 pr_sales_type_id=pr_sales_type_id,
    #                 pr_sales_in_units=float(row['pr_sales_in_units']),
    #                 pr_promo_sales_in_units=float(row['pr_promo_sales_in_units']),
    #                 pr_sales_in_rub=float(row['pr_sales_in_rub']),
    #                 pr_promo_sales_in_rub=float(row['pr_promo_sales_in_rub'])
    #             )
