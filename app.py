import streamlit as st
import pandas as pd
import pyperclip

# ✅ Pastikan layout aplikasi
st.set_page_config(page_title="Carian Pantun", layout="wide")

# ✅ Paparkan tajuk utama
st.title("📜 Carian Pantun")

# ✅ Muatkan data pantun dari CSV
@st.cache_data
def load_data():
    return pd.read_csv("pantun.csv")  # Gantikan dengan fail sebenar

df = load_data()

# ✅ Pastikan session state mempunyai nilai awal
if "kategori" not in st.session_state:
    st.session_state["kategori"] = "Semua"

if "search_query" not in st.session_state:
    st.session_state["search_query"] = ""

if "pilihan_pantun" not in st.session_state:
    st.session_state["pilihan_pantun"] = ""

# ✅ Input carian pantun
search_query = st.text_input("🔍 Masukkan kata kunci:", st.session_state["search_query"])

# ✅ Cari pantun berdasarkan kata kunci
df_filtered = df[df["Pantun"].str.contains(search_query, case=False, na=False)]

# ✅ Paparkan jadual pantun
st.write("📋 **Senarai Pantun**")
st.dataframe(df_filtered)

# ✅ Pilihan pantun dari hasil carian
if not df_filtered.empty:
    pilihan_pantun = st.selectbox("📜 **Pilih Pantun:**", df_filtered["Pantun"].tolist(), key="pantun_cari")
    st.session_state["pilihan_pantun"] = pilihan_pantun

    # ✅ Paparkan pantun yang dipilih
    st.markdown("### ✍️ Pantun Pilihan:")
    st.code(st.session_state["pilihan_pantun"], language="")

    # ✅ Butang salin pantun
    if st.button("📋 Salin Pantun", key="salin_pantun"):
        try:
            pyperclip.copy(st.session_state["pilihan_pantun"])
            st.success("✅ Pantun berjaya disalin! Gunakan CTRL + V untuk tampal.")
        except pyperclip.PyperclipException:
            st.text_area("⚠ Tidak dapat salin automatik. Sila salin secara manual:", st.session_state["pilihan_pantun"])
else:
    st.warning("⚠ Tiada pantun yang sepadan dengan carian.")

# ✅ Pilihan kategori
st.markdown("---")
st.subheader("📌 Carian Berdasarkan Kategori")

kategori_pilihan = st.selectbox(
    "📌 **Pilih kategori pencarian:**",
    ["Semua", "Penulis", "Tema", "Jenis", "Makna", "Situasi Penggunaan",
     "Situasi Formal", "Situasi Santai", "Situasi Kehidupan",
     "Acara/Majlis", "Acara Keagamaan", "Acara Sosial", "Acara Pendidikan"],
    key="kategori_select"
)

st.session_state["kategori"] = kategori_pilihan

if kategori_pilihan != "Semua":
    if kategori_pilihan in df.columns:
        pilihan_options = sorted(df[kategori_pilihan].dropna().unique())

        if pilihan_options:
            pilihan_kategori = st.selectbox(
                f"🎯 **Pilih nilai untuk '{kategori_pilihan}':**",
                pilihan_options,
                key="pilihan_kategori_select"
            )

            filtered_df = df[df[kategori_pilihan] == pilihan_kategori]
            st.write(f"✅ Menunjukkan hasil untuk: {kategori_pilihan} = {pilihan_kategori}")
            st.dataframe(filtered_df)
        else:
            st.warning("⚠ Tiada pilihan untuk kategori ini.")
    else:
        st.error("❌ Kategori tidak wujud dalam data.")
