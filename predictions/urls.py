from django.urls import path
from .views import (
    PredictDiseaseAPIView,
    PredictionHistoryListAPIView,
    PredictionHistoryDetailAPIView,
    DiseaseInfoListAPIView,
    DiseaseInfoDetailAPIView,
)

urlpatterns = [
    path("predict/", PredictDiseaseAPIView.as_view(), name="predict"),

    path(
        "history/",
        PredictionHistoryListAPIView.as_view(),
        name="prediction-history",
    ),

    path(
        "history/<int:pk>/",
        PredictionHistoryDetailAPIView.as_view(),
        name="prediction-detail",
    ),

    path(
        "diseases/",
        DiseaseInfoListAPIView.as_view(),
        name="disease-list",
    ),

    path(
        "diseases/<int:pk>/",
        DiseaseInfoDetailAPIView.as_view(),
        name="disease-detail",
    ),
]