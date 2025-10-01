from django.contrib import admin
from parler.admin import TranslatableAdmin
from apps.models import *

class ProductImagesInline(admin.StackedInline):
    model = ProductImage
    extra = 1


class AttributeInline(admin.StackedInline):
    model = Attributes
    extra = 1


@admin.register(Category)
class CategoryAdmin(TranslatableAdmin):
    pass


@admin.register(Products)
class ProductsAdmin(TranslatableAdmin):
    inlines = [ProductImagesInline, AttributeInline]


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    pass


@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    pass


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    pass


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    pass


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    pass


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    pass
