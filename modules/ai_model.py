import os
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Embedding, Input, LayerNormalization, MultiHeadAttention, Dropout
from tensorflow.keras.models import load_model
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.preprocessing import LabelEncoder
import tensorflow as tf

def prepare_sequences(data, digit_index, seq_len=10):
    X, y = [], []
    for i in range(len(data) - seq_len):
        seq = [int(data[j][digit_index]) for j in range(i, i + seq_len)]
        target = int(data[i + seq_len][digit_index])
        X.append(seq)
        y.append(target)
    return np.array(X), np.array(y)

def build_lstm_model(input_length, output_dim=10):
    model = Sequential([
        Embedding(input_dim=10, output_dim=8, input_length=input_length),
        LSTM(64, return_sequences=False),
        Dense(64, activation='relu'),
        Dense(output_dim, activation='softmax')
    ])
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    return model

def train_and_save_model(data, lokasi, model_type="LSTM"):
    for digit_index in range(4):
        X, y = prepare_sequences(data, digit_index)
        if model_type == "LSTM":
            model = build_lstm_model(input_length=X.shape[1])
        else:
            model = build_lstm_model(input_length=X.shape[1])  # Placeholder Transformer logic

        es = EarlyStopping(monitor='loss', patience=3, restore_best_weights=True)
        model.fit(X, y, epochs=20, batch_size=32, verbose=0, callbacks=[es])

        filename = f"saved_models/{lokasi.lower().replace(' ', '_')}_digit{digit_index}_{model_type}.h5"
        model.save(filename)

def top6_model(data, lokasi, model_type="LSTM"):
    result, probs = [], []
    for digit_index in range(4):
        model_path = f"saved_models/{lokasi.lower().replace(' ', '_')}_digit{digit_index}_{model_type}.h5"
        if not os.path.exists(model_path):
            result.append([0,1,2,3,4,5])
            probs.append([0.2]*6)
            continue

        model = load_model(model_path)
        seq = np.array([[int(row[digit_index]) for row in data[-10:]]])
        preds = model.predict(seq)[0]
        top_idx = preds.argsort()[-6:][::-1]
        result.append(top_idx.tolist())
        probs.append(preds[top_idx].tolist())
    return result, probs
