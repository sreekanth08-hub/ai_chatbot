import cv2
import numpy as np

def predict_disease_image(image_path):
    img = cv2.imread(image_path)

    if img is None:
        return {"error": "Invalid image file"}

    img = cv2.resize(img, (100, 100))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    mean_intensity = np.mean(gray)

    if mean_intensity < 90:
        disease = "Psoriasis"
    elif mean_intensity < 150:
        disease = "Eczema"
    else:
        disease = "Acne"

    return {
        "disease": disease,
        "analysis": "Image feature-based prediction",
        "confidence": "Moderate"
    }
