import streamlit as st
import pandas as pd
from countrycode import countrycode as cc

# setups
reference_year = st.sidebar.selectbox(
    "Select metric reference year?",
    [x for x in range(2015, 2021)],
    index=[x for x in range(2015, 2021)].index(2020)
)

years = [str(x) for x in range(2015, reference_year+1)]

df_bop = (pd.read_csv("https://raw.githubusercontent.com/KevinJCbed/BEA_stats/main/bop_trade.csv")
          .dropna()[['principal_trading_partners', "series", 'trade']+years]
          )
df_bop = df_bop[~(df_bop.principal_trading_partners.str.contains(
    "European Union") | df_bop.principal_trading_partners.str.contains(
    "elsewhere"))]

add_selectbox = st.sidebar.selectbox(
    "Which country?",
    df_bop.query("series == 'Services trade'")[
        'principal_trading_partners'].unique().tolist()
)

df_bop['iso'] = cc.countrycode(
    df_bop.principal_trading_partners, origin="country_name", target="iso3c")

fdi_iic = pd.read_csv(
    "https://raw.githubusercontent.com/KevinJCbed/BEA_stats/main/fdi_iic.csv")

fdi_iic['iso'] = cc.countrycode(
    fdi_iic.countries, origin="country_name", target="iso3c")

imf = pd.read_csv(
    "https://raw.githubusercontent.com/KevinJCbed/BEA_stats/main/IMFWEOOCT2021.csv", encoding="ISO-8859-1")


select_iso = cc.countrycode(
    add_selectbox, origin="country_name", target="iso3c")


df_bop = df_bop.query("iso == @select_iso")

st.title(f"Canada - {add_selectbox} common stats")

# BOP
st.title("BOP Trade Statistics, $M")

# Metrics
col1, col2, col3 = st.columns(3)
col1.metric(
    label=f"{str(reference_year)} Goods Export Value",
    value=int(df_bop.query("trade == 'Receipts' & series == 'Goods trade'")[
        str(reference_year)].values[0]),
    delta=round((df_bop.query("trade == 'Receipts' & series == 'Goods trade'")[
                str(reference_year)].values[0]/df_bop.query("trade == 'Receipts' & series == 'Goods trade'")[str(reference_year-1)].values[0]-1)*100, 1)
)

col1.metric(
    label=f"{str(reference_year)} Goods Import Value",
    value=int(df_bop.query("trade == 'Payments' & series == 'Goods trade'")[
        str(reference_year)].values[0]),
    delta=round((df_bop.query("trade == 'Payments' & series == 'Goods trade'")[
                str(reference_year)].values[0]/df_bop.query("trade == 'Payments' & series == 'Goods trade'")[str(reference_year-1)].values[0]-1)*100, 1)
)

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

df_bop.series = pd.Categorical(
    df_bop.series, ['Goods trade', "Services trade", "Goods and Services"])
df_bop.trade = pd.Categorical(
    df_bop.trade, ['Receipts', "Payments", "Balances", "Bilateral"])
st.table(
    df_bop.drop("principal_trading_partners",
                axis=1)[["series", 'trade']+years].sort_values(["series", 'trade']).round()
)


# FDIC
st.title(f"Bilateral FDI IIC, $M")
st.table(
    fdi_iic.query(
        "iso == @select_iso").drop(["series", "countries"], axis=1)[['FDI']+years]

)

# IMF Data
st.title(f"IMF WEO")
st.table(
    imf.query("iso == @select_iso").drop(["iso", "country"], axis=1)
)
