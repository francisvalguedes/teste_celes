import requests
import streamlit as st
from tenacity import retry, wait_fixed, stop_after_attempt

import io
import json
import xml.etree.ElementTree as ET

import httpx

def _segments_from_query(url):
    response = httpx.get(url)
    response.raise_for_status()

    if response.text == "No GP data found":
        raise ValueError(
            f"Query '{url}' did not return any results, try a different one"
        )
    tree = ET.parse(io.StringIO(response.text))
    root = tree.getroot()

    return response.text


# Interface do Streamlit
st.title("Verificador de Disponibilidade de Servidores")
st.markdown("Este aplicativo verifica a disponibilidade de servidores que fornecem arquivos CSV.")

# Campo de texto para inserir o endereço do servidor
server_url = st.text_input(
    "Insira o endereço do servidor (URL):",
    placeholder="Ex: https://celestrak.com/NORAD/elements/gp.php?CATNR=25544&FORMAT=csv"
)

# Botão para verificar o servidor
if st.button("Verificar Servidor"):
    if server_url:
        st.write(f"Verificando o servidor em {server_url}...")
        with st.spinner("Conectando ao servidor..."):
            message = _segments_from_query(server_url)
            st.write(message)
    else:
        st.warning("Por favor, insira um endereço de servidor válido.")

st.markdown("---")
st.markdown("Feito com ❤️ usando [Streamlit](https://streamlit.io/).")


# https://celestrak.com/NORAD/elements/gp.php?CATNR=25544&FORMAT=csv

# import requests
# import streamlit as st
# import time
# from tenacity import retry, wait_fixed, stop_after_attempt

# @retry(wait=wait_fixed(2), stop=stop_after_attempt(3))  # Tenta 3 vezes, com 2 segundos de espera entre tentativas
# def download_csv(norad_id):
#     url = f"https://celestrak.com/NORAD/elements/gp.php?CATNR={norad_id}&FORMAT=csv"
#     try:
#         response = requests.get(url, timeout=30)  # Timeout aumentado para 30 segundos
#         response.raise_for_status()
#         return response.content
#     except requests.exceptions.RequestException as e:
#         st.error(f"Erro ao baixar o arquivo CSV: {e}")
#         raise e

# def check_server_availability():
#     try:
#         response = requests.get("https://celestrak.org", timeout=10)
#         return response.status_code == 200
#     except requests.exceptions.RequestException:
#         return False

# norad_id = st.text_input("Digite o NORAD CAT ID:")
# if st.button("Baixar CSV"):
#     if not check_server_availability():
#         st.error("O servidor do Celestrak está temporariamente indisponível. Tente novamente mais tarde.")
#     else:
#         with st.spinner("Baixando..."):
#             try:
#                 csv_data = download_csv(norad_id)
#                 st.success("Download concluído!")
#                 st.download_button(
#                     label="Baixar CSV",
#                     data=csv_data,
#                     file_name=f"norad_{norad_id}.csv",
#                     mime="text/csv",
#                 )
#             except Exception as e:
#                 st.error(f"Falha ao baixar o arquivo CSV. Erro: {e}")