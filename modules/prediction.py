import streamlit as st
import pandas as pd

def tampilkan_hasil_prediksi(result, probs):
    with st.expander("🎯 Hasil Prediksi Top 6 Digit"):
        col1, col2 = st.columns(2)
        for i, label in enumerate(["Ribuan", "Ratusan", "Puluhan", "Satuan"]):
            with (col1 if i % 2 == 0 else col2):
                st.markdown(f"**{label}:** {', '.join(map(str, result[i]))}")

    if probs:
        with st.expander("📊 Confidence Bar per Digit"):
            for i, label in enumerate(["Ribuan", "Ratusan", "Puluhan", "Satuan"]):
                st.markdown(f"**🔢 {label}**")
                digit_data = pd.DataFrame({
                    "Digit": [str(d) for d in result[i]],
                    "Confidence": probs[i]
                }).sort_values(by="Confidence", ascending=True)
                st.bar_chart(digit_data.set_index("Digit"))

def tampilkan_kombinasi_terbaik(result, probs, top_n=10, power=1.0):
    kombinasi_list = []
    for i0, d0 in enumerate(result[0]):
        for i1, d1 in enumerate(result[1]):
            for i2, d2 in enumerate(result[2]):
                for i3, d3 in enumerate(result[3]):
                    score = (
                        (probs[0][i0] ** power) *
                        (probs[1][i1] ** power) *
                        (probs[2][i2] ** power) *
                        (probs[3][i3] ** power)
                    )
                    angka = f"{d0}{d1}{d2}{d3}"
                    kombinasi_list.append((angka, score))

    kombinasi_list.sort(key=lambda x: x[1], reverse=True)
    top_kombinasi = kombinasi_list[:top_n]

    with st.expander("💡 Simulasi Kombinasi 4D Terbaik"):
        col1, col2 = st.columns(2)
        for i, (komb, score) in enumerate(top_kombinasi):
            with (col1 if i % 2 == 0 else col2):
                st.markdown(f"`{komb}` - ⚡️ Confidence: `{score:.4f}`")
