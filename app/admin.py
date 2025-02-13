from django.contrib import admin

from .models import Currency, Provider, Block


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "api_key")


@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "currency",
        "provider",
        "block_number",
        "created_at",
        "stored_at",
    )
    list_filter = ("currency", "provider")
