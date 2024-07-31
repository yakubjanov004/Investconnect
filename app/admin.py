from django.contrib import admin
from app import models

admin.site.register(models.UserModel)
admin.site.register(models.Contract)
admin.site.register(models.Category)
admin.site.register(models.Comment)
admin.site.register(models.Product)
admin.site.register(models.Information)