"""
This app will serve as a cheat sheet of proteomics values.
"""

import pandas as pd
import streamlit as st
import peptacular as pt

from util import write_subscripted_ion_markdown

# set up the page (wide mode)
st.set_page_config(page_title='Amino Acid Mass Calculator', page_icon='📱',
                   initial_sidebar_state='expanded')

st.title('Amino Acid Mass Calculator 📱')

st.caption('A calculator to determine properties of amino acids, including monoisotopic and average masses, '
           'chemical compositions, and immonium ions.')

st.caption('Made with [peptacular](https://pypi.org/project/peptacular/)')

precision = 5
with st.container():


    c1, c2, c3 = st.columns(3)
    nterm = c2.checkbox('Include N-term', value=False, help='Include N-terminus (+H) in calculations.')
    cterm = c3.checkbox('Include C-term', value=False, help='Include C-terminus (+OH) in calculations.')


    #st.write('Precision')
    #precision = st.number_input('Decimal places', min_value=0, max_value=10, value=5, step=1, help='Number of decimal places to round the masses to.')

    isotope_mods = []

    with c1.popover('Select Isotopes'):
        carbon_isotope = st.radio('Carbon', ['12C', '13C', '14C'], index=0, horizontal=True,
                                  help='Select the carbon isotope. 12C is the default and most common isotope.')
        hydrogen_isotope = st.radio('Hydrogen', ['H', 'D', 'T'], index=0, horizontal=True,
                                    help='Select the hydrogen isotope. H is the default and most common isotope.')
        nitrogen_isotope = st.radio('Nitrogen', ['14N', '15N'], index=0, horizontal=True,
                                    help='Select the nitrogen isotope. 14N is the default and most common isotope.')
        oxygen_isotope = st.radio('Oxygen', ['16O', '17O', '18O'], index=0, horizontal=True,
                                  help='Select the oxygen isotope. 16O is the default and most common isotope.')
        sulfur_isotope = st.radio('Sulfur', ['32S', '33S', '34S', '36S'], index=0, horizontal=True,
                                  help='Select the sulfur isotope. 32S is the default and most common isotope.')
        selenium_isotope = st.radio('Selenium', ['74Se', '76Se', '77Se', '78Se', '80Se', '82Se'], index=0, horizontal=True,
                                    help='Select the selenium isotope. 74Se is the default and most common isotope.')

        if carbon_isotope != '12C':
            isotope_mods.append(pt.Mod(carbon_isotope, 1))
        if hydrogen_isotope != 'H':
            isotope_mods.append(pt.Mod(hydrogen_isotope, 1))
        if nitrogen_isotope != '14N':
            isotope_mods.append(pt.Mod(nitrogen_isotope, 1))
        if oxygen_isotope != '16O':
            isotope_mods.append(pt.Mod(oxygen_isotope, 1))
        if sulfur_isotope != '32S':
            isotope_mods.append(pt.Mod(sulfur_isotope, 1))
        if selenium_isotope != '74Se':
            isotope_mods.append(pt.Mod(selenium_isotope, 1))



aa_data = {'Name': [],
           '3 letter code': [],
           '1 letter code': [],
           'Monoisotopic Mass': [],
           'Average Mass': [],
           'Composition': [],
           'gif': [],
           'Isotopes': [],
           #'Immonium ion (+1)': [],
           #'Immonium ion (+1) composition': [],
           }

imonium_ion_data = {'Name': [],
                   '3 letter code': [],
                   '1 letter code': [],
                    'Monoisotopic Mass': [],
                    'Average Mass': [],
                    'Composition': [],
                    }

for aa in pt.AMINO_ACIDS:

    imonium_ion_data['Name'].append(pt.AA_TO_NAME[aa])
    imonium_ion_data['3 letter code'].append(pt.AA_TO_THREE_LETTER_CODE[aa])
    imonium_ion_data['1 letter code'].append(aa)

    aa_data['Name'].append(pt.AA_TO_NAME[aa])
    aa_data['3 letter code'].append(pt.AA_TO_THREE_LETTER_CODE[aa])
    aa_data['1 letter code'].append(aa)

    if aa == 'B' or aa == 'J' or aa == 'Z' or aa == 'X':
        aa_data['Monoisotopic Mass'].append(None)
        aa_data['Average Mass'].append(None)
        aa_data['Composition'].append(None)
        aa_data['gif'].append(None)
        aa_data['Isotopes'].append(None)
        #aa_data['Immonium ion (+1)'].append(None)
        #aa_data['Immonium ion (+1) composition'].append(None)

        imonium_ion_data['Monoisotopic Mass'].append(None)
        imonium_ion_data['Average Mass'].append(None)
        imonium_ion_data['Composition'].append(None)
        continue

    composition = pt.AA_COMPOSITIONS[aa]
    if nterm:
        composition = pt.merge_dicts(composition, pt.NTERM_COMPOSITION)
    if cterm:
        composition = pt.merge_dicts(composition, pt.CTERM_COMPOSITION)

    composition = pt.apply_isotope_mods_to_composition(composition, isotope_mods, )
    isotopes = [freq for cnt, freq in pt.isotopic_distribution(composition, use_neutron_count=True, distribution_resolution=1)]

    composition_subscript = write_subscripted_ion_markdown(composition)

    aa_data['Monoisotopic Mass'].append(pt.chem_mass(composition, monoisotopic=True))
    aa_data['Average Mass'].append(pt.chem_mass(composition, monoisotopic=False))
    aa_data['Composition'].append(composition_subscript)  #pt.write_chem_formula(composition, hill_order=True))

    ion_comp = pt.comp(aa, ion_type='i', charge=1)
    ion_comp = pt.apply_isotope_mods_to_composition(ion_comp, isotope_mods)

    ion_comp_subscript = write_subscripted_ion_markdown(ion_comp)

    aa_data['gif'].append(f'https://www.ionsource.com/Card/clipart/{pt.AA_TO_THREE_LETTER_CODE[aa].lower()}.gif')
    aa_data['Isotopes'].append(isotopes)
    #aa_data['Immonium ion (+1)'].append(pt.chem_mass(ion_comp, monoisotopic=True))
    #aa_data['Immonium ion (+1) composition'].append(ion_comp_subscript)

    imonium_ion_data['Monoisotopic Mass'].append(pt.chem_mass(ion_comp, monoisotopic=True))
    imonium_ion_data['Average Mass'].append(pt.chem_mass(ion_comp, monoisotopic=False))
    imonium_ion_data['Composition'].append(ion_comp_subscript)

aa_df = pd.DataFrame(aa_data)
# sort by mass
aa_df = aa_df.sort_values(by='Monoisotopic Mass')

precision_str = "{:." + str(precision) + "f}"

st.subheader('Amino Acids')
st.dataframe(
    aa_df.style.format({'Monoisotopic Mass': precision_str, 'Average Mass': precision_str, 'Immonium ion (+1)': precision_str}),
    column_config={
        "gif": st.column_config.ImageColumn(
            "Structure", help="Streamlit app preview screenshots.",
            width='medium'
        ),
        "Isotopes":  st.column_config.BarChartColumn(
            "Isotopes", help="Streamlit app preview screenshots",
            width='small', y_min=0, y_max=1
        ),
        "3 letter code": st.column_config.TextColumn(
            "3 Letter Code", help="Three letter code for amino acid..",
            width='small'
        ),
        "1 letter code": st.column_config.TextColumn(
            "1 Letter Code", help="One letter code for amino acid.",
            width='small'
        ),

        "Name": st.column_config.TextColumn(
            "Name", help="Name of amino acid.",
            width='small'
        ),

        "Composition": st.column_config.TextColumn(
            "Chem Formula", help="Chemical composition of amino acid.",
            width='small'
        ),

        "Monoisotopic Mass": st.column_config.NumberColumn(
            "Mono Mass", help="Monoisotopic mass of amino acid.",
            width='small'
        ),

        "Average Mass": st.column_config.NumberColumn(
            "Average Mass", help="Average mass of amino acid.",
            width='small'
        ),


    },
    hide_index=True,
    use_container_width=True,
    height=950,
    column_order=("Name", "3 letter code", "1 letter code", "Monoisotopic Mass", "Average Mass", "Composition")
)

st.subheader('Immonium Ions (+1)')
imonium_ion_df = pd.DataFrame(imonium_ion_data)
imonium_ion_df = imonium_ion_df.sort_values(by='Monoisotopic Mass')
st.dataframe(
    imonium_ion_df.style.format({'Monoisotopic Mass': precision_str
                                    , 'Average Mass': precision_str
                                    }),
    column_config={

        "3 letter code": st.column_config.TextColumn(
            "3 letter code", help="Three letter code for amino acid",
            width='small'
        ),
        "1 letter code": st.column_config.TextColumn(
            "1 letter code", help="One letter code for amino acid",
            width='small'
        ),

        "Name": st.column_config.TextColumn(
            "Name", help="Name of amino acid",
            width='small'
        ),

        "Composition": st.column_config.TextColumn(
            "Chem Formula", help="Chemical composition of amino acid.",
            width='small'
        ),

        "Monoisotopic Mass": st.column_config.NumberColumn(
            "Mono Mass", help="Monoisotopic mass of amino acid.",
            width='small'
        ),

        "Average Mass": st.column_config.NumberColumn(
            "Average Mass", help="Average mass of amino acid.",
            width='small'
        ),
    },

    hide_index=True,
    use_container_width=True,
    height=950

)