import requests
import streamlit as st
import time

def download_csv(norad_id):
    url = f"https://celestrak.com/NORAD/elements/gp.php?CATNR={norad_id}&FORMAT=csv"
    try:
        response = requests.get(url, timeout=10)  # Aumente o timeout se necessário
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao baixar o arquivo CSV: {e}")
        return None

norad_id = st.text_input("Digite o NORAD CAT ID:")
if st.button("Baixar CSV"):
    with st.spinner("Baixando..."):
        csv_data = download_csv(norad_id)
        if csv_data:
            st.success("Download concluído!")
            st.download_button(
                label="Baixar CSV",
                data=csv_data,
                file_name=f"norad_{norad_id}.csv",
                mime="text/csv",
            )