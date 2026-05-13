import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.efficientnet import preprocess_input

MODEL_PATH = "ml_models/crop_disease_model.keras"

loaded_model = load_model(MODEL_PATH)

class_names = [
    "Cassava__Bacterial_Blight_(CBB)",
    "Cassava__Brown_Streak_Disease_(CBSD)",
    "Cassava__Green_Mottle_(CGM)",
    "Cassava__Healthy",
    "Cassava__Mosaic_Disease_(CMD)",
    "Rice__BrownSpot",
    "Rice__Healthy",
    "Rice__Hispa",
    "Rice__LeafBlast",
    "apple__apple_scab",
    "apple__black_rot",
    "apple__cedar_apple_rust",
    "apple__healthy",
    "cherry(includingsour)__healthy",
    "cherry(includingsour)__powdery_mildew",
    "corn(maize)__cercospora_leaf_spot_gray_leaf_spot",
    "corn(maize)__common_rust",
    "corn(maize)__healthy",
    "corn(maize)__northern_leaf_blight",
    "grape__black_rot",
    "grape__esca_(black_measles)",
    "grape__healthy",
    "grape__leaf_blight_(isariopsis_leaf_spot)",
    "orange__haunglongbing_(citrus_greening)",
    "peach__bacterial_spot",
    "peach__healthy",
    "pepperbell__bacterial_spot",
    "pepperbell__healthy",
    "potato__early_blight",
    "potato__healthy",
    "potato__late_blight",
    "squash__powdery_mildew",
    "strawberry__healthy",
    "strawberry__leaf_scorch",
    "tomato__bacterial_spot",
    "tomato__early_blight",
    "tomato__healthy",
    "tomato__late_blight",
    "tomato__leaf_mold",
    "tomato__septoria_leaf_spot",
    "tomato__spider_mites_two-spotted_spider_mite",
    "tomato__target_spot",
    "tomato__tomato_mosaic_virus",
    "tomato__tomato_yellow_leaf_curl_virus",
]


IMG_SIZE = (224, 224)
BATCH_SIZE = 4

def predict_disease(img_path):

    img = tf.keras.utils.load_img(img_path, target_size=IMG_SIZE)
    img_array = tf.keras.utils.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)  # Create a batch

    # Preprocess the image
    preprocessed_img = preprocess_input(img_array)

    # Make prediction
    predictions = loaded_model.predict(preprocessed_img)

    top5_indices = np.argsort(predictions[0])[-5:][::-1] 

    results = []

    for i in top5_indices:
        label = class_names[i]
        confidence = float(predictions[0][i])

        crop, disease = label.split("__")

        disease = disease.replace("_"," ")

        results.append({
            "crop": crop.title(),
            "disease": disease.title(),
            "confidence": round(confidence*100,2)
        })

    return results