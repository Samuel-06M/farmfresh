from django.contrib import admin
from poultrypalace .models import User, Product
from poultrypalace .models import Cart, CartProduct
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'available', 'get_farmer')
    search_fields = ('name', 'description')

    def get_farmer(self, obj):
        return obj.farmer.username  # Assumes 'farmer' is a ForeignKey to User model

    get_farmer.short_description = 'Farmer'

    def save_model(self, request, obj, form, change):
        if not obj.farmer:
            obj.farmer = request.user  # Set the farmer to the current logged in user
        super().save_model(request, obj, form, change)

admin.site.register (User)
admin.site.register(Product, ProductAdmin)
admin.site.register (Cart)
admin.site.register (CartProduct)
