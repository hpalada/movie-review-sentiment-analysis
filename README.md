# Movie Review Sentiment Analysis

Desktop application that uses NLP and machine learning to classify movie reviews and score them on a 0–5 scale. Built with Python and PyQt6, with two trained models for ensemble prediction.

## Tech Stack

| Component | Technology |
|---|---|
| UI | Python, PyQt6 |
| ML Models | Scikit-learn (Logistic Regression, Ridge Regression) |
| NLP | TF-IDF vectorization, custom text pipeline |
| Data | CSV dataset, JSON-based persistence |

## How It Works

1. User enters a review in the desktop app
2. Text is cleaned and vectorized using a trained TF-IDF vectorizer
3. Two models (Logistic Regression + Ridge) each produce a score
4. Final rating = average of both models (0.0 – 5.0)
5. Emotion labels are extracted and displayed alongside the rating

### Model Communication Layer

```python
# ComunicacionModelo bridges the UI layer and the ML models
resultado = comunicacion.analizar_resena(texto)
# Returns: { "valoracion": 4.2, "etiquetas": ["positive", "engaging"] }
```

## Features

- **Review classification** — automated scoring from raw review text
- **Emotion detection** — keyword-based label extraction from review content
- **User authentication** — login, registration, and password change
- **Movie catalog** — browse movies, view average scores across all reviews
- **Review management** — create, view, and browse reviews per movie
- **Data persistence** — all data stored in JSON files; no external DB required

## Project Structure

```
PRUEBAPARAMELVIN/
├── principal.py            # Entry point
├── peliculaUI.py           # Main window
├── catalogoPrincipal.py    # Movie catalog view
├── clasePelicula.py        # Movie model
├── ClaseReseña.py          # Review model
├── ClaseUsuario.py         # User model
├── ClaseLogin.py           # Auth logic
├── ComunicacionModelo.Py   # ML bridge layer
├── Json.py                 # JSON I/O helpers
├── FormLogin.py            # Login form
├── FormRegistroUsuario.py  # Registration form
├── FormAgregaryEditar.py   # Add/edit forms
├── FormReseñas.py          # Review form
├── FormCambiarContra.py    # Password change form
├── rutas.py                # Navigation router
├── MODELO/
│   ├── algo2.py            # ML pipeline (vectorizer + models)
│   ├── lr_model.pkl        # Trained Logistic Regression model
│   ├── ridge_model.pkl     # Trained Ridge Regression model
│   ├── vectorizer.pkl      # Fitted TF-IDF vectorizer
│   └── DataSetFinal.csv    # Training dataset
└── data/                   # Runtime JSON data files
```

## Setup

```bash
pip install PyQt6 scikit-learn numpy scipy
python principal.py
```

## ML Pipeline

- **Text cleaning** — lowercasing, punctuation removal, stop word filtering
- **Feature extraction** — TF-IDF bag-of-words + custom handcrafted features
- **Models** — Logistic Regression and Ridge trained on a labeled review dataset
- **Ensemble** — average of both model outputs for final 0–5 score
- **Emotion tags** — rule-based keyword matching over cleaned tokens

## Highlights

- Trained and serialized two ML models from a custom labeled dataset
- Built a clean MVC architecture separating UI, business logic, and ML layers
- Ensemble scoring reduces individual model bias for more stable predictions
- Implemented full text processing pipeline: cleaning, vectorization, feature extraction
- JSON-based storage makes the app fully self-contained with no external dependencies
