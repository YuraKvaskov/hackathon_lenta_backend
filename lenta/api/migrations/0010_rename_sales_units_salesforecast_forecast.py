# Generated by Django 4.1.11 on 2023-10-11 12:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_rename_subcategory_product_pr_subcategory_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='salesforecast',
            old_name='sales_units',
            new_name='forecast',
        ),
    ]
