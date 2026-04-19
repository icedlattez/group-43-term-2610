from django.contrib import admin
from .models import Vendor, Stall


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'social_media')


@admin.register(Stall)
class StallAdmin(admin.ModelAdmin):
    list_display = ('stall_name', 'vendor', 'location', 'event_name')