import os
import numpy as np
import pandas as pd
import torch

from torch.utils.data import Dataset, DataLoader
from transformers import (
    DistilBertTokenizerFast,
    DistilBertForSequenceClassification,
    get_linear_schedule_with_warmup
)
from torch.optim import AdamW
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import psutil


# =====================================
# CONFIGURACIÓN
# =====================================

CONFIG = {
    "csv_path":        "DataSetFinal.csv",
    "sep":             ";",
    "text_col":        "reviewText",
    "score_col":       "Personalizado",
    "output_dir":      "modelo_guardado",
    "model_name":      "distilbert-base-uncased",
    "max_length":      256,
    "batch_size":      16,
    "grad_accum":      4,
    "epochs":          3,
    "learning_rate":   2e-5,
    "warmup_ratio":    0.1,
    "test_size":       0.1,
    "score_min":       0.0,
    "score_max":       5.0,
    "seed":            42,
}

torch.manual_seed(CONFIG["seed"])
np.random.seed(CONFIG["seed"])


# =====================================
# MONITOREO DE RECURSOS
# =====================================

def log_recursos(etapa=""):
    ram = psutil.virtual_memory()
    ram_usada = ram.used / 1024**3
    ram_total = ram.total / 1024**3
    ram_pct   = ram.percent
    linea_ram = f"RAM: {ram_usada:.1f}GB / {ram_total:.1f}GB ({ram_pct}%)"

    if torch.cuda.is_available():
        vram_usada = torch.cuda.memory_allocated() / 1024**3
        vram_total = torch.cuda.get_device_properties(0).total_memory / 1024**3
        linea_gpu  = f" | VRAM: {vram_usada:.1f}GB / {vram_total:.1f}GB"
    else:
        linea_gpu = " | GPU: no disponible"

    print(f"  [{etapa}] {linea_ram}{linea_gpu}")


# =====================================
# DATASET PERSONALIZADO
# =====================================

class ReviewDataset(Dataset):

    def __init__(self, texts, scores, tokenizer, max_length):
        self.encodings = tokenizer(
            texts,
            truncation=True,
            padding=True,
            max_length=max_length,
            return_tensors="pt"
        )
        self.scores = torch.tensor(
            [(s - CONFIG["score_min"]) / (CONFIG["score_max"] - CONFIG["score_min"])
             for s in scores],
            dtype=torch.float
        )

    def __len__(self):
        return len(self.scores)

    def __getitem__(self, idx):
        item = {key: val[idx] for key, val in self.encodings.items()}
        item["labels"] = self.scores[idx]
        return item


# =====================================
# MAIN
# =====================================

if __name__ == '__main__':

    print("\n" + "="*50)
    print("  ENTRENAMIENTO DISTILBERT — ANÁLISIS DE RESEÑAS")
    print("="*50 + "\n")

    # Detectar dispositivo
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    use_pin_memory = torch.cuda.is_available()
    print(f"► Dispositivo: {device}")
    if torch.cuda.is_available():
        print(f"  GPU: {torch.cuda.get_device_name(0)}")
    print()

    # ── Cargar datos ──
    print("► Cargando dataset...")
    log_recursos("inicio")

    data = pd.read_csv(CONFIG["csv_path"], sep=CONFIG["sep"])
    data = data[[CONFIG["text_col"], CONFIG["score_col"]]].copy()
    data.columns = ["review", "score"]

    data = data.dropna(subset=["review", "score"])
    data = data[data["score"].between(CONFIG["score_min"], CONFIG["score_max"])]
    data["review"] = data["review"].astype(str).str.strip()
    data = data[data["review"].str.len() > 5]

    print(f"  Filas válidas: {len(data):,}")
    print(f"  Score mínimo: {data['score'].min()} | Score máximo: {data['score'].max()}")
    print(f"  Score promedio: {data['score'].mean():.2f}\n")

    # ── Split ──
    train_texts, test_texts, train_scores, test_scores = train_test_split(
        data["review"].tolist(),
        data["score"].tolist(),
        test_size=CONFIG["test_size"],
        random_state=CONFIG["seed"]
    )
    print(f"► Split: {len(train_texts):,} entrenamiento | {len(test_texts):,} prueba\n")

    # ── Tokenizar ──
    print("► Cargando tokenizador...")
    tokenizer = DistilBertTokenizerFast.from_pretrained(CONFIG["model_name"])

    print("► Tokenizando datos de entrenamiento...")
    train_dataset = ReviewDataset(train_texts, train_scores, tokenizer, CONFIG["max_length"])
    log_recursos("después de tokenizar train")

    print("► Tokenizando datos de prueba...")
    test_dataset = ReviewDataset(test_texts, test_scores, tokenizer, CONFIG["max_length"])
    log_recursos("después de tokenizar test")

    train_loader = DataLoader(
        train_dataset,
        batch_size=CONFIG["batch_size"],
        shuffle=True,
        num_workers=0,
        pin_memory=use_pin_memory
    )

    test_loader = DataLoader(
        test_dataset,
        batch_size=CONFIG["batch_size"] * 2,
        shuffle=False,
        num_workers=0,
        pin_memory=use_pin_memory
    )

    print(f"  Batches de entrenamiento: {len(train_loader):,}")
    print(f"  Batches de prueba: {len(test_loader):,}\n")

    # ── Modelo ──
    print("► Cargando modelo DistilBERT...")
    model = DistilBertForSequenceClassification.from_pretrained(
        CONFIG["model_name"],
        num_labels=1
    )
    model = model.to(device)
    log_recursos("modelo cargado")
    print()

    # ── Optimizador ──
    optimizer = AdamW(model.parameters(), lr=CONFIG["learning_rate"], weight_decay=0.01)

    total_steps  = (len(train_loader) // CONFIG["grad_accum"]) * CONFIG["epochs"]
    warmup_steps = int(total_steps * CONFIG["warmup_ratio"])

    scheduler = get_linear_schedule_with_warmup(
        optimizer,
        num_warmup_steps=warmup_steps,
        num_training_steps=total_steps
    )

    loss_fn = torch.nn.MSELoss()

    # ── Entrenamiento ──
    print("► Iniciando entrenamiento...\n")
    mejor_mse = float("inf")
    os.makedirs(CONFIG["output_dir"], exist_ok=True)

    for epoch in range(CONFIG["epochs"]):

        model.train()
        total_loss    = 0
        pasos_totales = len(train_loader)
        optimizer.zero_grad()

        for paso, batch in enumerate(train_loader):

            input_ids      = batch["input_ids"].to(device)
            attention_mask = batch["attention_mask"].to(device)
            labels         = batch["labels"].to(device)

            outputs = model(input_ids=input_ids, attention_mask=attention_mask)
            logits  = outputs.logits.squeeze(-1)

            loss = loss_fn(logits, labels) / CONFIG["grad_accum"]
            loss.backward()
            total_loss += loss.item() * CONFIG["grad_accum"]

            if (paso + 1) % CONFIG["grad_accum"] == 0:
                torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
                optimizer.step()
                scheduler.step()
                optimizer.zero_grad()

            if (paso + 1) % 200 == 0 or (paso + 1) == pasos_totales:
                pct      = (paso + 1) / pasos_totales * 100
                avg_loss = total_loss / (paso + 1)
                print(f"  Epoch {epoch+1}/{CONFIG['epochs']} | "
                      f"Paso {paso+1}/{pasos_totales} ({pct:.1f}%) | "
                      f"Loss: {avg_loss:.4f}")

        log_recursos(f"fin epoch {epoch+1}")

        # ── Evaluación ──
        print(f"\n  Evaluando epoch {epoch+1}...")
        model.eval()
        preds_raw  = []
        labels_raw = []

        with torch.no_grad():
            for batch in test_loader:
                input_ids      = batch["input_ids"].to(device)
                attention_mask = batch["attention_mask"].to(device)
                labels         = batch["labels"].to(device)

                outputs = model(input_ids=input_ids, attention_mask=attention_mask)
                logits  = outputs.logits.squeeze(-1)

                preds_raw.extend(logits.cpu().numpy())
                labels_raw.extend(labels.cpu().numpy())

        preds_5  = np.clip(
            np.array(preds_raw) * (CONFIG["score_max"] - CONFIG["score_min"]) + CONFIG["score_min"],
            CONFIG["score_min"], CONFIG["score_max"]
        )
        labels_5 = np.array(labels_raw) * (CONFIG["score_max"] - CONFIG["score_min"]) + CONFIG["score_min"]

        mse = mean_squared_error(labels_5, preds_5)
        mae = np.mean(np.abs(labels_5 - preds_5))

        print(f"  MSE: {mse:.4f} | MAE: {mae:.4f}")

        if mse < mejor_mse:
            mejor_mse = mse
            model.save_pretrained(CONFIG["output_dir"])
            tokenizer.save_pretrained(CONFIG["output_dir"])
            print(f"  ✓ Mejor modelo guardado en '{CONFIG['output_dir']}' (MSE: {mejor_mse:.4f})")

        print()

    # ── Resumen ──
    print("="*50)
    print(f"  ENTRENAMIENTO COMPLETADO")
    print(f"  Mejor MSE alcanzado : {mejor_mse:.4f}")
    print(f"  Modelo guardado en  : {CONFIG['output_dir']}/")
    print("="*50)
    log_recursos("final")