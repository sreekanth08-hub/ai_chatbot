import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

data = pd.read_csv("../datasets/symptoms_dataset.csv")

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(data["symptoms"])
y = data["disease"]

model = MultinomialNB()
model.fit(X, y)

REMEDIES = {
    "Flu": [
        "Take adequate rest",
        "Drink warm fluids",
        "Steam inhalation",
        "Use paracetamol for fever"
    ],
    "Common Cold": [
        "Warm salt water gargle",
        "Stay hydrated",
        "Avoid cold drinks"
    ],
    "Heart Disease": [
        "Avoid physical exertion",
        "Maintain calm breathing",
        "Seek medical attention if pain persists"
    ],
    "Acne": [
        "Wash face twice daily",
        "Avoid oily cosmetics",
        "Drink plenty of water"
    ],
    "Eczema": [
        "Apply moisturizer regularly",
        "Avoid harsh soaps",
        "Keep skin hydrated"
    ],
    "Psoriasis": [
        "Apply moisturizing creams",
        "Avoid skin injuries",
        "Manage stress levels"
    ]
}

def predict_disease_text(symptoms):
    vec = vectorizer.transform([symptoms])
    disease = model.predict(vec)[0]

    return {
        "disease": disease,
        "recommendations": REMEDIES.get(disease, ["Maintain a healthy lifestyle"])
    }
