from django.contrib import admin
from django.utils.safestring import mark_safe
from django.forms import ModelChoiceField

from .models import *


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    prepopulated_fields = {"slug": ("name",)}

class SmartPhoneAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'show_image', 'is_available',)
    list_editable = ('is_available', )
    list_filter = ('is_available', 'price', )
    prepopulated_fields = {"slug": ("title",)}


    def show_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="75">')
        else:
            return "None"

    show_image.__name__ = 'Миниатюра'

    # Ограничивает выбор категории
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='smartphones'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class NotebookAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'show_image', 'is_available', )
    list_editable = ('is_available', )
    list_filter = ('is_available', 'price', )
    prepopulated_fields = {"slug": ("title",)}

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='notebooks'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def show_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="75">')
        else:
            return "None"

    show_image.__name__ = 'Миниатюра'


class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'first_name', 'last_name', 'phone', 'address', 'status', 'buying_type', 'comment', 'created_at', 'order_date',)

admin.site.register(Cart)
admin.site.register(Customer)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Notebook, NotebookAdmin)
admin.site.register(SmartPhone, SmartPhoneAdmin)
admin.site.register(CartProduct)
admin.site.register(Order, OrderAdmin)



# admin.site.site_title = ''
# admin.site.site_header = ''