import joblib
import numpy as np
import pandas as pd
from datetime import datetime

from django.contrib.auth.models import User
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import FlightQuery
from .serializers import RegisterSerializer, FlightQuerySerializer

# Load model once at startup
MODEL_PATH = "ml_model/flight_fare_model.pkl"
model = joblib.load(MODEL_PATH)

# --------- Auth Views ---------
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        from django.contrib.auth import authenticate
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)

        if not user:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        })


# --------- Prediction View ---------
class PredictPriceView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        data = request.data
        serializer = FlightQuerySerializer(data=data)
        if serializer.is_valid():
            airline = data.get("airline", "").lower().strip()
            source = data.get("from", "").lower().strip()
            destination = data.get("to", "").lower().strip()
            dep_time = data.get("departure_time", "")
            arr_time = data.get("arrival_time", "")
            duration = data.get("time_taken", "")
            date_str = data.get("date", "")

            # --------- Feature Engineering (like your training code) ---------
            try:
                date_obj = pd.to_datetime(date_str, errors="coerce")
                if pd.isnull(date_obj):
                    return Response({"error":"Invalid date format"},status=400)
                date = date_obj.date()
                journey_day = date.day
                journey_month = date.month
                journey_year = date.year
            except:
                return Response({"error": "Invalid date"}, status=400)

            dep = pd.to_datetime(dep_time, errors="coerce")
            arr = pd.to_datetime(arr_time, errors="coerce")

            dep_hour = dep.hour if pd.notnull(dep) else 0
            dep_min = dep.minute if pd.notnull(dep) else 0
            arr_hour = arr.hour if pd.notnull(arr) else 0
            arr_min = arr.minute if pd.notnull(arr) else 0

            # parse duration like "2h 30m"
            h, m = 0, 0
            try:
                if "h" in duration:
                    h = int(duration.split("h")[0].strip())
                if "m" in duration:
                    m = int(duration.split("h")[1].replace("m", "").strip())
            except:
                pass

            # Build single-row dataframe with same feature names as training
            row = pd.DataFrame([{
                "airline": airline,
                "from": source,
                "to": destination,
                "journey_day": journey_day,
                "journey_month": journey_month,
                "journey_year": journey_year,
                "dep_hour": dep_hour,
                "dep_min": dep_min,
                "arr_hour": arr_hour,
                "arr_min": arr_min,
                "Duration_hours": h,
                "Duration_mins": m,
            }])

            # Predict
            predicted_price = model.predict(row)[0]

            # Save query
            flight_query = FlightQuery.objects.create(
                user=request.user,
                airline=airline,
                source=source,
                destination=destination,
                departure_time=dep_time,
                arrival_time=arr_time,
                time_taken=duration,
                date=date,
                predicted_price=predicted_price
            )

            return Response({
                "predicted_price": predicted_price,
                "query": FlightQuerySerializer(flight_query).data
            })

        return Response(serializer.errors, status=400)