import pandas as pd
import streamlit as st
import streamlit_permalink as stp

import peptacular as pt

st.set_page_config(page_title='Element-Table', page_icon='🧰')

st.title('Element Masses 🧰')

st.markdown('Made with Made using [peptacular](https://github.com/pgarrett-scripps/peptacular): [![DOI](https://zenodo.org/badge/591504879.svg)](https://doi.org/10.5281/zenodo.15054278)', unsafe_allow_html=True)

precision = stp.slider('Precision', min_value=0, max_value=10, value=5, step=1, help='Number of decimal places to round the masses to.')

# Prepare data with precision applied
elements, ave_masses = pt.AVERAGE_ATOMIC_MASSES.keys(), pt.AVERAGE_ATOMIC_MASSES.values()
mono_masses = [round(pt.ISOTOPIC_ATOMIC_MASSES[e], precision) for e in elements]
ave_masses = [round(m, precision) for m in ave_masses]
atomic_number = [pt.ATOMIC_SYMBOL_TO_NUMBER[e] for e in elements]

df = pd.DataFrame({
    'Element': list(elements),
    'Atomic Number': atomic_number,
    'Average Mass': list(ave_masses),
    'Mono Mass': mono_masses,
})

# set index to be atomic number
df.set_index('Atomic Number', inplace=True)


# Apply precision formatting
df['Average Mass'] = df['Average Mass'].apply(lambda x: f"{x:.{precision}f}")
df['Mono Mass'] = df['Mono Mass'].apply(lambda x: f"{x:.{precision}f}")


st.table(df)