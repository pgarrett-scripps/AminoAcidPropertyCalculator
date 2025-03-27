import streamlit as st
import streamlit_permalink as stp
import peptacular as pt

from util import write_subscripted_ion_markdown

st.set_page_config(layout="centered", page_title='Formula-Calc', page_icon='🧰')


with st.container():
    st.title('Chemical Formula Calculator 🧰')

    st.markdown('Made with Made using [peptacular](https://github.com/pgarrett-scripps/peptacular): [![DOI](https://zenodo.org/badge/591504879.svg)](https://doi.org/10.5281/zenodo.15054278)', unsafe_allow_html=True)


    c1, c2 = st.columns([7, 3])
    with c1:
        formula = stp.text_input('Chemical formula', 'C6H12O6')

    with c2:
        moles = stp.number_input('Moles', value=1.0, help='Number of moles of the formula.')

    precision = stp.slider('Precision', min_value=0, max_value=10, value=5, step=1, help='Number of decimal places to round the masses to.')

st.divider()

composition = pt.parse_chem_formula(formula)
composition_subscript = write_subscripted_ion_markdown(composition)


mono_mass = pt.chem_mass(composition, monoisotopic=True, precision=precision)
avg_mass = pt.chem_mass(composition, monoisotopic=False, precision=precision)
mole_mass = moles * avg_mass

st.header(f'Chem Formula: {composition_subscript}')

c1, c2, c3 = st.columns(3)
c1.metric('Monoisotopic Mass (Da)', value=mono_mass)
c2.metric('Average Mass (Da)', value=avg_mass)
c3.metric(f'{round(moles, 2)} mol Weight (g)', value=round(mole_mass, 5) )

st.subheader('Elements')
for k, v in composition.items():
    c1, c2, c3, c4 = st.columns(4)
    element_average_mass = pt.chem_mass({k: v}, monoisotopic=False, precision=precision)
    element_subscript = write_subscripted_ion_markdown({k: v})
    c1.metric('Element', element_subscript)
    c2.metric('Monoisotopic Mass', pt.chem_mass({k: v}, monoisotopic=True, precision=precision))
    c3.metric('Average Mass', element_average_mass)
    c4.metric('Percent of mass', f'{round(element_average_mass / avg_mass * 100,2)} %')





