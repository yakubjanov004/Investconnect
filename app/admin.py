from django.contrib import admin
from app import models

class UserModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'firstname', 'lastname', 'phone', 'role', 'status')  
    search_fields = ('username',)  
    list_filter = ('role', 'status')  
    ordering = ('id',)  

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'degree', 'location', 'price', 'category')  
    search_fields = ('name', 'user__username', 'category__name')  
    list_filter = ('degree', 'category')  
    ordering = ('id',)  

class ContractAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id_display', 'user_username', 'contract')  
    search_fields = ('user__username', 'user__id')  
    ordering = ('id',) 

    def user_id_display(self, obj):
        return obj.user.id
    user_id_display.short_description = "Foydalanuvchi ID"

    def user_username(self, obj):
        return obj.user.username
    user_username.short_description = "Foydalanuvchi Username"

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
admin.site.register(models.Contract, ContractAdmin)
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Comment, CommentAdmin)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.PrivateInformation, InformationAdmin)