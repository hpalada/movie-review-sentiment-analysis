class Resena:
    def __init__(self, usuario, comentario, sentimiento, score):
        self.usuario = usuario
        self.comentario = comentario
        self.sentimiento = sentimiento
        self.score = score

    def to_dict(self):
        return {
            "usuario": self.usuario,
            "comentario": self.comentario,
            "analisis": {
                "sentimiento": self.sentimiento,
                "score": self.score
            }
        }
    