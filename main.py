from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import numpy as np
from io import BytesIO
from PIL import Image
import tensorflow as tf
from translate import Translator

translator = Translator(to_lang="Hindi")

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL = tf.keras.models.load_model(
    "./trained_model")
CLASS_NAMES = ["Early Blight", "Late Blight", "Healthy"]


@app.get("/ping")
async def ping():
    return "Hello, I am alive"


def read_file_as_image(data) -> np.ndarray:
    image = np.array(Image.open(BytesIO(data)))
    return image


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    image = read_file_as_image(await file.read())
    img_batch = np.expand_dims(image, 0)
    predictions = MODEL.predict(img_batch)
    pm = []
    pm_hindi = []
    predicted_class = CLASS_NAMES[np.argmax(predictions[0])]
    message1 = 'Welcome to the portal for detecting and rectifying potato plant disease !!!'
    message2 = 'आलू के पौधे की बीमारी का पता लगाने और उसे ठीक करने के पोर्टल में आपका स्वागत है !!!'
    if predicted_class == CLASS_NAMES[0]:
        pm_hindi = 'बेयर गार्डन ब्लाइट कंट्रोल'
        pm = 'bare garden blight control'
        class_hindi = 'अर्ली ब्लाइट'
    elif predicted_class == CLASS_NAMES[1]:
        pm_hindi = 'मैन्कोज़ेब का रोगनिरोधी स्प्रे 0.25% और उसके बाद सायमोक्सानिल+मैंकोज़ेब या डाइमेथोमोर्फ+मैनकोज़ेब 0.3% पर'
        pm = 'Prophylactic spray of mancozeb at 0.25% followed by cymoxanil+mancozeb or dimethomorph+mancozeb at 0.3%'
        class_hindi = 'लेट ब्लाइट'
    else:
        class_hindi = 'कोई बीमारी नहीं मिली :)'
    confidence = np.max(predictions[0])
    return {
        'Title': message1,
        'शीर्षक': message2,
        'class': predicted_class,
        'रोग का नाम': class_hindi,
        'confidence': float(confidence),
        'सटीकता': float(confidence),
        'Suggested Spray': pm,
        'सुझाया गया स्प्रे': pm_hindi
    }

#translator= Translator(to_lang="Hindi")
#translation = translator.translate("Good Morning!")
# print(translation)

if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=8000)
