import streamlit as st
import peptacular as pt

from util import write_subscripted_ion_markdown

st.set_page_config(layout="centered", page_title='Chemical Formula Mass Calculator', page_icon='🧪')


with st.container():
    st.title('Chemical Formula Calculator 🧪')
    st.caption('A calculator to determine the monoisotopic and average masses of a chemical formula.')
    st.caption('Made with [peptacular](https://pypi.org/project/peptacular/)')

    c1, c2 = st.columns([7, 3])
    formula = c1.text_input('Chemical formula', 'C6H12O6')
    moles = c2.number_input('Moles', value=1.0, help='Number of moles of the formula.')

st.divider()

composition = pt.parse_chem_formula(formula)
composition_subscript = write_subscripted_ion_markdown(composition)


mono_mass = pt.chem_mass(composition, monoisotopic=True, precision=5)
avg_mass = pt.chem_mass(composition, monoisotopic=False, precision=5)
mole_mass = moles * avg_mass

st.header(f'Chem Formula: {composition_subscript}')

c1, c2, c3 = st.columns(3)
c1.metric('Monoisotopic Mass (Da)', value=mono_mass)
c2.metric('Average Mass (Da)', value=avg_mass)
c3.metric(f'{round(moles, 2)} mol Weight (g)', value=round(mole_mass, 5) )

st.subheader('Elements')
for k, v in composition.items():
    c1, c2, c3, c4 = st.columns(4)
    element_average_mass = pt.chem_mass({k: v}, monoisotopic=False, precision=3)
    element_subscript = write_subscripted_ion_markdown({k: v})
    c1.metric('Element', element_subscript)
    c2.metric('Monoisotopic Mass', pt.chem_mass({k: v}, monoisotopic=True, precision=3))
    c3.metric('Average Mass', element_average_mass)
    c4.metric('Percent of mass', f'{round(element_average_mass / avg_mass * 100,2)} %')





