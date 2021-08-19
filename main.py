import streamlit as st
import pandas as pd
import requests
import io



st.set_page_config(
    page_title="Covid Stats by Province",
    page_icon="syringe"
)

#get csv
csv=requests.get('https://raw.githubusercontent.com/dsfsi/covid19za/master/data/covid19za_provincial_cumulative_timeline_confirmed.csv').content
df=pd.read_csv(io.StringIO(csv.decode('utf-8')))

#deaths
csv_deaths=requests.get('https://raw.githubusercontent.com/dsfsi/covid19za/master/data/covid19za_provincial_cumulative_timeline_deaths.csv').content
df_deaths=pd.read_csv(io.StringIO(csv_deaths.decode('utf-8')))

#vaccines
csv_vacc=requests.get('https://raw.githubusercontent.com/dsfsi/covid19za/master/data/covid19za_provincial_cumulative_timeline_vaccination.csv').content
df_vacc=pd.read_csv(io.StringIO(csv_vacc.decode('utf-8')))

#convert dates
df.date=pd.to_datetime(df.date,format="%d-%m-%Y")

df.dropna(inplace=True)
data=df[['date','EC', 'FS', 'GP', 'KZN', 'LP', 'MP', 'NC', 'NW',
       'WC','total']]
data[['EC', 'FS', 'GP', 'KZN', 'LP', 'MP', 'NC', 'NW',
       'WC','total']]=data[['EC', 'FS', 'GP', 'KZN', 'LP', 'MP', 'NC', 'NW',
       'WC','total']].diff().rolling(7).mean().round(0)
data.set_index("date",inplace=True)
data.dropna(inplace=True)


st.title("Daily New Covid Cases by Province")

container = st.beta_container()
all = st.checkbox("Select all")

if all:
    prov = container.multiselect("Choose a province:",
                                             sorted(list(data.columns)), sorted(list(data.columns)))
else:
    prov = container.multiselect("Choose a province:",
                                             sorted(list(data.columns)),default=['total'])


#Layout
col1, col2 = st.beta_columns([10,30])

st.markdown(
        f"""
<style>
    .reportview-container .main .block-container{{
        padding-top: {0}px;
        padding-right: {0}px;
        padding-left: {0}px;
        padding-bottom: {0}px;
    }}
</style>
""",
        unsafe_allow_html=True,
    )

peaks = data.loc['2020-12-01T00:00:00.000000000':'2021-02-25T00:00:00.000000000'].max()

with col1:
    if "total" in prov:
        st.subheader("Total cases:")
        st.write(f"{df.total.iloc[-1].sum():,}")

        st.subheader("Total deaths:")
        st.write(f"{df_deaths.total.iloc[-1].sum():,}")

        st.subheader("Total vaccinated:")
        st.write(f"{df_vacc.total.iloc[-1].sum():,}")

        if 0.3*peaks.total.sum()<data.total.iloc[-1]:
            st.markdown("_SA is still in the third wave_")
        else:
            st.markdown("_SA is no longer in the third wave_")
    else:
        st.subheader("Total cases:")
        st.write(f"{df[prov].iloc[-1].sum():,}")

        st.subheader("Total deaths:")
        st.write(f"{df_deaths[prov].iloc[-1].sum():,}")

        st.subheader("Total vaccinated:")
        st.write(f"{df_vacc[prov].iloc[-1].sum():,}")

        if 0.3*(peaks[prov].sum())<data[prov].iloc[-1].sum():
            st.markdown("_These/this province(s) are still in the third wave_")
        else:
            st.markdown("_These/this province(s) are no longer in the third wave_")

with col2:
    st.subheader("New cases (7 day moving-average)")
    st.line_chart(data[prov],width=850,height=400,use_container_width=False)
    st.caption("Data source: [https://github.com/dsfsi/covid19za/tree/master/data](https://github.com/dsfsi/covid19za/tree/master/data)")
