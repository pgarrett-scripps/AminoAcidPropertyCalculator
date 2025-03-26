import pandas as pd
import streamlit as st

import peptacular as pt

st.set_page_config(page_title='ElementMass', page_icon='🧰')

st.title('Element Mass Table 🧰')

st.caption('A table of elements with atomic numbers, average masses, and monoisotopic masses.')
st.caption('Made with [peptacular](https://pypi.org/project/peptacular/)')

elements, ave_masses = pt.AVERAGE_ATOMIC_MASSES.keys(), pt.AVERAGE_ATOMIC_MASSES.values()
mono_masses = [pt.ISOTOPIC_ATOMIC_MASSES[e] for e in elements]
atomic_number = [pt.ATOMIC_SYMBOL_TO_NUMBER[e] for e in elements]

df = pd.DataFrame({
    'Element': list(elements),
    'Atomic Number': atomic_number,
    'Average Mass': list(ave_masses),
    'Mono Mass': mono_masses,
})

# set index to be atomic number
df.set_index('Atomic Number', inplace=True)

st.table(df)