import streamlit as st
import pandas as pd

# Fungsi JavaScript untuk salin teks
def get_copy_js(text):
    return f"""
    <script>
    function copyToClipboard(text) {{
        navigator.clipboard.writeText(text).then(function() {{
            alert("✅ Pantun berjaya disalin!");
        }}, function(err) {{
            alert("❌ Gagal menyalin pantun.");
        }});
    }}
    </script>
    <button onclick="copyToClipboard(`{text}`)" style="
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

# ========== PAPAR PANTUN DAN BUTANG SALIN ==========
if "selected_pantun_query" in st.session_state:
    selected_pantun_text = st.session_state["selected_pantun_query"]

    st.markdown("### ✨ Pantun Yang Dipilih:")
    st.text_area("📖 Pantun:", selected_pantun_text, height=100, key="pantun_box")

    # Gunakan JavaScript untuk menyalin teks
    st.markdown(get_copy_js(selected_pantun_text), unsafe_allow_html=True)
