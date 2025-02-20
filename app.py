import streamlit as st
import pandas as pd

# 📂 Muatkan Data
@st.cache_data
def load_data():
    return pd.read_csv("Data_Pantun_Dikemas_Kini.csv")  # Pastikan fail betul

df = load_data()

# 🔍 Carian Pantun
search_query = st.text_input("🔍 Cari pantun berdasarkan kata kunci:", "")

if search_query:
    df_filtered = df[df["Pantun"].str.contains(search_query, case=False, na=False)]
    if not df_filtered.empty:
        selected_pantun_query = st.selectbox("📜 **Pilih Pantun:**", df_filtered["Pantun"].tolist(), key="pantun_cari")
        st.markdown("### ✍️ Pantun Pilihan:")
        st.code(selected_pantun_query, language="")

    else:
        st.warning("❌ Tiada pantun yang sepadan!")

# 🎯 Carian Berdasarkan Kategori
kategori = st.selectbox("📌 Pilih kategori pencarian:", ["Semua"] + list(df.columns[1:]), key="kategori_select")

if kategori != "Semua":
    pilihan_list = df[kategori].dropna().unique().tolist()
    pilihan = st.selectbox(f"🎯 **Pilih nilai untuk '{kategori}':**", pilihan_list, key="pilihan")

    if pilihan:
        filtered_df = df[df[kategori] == pilihan]
        if not filtered_df.empty:
            pantun_kategori = st.selectbox("📜 **Pilih Pantun:**", filtered_df["Pantun"].tolist(), key="pantun_kategori")
            st.markdown("### ✍️ Pantun Pilihan:")
            st.code(pantun_kategori, language="")
        else:
            st.warning("❌ Tiada pantun dalam kategori ini!")

st.markdown("---")
st.info("🔄 Untuk reset semua, **refresh halaman ini (F5 / CTRL + R)**.")
