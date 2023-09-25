import csv
from django.conf import settings
from .models import Store, Product, Sales
from datetime import datetime
import os


def process_and_save_pr_st_file(file_path):
	with open(file_path, 'r') as file:
		reader = csv.DictReader(file)

		for row in reader:
			Store.objects.create(
				st_id=row['st_id'],
				st_city_id=row['st_city_id'],
				st_division_code=row['st_division_code'],
				st_type_format_id=row['st_type_format_id'],
				st_type_loc_id=row['st_type_loc_id'],
				st_type_size_id=row['st_type_size_id'],
				st_is_active=bool(int(row['st_is_active']))
			)


def process_and_save_pr_df_file(file_path):
	with open(file_path, 'r') as file:
		reader = csv.DictReader(file)

		for row in reader:
			Product.objects.create(
				pr_group_id=row['pr_group_id'],
				pr_cat_id=row['pr_cat_id'],
				pr_subcat_id=row['pr_subcat_id'],
				pr_sku_id=row['pr_sku_id'],
				pr_uom_id=row['pr_uom_id']
			)


def process_and_save_sales_df_file(file_path):
	with open(file_path, 'r') as file:
		reader = csv.DictReader(file)

		for row in reader:
			store, _ = Store.objects.get_or_create(st_id=row['st_id'])
			product, _ = Product.objects.get_or_create(pr_sku_id=row['pr_sku_id'])

			date = datetime.strptime(row['date'], '%Y-%m-%d')

			Sales.objects.create(
				store=store,
				product=product,
				date=date,
				pr_sales_type_id=bool(int(row['pr_sales_type_id'])),
				pr_sales_in_units=row['pr_sales_in_units'],
				pr_promo_sales_in_units=row['pr_promo_sales_in_units'],
				pr_sales_in_rub=row['pr_sales_in_rub'],
				pr_promo_sales_in_rub=row['pr_promo_sales_in_rub']
			)


data_folder = os.path.join(settings.BASE_DIR, 'data')

pr_st_file_path = os.path.join(data_folder, 'pr_st.csv')
pr_df_file_path = os.path.join(data_folder, 'pr_df.csv')
sales_df_file_path = os.path.join(data_folder, 'sales_df_train.csv')

process_and_save_pr_st_file(pr_st_file_path)
process_and_save_pr_df_file(pr_df_file_path)
process_and_save_sales_df_file(sales_df_file_path)