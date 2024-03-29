import streamlit as st

st.set_page_config(page_title='Home Page', page_icon='🏠')
st.title("Home Page :house_with_garden:")

st.markdown("A collection of Streamlit apps that demonstrate the use of the [peptacular](https://pypi.org/project/peptacular/) library.")

st.subheader("Apps:")
st.page_link(page="pages/Amino_Acid_Mass_Calculator.py", label="Amino Acid Mass Calculator", icon="📱")
st.page_link(page="pages/Chemical_Formula_Calculator.py", label="Chemical Formula Calculator", icon="🧪")
st.page_link(page="pages/Element_Mass_Table.py", label="Elemental Mass Table", icon="🧮")
st.page_link(page="pages/Modification_Mass_Table.py", label="Modification Mass Table", icon="🧰")

st.subheader("Other Apps:")
st.page_link(page="https://proteincleaver-dev.streamlit.app/", label="Protein Cleaver", icon="🔪")
st.page_link(page="https://peptide-fragmenter-dev.streamlit.app/", label="Peptide Fragmenter", icon="💣")
st.page_link(page="https://spectra-viewer-dev.streamlit.app/", label="Spectra Viewer", icon="👓")
st.page_link(page="https://isotopic-distributions.streamlit.app/", label="Isotopic Distribution Calculator", icon="📊")
st.page_link(page="https://peptide-isotopic-distributions.streamlit.app/", label="Isotopic Distribution Calculator", icon="💻")

