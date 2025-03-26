import pandas as pd
import streamlit as st

import peptacular as pt
from peptacular import chem_mass

from util import write_subscripted_ion_markdown


st.set_page_config(page_title='PeptideMods', page_icon='🧰')

st.title('Peptide Modification Mass Table 🧰')

st.caption('A table of modifications with monoisotopic and average masses.')
st.caption('Made with [peptacular](https://pypi.org/project/peptacular/)')

precision = 5

with st.container():


    c1, c2 = st.columns([5, 7])
    show_orig_values = c2.checkbox('Show Original Values', value=False, help='Use a simplified set of columns.')
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

    #st.subheader('Precision')
    #precision = st.number_input('Decimal places', min_value=0, max_value=10, value=5, step=1, help='Number of decimal places to round the masses to.')




def db_df(db: pt.EntryDb) -> pd.DataFrame:
    data = {'ID': [], 'Name': [], 'Monoisotopic Mass': [], 'Average Mass': [], 'Composition': [],
            'Orig Monoisotopic Mass': [], 'Orig Average Mass': [], 'Orig Composition': []}
    for entry in db:
        data['ID'].append(entry.id)
        data['Name'].append(entry.name)

        original_composition = entry.composition

        original_composition_sub = None
        if original_composition is not None:
            original_composition_sub = write_subscripted_ion_markdown(pt.parse_chem_formula(original_composition))


        if original_composition is None:
            data['Composition'].append(None)
            data['Monoisotopic Mass'].append(None)
            data['Average Mass'].append(None)
            data['Orig Composition'].append(None)
        else:
            composition = pt.apply_isotope_mods_to_composition(original_composition, isotope_mods)
            composition_sub = write_subscripted_ion_markdown(composition)
            data['Composition'].append(composition_sub)
            data['Monoisotopic Mass'].append(chem_mass(composition, monoisotopic=True))
            data['Average Mass'].append(chem_mass(composition, monoisotopic=False))
            data['Orig Composition'].append(original_composition_sub)

        data['Orig Monoisotopic Mass'].append(entry.mono_mass)
        data['Orig Average Mass'].append(entry.avg_mass)

    df = pd.DataFrame(data)
    df['Mono Diff'] = df['Monoisotopic Mass'] - df['Orig Monoisotopic Mass']
    df['Avg Diff'] = df['Average Mass'] - df['Orig Average Mass']
    return df


simple_columns = ['ID', 'Name', 'Monoisotopic Mass', 'Average Mass', 'Composition']


column_config = {
    'ID': st.column_config.TextColumn(label="ID", width='small',),
    'Name': st.column_config.TextColumn(label="Name", width='medium'),
    'Monoisotopic Mass': st.column_config.NumberColumn(label="Mono Mass", width='small',),
    'Average Mass': st.column_config.NumberColumn(label="Average Mass", width='small',),
    'Composition': st.column_config.TextColumn(label="Composition", width='medium'),
}

# UNIMOD
unimod_df = db_df(pt.UNIMOD_DB)
st.subheader('UNIMOD')
st.dataframe(unimod_df,
             hide_index=True,
             column_order=None if show_orig_values else simple_columns,
             use_container_width=True,
             column_config=column_config)

# PSI-MOD
psimod_df = db_df(pt.PSI_MOD_DB)
st.subheader('PSI-MOD')
st.dataframe(psimod_df,
             hide_index=True,
             column_order=None if show_orig_values else simple_columns,
             use_container_width=True,
             column_config=column_config)
# MONO
monomass_df = db_df(pt.MONOSACCHARIDES_DB)
st.subheader('MONO')
st.dataframe(monomass_df,
             hide_index=True,
             column_order=None if show_orig_values else simple_columns,
             use_container_width=True,
             column_config=column_config)
# XL-MOD
xlmod_df = db_df(pt.XLMOD_DB)
st.subheader('XL-MOD')
st.dataframe(xlmod_df,
             hide_index=True,
             column_order=None if show_orig_values else simple_columns,
             use_container_width=True,
             column_config=column_config)