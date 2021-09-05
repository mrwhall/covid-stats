import streamlit as st
import pandas as pd
import requests
import io

@st.cache
def MA(df):
    return df.diff().rolling(7).mean().round(0)

def perc_change(new, old):
    return (new-old)/old



def per100000(df,columns):
    data100000 = pd.DataFrame()
    for province in columns:
        data100000[province] = data[province] / int(
            df_pop["population"][df_pop["province"] == provinces[province]]) * 100000
    data100000["total"]=df['total']/sum(df_pop["population"])*100000

    return data100000


st.set_page_config(
    page_title="Covid Stats by Province",
    page_icon="syringe"
)

#get csv
csv=requests.get('https://raw.githubusercontent.com/dsfsi/covid19za/master/data/covid19za_provincial_cumulative_timeline_confirmed.csv').content
df_cases=pd.read_csv(io.StringIO(csv.decode('utf-8')))

#deaths
csv_deaths=requests.get('https://raw.githubusercontent.com/dsfsi/covid19za/master/data/covid19za_provincial_cumulative_timeline_deaths.csv').content
df_deaths=pd.read_csv(io.StringIO(csv_deaths.decode('utf-8')))

#vaccines
csv_vacc=requests.get('https://raw.githubusercontent.com/dsfsi/covid19za/master/data/covid19za_provincial_cumulative_timeline_vaccination.csv').content
df_vacc=pd.read_csv(io.StringIO(csv_vacc.decode('utf-8')))


#population
csv_pop=requests.get('https://raw.githubusercontent.com/dsfsi/covid19za/master/data/district_data/za_province_pop.csv').content
df_pop=pd.read_csv(io.StringIO(csv_pop.decode('utf-8')),names=["province","population"])

prov_short=['EC', 'FS', 'GP', 'KZN', 'LP', 'MP', 'NC', 'NW',
       'WC']

provandTotal=['EC', 'FS', 'GP', 'KZN', 'LP', 'MP', 'NC', 'NW',
       'WC','total']

st.title("Daily New Covid Cases by Province")

container = st.container()
all = st.checkbox("Select all")

if all:
    prov = container.multiselect("Choose a province:",
                                             sorted(provandTotal), sorted(provandTotal))
else:
    prov = container.multiselect("Choose a province:",
                                             sorted(provandTotal),default=['total'])

peaks = df_cases.loc['2020-12-01T00:00:00.000000000':'2021-02-25T00:00:00.000000000'].max()

if prov == []:
    st.stop()

with st.sidebar:
    st.title("Overall numbers and daily changes")
    if "total" in prov:
        st.metric(label="Total cases",value=f"{df_cases.total.iloc[-1]:,}",
                  delta=f"{perc_change(df_cases.total.diff().iloc[-1],df_cases.total.diff().iloc[-2]):.1%} = {(df_cases.total.diff()).iloc[-1]-(df_cases.total.diff()).iloc[-2]:,}",
                  delta_color="inverse")

        st.metric(label="Total deaths",value=f"{df_deaths.total.iloc[-1]:,}",
                  delta=f"{perc_change(df_deaths.total.diff().iloc[-1],df_deaths.total.diff().iloc[-2]):.1%} = {(df_deaths.total.diff()).iloc[-1]-(df_deaths.total.diff()).iloc[-2]:,}",
                  delta_color="inverse")

        st.metric(label="Total vaccinated",value=f"{df_vacc.total.iloc[-1]:,}",
                  delta=f"{perc_change(df_vacc.total.diff().iloc[-1],df_vacc.total.diff().iloc[-2]):.1%} = {(df_vacc.total.diff()).iloc[-1]-df_vacc.total.diff().iloc[-2]:,}")

        if 0.3*peaks.total.sum()<df_cases.total.iloc[-1]:
            st.markdown("_SA is still in the third wave_")
        else:
            st.markdown("_SA is no longer in the third wave_")
    else:
        st.metric(label="Total cases",value=f"{df_cases[prov].iloc[-1].sum():,}",
                  delta=f"{perc_change(df_cases[prov].diff().iloc[-1].sum(),df_cases[prov].diff().iloc[-2].sum()):.1%} = {(df_cases[prov].diff()).iloc[-1].sum()-(df_cases[prov].diff()).iloc[-2].sum():.0f}",
                  delta_color="inverse")

        st.metric(label="Total deaths", value=f"{df_deaths[prov].iloc[-1].sum():,}",
                  delta=f"{perc_change(df_deaths[prov].diff().iloc[-1].sum(), df_deaths[prov].diff().iloc[-2].sum()):.1%} = {(df_deaths[prov].diff()).iloc[-1].sum() - (df_deaths[prov].diff()).iloc[-2].sum():.0f}",
                  delta_color="inverse")

        st.metric(label="Total vaccinated", value=f"{df_vacc[prov].iloc[-1].sum():,}",
                  delta=f"{perc_change(df_vacc[prov].diff().iloc[-1].sum(), df_vacc[prov].diff().iloc[-2].sum()):.1%} = {(df_vacc[prov].diff()).iloc[-1].sum() - (df_vacc[prov].diff()).iloc[-2].sum():.0f}")
        if 0.3*(peaks[prov].sum())<df_cases[prov].iloc[-1].sum():
            st.markdown("_These/this province(s) are still in the third wave_")
        else:
            st.markdown("_These/this province(s) are no longer in the third wave_")

    graphType = st.radio("Toggle graph", ["Daily Cases", "Daily Deaths", "Daily Vaccinated"])

if graphType == "Daily Cases":
    df = df_cases
    title="New cases (7 day moving-average)"

elif graphType == "Daily Deaths":
    df = df_deaths
    title = "Daily deaths (7 day moving-average)"

elif graphType == "Daily Vaccinated":
    df=df_vacc
    title = "Daily vaccinated (7 day moving-average)"
    df.date = pd.to_datetime(df.date, format="%Y-%m-%d")

#convert dates
if graphType != "Daily Vaccinated":
    df.date=pd.to_datetime(df.date,format="%d-%m-%Y")

df.dropna(inplace=True)
data=df[['date','EC', 'FS', 'GP', 'KZN', 'LP', 'MP', 'NC', 'NW',
       'WC','total']]
data[['EC', 'FS', 'GP', 'KZN', 'LP', 'MP', 'NC', 'NW',
       'WC','total']]=MA(data[['EC', 'FS', 'GP', 'KZN', 'LP', 'MP', 'NC', 'NW',
       'WC','total']])
data.set_index("date",inplace=True)
data.dropna(inplace=True)

provinces=dict(zip(sorted(prov_short),sorted(list(df_pop["province"]))))


data100000=per100000(data,prov_short)


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



if st.checkbox("Per 100,000 people"):
    st.subheader(title[:-1]+" per 100,000 people)")
    st.line_chart(data100000[prov], width=850, height=400, use_container_width=False)
    st.caption(
        "Data source: [https://github.com/dsfsi/covid19za/tree/master/data](https://github.com/dsfsi/covid19za/tree/master/data)")
else:
    st.subheader(title)
    st.line_chart(data[prov],width=850,height=400,use_container_width=False)
    st.caption("Data source: [https://github.com/dsfsi/covid19za/tree/master/data](https://github.com/dsfsi/covid19za/tree/master/data)")

