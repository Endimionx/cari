import streamlit as st
from modules.sidebar_config import configure_sidebar
from modules.data_loader import load_data, cari_putaran_terbaik
from modules.model_management import tampilkan_manajemen_model
from modules.prediction import tampilkan_hasil_prediksi, tampilkan_kombinasi_terbaik

st.set_page_config(page_title="Prediksi Togel AI", layout="wide")
st.title("🔮 Prediksi Togel 4D - Markov, AI & Gabungan")

# User Manual (Panduan)
with st.expander("📘 Panduan Penggunaan Aplikasi"):
    st.markdown("""
    1. Pilih lokasi, hari, dan metode prediksi.
    2. Aktifkan "Cari Otomatis" untuk menentukan putaran terbaik secara otomatis.
    3. Klik "🔮 Prediksi" untuk melihat hasil prediksi top 6 digit per posisi.
    4. Lihat visualisasi confidence dan kombinasi 4D terkuat.
    """)

# Sidebar
config = configure_sidebar()

# === Pencarian Putaran Terbaik (Jika Otomatis) ===
if config['cari_otomatis']:
    st.info("🔍 Mencari putaran terbaik berdasarkan akurasi...")
    best_putaran, best_acc = cari_putaran_terbaik(
        config['lokasi'], config['hari'], config['metode'], config['max_auto_putaran'],
        config['model_type'], config['top6_markov'], config['top6_markov_order2'],
        config['top6_markov_hybrid'], config['top6_model']
    )
    st.success(f"✅ Putaran terbaik: {best_putaran} (Akurasi: {best_acc:.2f}%)")
    config['putaran'] = best_putaran

# === Ambil Data dari API ===
angka_list = load_data(config['lokasi'], config['hari'], config['putaran'])
df = None
if angka_list:
    df = st.session_state['df'] = angka_list
    with st.expander("📄 Data Angka (Hasil dari API)"):
        st.dataframe({"Angka": angka_list}, use_container_width=True)
else:
    st.warning("⚠️ Data tidak tersedia untuk lokasi dan hari tersebut.")

# === Manajemen Model ===
if config["metode"] in ["LSTM AI", "Ensemble AI + Markov"]:
    tampilkan_manajemen_model(config['lokasi'], config['model_type'])

# === Prediksi dan Visualisasi ===
if st.button("🔮 Prediksi") and df:
    result, probs = config['predict'](df, config)

    with st.expander("🎯 Hasil Prediksi Angka Top-6"):
        tampilkan_hasil_prediksi(result, probs)

    tampilkan_kombinasi_terbaik(result, probs)
