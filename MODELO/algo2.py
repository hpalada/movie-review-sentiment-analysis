import pandas as pd
import nltk
import string
import re
import numpy as np
import joblib
import os
from scipy.sparse import hstack, csr_matrix

from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import mean_squared_error


# =====================================
# PREPARACIÓN
# =====================================

nltk.download('stopwords')
nltk.download('vader_lexicon')

stop_words = set(stopwords.words("english"))
sia = SentimentIntensityAnalyzer()


# =====================================
# DICCIONARIO DE EMOCIONES
# =====================================

EMOTION_KEYWORDS = {
    " Enojo": {
        "terrible", "awful", "horrible", "disgusting", "hate", "hated", "worst",
        "garbage", "trash", "pathetic", "ridiculous", "useless", "stupid", "idiot",
        "angry", "furious", "outraged", "infuriating", "annoying", "irritating"
    },
    " Decepción": {
        "disappointed", "disappointing", "disappointment", "expected", "expected more",
        "letdown", "underwhelming", "mediocre", "boring", "dull", "bland", "flat",
        "waste", "wasted", "not worth", "overrated", "overhyped"
    },
    " Humor / Sarcasmo": {
        "seriously", "really", "supposed", "apparently", "clearly", "obviously",
        "sure", "right", "yeah", "lol", "haha", "funny", "joke", "comedy",
        "laughable", "absurd", "ridiculous", "unbelievable"
    },
    " Satisfacción": {
        "good", "great", "nice", "enjoyed", "solid", "decent", "fine",
        "happy", "pleased", "satisfied", "worth", "recommend", "liked"
    },
    " Entusiasmo": {
        "amazing", "excellent", "outstanding", "fantastic", "incredible", "brilliant",
        "masterpiece", "perfect", "love", "loved", "best", "awesome", "superb",
        "extraordinary", "phenomenal", "spectacular", "wonderful", "magnificent"
    },
    " Miedo / Tensión": {
        "scary", "terrifying", "frightening", "tense", "suspense", "thriller",
        "horror", "disturbing", "unsettling", "creepy", "eerie", "dread", "fear"
    },
    " Aburrimiento": {
        "boring", "bored", "slow", "dragging", "dragged", "tedious", "dull",
        "uninteresting", "pointless", "monotonous", "repetitive", "long", "endless"
    },
    " Confusión": {
        "confused", "confusing", "unclear", "makes no sense", "nonsense",
        "incoherent", "lost", "weird", "strange", "odd", "bizarre", "random"
    }
}


def detect_emotions(text):
    text_lower = str(text).lower()
    words = set(text_lower.split())
    detected = []

    for emotion, keywords in EMOTION_KEYWORDS.items():
        if words & keywords:
            detected.append(emotion)

    return detected if detected else [" Neutral"]


# =====================================
# FUNCIONES DE PROCESAMIENTO
# =====================================

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'<.*?>', '', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    words = text.split()
    words = [word for word in words if word not in stop_words]
    return " ".join(words)


def extract_features(text):
    text = str(text)

    vader_scores = sia.polarity_scores(text)
    vader_compound = vader_scores['compound']
    vader_pos = vader_scores['pos']
    vader_neg = vader_scores['neg']

    words = text.split()
    uppercase_ratio = sum(1 for w in words if w.isupper() and len(w) > 1) / (len(words) + 1)

    exclamation_count = text.count('!')
    question_count = text.count('?')

    negation_words = {"not", "no", "never", "nothing", "nobody", "nowhere",
                      "neither", "nor", "hardly", "barely", "scarcely"}
    negation_count = sum(1 for w in words if w.lower() in negation_words)

    review_length = len(words)

    return [
        vader_compound,
        vader_pos,
        vader_neg,
        uppercase_ratio,
        exclamation_count,
        question_count,
        negation_count,
        review_length
    ]


# =====================================
# RUTAS DE LOS ARCHIVOS GUARDADOS
# =====================================

_dir = os.path.dirname(os.path.abspath(__file__))
RUTA_VECTORIZER  = os.path.join(_dir, "vectorizer.pkl")
RUTA_LR_MODEL    = os.path.join(_dir, "lr_model.pkl")
RUTA_RIDGE_MODEL = os.path.join(_dir, "ridge_model.pkl")

modelos_existen = (
    os.path.exists(RUTA_VECTORIZER) and
    os.path.exists(RUTA_LR_MODEL) and
    os.path.exists(RUTA_RIDGE_MODEL)
)


# =====================================
# CARGAR O ENTRENAR MODELOS
# =====================================

if modelos_existen:
    # ✅ Cargar modelos ya entrenados
    print("Cargando modelos guardados...")
    vectorizer  = joblib.load(RUTA_VECTORIZER)
    lr_model    = joblib.load(RUTA_LR_MODEL)
    ridge_model = joblib.load(RUTA_RIDGE_MODEL)
    print("Modelos cargados correctamente.")

else:
    # 🔁 Primera vez: cargar datos, entrenar y guardar
    print("Entrenando modelos por primera vez...")

    data = pd.read_csv("DataSetFinal.csv", sep=";")
    print("Dataset cargado")

    # Ruta absoluta relativa a donde está algo2.py
    _dir = os.path.dirname(os.path.abspath(__file__))
    data = pd.read_csv(os.path.join(_dir, "DataSetFinal.csv"), sep=";")
    data.columns = ["review", "score"]

    data["clean_review"] = data["review"].apply(clean_text)
    print("Texto limpio")

    vectorizer = TfidfVectorizer(max_features=10000)
    X_tfidf = vectorizer.fit_transform(data["clean_review"])

    extra_features = np.array(data["review"].apply(extract_features).tolist())
    X_extra = csr_matrix(extra_features)

    X = hstack([X_tfidf, X_extra])
    y = data["score"]

    print("Features combinadas listas")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Modelo 1 — Linear Regression
    lr_model = LinearRegression()
    lr_model.fit(X_train, y_train)
    lr_pred = lr_model.predict(X_test)
    lr_mse = mean_squared_error(y_test, lr_pred)
    print("Listo Linear Regression — MSE:", round(lr_mse, 4))

    # Modelo 2 — Ridge Regression
    ridge_model = Ridge(alpha=1.0)
    ridge_model.fit(X_train, y_train)
    ridge_pred = ridge_model.predict(X_test)
    ridge_mse = mean_squared_error(y_test, ridge_pred)
    print("Listo Ridge Regression — MSE:", round(ridge_mse, 4))

    # 💾 Guardar los tres archivos
    joblib.dump(vectorizer,  RUTA_VECTORIZER)
    joblib.dump(lr_model,    RUTA_LR_MODEL)
    joblib.dump(ridge_model, RUTA_RIDGE_MODEL)
    print("Modelos guardados para próximas ejecuciones.")


