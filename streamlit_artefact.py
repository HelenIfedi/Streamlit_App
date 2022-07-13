import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
#import plotly_express as px
import plotly.express as px

#magic uses st.write
st.write('# Python for Visualisation') #st.title('')
st.markdown('''
This dashboard shows *different plot type* of several python libraries  
Data source: [Github: The Center for Systems Science and Engineering (CSSE) at JHU ](https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_time_series)
''')
#Row A
b1, b2= st.columns(2)
b1.button('Static Visualisation')
b2.button('Interactive Visualisation')
#Row B
b3, b4= st.columns(2)
b3.button('Animation')
b4.button('Covid Dashboard')

#Load Dataset
dfn = pd.read_csv('https://raw.githubusercontent.com/HelenIfedi/Bokeh_covid_artefact/main/covid_proj_data3.csv',
                  index_col='country')

dfn.dropna(subset=['Lat', 'Long'], inplace=True)

dfn.drop(['Lat', 'Long'], axis=1, inplace=True)
ncntry = dfn.shape[0]
nslices = dfn.shape[1]
DEFAULT_TICKERS = dfn.index

dfn.reset_index(inplace=True)

df_all = pd.melt(dfn, id_vars=['country'], value_vars=dfn.columns[1:])

df_all['circle_sizes'] = df_all['value'] / df_all['value'].max() * 100
df_all['circle_sizes'] = df_all['circle_sizes'].apply(lambda x: x if x > 0 else 1)

df_all.rename(columns={'variable': 'dates', 'value': 'cases'}, inplace=True)

df_all['dates'] = pd.to_datetime(df_all['dates'])
#country
country_select = "United Kingdom"
df_uk = df_all[["dates", "cases", "country"]].loc[(df_all['country']==country_select  )]
uk_ind = df_uk.loc[df_uk["dates"]=='2022-01-31'].index
df_uk.loc[uk_ind[0], "cases"]=int(df_uk["cases"].mean())

#Chart 1
st.header('Daily Covid cases in the United Kingdom Tabble')
st.dataframe(df_uk)

#st.header('Line chart(UK Dialy cases)')
#line_uk = px.line(df_uk, x='dates', y='cases', title='Plotly Line Chart')
#st.plotly(line_uk)

#Chart 1
st.header('Line Daily Covid cases in the United Kingdom, Matplotlib')
fig, ax = plt.subplots(1,1)
ax.scatter(x=df_uk['dates'], y=df_uk['cases'])
ax.set_xlabel("Date")
ax.set_ylabel("Daily Cases")
st.pyplot(fig)

#Interactive plot
#Chart 2
st.header('Ploty Interactive charts')
y_axis_val = st.selectbox("Select country", options = DEFAULT_TICKERS)
#y_axis_val2 = st.selectbox("Change country", options = DEFAULT_TICKERS)
plot = px.scatter(df_uk, x='dates', y=df_all["cases"].loc[(df_all['country']==y_axis_val )])
#plot = px.line(df_uk, x='dates', y=df_all["cases"].loc[(df_all['country']==y_axis_val )])
col = st.color_picker('Change plot color Here')
plot.update_traces(marker=dict(color=col))
st.plotly_chart(plot)

#Chart 3
st.header('Line Chart of Daily Covid cases, with Plotly Visualisation Library')
plot2 = px.line(df_uk, x='dates', y=df_all["cases"].loc[(df_all['country']==y_axis_val)])
st.plotly_chart(plot2)

#Chart 3
st.header('Line Chart of Daily Covid cases, with Plotly Visualisation Library')
plot3 = px.bar(df_uk, x='dates', y='cases' )
st.plotly_chart(plot3)

#Ading Sidebar
with st.sidebar:
    st.subheader('Project Artefacts')
    st.button('Static Visualisation2')
    st.button('Interactive Visualisation2')
    st.button('Animation2')
    st.button('Covid Dashboard2')
