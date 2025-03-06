"""
Creator: Francisval Guedes Soares
Date: 2021
"""

import streamlit as st
import pandas as pd

import requests
from io import StringIO


def load_original_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return pd.read_csv(StringIO(response.text))
    else:
        st.error("Failed to load data from Celestrak.")
        return None
    
def main():
    norad_id = norad_id = st.number_input('Unique NORAD_CAT_ID', 0, 999999,value= 25544, format="%d")        
    urlCelestrak = 'https://celestrak.org/NORAD/elements/gp.php?CATNR='+ str(norad_id) +'&FORMAT=csv'

    st.write('spacetrak')
    elem_df = load_original_data(urlCelestrak)
    # elem_df = pd.read_csv(urlCelestrak)
    st.dataframe(elem_df)


if __name__== '__main__':
    main()