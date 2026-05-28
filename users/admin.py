from django.contrib import admin
from .models import User,  Product


admin.site.register(User)






@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_sold', 'created_at')
    list_filter = ('category', 'is_sold')
    search_fields = ('name', 'phone')