"""
FT-Transformer + BiLSTM Hybrid Model for AMR Prediction.

Architecture:
  Input features -> Per-feature embeddings -> Self-Attention (FT-Transformer)
  -> BiLSTM (captures interaction patterns) -> Sigmoid output (15 drugs)
"""

import torch
import torch.nn as nn
import numpy as np


class FeatureEmbedding(nn.Module):
    """Embed each numerical feature into d_model dimensions."""

    def __init__(self, n_features, d_model):
        super().__init__()
        self.embeddings = nn.ModuleList([
            nn.Sequential(
                nn.Linear(1, d_model),
                nn.ReLU(),
                nn.Linear(d_model, d_model),
            )
            for _ in range(n_features)
        ])
        self.cls_token = nn.Parameter(torch.randn(1, 1, d_model))

    def forward(self, x):
        embedded = []
        for i, emb in enumerate(self.embeddings):
            feat = x[:, i:i+1]
            embedded.append(emb(feat))
        embedded = torch.stack(embedded, dim=1)
        cls = self.cls_token.expand(x.size(0), -1, -1)
        embedded = torch.cat([cls, embedded], dim=1)
        return embedded


class FTTransformerBiLSTM(nn.Module):
    """
    FT-Transformer + BiLSTM hybrid.

    FT-Transformer: per-feature embedding + multi-head self-attention
    BiLSTM: captures sequential interaction patterns from attention outputs
    Output: 15 drug predictions (sigmoid)
    """

    def __init__(self, n_features, n_drugs, d_model=64, n_heads=4,
                 n_transformer_layers=2, lstm_hidden=64, dropout=0.2):
        super().__init__()

        self.feature_embedding = FeatureEmbedding(n_features, d_model)

        encoder_layer = nn.TransformerEncoderLayer(
            d_model=d_model,
            nhead=n_heads,
            dim_feedforward=d_model * 4,
            dropout=dropout,
            batch_first=True,
        )
        self.transformer = nn.TransformerEncoder(
            encoder_layer, num_layers=n_transformer_layers
        )

        self.layer_norm = nn.LayerNorm(d_model)

        self.bilstm = nn.LSTM(
            input_size=d_model,
            hidden_size=lstm_hidden,
            num_layers=1,
            batch_first=True,
            bidirectional=True,
            dropout=0,
        )

        self.dropout = nn.Dropout(dropout)

        self.classifier = nn.Sequential(
            nn.Linear(lstm_hidden * 2, 128),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(128, n_drugs),
        )

    def forward(self, x):
        embedded = self.feature_embedding(x)
        attended = self.transformer(embedded)
        attended = self.layer_norm(attended)
        lstm_out, _ = self.bilstm(attended)
        cls_output = lstm_out[:, 0, :]
        cls_output = self.dropout(cls_output)
        logits = self.classifier(cls_output)
        return logits


class FTBiLSTMWrapper:
    """Sklearn-compatible wrapper for training and prediction."""

    def __init__(self, n_features, n_drugs, epochs=50, lr=0.001, batch_size=128):
        self.n_features = n_features
        self.n_drugs = n_drugs
        self.epochs = epochs
        self.lr = lr
        self.batch_size = batch_size
        self.device = torch.device("cpu")
        self.model = None
        self.thresholds = None

    def fit(self, X, y):
        self.model = FTTransformerBiLSTM(
            n_features=self.n_features,
            n_drugs=self.n_drugs,
        ).to(self.device)

        optimizer = torch.optim.AdamW(self.model.parameters(), lr=self.lr, weight_decay=1e-4)

        # Compute class weights per drug
        pos_weights = []
        for i in range(y.shape[1]):
            n_pos = y[:, i].sum()
            n_neg = len(y[:, i]) - n_pos
            weight = n_neg / max(n_pos, 1)
            pos_weights.append(min(weight, 5.0))
        pos_weight_tensor = torch.FloatTensor(pos_weights).to(self.device)
        criterion = nn.BCEWithLogitsLoss(pos_weight=pos_weight_tensor)

        X_t = torch.FloatTensor(X).to(self.device)
        y_t = torch.FloatTensor(y).to(self.device)

        dataset = torch.utils.data.TensorDataset(X_t, y_t)
        loader = torch.utils.data.DataLoader(
            dataset, batch_size=self.batch_size, shuffle=True
        )

        self.model.train()
        for epoch in range(self.epochs):
            total_loss = 0
            for batch_X, batch_y in loader:
                optimizer.zero_grad()
                logits = self.model(batch_X)
                loss = criterion(logits, batch_y)
                loss.backward()
                torch.nn.utils.clip_grad_norm_(self.model.parameters(), 1.0)
                optimizer.step()
                total_loss += loss.item()

            if (epoch + 1) % 10 == 0:
                avg = total_loss / len(loader)
                print(f"    Epoch {epoch+1}/{self.epochs} - Loss: {avg:.4f}")

        return self

    def optimize_thresholds(self, X_val, y_val):
        """Find best threshold per drug on validation set."""
        from sklearn.metrics import f1_score
        probs = self.predict_proba(X_val)
        self.thresholds = np.full(self.n_drugs, 0.5)
        for i in range(self.n_drugs):
            best_f1 = 0
            best_t = 0.5
            for t in np.arange(0.2, 0.8, 0.05):
                preds = (probs[:, i] >= t).astype(int)
                f1 = f1_score(y_val[:, i], preds, zero_division=0)
                if f1 > best_f1:
                    best_f1 = f1
                    best_t = t
            self.thresholds[i] = best_t
        return self.thresholds

    def predict(self, X):
        self.model.eval()
        X_t = torch.FloatTensor(X).to(self.device)
        with torch.no_grad():
            logits = self.model(X_t)
            probs = torch.sigmoid(logits).cpu().numpy()
        thresholds = self.thresholds if self.thresholds is not None else np.full(self.n_drugs, 0.5)
        return (probs >= thresholds).astype(int)

    def predict_proba(self, X):
        self.model.eval()
        X_t = torch.FloatTensor(X).to(self.device)
        with torch.no_grad():
            logits = self.model(X_t)
            probs = torch.sigmoid(logits).cpu().numpy()
        return probs
