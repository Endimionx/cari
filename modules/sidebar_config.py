import streamlit as st
from modules.lokasi_list import lokasi_list


def configure_sidebar():
    lokasi = st.selectbox("Lokasi", lokasi_list)
    hari = st.selectbox("Hari", ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"])
    metode = st.selectbox("Metode Prediksi", ["Markov", "Markov Order-2", "LSTM AI", "Ensemble AI + Markov"])

    model_type = None
    if metode in ["LSTM AI", "Ensemble AI + Markov"]:
        model_type = st.selectbox("Pilih Model AI", ["LSTM", "Transformer"])

    cari_otomatis = st.checkbox("Cari Putaran Terbaik Otomatis")
    max_auto_putaran = st.number_input("Jumlah Maksimal Putaran", min_value=50, max_value=1000, step=50, value=200)
    putaran = st.number_input("Jumlah Putaran (jika tidak otomatis)", min_value=50, max_value=1000, step=50, value=200)

    return {
        "lokasi": lokasi,
        "hari": hari,
        "metode": metode,
        "model_type": model_type,
        "cari_otomatis": cari_otomatis,
        "max_auto_putaran": max_auto_putaran,
        "putaran": putaran,
        "top6_markov": lambda df: [[0,1,2,3,4,5]] * 4,
        "top6_markov_order2": lambda df: [[5,4,3,2,1,0]] * 4,
        "top6_markov_hybrid": lambda df: [[0,2,4,6,8,1]] * 4,
        "top6_model": lambda df, lokasi, model_type: ([[0,1,2,3,4,5]] * 4),
        "predict": lambda df, config: (
            [[0,1,2,3,4,5]] * 4, [[0.2,0.2,0.2,0.2,0.1,0.1]] * 4
        ),
  }
