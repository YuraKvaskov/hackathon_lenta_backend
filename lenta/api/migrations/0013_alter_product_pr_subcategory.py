# Generated by Django 4.1.11 on 2023-10-11 19:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_alter_productsubcategory_pr_cat_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='pr_subcategory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='api.productsubcategory'),
        ),
    ]
