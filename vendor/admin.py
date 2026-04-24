from django.contrib import admin
from .models import Vendor, Stall

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'social_media')


@admin.register(Stall)
class StallAdmin(admin.ModelAdmin):
    list_display = ('event_name', 'category', 'location', 'status', 'vendor')
    ordering = ('event_name',)