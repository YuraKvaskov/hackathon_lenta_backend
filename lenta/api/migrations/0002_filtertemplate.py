# Generated by Django 4.1.11 on 2023-10-04 19:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FilterTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('st_city_id', models.CharField(blank=True, max_length=255, null=True)),
                ('store_id', models.CharField(blank=True, max_length=255, null=True)),
                ('pr_group_id', models.CharField(blank=True, max_length=255, null=True)),
                ('pr_cat_id', models.CharField(blank=True, max_length=255, null=True)),
                ('pr_subcat_id', models.CharField(blank=True, max_length=255, null=True)),
                ('selected_interval', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]