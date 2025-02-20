import streamlit as st
import pandas as pd

# ========== 💾 MEMBACA DATA ==========
file_path = "Data_Pantun_Dikemas_Kini.csv"  # Pastikan fail ini ada dalam repo GitHub
df = pd.read_csv(file_path, encoding="utf-8")

# ========== 🔄 PEMBERSIHAN DATA ==========
df.replace(["X", "x", "Tidak", "No"], "❌", inplace=True)
df.replace(["Ya", "Yes"], "✅", inplace=True)
df.fillna("Tidak Ada Data", inplace=True)

# ========== 🎨 GAYA PAPARAN STREAMLIT ==========
st.set_page_config(
    page_title="Carian Pantun",
    page_icon="📖",
    layout="wide"
)

# ========== 🏆 TAJUK UTAMA ==========
st.markdown("<h1 style='text-align: center; color: darkblue;'>🔍 Carian Pantun Interaktif</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: grey;'>Cari pantun berdasarkan kategori atau kata kunci</h4>", unsafe_allow_html=True)

# ========== 🔎 CARI PANTUN BERDASARKAN KATA KUNCI ==========
st.markdown("### 🔍 Carian Berdasarkan Kata Kunci")
search_query = st.text_input("Masukkan kata kunci pantun:", key="search_query")

if search_query:
    df_filtered = df[df["Pantun"].str.contains(search_query, case=False, na=False)]
    st.write(f"### Hasil carian untuk: '{search_query}'")
    st.dataframe(df_filtered, height=400, use_container_width=True)
    
    if not df_filtered.empty:
        selected_pantun_query = df_filtered.iloc[0]["Pantun"]  
        
        st.markdown("### ✨ Pantun dari Hasil Carian:")
        st.text_area("📖 Pantun:", selected_pantun_query, height=100, key="selected_pantun_query")

        # Gunakan JavaScript untuk menyalin teks
        copy_js = f"""
        <script>
        function copyToClipboard(text) {{
            navigator.clipboard.writeText(text).then(function() {{
                alert("✅ Pantun berjaya disalin!");
            }}, function(err) {{
                alert("❌ Gagal menyalin pantun.");
            }});
        }}
        </script>
        <button onclick="copyToClipboard(`{selected_pantun_query}`)" style="
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px 20px;
            font-size: 16px;
            cursor: pointer;
            border-radius: 5px;">
            📋 Salin Pantun
        </button>
        """
        st.markdown(copy_js, unsafe_allow_html=True)

    st.markdown("---")

# ========== 🎛️ PILIHAN DROPDOWN ==========
st.markdown("### 🎯 Carian Berdasarkan Kategori")

kategori_list = [
    "Kosong tanpa kategori",  # Pilihan "Home"
    "Semua",  # Paparkan semua pantun dalam data
    "Penulis", "Tema", "Jenis", "Makna", "Situasi Penggunaan", 
    "Situasi Formal", "Situasi Santai", "Situasi Kehidupan",
    "Acara/Majlis", "Acara Keagamaan", "Acara Sosial", "Acara Pendidikan"
]

kategori = st.selectbox(
    "📌 **Pilih kategori pencarian:**",
    kategori_list,
    key="kategori"
)

# ========== 📊 PAPARAN HASIL ==========
if kategori == "Kosong tanpa kategori":
    st.info("🔹 Sila pilih kategori untuk melihat hasil.")

elif kategori == "Semua":
    st.markdown("### ✅ Menunjukkan semua pantun dalam data:")
    st.dataframe(df, height=400, use_container_width=True)

else:
    pilihan_list = sorted(df[kategori].dropna().unique()) if kategori in df.columns else ["Tidak Ada Data"]
    pilihan = st.selectbox(
        f"🎯 **Pilih nilai untuk '{kategori}':**",
        pilihan_list,
        key="pilihan"
    )

    filtered_df = df[df[kategori] == pilihan]
    st.markdown(f"<h3 style='color: darkgreen;'>✅ Menunjukkan hasil untuk: {kategori} = {pilihan}</h3>", unsafe_allow_html=True)
    selected_row = st.data_editor(filtered_df, height=400, use_container_width=True, key="pantun_table")

    if selected_row is not None and not selected_row.empty:
        selected_pantun_text = selected_row.iloc[0]["Pantun"]

        st.markdown("### ✨ Pantun Yang Dipilih:")
        st.text_area("📖 Pantun:", selected_pantun_text, height=100, key="selected_pantun")

        copy_js_pantun = f"""
        <script>
        function copyToClipboard(text) {{
            navigator.clipboard.writeText(text).then(function() {{
                alert("✅ Pantun berjaya disalin!");
            }}, function(err) {{
                alert("❌ Gagal menyalin pantun.");
            }});
        }}
        </script>
        <button onclick="copyToClipboard(`{selected_pantun_text}`)" style="
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px 20px;
            font-size: 16px;
            cursor: pointer;
            border-radius: 5px;">
            📋 Salin Pantun
        </button>
        """
        st.markdown(copy_js_pantun, unsafe_allow_html=True)

# ========== 🔄 BUTANG RESET ==========
st.markdown("---")
if st.button("🔄 Reset Pilihan"):
    keys_to_reset = ["search_query", "kategori", "pilihan", "selected_pantun", "selected_pantun_query"]

    for key in keys_to_reset:
        if key in st.session_state:
            del st.session_state[key]

    st.session_state["kategori"] = "Kosong tanpa kategori"  # Kembali ke 'Home'
    st.rerun()
