# Generated by Django 4.1.11 on 2023-10-11 09:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_city_productcategory_productgroup_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='store',
            old_name='city',
            new_name='st_city_id',
        ),
    ]
