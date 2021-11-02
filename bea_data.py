import streamlit as st
df = pd.read_csv("https://raw.githubusercontent.com/KevinJCbed/BEA_stats/main/g_s.csv")

st.write("Top Canadian goods and services trading partners in 2020 ($ Millions)")
st.dataframe(df)