# Generated by Django 4.1.11 on 2023-10-11 10:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_rename_city_store_st_city_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='subcategory',
            new_name='pr_subcategory',
        ),
        migrations.AddField(
            model_name='product',
            name='pr_category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='api.productcategory'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='pr_group',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='api.productgroup'),
            preserve_default=False,
        ),
    ]