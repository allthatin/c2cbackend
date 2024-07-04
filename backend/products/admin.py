from django.contrib import admin
from .models import \
Products, \
Tag, \
Category, \
ProductImage, \
ProductReview, \
Manufacturer,\
MarketingCategory

@admin.register(Products)
class ProductAdmin(admin.ModelAdmin):
    
    # add m2m fields to the list_display
    def marketing_categories(self, obj):
        return ', '.join([mc.name for mc in obj.marketing_categories.all()])
    marketing_categories.short_description = 'Marketing Categories'

    list_display = ('model', 'name', 'age', 'is_display', 'marketing_categories', )
    list_filter = ('is_display', 'category')
    search_fields = ('name', 'description', 'model', 'code_name')
    ordering = ('-created_on',)



@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('-created_on',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('-created_on',)

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('image', 'id')
    # list_filter = ('product',)
    ordering = ('-created_on',)

@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'title', 'rating', 'is_display')
    list_filter = ('is_display', 'rating', 'product')
    search_fields = ('title', 'content')
    ordering = ('-created_on',)

@admin.register(Manufacturer)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('-created_on',)

@admin.register(MarketingCategory)
class MartketingCategoryAdmin(admin.ModelAdmin):
    list_display = ('name','id',)
    search_fields = ('name',)
    ordering = ('-created_on',)
