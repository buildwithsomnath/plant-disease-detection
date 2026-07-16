import json
import os
import numpy as np

from django.conf import settings
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from tensorflow import keras

from .models import PredictionHistory, DiseaseInfo
from .serializers import (
    PredictionHistorySerializer,
    DiseaseInfoSerializer,
    ImageUploadSerializer,
)

from PIL import Image


# -----------------------------
# Load Model
# -----------------------------
MODEL = keras.models.load_model(settings.MODEL_PATH)

with open(
    os.path.join(settings.BASE_DIR, "models", "class_names.json"),
    "r",
) as f:
    CLASS_NAMES = json.load(f)


# -----------------------------
# Helper Functions
# -----------------------------
def preprocess_image(image_file):
    image = Image.open(image_file)

    if image.mode != "RGB":
        image = image.convert("RGB")

    image = image.resize((224, 224))

    image = np.array(image).astype("float32") / 255.0
    image = np.expand_dims(image, axis=0)

    return image


def get_recommendation(disease_name):
    disease = DiseaseInfo.objects.filter(
        disease_name=disease_name
    ).first()

    if disease:
        return {
            "description": disease.description,
            "symptoms": disease.symptoms,
            "causes": disease.causes,
            "prevention": disease.prevention,
            "treatment": disease.treatment,
            "fertilizer": disease.fertilizer,
        }

    return {
        "description": "",
        "symptoms": "",
        "causes": "",
        "prevention": "",
        "treatment": "",
        "fertilizer": "",
    }


# -----------------------------
# Prediction API
# -----------------------------
class PredictDiseaseAPIView(APIView):

    def post(self, request):

        serializer = ImageUploadSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        image = serializer.validated_data["image"]

        processed = preprocess_image(image)

        prediction = MODEL.predict(processed)

        class_index = np.argmax(prediction)

        confidence = float(prediction[0][class_index])

        disease_name = CLASS_NAMES[class_index]

        plant_type = disease_name.split("_")[0]

        recommendation = get_recommendation(disease_name)

        image.seek(0)

        history = PredictionHistory.objects.create(
            image=image,
            predicted_disease=disease_name,
            confidence=confidence,
            plant_type=plant_type,
            fertilizer_recommendation=recommendation["fertilizer"],
            treatment_recommendation=recommendation["treatment"],
        )

        return Response(
            {
                "success": True,
                "prediction_id": history.id,
                "prediction": {
                    "disease": disease_name,
                    "confidence": round(confidence * 100, 2),
                    "plant_type": plant_type,
                    **recommendation,
                },
            },
            status=status.HTTP_200_OK,
        )


# -----------------------------
# Prediction History
# -----------------------------
class PredictionHistoryListAPIView(generics.ListAPIView):
    queryset = PredictionHistory.objects.all()
    serializer_class = PredictionHistorySerializer


# -----------------------------
# Prediction Details
# -----------------------------
class PredictionHistoryDetailAPIView(generics.RetrieveAPIView):
    queryset = PredictionHistory.objects.all()
    serializer_class = PredictionHistorySerializer


# -----------------------------
# Disease Information
# -----------------------------
class DiseaseInfoListAPIView(generics.ListAPIView):
    queryset = DiseaseInfo.objects.all()
    serializer_class = DiseaseInfoSerializer


class DiseaseInfoDetailAPIView(generics.RetrieveAPIView):
    queryset = DiseaseInfo.objects.all()
    serializer_class = DiseaseInfoSerializer