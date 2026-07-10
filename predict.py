import argparse
import json
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

from tensorflow import keras
import tensorflow as tf


# -----------------------------
# Configuration
# -----------------------------
MODEL_PATH = Path("models/plant_disease_model.keras")
CLASS_NAMES_PATH = Path("models/class_names.json")
IMAGE_SIZE = (224, 224)


# -----------------------------
# Load Model
# -----------------------------
def load_model_and_classes():
    print("📦 Loading model...")

    if MODEL_PATH.exists():
        model = keras.models.load_model(MODEL_PATH)
    else:
        model = keras.models.load_model("models/plant_disease_model.h5")

    with open(CLASS_NAMES_PATH, "r", encoding="utf-8") as f:
        class_names = json.load(f)

    print("✅ Model loaded successfully!")
    print(f"📚 Loaded {len(class_names)} disease classes\n")

    return model, class_names


# -----------------------------
# Preprocess Image
# -----------------------------
def preprocess_image(image_path):
    img = keras.preprocessing.image.load_img(
        image_path,
        target_size=IMAGE_SIZE
    )

    img_array = keras.preprocessing.image.img_to_array(img)
    img_array = img_array / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    return img, img_array


# -----------------------------
# Predict
# -----------------------------
def predict_image(model, class_names, image_path):
    img, img_array = preprocess_image(image_path)

    predictions = model.predict(img_array, verbose=0)[0]

    predicted_idx = np.argmax(predictions)
    confidence = predictions[predicted_idx]

    print("=" * 60)
    print("🌿 Plant Disease Prediction")
    print("=" * 60)

    print(f"\n📷 Image      : {image_path}")
    print(f"🦠 Disease    : {class_names[predicted_idx]}")
    print(f"🎯 Confidence : {confidence * 100:.2f}%")

    print("\n🏆 Top 3 Predictions")

    top3 = np.argsort(predictions)[-3:][::-1]

    for i, idx in enumerate(top3, start=1):
        print(f"{i}. {class_names[idx]:40} {predictions[idx]*100:.2f}%")

    # Display image
    plt.figure(figsize=(6, 6))
    plt.imshow(img)
    plt.axis("off")
    plt.title(
        f"{class_names[predicted_idx]}\nConfidence: {confidence*100:.2f}%"
    )
    plt.show()


# -----------------------------
# Main
# -----------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Plant Disease Prediction"
    )

    parser.add_argument(
        "image",
        help="Path to the leaf image"
    )

    args = parser.parse_args()

    image_path = Path(args.image)

    if not image_path.exists():
        print(f"❌ Image not found:\n{image_path}")
        return

    model, class_names = load_model_and_classes()

    predict_image(
        model,
        class_names,
        image_path
    )


if __name__ == "__main__":
    main()