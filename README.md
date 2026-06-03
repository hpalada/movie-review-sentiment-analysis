# Movie Review Sentiment Analysis

Desktop application that classifies movie reviews as positive or negative and scores them 0–5 using a custom NLP pipeline. Two trained scikit-learn models run as an ensemble for more stable predictions.

## Stack

**UI** — Python · PyQt6  
**ML** — scikit-learn (Logistic Regression + Ridge Regression)  
**NLP** — TF-IDF vectorization · custom text preprocessing  
**Persistence** — JSON files · serialized `.pkl` model artifacts  

## How It Works

1. User enters a review in the desktop app
2. Text is cleaned — lowercased, punctuation removed, stop words filtered
3. TF-IDF vectorizer converts the text into a feature vector
4. Logistic Regression and Ridge each produce a score (0–5)
5. Final rating = average of both model outputs
6. Emotion labels extracted via keyword matching over cleaned tokens

```python
resultado = comunicacion.analizar_resena(texto)
# → { "valoracion": 4.2, "etiquetas": ["positive", "engaging"] }
```

## Features

- **Review classification** — automated 0–5 scoring from raw text
- **Emotion detection** — keyword-based label extraction alongside the score
- **User auth** — register, login, password change
- **Movie catalog** — browse movies, view aggregate scores
- **Review management** — create, view, and browse reviews per movie
- **Self-contained** — all data in JSON files, no external database

## Project Structure

```
├── principal.py            # Entry point
├── peliculaUI.py           # Main window
├── catalogoPrincipal.py    # Movie catalog view
├── ComunicacionModelo.Py   # ML bridge layer
├── Json.py                 # JSON I/O helpers
├── rutas.py                # Navigation router
├── Form*.py                # Login, register, add/edit, review forms
├── Clase*.py               # Domain models (Movie, Review, User, Auth)
└── MODELO/
    ├── algo2.py            # Full ML pipeline
    ├── lr_model.pkl        # Trained Logistic Regression
    ├── ridge_model.pkl     # Trained Ridge Regression
    ├── vectorizer.pkl      # Fitted TF-IDF vectorizer
    └── DataSetFinal.csv    # Labeled training dataset
```

## Setup

```bash
pip install PyQt6 scikit-learn numpy scipy
python principal.py
```

## ML Pipeline

- **Cleaning** — lowercase, strip punctuation, remove stop words
- **Features** — TF-IDF bag-of-words + handcrafted sentiment features
- **Ensemble** — average of Logistic Regression + Ridge outputs reduces individual model bias
- **Labels** — rule-based keyword matching for emotion tags

## Highlights

- Trained and serialized two ML models from a custom labeled dataset — no pre-built NLP library
- Ensemble scoring produces more stable predictions than a single model
- Clean MVC architecture separating UI, business logic, and ML layers

---

Built by Homer Palada — CS student at Universidad Católica de Honduras, graduating May 2027.
