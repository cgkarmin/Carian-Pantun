import streamlit as st
import pandas as pd
import pyperclip

# ========== 💾 MEMBACA DATA ==========
file_path = "Data_Pantun_Dikemas_Kini.csv"
df = pd.read_csv(file_path, encoding="utf-8")

# ========== 📌 SET DEFAULT SESSION_STATE ==========
if "search_query" not in st.session_state:
    st.session_state["search_query"] = ""

if "kategori" not in st.session_state:
    st.session_state["kategori"] = "Semua"

if "pilihan_kategori" not in st.session_state:
    st.session_state["pilihan_kategori"] = None

if "pantun_cari" not in st.session_state:
    st.session_state["pantun_cari"] = None

if "pantun_kategori" not in st.session_state:
    st.session_state["pantun_kategori"] = None

# ========== 🎨 GAYA PAPARAN STREAMLIT ==========
st.set_page_config(
    page_title="Carian Pantun",
    page_icon="📖",
    layout="wide"
)

# ========== 🏆 TAJUK UTAMA ==========
st.markdown("<h1 style='text-align: center; color: darkblue;'>🔍 Carian Pantun Interaktif</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: grey;'>Cari pantun berdasarkan kategori atau kata kunci</h4>", unsafe_allow_html=True)

# ========== 🖥️ PAPAR DATA PENUH ==========
st.markdown("### 📌 Data Penuh:")
st.dataframe(df, height=400, use_container_width=True)

# ========== 🔎 CARI PANTUN BERDASARKAN KATA KUNCI ==========
st.markdown("---")
search_input = st.text_input("🔍 **Cari pantun berdasarkan kata kunci:**", st.session_state["search_query"], key="search_bar")

if search_input:
    df_filtered = df[df["Pantun"].str.contains(search_input, case=False, na=False)]
    st.write(f"### Hasil carian untuk: '{search_input}'")

    if not df_filtered.empty:
        pantun_cari = st.selectbox("📜 **Pilih Pantun:**", df_filtered["Pantun"].tolist(), key="pantun_cari_select")
        st.markdown(f"### ✍️ Pantun Pilihan:\n\n📜 {pantun_cari}")

        if st.button("📋 Salin Pantun", key="salin_kata_kunci"):
            pyperclip.copy(pantun_cari)
            st.success("✅ Pantun berjaya disalin! Tekan CTRL + V untuk tampal.")

st.markdown("---")

# ========== 🎛️ PILIHAN DROPDOWN ==========
st.markdown("### 🎯 Carian Berdasarkan Kategori")

col1, col2 = st.columns(2)

with col1:
    kategori_pilihan = st.selectbox(
        "📌 **Pilih kategori pencarian:**",
        ["Semua", "Penulis", "Tema", "Jenis", "Makna", "Situasi Penggunaan",
         "Situasi Formal", "Situasi Santai", "Situasi Kehidupan",
         "Acara/Majlis", "Acara Keagamaan", "Acara Sosial", "Acara Pendidikan"],
        index=0 if st.session_state["kategori"] == "Semua" else None,
        key="kategori_select"
    )

if kategori_pilihan != "Semua":
    with col2:
        pilihan_options = sorted(df[kategori_pilihan].dropna().unique())
        pilihan_kategori = st.selectbox(
            f"🎯 **Pilih nilai untuk '{kategori_pilihan}':**",
            pilihan_options,
            key="pilihan_kategori_select"
        )

    filtered_df = df[df[kategori_pilihan] == pilihan_kategori]
    st.markdown(f"<h3 style='color: darkgreen;'>✅ Menunjukkan hasil untuk: {kategori_pilihan} = {pilihan_kategori}</h3>", unsafe_allow_html=True)

    if not filtered_df.empty:
        pantun_kategori = st.selectbox("📜 **Pilih Pantun:**", filtered_df["Pantun"].tolist(), key="pantun_kategori_select")
        st.markdown(f"### ✍️ Pantun Pilihan:\n\n📜 {pantun_kategori}")

        if st.button("📋 Salin Pantun", key="salin_kategori"):
            pyperclip.copy(pantun_kategori)
            st.success("✅ Pantun berjaya disalin! Tekan CTRL + V untuk tampal.")

st.markdown("---")
