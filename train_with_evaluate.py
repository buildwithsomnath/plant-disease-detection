import seaborn as sns
import os
import json
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parent

CONFIG = {
    "dataset_path": PROJECT_ROOT / "data" / "plant_disease_data",
    "model_save_path": PROJECT_ROOT / "models" / "plant_disease_model.h5",
    "class_names_path": PROJECT_ROOT / "models" / "class_names.json",
    "history_plot_path": PROJECT_ROOT / "models" / "training_history.png",
    "confusion_matrix_path": PROJECT_ROOT / "models" / "confusion_matrix.png", 
    'image_size': 224,
    'batch_size': 8,
    'epochs': 1,
    'learning_rate': 0.001,
    'validation_split': 0.2,
    'test_split': 0.1,
}

def prepare_dataset(dataset_path, image_size, batch_size, validation_split):
    print("Scanning dataset directory...")
    class_names = sorted([d for d in os.listdir(dataset_path) if   os.path.isdir(os.path.join(dataset_path,d))])

    num_classes = len(class_names)
    print(f"✅ Found {num_classes} disease classes: ")
    for i, cls in enumerate(class_names):
        img_count = len(os.listdir(os.path.join(dataset_path,cls)))
        print(f"  {i+1}.{cls}: {img_count} images")

    # Data augmentation for training
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        brightness_range=[0.8, 1.2],
        fill_mode='nearest',
        validation_split=validation_split
    )
    
    # Only rescaling for testing (no augmentation)
    test_datagen = ImageDataGenerator(rescale=1./255)
    
    # Load training data
    print("\n📊 Loading training data...")
    train_generator = train_datagen.flow_from_directory(
        dataset_path,
        target_size=(image_size, image_size),
        batch_size=batch_size,
        class_mode='categorical',
        subset='training',
        seed=42
    )
    
    # Load validation data
    print("📊 Loading validation data...")
    validation_generator = train_datagen.flow_from_directory(
        dataset_path,
        target_size=(image_size, image_size),
        batch_size=batch_size,
        class_mode='categorical',
        subset='validation',
        seed=42
    )
    
    return train_generator, validation_generator, class_names


# BUILD CNN MODEL
def build_model(num_classes, input_size=224):
    print("\n 🏗️ Building model architecture...")
    print("   Using Transfer Learning with MobileNetV2...")
    base_model = keras.applications.MobileNetV2(
        input_shape=(input_size,input_size,3),
        include_top=False,
        weights='imagenet'
    )

    # Freeze base model layers
    base_model.trainable = False

    #Build complete model
    model = models.Sequential([
        keras.Input(shape=(input_size,input_size,3)),
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.Dense(256, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.3),
        layers.Dense(num_classes, activation='softmax')
    ])

    print("✅ Model architecture: ")
    model.summary()

    return model

def build_custom_cnn(num_classes, input_size=224):
    print("\n🏗️ Building custom CNN Architecture...")
    model = models.Sequential([
        #Block 1
        keras.Input(shape=(input_size, input_size, 3)),
        layers.Conv2D(32,(3,3),activation='relu',padding='same'),
        layers.BatchNormalization(),
        layers.Conv2D(32,(3,3),activation='relu',padding='same'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2,2)),
        layers.Dropout(0.25),

        #Block 2
        layers.Conv2D(32,(3,3),activation='relu',padding='same'),
        layers.BatchNormalization(),
        layers.Conv2D(32,(3,3),activation='relu',padding='same'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2,2)),
        layers.Dropout(0.25),

        #Block 3
        layers.Conv2D(32,(3,3),activation='relu',padding='same'),
        layers.BatchNormalization(),
        layers.Conv2D(32,(3,3),activation='relu',padding='same'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2,2)),
        layers.Dropout(0.25),

        #Block 4
        layers.Conv2D(32,(3,3),activation='relu',padding='same'),
        layers.BatchNormalization(),
        layers.Conv2D(32,(3,3),activation='relu',padding='same'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2,2)),
        layers.Dropout(0.25),

        #Dense Layers
        layers.Flatten(),
        layers.Dense(512,activation='relu'),
        layers.BatchNormalization(),
        layers.Dropout(0.5),
        layers.Dense(256,activation='relu'),
        layers.BatchNormalization(),
        layers.Dropout(0.3),
        layers.Dense(num_classes, activation='softmax')

    ])

    print("✅ Custom CNN architecture:")
    model.summary()

    return model

# Compile Model
def compile_model(model, learning_rate=0.001):
    print("\n⚙️ Compiling model...")

    optimizer = keras.optimizers.Adam(learning_rate=learning_rate)

    model.compile(
        optimizer=optimizer,
        loss='categorical_crossentropy',
        metrics=['accuracy',keras.metrics.Precision(),keras.metrics.Recall()]
    )

    print("✅ Model compiled successfully")
    return model

# callbacks

def get_callbacks(model_path):
    callbacks = [
        #save best model
        keras.callbacks.ModelCheckpoint(
            model_path,
            monitor='val_accuracy',
            save_best_only = True,
            mode='max',
            verbose=1
        ),
        #early stopping to prevent overfitting
        keras.callbacks.EarlyStopping(
            monitor='val_loss',
            patience=5,
            restore_best_weights=True,
            verbose=1
        ),

        #learning rate reduction
        keras.callbacks.ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=3,
            min_lr=1e-7,
            verbose=1
        )
        
    ]
    return callbacks

def train_model(model, train_generator, validation_generator, epochs, callbacks):
    # Train the Model
    print("\n 🚀 Starting Training...")
    print(f"  Epochs:{epochs}")
    print(f"  Batch Size: {train_generator.batch_size}")
    print(f"  Training Samples: {train_generator.samples}")
    print(f"  Validation Samples: {validation_generator.samples}")

    history = model.fit(
        train_generator,
        validation_data = validation_generator,
        epochs = epochs,
        callbacks = callbacks,
        verbose=1
    )

    print("\n✅ Training Completed!")
    return history

# Evaluate Model
def evaluate_model(model, validation_generator):
    print("\n 📊 Evaluation model on validation set...")

    results = model.evaluate(validation_generator, verbose=1)

    print(f"\n  Validation Loss: {results[0]:.4f}")
    print(f"  Validation Accuracy: {results[1]:.4f}")
    print(f"  Validation Precision: {results[2]:.4f}")
    print(f"  Validation Recall: {results[3]:.4f}")

    return results

def generate_classification_report(model, validation_generator, class_names, save_dir):
    print("\n📊 Generating Classification Report...")

    validation_generator.reset()

    predictions = model.predict(validation_generator, verbose=1)

    y_pred = np.argmax(predictions, axis=1)
    y_true = validation_generator.classes

    # Confusion Matrix
    cm = confusion_matrix(y_true, y_pred)

    plt.figure(figsize=(18, 15))
    sns.heatmap(
        cm,
        cmap="Blues",
        xticklabels=class_names,
        yticklabels=class_names
    )

    plt.title("Confusion Matrix", fontsize=16, fontweight="bold")
    plt.xlabel("Predicted Label")
    plt.ylabel("True Label")
    plt.xticks(rotation=90)
    plt.yticks(rotation=0)

    confusion_path = os.path.join(save_dir, "confusion_matrix.png")
    plt.tight_layout()
    plt.savefig(confusion_path, dpi=300)
    plt.close()

    print(f"✅ Confusion Matrix saved to {confusion_path}")

    # Classification Report
    report = classification_report(
        y_true,
        y_pred,
        target_names=class_names
    )

    report_path = os.path.join(save_dir, "classification_report.txt")

    with open(report_path, "w") as f:
        f.write(report)

    print(report)
    print(f"✅ Classification Report saved to {report_path}")
# Save model

def save_model(model, save_path):
    # save model in h5 format
    print(f"\n 🛟 Saving Model to {save_path}...")

    dirpath = os.path.dirname(save_path) or '.'
    os.makedirs(dirpath, exist_ok=True)

    model.save(save_path)

    print(f"✅ Model Saved successfully!")
def save_class_names(class_names, save_path="models/class_names.json"):
    """
    Save class names to models/class_names.json
    """

    # Always use the models directory
    models_dir = "models"
    os.makedirs(models_dir, exist_ok=True)

    save_path = os.path.join(models_dir, "class_names.json")

    print(f"\n💾 Saving class names to {save_path}")

    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(class_names, f, indent=4)

    print("✅ Class names saved successfully!")

def save_model_tflite(model, save_path):
    """Convert and save model as TensorFlow Lite."""

    print("\n📦 Converting model to TensorFlow Lite...")

    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    tflite_model = converter.convert()

    # Create .tflite path
    tflite_save_path = save_path.with_suffix(".tflite")

    with open(tflite_save_path, "wb") as f:
        f.write(tflite_model)

    print(f"✅ TensorFlow Lite model saved to {tflite_save_path}")

# Plotting and Visualition
from pathlib import Path
import matplotlib.pyplot as plt

def plot_training_history(history, save_path):
    """
    Plot and save training history.
    """

    print("\n📈 Plotting training history...")

    save_path = Path(save_path)
    save_path.parent.mkdir(parents=True, exist_ok=True)

    fig, axes = plt.subplots(1, 2, figsize=(15, 5))

    # Accuracy Plot
    if "accuracy" in history.history:
        axes[0].plot(history.history["accuracy"], label="Training Accuracy", linewidth=2)

    if "val_accuracy" in history.history:
        axes[0].plot(history.history["val_accuracy"], label="Validation Accuracy", linewidth=2)

    axes[0].set_title("Model Accuracy", fontsize=14, fontweight="bold")
    axes[0].set_xlabel("Epoch")
    axes[0].set_ylabel("Accuracy")
    axes[0].legend()
    axes[0].grid(True, linestyle="--", alpha=0.5)

    # Loss Plot
    if "loss" in history.history:
        axes[1].plot(history.history["loss"], label="Training Loss", linewidth=2)

    if "val_loss" in history.history:
        axes[1].plot(history.history["val_loss"], label="Validation Loss", linewidth=2)

    axes[1].set_title("Model Loss", fontsize=14, fontweight="bold")
    axes[1].set_xlabel("Epoch")
    axes[1].set_ylabel("Loss")
    axes[1].legend()
    axes[1].grid(True, linestyle="--", alpha=0.5)

    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close(fig)

    print(f"✅ Training history saved to {save_path}")

# main execution

def main():
    # main training execution

    print("+"*60)
    print(" 🌿 PLANT DISEASE DETECTION MODEL TRAINING")
    print("+"*60)

    # dataset preparation
    train_generator, validation_generator, class_names = prepare_dataset(
        CONFIG['dataset_path'],
        CONFIG['image_size'],
        CONFIG['batch_size'],
        CONFIG['validation_split']
    )

    # BUILD THE MODEL
    model = build_model(len(class_names), CONFIG['image_size'])

    # COMPILE MODEL
    model = compile_model(model, CONFIG['learning_rate'])

    # Get callbacks
    callbacks = get_callbacks(CONFIG['model_save_path'])

    # Train model
    history = train_model(
        model,
        train_generator,
        validation_generator,
        CONFIG['epochs'],
        callbacks
    )

    #Evaluate model
    evaluate_model(model, validation_generator)
    generate_classification_report(
        model,
        validation_generator,
        class_names,
        "models"
    )
    # Save Model
    # Save .h5
    save_model(model, CONFIG['model_save_path'])

    # Save .keras
    keras_path = CONFIG['model_save_path'].with_suffix(".keras")
    model.save(keras_path)

    print(f"✅ Keras model saved to {keras_path}")
    save_class_names(class_names, CONFIG['class_names_path'])

    # Save TFlite version
    save_model_tflite(model, CONFIG['model_save_path'])

    # Plot training history
    plot_training_history(history, CONFIG['history_plot_path'])

    print("\n"+"+" * 60)
    print("✅ TRAINING COMPLETE!")
    print("="*60)
    print("\n📁 Generated Files:")
    print("models/")
    print(f"├── {CONFIG['model_save_path'].with_suffix('.keras').name}      # Preferred Keras format")
    print(f"├── {CONFIG['model_save_path'].name}         # HDF5 compatibility format")
    print(f"├── {CONFIG['model_save_path'].with_suffix('.tflite').name}     # TensorFlow Lite model")
    print(f"├── {CONFIG['class_names_path'].name}              # Disease class names")
    print(f"├── {CONFIG['history_plot_path'].name}          # Accuracy & Loss curves")
    print(f"├── confusion_matrix.png          # Confusion matrix")
    print(f"└── classification_report.txt     # Precision, Recall & F1-Score")


if __name__ == "__main__":
    main()