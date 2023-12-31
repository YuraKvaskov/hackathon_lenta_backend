# Generated by Django 4.1.11 on 2023-10-11 09:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_alter_product_pr_cat_id_alter_product_pr_group_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('st_city_id', models.CharField(db_index=True, max_length=255, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('pr_cat_id', models.CharField(db_index=True, max_length=255, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='ProductGroup',
            fields=[
                ('pr_group_id', models.CharField(db_index=True, max_length=255, primary_key=True, serialize=False)),
            ],
        ),
        migrations.RemoveField(
            model_name='product',
            name='pr_cat_id',
        ),
        migrations.RemoveField(
            model_name='product',
            name='pr_group_id',
        ),
        migrations.RemoveField(
            model_name='product',
            name='pr_subcat_id',
        ),
        migrations.RemoveField(
            model_name='store',
            name='st_city_id',
        ),
        migrations.CreateModel(
            name='ProductSubcategory',
            fields=[
                ('pr_subcat_id', models.CharField(db_index=True, max_length=255, primary_key=True, serialize=False)),
                ('pr_cat_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.productcategory')),
            ],
        ),
        migrations.AddField(
            model_name='productcategory',
            name='pr_group_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.productgroup'),
        ),
        migrations.AddField(
            model_name='product',
            name='subcategory',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='api.productsubcategory'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='store',
            name='city',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='api.city'),
            preserve_default=False,
        ),
    ]
