
# Generated by Django 4.1.11 on 2023-10-05 12:10


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_filtertemplate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sales',
            name='pr_sales_type_id',
            field=models.IntegerField(),
        ),
    ]