
from django.contrib import admin
from .models import User, Vendor, Category, Product, Order, OrderItem

# Kusajili Custom User Model
admin.site.register(User)

# Kusajili Category
admin.site.register(Category)

# Kusajili Vendor kwa muonekano mzuri wa jedwali
@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('shop_name', 'user', 'is_verified')
    list_filter = ('is_verified',)
    search_fields = ('shop_name', 'user__username')

# Kusajili Product
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'vendor', 'category', 'price', 'stock')
    list_filter = ('category', 'vendor')
    search_fields = ('name', 'description')

# Kusajili Order na OrderItem kwa pamoja (Inline)
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'status', 'total_price', 'created_at')
    list_filter = ('status', 'created_at')
    inlines = [OrderItemInline]