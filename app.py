import streamlit as st
import pandas as pd
import os

# ========== 📌 WAJIB: Set Page Config ==========
st.set_page_config(
    page_title="Carian Pantun",
    page_icon="📖",
    layout="wide"
)

# ========== 🔍 DEBUGGING ==========
st.write("✅ Aplikasi berjaya dimuatkan!")  
st.write("📂 Lokasi kerja semasa:", os.getcwd())  

# ========== 💾 MEMBACA DATA ==========
file_path = "Data_Pantun_Dikemas_Kini.csv"

if os.path.exists(file_path):
    df = pd.read_csv(file_path, encoding="utf-8")
    st.write("✅ CSV berjaya dimuatkan!")  
    st.dataframe(df.head())  
else:
    st.error("❌ Gagal menemui fail CSV! Pastikan nama fail betul dalam repo GitHub.")
    st.stop()

# ========== 🏆 TAJUK UTAMA ==========
st.markdown("<h1 style='text-align: center; color: darkblue;'>🔍 Carian Pantun Interaktif</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: grey;'>Cari pantun berdasarkan kategori atau kata kunci</h4>", unsafe_allow_html=True)

# ========== 🔎 CARI PANTUN BERDASARKAN KATA KUNCI ==========
st.write("📌 Debug: Memaparkan kotak carian...")
search_query = st.text_input("Masukkan kata kunci pantun:", key="search_query")

if search_query:
    df_filtered = df[df["Pantun"].str.contains(search_query, case=False, na=False)]
    st.write(f"### Hasil carian untuk: '{search_query}'")
    st.dataframe(df_filtered, height=400, use_container_width=True)

    if not df_filtered.empty:
        selected_pantun_query = df_filtered.iloc[0]["Pantun"]  
        st.markdown("### ✨ Pantun dari Hasil Carian:")
        st.text_area("📖 Pantun:", selected_pantun_query, height=100, key="selected_pantun_query")

# ========== 🎛️ PILIHAN DROPDOWN ==========
st.write("📌 Debug: Memaparkan dropdown kategori...")
kategori_list = [
    "Kosong tanpa kategori",
    "Semua",
    "Penulis", "Tema", "Jenis", "Makna", "Situasi Penggunaan", 
    "Situasi Formal", "Situasi Santai", "Situasi Kehidupan",
    "Acara/Majlis", "Acara Keagamaan", "Acara Sosial", "Acara Pendidikan"
]

kategori = st.selectbox(
    "📌 **Pilih kategori pencarian:**",
    kategori_list,
    key="kategori"
)

if kategori == "Kosong tanpa kategori":
    st.info("🔹 Sila pilih kategori untuk melihat hasil.")

elif kategori == "Semua":
    st.markdown("### ✅ Menunjukkan semua pantun dalam data:")
    st.dataframe(df, height=400, use_container_width=True)

else:
    st.write(f"📌 Debug: Memproses kategori {kategori}...")
    pilihan_list = sorted(df[kategori].dropna().unique()) if kategori in df.columns else ["Tidak Ada Data"]
    pilihan = st.selectbox(
        f"🎯 **Pilih nilai untuk '{kategori}':**",
        pilihan_list,
        key="pilihan"
    )

    filtered_df = df[df[kategori] == pilihan]
    st.markdown(f"<h3 style='color: darkgreen;'>✅ Menunjukkan hasil untuk: {kategori} = {pilihan}</h3>", unsafe_allow_html=True)
    st.dataframe(filtered_df, height=400, use_container_width=True)

# ========== 🔄 BUTANG RESET ==========
st.markdown("---")
if st.button("🔄 Reset Pilihan"):
    st.write("📌 Debug: Reset ditekan!")
    keys_to_reset = ["search_query", "kategori", "pilihan", "selected_pantun_query"]
    for key in keys_to_reset:
        if key in st.session_state:
            del st.session_state[key]
    st.session_state["kategori"] = "Kosong tanpa kategori"  
    st.rerun()

# ========== 🔚 PENGESAHAN AKHIR ==========
st.write("✅ Debug: Kod berjaya sampai ke penghujung!")  
