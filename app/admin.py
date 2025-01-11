from django.contrib import admin
from app import models

class UserModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'firstname', 'lastname', 'phone', 'role', 'status')  
    search_fields = ('username',)  
    list_filter = ('role', 'status')  
    ordering = ('id',)  

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'location', 'price', 'category')  
    search_fields = ('name', 'user__username', 'category__name')  
    list_filter = ('category',)  
    ordering = ('id',)  


class InformationAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_name',)  
    search_fields = ('product__name',)     
    list_filter = ('product__name',)                      
    ordering = ('id',)                                    

    def product_name(self, obj):
        return obj.product.name
    product_name.short_description = "Mahsulot Nomi"

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name') 
    search_fields = ('name',)     
    ordering = ('id',)  

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_name', 'user_username', 'short_description')  
    search_fields = ('product__name', 'user__username', 'description')                                       
    ordering = ('id',)                                                        

    def product_name(self, obj):
        return obj.product.name
    product_name.short_description = "Mahsulot Nomi"

    def user_username(self, obj):
        return obj.user.username
    user_username.short_description = "Foydalanuvchi"

    def short_description(self, obj):
        return f"{obj.description[:30]}..." if obj.description else ""
    short_description.short_description = "Sharh"


admin.site.register(models.UserModel, UserModelAdmin)
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Comment, CommentAdmin)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.PrivateInformation, InformationAdmin)