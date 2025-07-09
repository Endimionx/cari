import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

def hitung_akurasi(prediksi, aktual):
    benar, total = 0, 0
    for i in range(len(aktual)):
        actual = f"{int(aktual[i]):04d}"
        for j in range(4):
            if int(actual[j]) in prediksi[j]:
                benar += 1
            total += 1
    return benar / total * 100 if total else 0

def tampilkan_heatmap(prediksi_digit, aktual_digit):
    matrix = np.zeros((10, 10))
    for pred, act in zip(prediksi_digit, aktual_digit):
        matrix[int(act)][int(pred)] += 1

    plt.figure(figsize=(6, 4))
    sns.heatmap(matrix, annot=True, fmt="g", cmap="YlGnBu", xticklabels=range(10), yticklabels=range(10))
    plt.xlabel("Prediksi")
    plt.ylabel("Aktual")
    st.pyplot(plt)
