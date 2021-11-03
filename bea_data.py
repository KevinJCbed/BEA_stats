import streamlit as st
import pandas as pd
#df = pd.read_csv("https://raw.githubusercontent.com/KevinJCbed/BEA_stats/main/g_s.csv")

df_bop = (pd.read_csv("https://raw.githubusercontent.com/KevinJCbed/BEA_stats/main/bop_trade.csv")
.dropna()[['principal_trading_partners',"series",'trade',"2018","2019",'2020']]
)

add_selectbox = st.sidebar.selectbox(
    "Which country?",
    df_bop.query("series == 'Services trade'")['principal_trading_partners'].unique().tolist()
)

df_bop = df_bop.query("principal_trading_partners == @add_selectbox")
#df_bop['2020'] = df_bop['2020'].astype(int)

st.title(f"Canada - {add_selectbox} BOP Trade Statistics, $ Millions")

# Metrics
col1, col2, col3 = st.columns(3)
col1.metric(
    label="2020 Goods Export Value", 
    value= df_bop.query("trade == 'Receipts' & series == 'Goods trade'")['2020'].values[0],
    delta = round((df_bop.query("trade == 'Receipts' & series == 'Goods trade'")['2020'].values[0]/df_bop.query("trade == 'Receipts' & series == 'Goods trade'")['2019'].values[0]-1)*100,1)
    )

col1.metric(
    label="2020 Goods Import Value", 
    value= df_bop.query("trade == 'Payments' & series == 'Goods trade'")['2020'].values[0],
    delta = round((df_bop.query("trade == 'Payments' & series == 'Goods trade'")['2020'].values[0]/df_bop.query("trade == 'Payments' & series == 'Goods trade'")['2019'].values[0]-1)*100,1)
    )

col2.metric(
    label="2020 Services Export Value", 
    value= df_bop.query("trade == 'Receipts' & series == 'Services trade'")['2020'].values[0],
    delta = round((df_bop.query("trade == 'Receipts' & series == 'Services trade'")['2020'].values[0]/df_bop.query("trade == 'Receipts' & series == 'Services trade'")['2019'].values[0]-1)*100,1)
    )

col2.metric(
    label="2020 Services Import Value", 
    value= df_bop.query("trade == 'Payments' & series == 'Services trade'")['2020'].values[0],
    delta = round((df_bop.query("trade == 'Payments' & series == 'Services trade'")['2020'].values[0]/df_bop.query("trade == 'Payments' & series == 'Services trade'")['2019'].values[0]-1)*100,1)
    )



st.dataframe(
    df_bop.drop("principal_trading_partners",axis = 1)[["series",'trade',"2018","2019",'2020']].sort_values("series").round()
    )
