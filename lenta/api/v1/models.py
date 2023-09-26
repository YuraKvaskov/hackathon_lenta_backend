from django.db import models


class Store(models.Model):
    st_id = models.CharField(max_length=255)
    st_city_id = models.CharField(max_length=255)
    st_division_code = models.CharField(max_length=255)
    st_type_format_id = models.IntegerField()
    st_type_loc_id = models.IntegerField()
    st_type_size_id = models.IntegerField()
    st_is_active = models.BooleanField()

    def __str__(self):
        return self.st_id


class Product(models.Model):
    pr_group_id = models.CharField(max_length=255)
    pr_cat_id = models.CharField(max_length=255)
    pr_subcat_id = models.CharField(max_length=255)
    pr_sku_id = models.CharField(max_length=255)
    pr_uom_id = models.IntegerField()

    def __str__(self):
        return self.pr_sku_id


class Sales(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateField()
    pr_sales_type_id = models.BooleanField()
    pr_sales_in_units = models.IntegerField()
    pr_promo_sales_in_units = models.IntegerField()
    pr_sales_in_rub = models.FloatField()
    pr_promo_sales_in_rub = models.FloatField()


class SalesForecast(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    forecast_date = models.DateField()
    sales_units = models.JSONField()