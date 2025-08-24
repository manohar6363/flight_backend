from django.contrib import admin
from .models import FlightQuery

@admin.register(FlightQuery)
class FlightQueryAdmin(admin.ModelAdmin):
    list_display = ("user", "airline", "source", "destination", "departure_time", "arrival_time", "date", "predicted_price", "created_at")
    list_filter = ("airline", "date")
    search_fields = ("user__username", "source", "destination", "airline")