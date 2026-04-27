from django.contrib import admin
from .models import Event, EventRegistration


# ------------------------
# EVENT ADMIN
# ------------------------
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'location',
        'start_date',
        'end_date',
        'status',
        'organizer',
    )

    list_filter = (
        'status',
        'start_date',
        'end_date',
        'location',
    )

    search_fields = (
        'title',
        'location',
        'description',
        'organizer__username',
    )

    ordering = ('start_date',)


# ------------------------
# EVENT REGISTRATION ADMIN
# ------------------------
@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'event',
        'registered_at',
    )

    list_filter = (
        'event',
        'user',
    )

    search_fields = (
        'user__username',
        'event__title',
    )

    ordering = ('-registered_at',)