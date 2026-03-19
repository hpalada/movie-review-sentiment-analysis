import sys
import os

# Apunta a la carpeta MODELO que está al mismo nivel que este archivo
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'MODELO'))

import numpy as np
from scipy.sparse import hstack, csr_matrix

from algo2 import (  # type: ignore
    vectorizer,
    lr_model,
    ridge_model,
    clean_text,
    extract_features,
    detect_emotions
)


class ComunicacionModelo:
    """
    Capa de comunicación entre la clase Resena y el modelo de IA.
    Recibe el texto de una reseña, lo analiza y devuelve
    únicamente la valoración y las etiquetas.
    """

    def __init__(self):
        self.vectorizer  = vectorizer
        self.lr_model    = lr_model
        self.ridge_model = ridge_model

    def analizar_resena(self, texto: str) -> dict:
        """
        Recibe el texto de una reseña desde la clase Resena.
        Retorna un diccionario con:
          - valoracion : float (0.0 - 5.0), promedio de ambos modelos
          - etiquetas  : list[str], emociones detectadas en el texto
        """
        if not texto or not texto.strip():
            return {
                "valoracion": 0.0,
                "etiquetas" : [" Neutral"]
            }

        # 1. Limpiar y vectorizar
        texto_limpio = clean_text(texto)
        tfidf_vector = self.vectorizer.transform([texto_limpio])

        # 2. Features adicionales (VADER, mayúsculas, negaciones, etc.)
        extra        = np.array(extract_features(texto)).reshape(1, -1)
        extra_sparse = csr_matrix(extra)

        # 3. Combinar vectores
        vector_final = hstack([tfidf_vector, extra_sparse])

        # 4. Predicción con ambos modelos
        score_lr     = float(np.clip(self.lr_model.predict(vector_final)[0], 0, 5))
        score_ridge  = float(np.clip(self.ridge_model.predict(vector_final)[0], 0, 5))

        # 5. Valoración final como promedio de ambos modelos
        valoracion   = round((score_lr + score_ridge) / 2, 2)

        # 6. Etiquetas emocionales
        etiquetas    = detect_emotions(texto)

        return {
            "valoracion": valoracion,
            "etiquetas" : etiquetas
        }