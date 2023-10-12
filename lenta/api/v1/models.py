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



class City(models.Model):
    st_city_id = models.CharField(max_length=255, primary_key=True, db_index=True)
    # Другие поля, связанные с городом

    def __str__(self):
        return self.st_city_id


class ProductGroup(models.Model):
    pr_group_id = models.CharField(max_length=255, primary_key=True, db_index=True)

    def __str__(self):
        return self.pr_group_id


class ProductCategory(models.Model):
    pr_cat_id = models.CharField(max_length=255, primary_key=True, db_index=True)
    pr_group_id = models.ForeignKey(ProductGroup, on_delete=models.CASCADE, related_name='categories')

    def __str__(self):
        return self.pr_cat_id


class ProductSubcategory(models.Model):
    pr_subcat_id = models.CharField(max_length=255, primary_key=True, db_index=True)
    pr_cat_id = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='subcategories')
    # Другие поля, связанные с подкатегорией продуктов

    def __str__(self):
        return self.pr_subcat_id


class Product(models.Model):
    pr_sku_id = models.CharField(max_length=255, primary_key=True, db_index=True)
    pr_group = models.ForeignKey(ProductGroup, on_delete=models.CASCADE)
    pr_category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    pr_subcategory = models.ForeignKey(ProductSubcategory, on_delete=models.CASCADE, related_name='products')
    pr_uom_id = models.IntegerField(db_index=True)

    def __str__(self):
        return self.pr_sku_id


class Store(models.Model):
    st_id = models.CharField(max_length=255, primary_key=True, db_index=True)
    st_city_id = models.ForeignKey(City, on_delete=models.CASCADE, db_index=True)  # Используйте новую модель City
    st_division_code = models.CharField(max_length=255, db_index=True)
    st_type_format_id = models.IntegerField()
    st_type_loc_id = models.IntegerField()
    st_type_size_id = models.IntegerField()
    st_is_active = models.BooleanField(db_index=True)

    def __str__(self):
        return self.st_id


class Sales(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, db_index=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, db_index=True)
    date = models.DateField(db_index=True)
    pr_sales_type_id = models.IntegerField()
    pr_sales_in_units = models.IntegerField()
    pr_promo_sales_in_units = models.IntegerField()
    pr_sales_in_rub = models.FloatField()
    pr_promo_sales_in_rub = models.FloatField()

    def __str__(self):
        return f"Sales record for {self.product} at {self.store} on {self.date}"


class SalesForecast(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, db_index=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    forecast_date = models.DateField()
    forecast = models.JSONField()

    def __str__(self):
        return f"SalesForecast for {self.product} at {self.store} on {self.forecast_date}"

# class Store(models.Model):
#     st_id = models.CharField(max_length=255, primary_key=True, db_index=True)
#     st_city_id = models.CharField(max_length=255, db_index=True)
#     st_division_code = models.CharField(max_length=255, db_index=True)
#     st_type_format_id = models.IntegerField()
#     st_type_loc_id = models.IntegerField()
#     st_type_size_id = models.IntegerField()
#     st_is_active = models.BooleanField(db_index=True)
#
#     def __str__(self):
#         return self.st_id
#
#
# class Product(models.Model):
#     pr_sku_id = models.CharField(max_length=255, primary_key=True, db_index=True)
#     pr_group_id = models.CharField(max_length=255, db_index=True)
#     pr_cat_id = models.CharField(max_length=255, db_index=True)
#     pr_subcat_id = models.CharField(max_length=255, db_index=True)
#     pr_uom_id = models.IntegerField(db_index=True)
#
#     def __str__(self):
#         return self.pr_sku_id
#
#
# class Sales(models.Model):
#     store = models.ForeignKey(Store, on_delete=models.CASCADE, db_index=True)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, db_index=True)
#     date = models.DateField(db_index=True)
#     pr_sales_type_id = models.IntegerField()
#     pr_sales_in_units = models.IntegerField()
#     pr_promo_sales_in_units = models.IntegerField()
#     pr_sales_in_rub = models.FloatField()
#     pr_promo_sales_in_rub = models.FloatField()
#
#
# class SalesForecast(models.Model):
#     store = models.ForeignKey(Store, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     forecast_date = models.DateField()
#     sales_units = models.JSONField()