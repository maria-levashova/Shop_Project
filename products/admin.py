# администратор для управления древовидной структурой
from mptt.admin import DraggableMPTTAdmin
from django.contrib import admin
from products.models import *


@admin.register(CategoryList)
class CategoryListAdmin(DraggableMPTTAdmin):
    list_display = ('parent', 'order', 'title', 'image')
    list_display_links = ('title',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'category', 'is_in_stock']


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'product']


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'category']

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']

@admin.register(ProductTag)
class ProductTagAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'tag']

@admin.register(Reason)
class ReasonAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']

@admin.register(ProductReason)
class ProductReasonAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'reason']

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'created_at', 'phone_number', 'status',
                    'total_price']
    list_filter = ['status']
    inlines = [OrderItemInline]