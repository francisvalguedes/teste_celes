"""
Creator: Francisval Guedes Soares
Date: 2021
"""

import streamlit as st
import pandas as pd

import requests
from io import StringIO
# import datetime
from datetime import datetime, timezone
import os
from glob import glob

def _(text):
    return text

def get_celestrack_oe():
    norad_id = st.number_input(_('Select the NORAD_CAT_ID of the space object to obtain orbital elements:'), 0, 999999, value=25544, format="%d")
    current_day = datetime.now(timezone.utc).strftime('%Y_%m_%d_')
    celet_fil_n = 'data/celestrak/' + current_day + str(norad_id) + '.csv'
    
    if not os.path.exists(celet_fil_n):                
        urlCelestrak = 'https://celestrak.org/NORAD/elements/gp.php?CATNR=' + str(norad_id) + '&FORMAT=csv'
        try:
            elem_df = pd.read_csv(urlCelestrak) 
            if 'MEAN_MOTION' in elem_df.columns.to_list():
                elem_df.to_csv(celet_fil_n, index=False)                     
            else:
                st.error(_('No orbital elements for this object in Celestrak'))
                st.stop()
        except OSError as e:
            st.error(_('Celestrak error, use Space-Track or load orbital elements manually'))
            st.stop()
    else:        
        elem_df = pd.read_csv(celet_fil_n)  
    return elem_df


def load_original_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return pd.read_csv(StringIO(response.text))
    else:
        st.error("Failed to load data from Celestrak.")
        return None
    
def main():
    # norad_id = norad_id = st.number_input('Unique NORAD_CAT_ID', 0, 999999,value= 25544, format="%d")        
    # urlCelestrak = 'https://celestrak.org/NORAD/elements/gp.php?CATNR='+ str(norad_id) +'&FORMAT=csv'

    # st.write('spacetrak')
    # elem_df = load_original_data(urlCelestrak)
    # # elem_df = pd.read_csv(urlCelestrak)
    elem_df = get_celestrack_oe()
    st.dataframe(elem_df)

    arquivos = glob('data/celestrak/*.csv') # Para listar somente .txt altere para "*.txt"
    for arquivo in arquivos:
        st.write(arquivo)


if __name__== '__main__':
    main()