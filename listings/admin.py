from django.contrib import admin
from .models import Product, Category, Review

# Register your models here.

class OrderREviewInline(admin.TabularInline):
    model = Review

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'slug', 'price', 'available')
    list_filter = ('category', 'available')
    list_editable = ('price', 'available')
    prepopulated_fields = {'slug': ('name',)}

    inlines = [OrderREviewInline]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

