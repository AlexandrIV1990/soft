from django.contrib import admin

from image.models import Image, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    filter_horizontal = (
        'categories',
    )
