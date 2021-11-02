import streamlit as st
import pandas as pd
df = pd.read_csv("https://raw.githubusercontent.com/KevinJCbed/BEA_stats/main/g_s.csv")





add_selectbox = st.sidebar.selectbox(
    "Which country?",
    df['Principal trading partners'].unique().tolist()
)

col1, col2, col3 = st.columns(3)
col1.metric(label="Number of countries", value=df.shape[0]-1)
col2.metric(label="Year", value=2020)

st.write("Top Canadian goods and services trading partners in 2020 ($ Millions)")
st.dataframe(df.style.highlight_max(axis=0))
st.write(f"you have selected {add_selectbox}")
#st.dataframe(df.style.applymap(lambda x: 'background-color : yellow' if x['Principal trading partners']==add_selectbox else ''))
