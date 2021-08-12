import streamlit as st
import pandas as pd
import requests
import io



st.set_page_config(
    page_title="Covid Stats by Province",
    page_icon="flag-za"
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

# st.plotly_chart(df.WC)
df.dropna(inplace=True)
# df.rename(columns={"date":"Date"},inplace=True)
data=df[['date','EC', 'FS', 'GP', 'KZN', 'LP', 'MP', 'NC', 'NW',
       'WC','total']]
data[['EC', 'FS', 'GP', 'KZN', 'LP', 'MP', 'NC', 'NW',
       'WC','total']]=data[['EC', 'FS', 'GP', 'KZN', 'LP', 'MP', 'NC', 'NW',
       'WC','total']].diff().rolling(7).mean().round(0)
data.set_index("date",inplace=True)
# data.rename(columns={"total":"Total"},inplace=True)
data.dropna(inplace=True)


# data.columns
# data.set_index("YYYYMMDD")
# prov=st.multiselect(options=list(data.columns)),label="Choose province")
st.title("Daily New Covid Cases by Province")

container = st.beta_container()
all = st.checkbox("Select all")

if all:
    prov = container.multiselect("Choose a province:",
                                             list(data.columns), list(data.columns))
else:
    prov = container.multiselect("Choose a province:",
                                             list(data.columns))
#
# data.head()
# # data.set_index("YYYYMMDD")
# to_plot=data.loc['date',prov].set_index('date')
# st.line_chart(data[prov])




#
# chart_data = go.Scatter(y=data.EC.diff().rolling(7).mean(),x=data['date'])
#
# layout = go.Layout(title='Covid Cases by Province', xaxis=dict(title='Date'),
#                    yaxis=dict(title='Cases'))
# fig = go.Figure(data=[chart_data], layout=layout)
# st.plotly_chart(fig)

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


# data_melt = data.melt(id_vars='date', value_vars=['EC', 'FS', 'GP', 'KZN', 'LP', 'MP', 'NC', 'NW',
#        'WC','Total'])
#
# fig=px.line(data_melt, x='date' , y='value' , color='variable',
#             labels={'date':'Date', 'value':'7 Day Moving Average'},
#             width=1000, height=600,
#             template="plotly_white",)
# fig.update_layout(legend_title_text='Province')
# fig.update_layout(
#     hoverlabel=dict(
#         # bgcolor="white",
#         font_size=12,
#         font_family="IBM Plex Sans"
#     )
# )
# fig.update_traces(hovertemplate='%{y}<br>%{x}')

# st.title("Daily New Covid Cases by Province")

# st.plotly_chart(fig)
# np.char.replace(prov, 'Total', 'total')
with col1:
    if "total" in prov:
        st.subheader("Total cases:")
        st.write(f"{df.total.iloc[-1].sum():,}")

        st.subheader("Total deaths:")
        st.write(f"{df_deaths.total.iloc[-1].sum():,}")

        st.subheader("Total vaccinated:")
        st.write(f"{df_vacc.total.iloc[-1].sum():,}")
    else:
        st.subheader("Total cases:")
        st.write(f"{df[prov].iloc[-1].sum():,}")

        st.subheader("Total deaths:")
        st.write(f"{df_deaths[prov].iloc[-1].sum():,}")

        st.subheader("Total vaccinated:")
        st.write(f"{df_vacc[prov].iloc[-1].sum():,}")

with col2:
    st.line_chart(data[prov],width=850,height=400,use_container_width=False)




