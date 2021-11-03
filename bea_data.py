import streamlit as st
import pandas as pd

#setups
years = [str(x) for x in range(2015,2021)]
df_bop = (pd.read_csv("https://raw.githubusercontent.com/KevinJCbed/BEA_stats/main/bop_trade.csv")
.dropna()[['principal_trading_partners',"series",'trade']+years]
)
fdi_iic = pd.read_csv("https://raw.githubusercontent.com/KevinJCbed/BEA_stats/main/fdi_iic.csv")


#selection box
# add_selectbox = st.sidebar.selectbox(
#     "Which country?",
#     df_bop.query("series == 'Services trade'")['principal_trading_partners'].unique().tolist()
# )

add_selectbox = st.sidebar.selectbox(
    "Which country?",
    df_bop.query("series == 'Services trade'")['principal_trading_partners'].unique().tolist()
)

st.title(f"Canada - {add_selectbox} common stats")

#BOP
st.title("BOP Trade Statistics, $M")

# Metrics
# col1, col2, col3 = st.columns(3)
# col1.metric(
#     label="2020 Goods Export Value", 
#     value= df_bop.query("trade == 'Receipts' & series == 'Goods trade'")['2020'].values[0],
#     delta = round((df_bop.query("trade == 'Receipts' & series == 'Goods trade'")['2020'].values[0]/df_bop.query("trade == 'Receipts' & series == 'Goods trade'")['2019'].values[0]-1)*100,1)
#     )

# col1.metric(
#     label="2020 Goods Import Value", 
#     value= df_bop.query("trade == 'Payments' & series == 'Goods trade'")['2020'].values[0],
#     delta = round((df_bop.query("trade == 'Payments' & series == 'Goods trade'")['2020'].values[0]/df_bop.query("trade == 'Payments' & series == 'Goods trade'")['2019'].values[0]-1)*100,1)
#     )

# col2.metric(
#     label="2020 Services Export Value", 
#     value= df_bop.query("trade == 'Receipts' & series == 'Services trade'")['2020'].values[0],
#     delta = round((df_bop.query("trade == 'Receipts' & series == 'Services trade'")['2020'].values[0]/df_bop.query("trade == 'Receipts' & series == 'Services trade'")['2019'].values[0]-1)*100,1)
#     )

# col2.metric(
#     label="2020 Services Import Value", 
#     value= df_bop.query("trade == 'Payments' & series == 'Services trade'")['2020'].values[0],
#     delta = round((df_bop.query("trade == 'Payments' & series == 'Services trade'")['2020'].values[0]/df_bop.query("trade == 'Payments' & series == 'Services trade'")['2019'].values[0]-1)*100,1)
#     )

df_bop.series = pd.Categorical(df_bop.series, ['Goods trade',"Services trade","Goods and Services"])
df_bop.trade = pd.Categorical(df_bop.trade, ['Receipts',"Payments","Balances","Bilateral"])
st.table(
    df_bop.query("principal_trading_partners == @add_selectbox").drop("principal_trading_partners",axis = 1)[["series",'trade']+years].sort_values(["series",'trade']).round()
    )



st.title(f"Bilateral FDI IIC, $M")
st.dataframe(
    fdi_iic.query("countries == @add_selectbox").drop("series",axis = 1)
    
    )
