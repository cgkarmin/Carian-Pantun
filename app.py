import os
import pandas as pd
import streamlit as st
import pyperclip

# ---------------------- Pemuatan Data ----------------------
# Gunakan nama fail yang betul
file_path = os.path.join(os.path.dirname(__file__), "Data_Pantun_Dikemas_Kini.csv")

# Periksa jika fail wujud
if not os.path.exists(file_path):
    st.error("❌ Fail 'Data_Pantun_Dikemas_Kini.csv' tidak dijumpai. Sila muat naik fail ke dalam direktori projek.")
    st.stop()

@st.cache_data
def load_data():
    return pd.read_csv(file_path)

df = load_data()

# ---------------------- UI Streamlit ----------------------
st.set_page_config(page_title="📜 Carian Pantun", layout="wide")
st.title("📜 Carian Pantun")

# ---------------------- Carian Kata Kunci ----------------------
st.subheader("🔍 Carian Berdasarkan Kata Kunci")
search_query = st.text_input("Masukkan kata kunci:", key="search_query")

if search_query:
    df_filtered = df[df.apply(lambda row: search_query.lower() in row.to_string().lower(), axis=1)]
else:
    df_filtered = df.copy()

if df_filtered.empty:
    st.warning("⚠️ Tiada pantun yang sepadan dengan kata kunci anda.")
else:
    selected_pantun_query = st.selectbox("📜 **Pilih Pantun:**", df_filtered["Pantun"].tolist(), key="pantun_cari")
    st.markdown(f"### ✍️ Pantun Pilihan:\n\n📜 {selected_pantun_query}")

    if st.button("📋 Salin Pantun", key="salin_carian"):
        pyperclip.copy(selected_pantun_query)
        st.success("✅ Pantun berjaya disalin! Tekan **CTRL + V** untuk tampal.")

st.markdown("---")

# ---------------------- Carian Berdasarkan Kategori ----------------------
st.subheader("🎯 Carian Berdasarkan Kategori")
kategori_list = ["Pilih kategori"] + [col for col in df.columns if col != "Pantun"]
kategori = st.selectbox("📌 Pilih kategori pencarian:", kategori_list, key="kategori_select")

if kategori and kategori != "Pilih kategori":
    pilihan_list = ["Pilih nilai"] + sorted(df[kategori].dropna().unique().tolist())
    pilihan = st.selectbox(f"🎯 **Pilih nilai untuk '{kategori}':**", pilihan_list, key="pilihan")

    if pilihan and pilihan != "Pilih nilai":
        filtered_df = df[df[kategori] == pilihan]
        pantun_kategori = st.selectbox("📜 **Pilih Pantun:**", filtered_df["Pantun"].tolist(), key="pantun_kategori")
        st.markdown(f"### ✍️ Pantun Pilihan:\n\n📜 {pantun_kategori}")

        if st.button("📋 Salin Pantun", key="salin_kategori"):
            pyperclip.copy(pantun_kategori)
            st.success("✅ Pantun berjaya disalin! Tekan **CTRL + V** untuk tampal.")

st.markdown("---")

# ---------------------- Penutup ----------------------
st.info("🔄 Untuk reset semua pilihan, sila **refresh** halaman ini.")
st.success("✅ Aplikasi berjaya dimuatkan!")
