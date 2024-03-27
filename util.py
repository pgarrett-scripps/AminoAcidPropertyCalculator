import peptacular as pt
import streamlit as st
def write_subscripted_ion_markdown(composition: dict) -> str:

    composition = dict(sorted(composition.items(), key=lambda item: pt.HILL_ORDER.get(item[0], 10_000)))

    subscript_map = str.maketrans("0123456789+-", "₀₁₂₃₄₅₆₇₈₉₊₋")
    formula = ''
    for element, count in composition.items():
        # Convert numbers to subscript characters
        subscript_count = str(count).translate(subscript_map)
        formula += f"{element}{subscript_count}"
    return formula


def get_page_navigator_header():
    pages = ['pages/Amino_Acid_Mass_Calculator.py', 'pages/Chemical_Formula_Calculator.py', 'pages/Element_Mass_Table.py', 'pages/Modification_Mass_Table.py']

    #make page links

    cols = st.columns(len(pages))
    for i, page in enumerate(pages):
        cols[i].page_link(page)