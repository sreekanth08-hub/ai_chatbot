def map_symptoms(symptoms):
    symptoms = symptoms.lower()

    if "fever" in symptoms and "cough" in symptoms:
        return "Flu"
    elif "chest pain" in symptoms:
        return "Heart Disease"
    elif "rash" in symptoms:
        return "Skin Infection"
    else:
        return "Unknown"
