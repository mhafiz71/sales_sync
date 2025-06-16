from django.contrib import admin
from .models import Product, Sale, SaleItem

admin.site.site_header = "SaleSync Administration"
admin.site.site_title = "SaleSync Admin Portal"
admin.site.index_title = "Welcome to the SaleSync Portal"

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'description')
    search_fields = ('name', 'description')
    list_filter = ('price', 'stock')

class SaleItemInline(admin.TabularInline):
    model = SaleItem
    readonly_fields = ('subtotal',)
    extra = 1

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'customer_name', 'total_amount')
    readonly_fields = ('created_at', 'total_amount')
    list_filter = ('created_at',)
    search_fields = ('customer_name', 'id')
    inlines = [SaleItemInline]

@admin.register(SaleItem)
class SaleItemAdmin(admin.ModelAdmin):
    list_display = ('sale', 'product', 'quantity', 'price', 'subtotal')