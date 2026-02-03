import argparse
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from PIL import Image
import os

IMAGE_DIM = (128, 128)

def load_prediction_artifacts(model_path, labels_path):
    try:
        model = load_model(model_path)
        with open(labels_path, "r") as f:
            labels = [line.strip() for line in f.readlines()]
        return model, labels
    except Exception as e:
        print("Error loading model or labels:", e)
        return None, None

def preprocess_image(image_path, target_size):
    if not os.path.exists(image_path):
        print("Image not found:", image_path)
        return None
    try:
        img = Image.open(image_path).convert("RGB")
        img = img.resize(target_size)
        arr = np.array(img) / 255.0
        arr = np.expand_dims(arr, axis=0)
        return arr
    except Exception as e:
        print("Image processing error:", e)
        return None

def predict_breed(model, img_array, labels):
    preds = model.predict(img_array)
    idx = np.argmax(preds[0])
    print("\n--- Prediction ---")
    print("Breed:", labels[idx])
    print("Confidence:", f"{preds[0][idx] * 100:.2f}%")

    print("\nTop 3 Predictions:")
    top3 = np.argsort(preds[0])[-3:][::-1]
    for i in top3:
        print(labels[i], f"{preds[0][i] * 100:.2f}%")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cat Breed Classifier")
    parser.add_argument("--model", required=True)
    parser.add_argument("--labels", required=True)
    parser.add_argument("--image", required=True)
    args = parser.parse_args()

    model, labels = load_prediction_artifacts(args.model, args.labels)
    if model is None:
        exit()

    img = preprocess_image(args.image, IMAGE_DIM)
    if img is not None:
        predict_breed(model, img, labels)
    else:
        print("Prediction aborted.")