from django.db import models
from django.contrib.auth.models import User

class FlightQuery(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="queries")
    airline = models.CharField(max_length=100)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_time = models.CharField(max_length=50)
    arrival_time = models.CharField(max_length=50)
    time_taken = models.CharField(max_length=50)
    date = models.DateField()
    predicted_price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.source} → {self.destination} ({self.date})"