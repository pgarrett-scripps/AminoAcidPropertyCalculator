import peptacular as pt
import streamlit as st
import pandas as pd

st.set_page_config(page_title='Protease-Regexes', page_icon='🧰')

st.title('Protease Regexes 🧰')
st.markdown('Made with Made using [peptacular](https://github.com/pgarrett-scripps/peptacular): [![DOI](https://zenodo.org/badge/591504879.svg)](https://doi.org/10.5281/zenodo.15054278)', unsafe_allow_html=True)

# Convert protease dictionary into a DataFrame
regexes: dict[str, str] = pt.PROTEASES
df = pd.DataFrame(list(regexes.items()), columns=["Protease", "Regex"])

# Display as a table
st.table(df)
