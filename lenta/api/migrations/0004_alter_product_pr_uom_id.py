# Generated by Django 4.1.11 on 2023-10-07 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_sales_pr_sales_type_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='pr_uom_id',
            field=models.IntegerField(null=True),
        ),
    ]
