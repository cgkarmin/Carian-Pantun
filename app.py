import streamlit as st
import pandas as pd
import pyperclip

# --- SETUP ---
st.set_page_config(page_title="Carian Pantun Berguna", layout="centered")

# --- HEADER ---
st.title("📜 Carian Pantun Berguna")
st.markdown("Sebuah carian pantun berguna yang boleh digunakan dalam acara dan majlis.")

# --- LOAD DATA ---
@st.cache_data
def load_data():
    return pd.read_csv("Data_Pantun_Dikemas_Kini.csv")  # Pastikan fail ini ada

df = load_data()

# --- CARI PANTUN BERDASARKAN KATA KUNCI ---
st.subheader("🔎 Cari Pantun Berdasarkan Kata Kunci:")
search_query = st.text_input("Masukkan kata kunci:", "")

if search_query:
    df_filtered = df[df["Pantun"].str.contains(search_query, case=False, na=False)]
    if not df_filtered.empty:
        selected_pantun_query = st.selectbox("📜 Pilih Pantun:", df_filtered["Pantun"].tolist(), key="pantun_cari")
        if st.button("📋 Salin Pantun", key="salin_query"):
            pyperclip.copy(selected_pantun_query)
            st.success("✅ Pantun berjaya disalin! Tekan **CTRL + V** untuk tampal.")
    else:
        st.warning("⚠️ Tiada pantun dijumpai untuk kata kunci tersebut.")

st.markdown("---")

# --- CARI PANTUN BERDASARKAN KATEGORI ---
st.subheader("📂 Cari Pantun Berdasarkan Kategori:")
kategori = st.selectbox("📌 Pilih Kategori:", ["Pilih"] + df.columns[1:].tolist(), key="kategori_select")

if kategori != "Pilih":
    pilihan_list = df[kategori].dropna().unique().tolist()
    pilihan = st.selectbox(f"🎯 **Pilih nilai untuk '{kategori}':**", pilihan_list, key="pilihan")
    
    filtered_df = df[df[kategori] == pilihan]
    if not filtered_df.empty:
        pantun_kategori = st.selectbox("📜 Pilih Pantun:", filtered_df["Pantun"].tolist(), key="pantun_kategori")
        if st.button("📋 Salin Pantun", key="salin_kategori"):
            pyperclip.copy(pantun_kategori)
            st.success("✅ Pantun berjaya disalin! Tekan **CTRL + V** untuk tampal.")
    else:
        st.warning("⚠️ Tiada pantun dijumpai untuk pilihan ini.")

st.markdown("---")

# --- FOOTER ---
st.markdown(
    """
    <div style="text-align: center; font-size: 12px; color: gray;">
    © 2008-2025 Carian Pantun Berguna. v2. 2008-2025. 
    Sebuah carian pantun berguna yang boleh digunakan dalam acara dan majlis.
    </div>
    """,
    unsafe_allow_html=True
)
