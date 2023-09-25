from django.contrib import admin
from . import models

admin.site.register(models.Store)
admin.site.register(models.Product)
admin.site.register(models.Sales)
