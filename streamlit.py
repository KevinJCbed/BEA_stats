import pandas as pd
from pandasql import sqldf
import streamlit as st
from countrycode import countrycode as cc
pysqldf = lambda q: sqldf(q, globals())
def convert_df(df):
   return df.to_csv().encode('utf-8')

def iso_to_name(name):
   return cc.countrycode(name, origin = "iso3c", target = "country_name")


#print(pd.read_sql("select * from goods", conn)['Principal trading partners'].unique().tolist())
add_selection = st.sidebar.selectbox(
    "Which country?",
    ['DZA',
 'AUS',
 'BEL',
 'BRA',
 'CHN',
 'GBR',
 'FRA',
 'DEU',
 'HKG',
 'IND',
 'IDN',
 'IRQ',
 'ITA',
 'JPN',
 'MEX',
 'NLD',
 'NOR',
 'PER',
 'RUS',
 'SAU',
 'SGP',
 'KOR',
 'ESP',
 'CHE',
 'TWN',
 'Total of all countries',
 'TUR',
 'USA'],

)

year_selection = st.sidebar.slider(
    "Year range?",
    min_value = 2010,
    max_value = 2021,
    value = [2018,2020])


overview = pd.read_csv("https://raw.githubusercontent.com/KevinJCbed/BEA_stats/main/overview.csv")
fdi = pd.read_csv("https://raw.githubusercontent.com/KevinJCbed/BEA_stats/main/fdi.csv")
imf = pd.read_csv("https://raw.githubusercontent.com/KevinJCbed/BEA_stats/main/imf.csv")
top_bop = pd.read_csv("https://raw.githubusercontent.com/KevinJCbed/BEA_stats/main/top_bop.csv")

q1 = f"""
select * from overview
WHERE iso == '{add_selection}' AND Year >= {year_selection[0]} AND Year <= {year_selection[1]};
"""

q3 = f"""
select * from fdi
WHERE iso == '{add_selection}' AND Year >= {year_selection[0]} AND Year <= {year_selection[1]};
""" 

q4 = f"""
select * from imf
WHERE iso == '{add_selection}';
""" 

df1 = pysqldf(q1).pivot_table(index = "Series",columns = "Year",values = "Value").fillna(0).sort_values("Series")
df3 = pysqldf(q3).pivot_table(index = "Series",columns = "Year",values = "VALUE").fillna(0)
df4 = pysqldf(q4)
df5 = pysqldf(f"select * from top_bop where Year == {year_selection[1]}").pivot_table(index = ["Year","Principal_trading_partners"],columns = "Series",values = "Value").fillna(0).sort_values("G_S, Bilateral",ascending=False)

st.title(f"BOP Trade: Canada - {iso_to_name(add_selection)}, $M")
st.dataframe(df1)
st.download_button(
   "Download",
   convert_df(df1),
   "goods_trade.csv",
   "text/csv",
   key='download-df1'
)
st.button(
   "To Clipboard",
   on_click = df1.to_clipboard(),
   help = "Click to copy data to clipboard",
   key = '1'
)

st.title(f"FDI stock: Canada - {iso_to_name(add_selection)}, $M")
st.dataframe(df3)
st.download_button(
   "Download",
   convert_df(df3),
   "fdi.csv",
   "text/csv",
   key='download-df3'
)
st.button(
   "To Clipboard",
   on_click = df3.to_clipboard(),
   help = "Click to copy data to clipboard",
   key = '3'
)

st.title(f"IMF WEO Oct 2021: {iso_to_name(add_selection)}")
st.dataframe(df4)
st.download_button(
   "Download",
   convert_df(df4),
   "imf.csv",
   "text/csv",
   key='download-df4'
)
st.button(
   "To Clipboard",
   on_click = df4.to_clipboard(),
   help = "Click to copy data to clipboard",
   key = '4'
)

st.title(f"Top goods and services trading partners in {year_selection[1]}, $M")
st.dataframe(df5)
st.download_button(
   "Download",
   convert_df(df5),
   "topbop.csv",
   "text/csv",
   key='download-df5'
)
st.button(
   "To Clipboard",
   on_click = df5.to_clipboard(),
   help = "Click to copy data to clipboard",
   key = '5'
)
