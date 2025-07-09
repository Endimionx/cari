import os
import streamlit as st

def tampilkan_manajemen_model(selected_lokasi, model_type):
    with st.expander("⚙️ Manajemen Model"):
        for i in range(4):  # 0 = ribuan, 1 = ratusan, dst.
            model_path = f"saved_models/{selected_lokasi.lower().replace(' ', '_')}_digit{i}_{model_type}.h5"
            col1, col2 = st.columns([2, 1])
            with col1:
                if os.path.exists(model_path):
                    st.info(f"📂 Model Digit-{i} tersedia ({model_type}).")
                else:
                    st.warning(f"⚠️ Model Digit-{i} belum tersedia.")
            with col2:
                if os.path.exists(model_path):
                    if st.button(f"🗑 Hapus Digit-{i}", key=f"hapus_digit_{i}"):
                        os.remove(model_path)
                        st.success(f"✅ Model Digit-{i} dihapus.")

        if st.button("📚 Latih & Simpan Semua Model"):
            if "df" not in st.session_state or not st.session_state["df"]:
                st.warning("⚠️ Data belum tersedia untuk pelatihan.")
                return
            with st.spinner(f"🔄 Melatih semua model per digit ({model_type})..."):
                from modules.ai_model import train_and_save_model
                train_and_save_model(st.session_state['df'], selected_lokasi, model_type=model_type)
            st.success("✅ Semua model berhasil dilatih dan disimpan.")
