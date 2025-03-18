import streamlit as st
import pandas as pd

# Tajuk aplikasi
st.title("RAJA PRIA - Analisis Pantun")

# Input pantun
pantun = st.text_area("Masukkan pantun anda di sini:")

# Fungsi untuk membaca database CSV
@st.cache_data
def load_database():
    try:
        df = pd.read_csv("db.csv")
        return dict(zip(df["Perkataan"].str.lower(), df["Pecahan Suku Kata"]))
    except Exception as e:
        st.error(f"Ralat membaca fail database: {e}")
        return {}

suku_kata_database = load_database()

# Fungsi pecah suku kata
def pecah_suku_kata(teks):
    baris = teks.split("\n")
    hasil = []
    for index, baris_text in enumerate(baris):
        baris_text = baris_text.strip().rstrip(".,;")  # Buang tanda baca di akhir baris
        if baris_text:
            perkataan = baris_text.split()
            pecahan_baris = [suku_kata_database.get(kata.lower(), kata) for kata in perkataan]
            hasil.append(f"Baris {index + 1}: {' '.join(pecahan_baris)}")
    return hasil

# Butang periksa
if st.button("Periksa"):
    if pantun:
        hasil = pecah_suku_kata(pantun)
        st.subheader("Laporan Analisis:")
        for baris in hasil:
            st.write(baris)
    else:
        st.warning("Sila masukkan pantun terlebih dahulu!")
