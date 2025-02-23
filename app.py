import streamlit as st
import pandas as pd

# ✅ Konfigurasi halaman
st.set_page_config(page_title="Carian Pantun Berguna", layout="centered")

# ✅ URL CSV dari GitHub (PASTIKAN GUNA PAUTAN RAW)
csv_url = "https://raw.githubusercontent.com/cgkarmin/Carian-Pantun/main/Data_Pantun_Dikemas_Kini.csv"

# ✅ Fungsi untuk memuatkan data pantun dari GitHub
@st.cache_data
def load_data(url):
    try:
        df = pd.read_csv(url, encoding='utf-8')
        return df
    except Exception as e:
        st.error(f"❌ Ralat membaca fail CSV dari GitHub: {e}")
        return pd.DataFrame()

# ✅ Muatkan DataFrame pantun
df = load_data(csv_url)

# ✅ Tajuk utama
st.markdown("<h1 style='text-align: center;'>📜 Carian Pantun Berguna</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Sebuah carian pantun berguna yang boleh digunakan dalam acara dan majlis.</p>", unsafe_allow_html=True)

# ✅ Jika CSV berjaya dimuatkan, papar carian
if not df.empty:
    # --- CARI PANTUN BERDASARKAN KATA KUNCI ---
    st.markdown("### 🔎 Cari Pantun Berdasarkan Kata Kunci:")
    search_query = st.text_input("Masukkan kata kunci:", "")

    if search_query:
        df_filtered = df[df["Pantun"].str.contains(search_query, case=False, na=False)]
        if not df_filtered.empty:
            selected_pantun_query = st.selectbox("📜 Pilih Pantun:", df_filtered["Pantun"].tolist(), key="pantun_cari")

            # ✅ Paparkan pantun dalam format 4 baris
            st.markdown("### 📋 Salin Pantun:")
            st.text_area("", "\n".join(selected_pantun_query.splitlines()), height=120)

        else:
            st.warning("⚠️ Tiada pantun dijumpai untuk kata kunci tersebut.")

    st.markdown("---")

    # --- CARI PANTUN BERDASARKAN KATEGORI ---
    st.markdown("### 📂 Cari Pantun Berdasarkan Kategori:")
    kategori = st.selectbox("📌 Pilih Kategori:", ["Pilih"] + df.columns[1:].tolist(), key="kategori_select")

    if kategori != "Pilih":
        pilihan_list = df[kategori].dropna().unique().tolist()
        pilihan = st.selectbox(f"🎯 **Pilih nilai untuk '{kategori}':**", pilihan_list, key="pilihan")
        
        filtered_df = df[df[kategori] == pilihan]
        if not filtered_df.empty:
            pantun_kategori = st.selectbox("📜 Pilih Pantun:", filtered_df["Pantun"].tolist(), key="pantun_kategori")

            # ✅ Paparkan pantun dalam format 4 baris
            st.markdown("### 📋 Salin Pantun Kategori:")
            st.text_area("", "\n".join(pantun_kategori.splitlines()), height=120)

        else:
            st.warning("⚠️ Tiada pantun dijumpai untuk pilihan ini.")

    st.markdown("---")

else:
    st.warning("⚠ Tiada pantun tersedia untuk dipaparkan. Pastikan fail CSV di GitHub wujud dan boleh diakses.")

# ✅ Footer
st.markdown(
    """
    <div style="text-align: center; font-size: 12px; color: gray;">
    © 2008-2025 Carian Pantun Berguna. v2. 2008-2025. 
    Sebuah carian pantun berguna yang boleh digunakan dalam acara dan majlis.
    </div>
    """,
    unsafe_allow_html=True
)
