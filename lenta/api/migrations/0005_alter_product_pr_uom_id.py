# Generated by Django 4.1.11 on 2023-10-07 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_product_pr_uom_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='pr_uom_id',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
