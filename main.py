import requests
import streamlit as st
from tenacity import retry, wait_fixed, stop_after_attempt

# Lista de servidores para verificar
SERVERS = {
    "Celestrak": "https://celestrak.com/NORAD/elements/gp.php?CATNR=25544&FORMAT=csv",
    "teste": "https://www.stats.govt.nz/large-datasets/csv-files-for-download/",
    "Spacetrak": "https://spacetrak.org/data/example.csv",  # Substitua pela URL correta do Spacetrak
    # Adicione mais servidores aqui
}

# Função para verificar a disponibilidade de um servidor
@retry(wait=wait_fixed(2), stop=stop_after_attempt(3))  # Tenta 3 vezes, com 2 segundos de espera entre tentativas
def check_server_availability(name, url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Verifica se a resposta é válida (status code 200)
        return True, f"{name} está online e respondendo."
    except requests.exceptions.RequestException as e:
        return False, f"{name} está offline ou não respondeu. Erro: {e}"

# Interface do Streamlit
st.title("Verificador de Disponibilidade de Servidores")
st.markdown("Este aplicativo verifica a disponibilidade de servidores que fornecem arquivos CSV.")

# Verifica a disponibilidade de cada servidor
for server_name, server_url in SERVERS.items():
    st.write(f"Verificando {server_name}...")
    with st.spinner(f"Conectando a {server_name}..."):
        status, message = check_server_availability(server_name, server_url)
        if status:
            st.success(message)
        else:
            st.error(message)

st.markdown("---")
st.markdown("Feito com ❤️ usando [Streamlit](https://streamlit.io/).")















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