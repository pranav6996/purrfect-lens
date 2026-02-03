import os
import numpy as np
from PIL import Image
from django.conf import settings

# Global variables to store loaded model
MODEL = None
LABELS = []
IMAGE_DIM = (128, 128)

def load_model_and_labels():
    global MODEL, LABELS
    if MODEL is not None:
        return MODEL, LABELS
    
    # Lazy import to avoid segfaults on import or in management commands
    import tensorflow as tf
    from tensorflow.keras.models import load_model

    model_path = settings.BASE_DIR.parent / 'models' / 'pranav_cat_classifier_new_run.keras'
    labels_path = settings.BASE_DIR.parent / 'models' / 'breed_labels_new_run.txt'

    try:
        print(f"Loading model from {model_path}...")
        MODEL = load_model(str(model_path))
        with open(labels_path, "r") as f:
            LABELS = [line.strip() for line in f.readlines()]
        print("Model and labels loaded successfully.")
    except Exception as e:
        print(f"Error loading model: {e}")
    
    return MODEL, LABELS

def preprocess_image(image_file):
    try:
        img = Image.open(image_file).convert("RGB")
        img = img.resize(IMAGE_DIM)
        arr = np.array(img) / 255.0
        arr = np.expand_dims(arr, axis=0)
        return arr
    except Exception as e:
        print(f"Image processing error: {e}")
        return None

def predict_breed_from_image(image_file):
    model, labels = load_model_and_labels()
    if model is None:
        return None
    
    img_array = preprocess_image(image_file)
    if img_array is None:
        return None

    preds = model.predict(img_array)
    idx = np.argmax(preds[0])
    confidence = preds[0][idx] * 100
    breed = labels[idx]

    return {
        "breed": breed,
        "confidence": round(confidence, 2)
    }

