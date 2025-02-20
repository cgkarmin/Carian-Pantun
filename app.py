import streamlit as st
import pandas as pd

# --- SETUP ---
st.set_page_config(page_title="Carian Pantun Berguna", layout="centered")

# --- HEADER ---
st.markdown("<h1 style='text-align: center;'>📜 Carian Pantun Berguna</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Sebuah carian pantun berguna yang boleh digunakan dalam acara dan majlis.</p>", unsafe_allow_html=True)

# --- LOAD DATA ---
@st.cache_data
def load_data():
    return pd.read_csv("Data_Pantun_Dikemas_Kini.csv")  # Pastikan fail ini ada

df = load_data()

# --- CARI PANTUN BERDASARKAN KATA KUNCI ---
st.markdown("### 🔎 Cari Pantun Berdasarkan Kata Kunci:")
search_query = st.text_input("Masukkan kata kunci:", "")

if search_query:
    df_filtered = df[df["Pantun"].str.contains(search_query, case=False, na=False)]
    if not df_filtered.empty:
        selected_pantun_query = st.selectbox("📜 Pilih Pantun:", df_filtered["Pantun"].tolist(), key="pantun_cari")
        
        # Kotak teks tidak perlu, gantikan dengan butang Salin
        if st.button("📋 Salin Pantun"):
            st.markdown(f"""
                <script>
                function copyToClipboard(text) {{
                    navigator.clipboard.writeText(text).then(() => {{
                        alert("✅ Pantun berjaya disalin!");
                    }});
                }}
                copyToClipboard("{selected_pantun_query}");
                </script>
                """, unsafe_allow_html=True)

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

        # Butang Salin untuk kategori
        if st.button("📋 Salin Pantun Kategori"):
            st.markdown(f"""
                <script>
                function copyToClipboard(text) {{
                    navigator.clipboard.writeText(text).then(() => {{
                        alert("✅ Pantun berjaya disalin!");
                    }});
                }}
                copyToClipboard("{pantun_kategori}");
                </script>
                """, unsafe_allow_html=True)

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
