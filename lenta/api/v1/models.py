from django.db import models
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model


User = get_user_model()


class FilterTemplate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    st_city_id = models.CharField(max_length=255, blank=True, null=True)
    store_id = models.CharField(max_length=255, blank=True, null=True)
    pr_group_id = models.CharField(max_length=255, blank=True, null=True)
    pr_cat_id = models.CharField(max_length=255, blank=True, null=True)
    pr_subcat_id = models.CharField(max_length=255, blank=True, null=True)
    selected_interval = models.IntegerField()

    def apply_filters(self, queryset):
        filters = {}
        if self.st_city_id:
            filters['store__st_city_id'] = self.st_city_id
        if self.store_id:
            filters['store__st_id'] = self.store_id
        if self.pr_group_id:
            filters['product__pr_group_id'] = self.pr_group_id
        if self.pr_cat_id:
            filters['product__pr_cat_id'] = self.pr_cat_id
        if self.pr_subcat_id:
            filters['product__pr_subcat_id'] = self.pr_subcat_id

        start_date = datetime.now().date() + timedelta(days=1)
        end_date = start_date + timedelta(days=self.selected_interval)

        return queryset.filter(
            forecast_date__gte=start_date,
            forecast_date__lte=end_date,
            **filters
        )

    def __str__(self):
        return self.name


class Store(models.Model):
    st_id = models.CharField(max_length=255, primary_key=True)
    st_city_id = models.CharField(max_length=255)
    st_division_code = models.CharField(max_length=255)
    st_type_format_id = models.IntegerField()
    st_type_loc_id = models.IntegerField()
    st_type_size_id = models.IntegerField()
    st_is_active = models.BooleanField()
    
    def __str__(self):
        return self.st_id


class Product(models.Model):
    pr_sku_id = models.CharField(max_length=255, primary_key=True)
    pr_group_id = models.CharField(max_length=255)
    pr_cat_id = models.CharField(max_length=255)
    pr_subcat_id = models.CharField(max_length=255)
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