import peptacular as pt
import streamlit as st
import pandas as pd

# Set page configuration
st.set_page_config(page_title='ProteaseRegex', page_icon='🧰')

# Custom CSS for improved styling
st.markdown("""
<style>
.title {
    color: #2c3e50;
    text-align: center;
    font-weight: bold;
    margin-bottom: 30px;
}
.dataframe {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
}
.dataframe th {
    background-color: #3498db;
    color: white;
    padding: 12px;
    text-align: left;
}
.dataframe td {
    padding: 10px;
    border-bottom: 1px solid #ecf0f1;
}
.dataframe tr:nth-child(even) {
    background-color: #f2f2f2;
}
.dataframe tr:hover {
    background-color: #e6f2ff;
}
</style>
""", unsafe_allow_html=True)

# Title with custom styling
st.markdown('<h1 class="title">Protease Regexes 🧰 </h1>', unsafe_allow_html=True)

# Convert protease dictionary into a DataFrame
regexes: dict[str, str] = pt.PROTEASES
df = pd.DataFrame(list(regexes.items()), columns=["Protease", "Regex"])

# Style the DataFrame
def highlight_regex(s):
    return ['background-color: #e6f3ff' if idx % 2 == 0 else 'background-color: #f0f8ff' for idx in range(len(s))]

styled_df = df.style.apply(highlight_regex, axis=0)\
    .set_properties(**{
        'font-size': '14px',
        'text-align': 'left',
        'padding': '10px',
    })\
    .set_table_styles([{
        'selector': 'th',
        'props': [
            ('background-color', '#3498db'),
            ('color', 'white'),
            ('font-weight', 'bold'),
            ('text-align', 'left')
        ]
    }])

# Display the styled DataFrame
st.table(styled_df)