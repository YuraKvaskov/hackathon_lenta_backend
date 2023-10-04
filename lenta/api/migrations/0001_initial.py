# Generated by Django 4.1.11 on 2023-10-04 10:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('pr_sku_id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('pr_group_id', models.CharField(max_length=255)),
                ('pr_cat_id', models.CharField(max_length=255)),
                ('pr_subcat_id', models.CharField(max_length=255)),
                ('pr_uom_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('st_id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('st_city_id', models.CharField(max_length=255)),
                ('st_division_code', models.CharField(max_length=255)),
                ('st_type_format_id', models.IntegerField()),
                ('st_type_loc_id', models.IntegerField()),
                ('st_type_size_id', models.IntegerField()),
                ('st_is_active', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='SalesForecast',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('forecast_date', models.DateField()),
                ('sales_units', models.JSONField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.product')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.store')),
            ],
        ),
        migrations.CreateModel(
            name='Sales',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('pr_sales_type_id', models.BooleanField()),
                ('pr_sales_in_units', models.IntegerField()),
                ('pr_promo_sales_in_units', models.IntegerField()),
                ('pr_sales_in_rub', models.FloatField()),
                ('pr_promo_sales_in_rub', models.FloatField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.product')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.store')),
            ],
        ),
    ]
