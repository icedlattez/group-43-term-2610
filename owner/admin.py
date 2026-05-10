from django.contrib import admin
from .models import Owner, Stall


@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone')
    search_fields = ('name', 'phone')


@admin.register(Stall)
class StallAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'owner', 'event', 'location', 'capacity', 'rental_fee')
    list_filter = ('owner', 'event')
    search_fields = ('name', 'location', 'owner__name', 'event__name')