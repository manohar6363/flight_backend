from rest_framework import serializers
from django.contrib.auth.models import User
from .models import FlightQuery

# Register serializer
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"]
        )
        return user

# Flight Query serializer
class FlightQuerySerializer(serializers.ModelSerializer):
    date = serializers.DateField(format="%Y-%m-%d")
    class Meta:
        model = FlightQuery
        fields = "__all__"
        read_only_fields = ["user", "predicted_price", "created_at"]