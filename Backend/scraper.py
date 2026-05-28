import requests
from bs4 import BeautifulSoup
import json


# Predefined templates
TEMPLATES = {

    "fever": {
        "symptoms": {
            "fever": 3,
            "fatigue": 2,
            "headache": 2,
            "body_pain": 2
        },
        "core": ["fever"],
        "duration": [2, 7],
        "severity": "high",
        "test": "CBC"
    },

    "respiratory": {
        "symptoms": {
            "cough": 3,
            "breathlessness": 3,
            "chest_pain": 2
        },
        "core": ["cough"],
        "duration": [3, 10],
        "severity": "high",
        "test": "Chest X-ray"
    },

    "digestive": {
        "symptoms": {
            "nausea": 3,
            "vomiting": 3,
            "abdominal_pain": 2
        },
        "core": ["vomiting"],
        "duration": [1, 5],
        "severity": "medium",
        "test": "Stool Test"
    },

    "general": {
        "symptoms": {
            "fatigue": 2,
            "pain": 2,
            "weakness": 2
        },
        "core": ["fatigue"],
        "duration": [1, 5],
        "severity": "low",
        "test": "Blood Test"
    }
}


# Proper disease keywords
VALID_DISEASE_KEYWORDS = [

    "disease",
    "fever",
    "infection",
    "syndrome",
    "disorder",
    "cancer",
    "asthma",
    "pneumonia",
    "bronchitis",
    "diabetes",
    "arthritis",
    "migraine",
    "malaria",
    "dengue",
    "typhoid",
    "tuberculosis",
    "covid",
    "flu",
    "gastritis",
    "hypertension",
    "poisoning",
    "virus"
]


# Disease Classification
def classify_disease(name):

    name = name.lower()

    if any(word in name for word in [
        "dengue",
        "malaria",
        "typhoid",
        "fever",
        "covid",
        "flu",
        "virus"
    ]):
        return "fever"

    elif any(word in name for word in [
        "asthma",
        "pneumonia",
        "bronchitis",
        "lung",
        "tuberculosis"
    ]):
        return "respiratory"

    elif any(word in name for word in [
        "food",
        "stomach",
        "gastritis",
        "diarrhea",
        "vomiting",
        "poisoning"
    ]):
        return "digestive"

    else:
        return "general"


# Scraper Function
def scrape_diseases():

    url = "https://www.healthline.com/health/diseases-conditions"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")

    diseases = set()

    # Extract disease names
    for tag in soup.find_all("a", href=True):

        text = tag.get_text(strip=True)

        # Skip empty text
        if not text:
            continue

        text_lower = text.lower()

        # Keep only disease-related names
        if any(keyword in text_lower for keyword in VALID_DISEASE_KEYWORDS):

            # Basic filtering
            if (
                len(text) > 3 and
                len(text.split()) <= 4 and
                text[0].isupper()
            ):

                diseases.add(text)

    # Add important diseases manually
    manual_diseases = [

    "Dengue",
    "Malaria",
    "Typhoid",
    "Pneumonia",
    "Asthma",
    "Migraine",
    "Tuberculosis",
    "COVID-19",
    "Diabetes",
    "Hypertension",
    "Bronchitis",
    "Gastritis",
    "Arthritis",
    "Food Poisoning",
    "Viral Fever",

    "Common Cold",
    "Chickenpox",
    "Influenza",
    "Sinus Infection",
    "Hepatitis",
    "Anemia",
    "Leukemia",
    "Skin Allergy",
    "Appendicitis",
    "Kidney Stone",

    "Heart Disease",
    "Stroke",
    "Obesity",
    "Depression",
    "Anxiety Disorder",
    "Epilepsy",
    "Parkinson Disease",
    "Alzheimer Disease",
    "Thyroid Disorder",
    "Ulcer",

    "Cholera",
    "Jaundice",
    "Conjunctivitis",
    "Ear Infection",
    "Eye Flu",
    "Psoriasis",
    "Acne",
    "Eczema",
    "Back Pain",
    "Sciatica",

    "Liver Disease",
    "Lung Cancer",
    "Breast Cancer",
    "Oral Cancer",
    "Brain Tumor",
    "Osteoporosis",
    "Rheumatoid Arthritis",
    "Bronchial Asthma",
    "Sinusitis",
    "Piles",

    "Constipation",
    "Diarrhea",
    "Vomiting",
    "Dehydration",
    "Insomnia",
    "Sleep Apnea",
    "High Cholesterol",
    "Low Blood Pressure",
    "High Blood Pressure",
    "PCOS",

    "Endometriosis",
    "Urinary Infection",
    "Diphtheria",
    "Measles",
    "Mumps",
    "Rubella",
    "Rabies",
    "Polio",
    "HIV",
    "AIDS",

    "Gallstones",
    "Pancreatitis",
    "Astigmatism",
    "Cataract",
    "Glaucoma",
    "Vertigo",
    "Motion Sickness",
    "Asthenia",
    "Fibromyalgia",
    "Scoliosis",

    "Sprain",
    "Fracture",
    "Osteoarthritis",
    "Gout",
    "Tonsillitis",
    "Pharyngitis",
    "Laryngitis",
    "Whooping Cough",
    "Dysentery",
    "Heat Stroke",

    "Sunburn",
    "Fungal Infection",
    "Ringworm",
    "Herpes",
    "Dengue Hemorrhagic Fever",
    "Swine Flu",
    "Bird Flu",
    "Zika Virus",
    "Chikungunya",
    "Norovirus"
]

    for d in manual_diseases:
        diseases.add(d)

    return sorted(list(diseases))[:100]


# Build Dataset
def build_dataset():

    scraped = scrape_diseases()

    dataset = {}

    for disease in scraped:

        category = classify_disease(disease)

        template = TEMPLATES[category]

        dataset[disease] = {
            "symptoms": template["symptoms"],
            "core_symptoms": template["core"],
            "duration": template["duration"],
            "severity": template["severity"],
            "test": template["test"]
        }

    return dataset


# Save Dataset
def save_dataset(data):

    with open("dataset.json", "w") as f:
        json.dump(data, f, indent=4)


# Main
if __name__ == "__main__":

    data = build_dataset()

    save_dataset(data)

    print("dataset.json generated successfully!")