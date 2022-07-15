import altair as alt
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import pydeck as pdk
import numpy as np

st.set_page_config(layout="wide")

# Data
dfn = pd.read_csv('https://raw.githubusercontent.com/HelenIfedi/Bokeh_covid_artefact/main/covid_proj_data3.csv')

dfn.dropna(subset=['Lat', 'Long'], inplace=True)
dfn.drop(['Lat', 'Long'], axis=1, inplace=True)

df_all = pd.melt(dfn, id_vars=['country'], value_vars=dfn.columns[1:])
df_all.rename(columns={'variable': 'dates', 'value': 'cases'}, inplace=True)
df_all['dates'] = pd.to_datetime(df_all['dates'])
DEFAULT_TICKERS = df_all['country'].unique()
#country
country_select = "United Kingdom"
df_uk = df_all[["dates", "cases", "country"]].loc[(df_all['country']==country_select)]
uk_ind = df_uk.loc[df_uk["dates"]=='2022-01-31'].index
df_uk.loc[uk_ind[0], "cases"]=int(df_uk["cases"].mean())

df_all3 = df_all[["dates", "cases", "country"]].loc[(df_all['country']=="US") | (df_all['country']=="United Kingdom")| (df_all['country']=="Spain" )]
df_all3l = pd.pivot(df_all3, index="dates", columns="country", values="cases")

suu = {"index" : [50, 51, 52, 53, 54, 55, 56, 57, 58, 59],
          "dates": ['2020-03-12','2020-03-13','2020-03-14','2020-03-15','2020-03-16','2020-03-17','2020-03-18',
                    '2020-03-19','2020-03-20', '2020-03-21'],
          "Spain" : [0, 2955, 1159, 1407, 2144, 1806, 2162, 4053, 2447, 4964],
          "US" : [439, 633, 759, 234, 1467, 1833, 2657, 4494, 6367, 5995],
          "United Kingdom" : [489, 479, 364, 442, 612, 768, 999, 1055, 1254, 1197]}

df_suu=pd.DataFrame(suu)

dfn2 = pd.read_csv('https://raw.githubusercontent.com/HelenIfedi/Bokeh_covid_artefact/main/covid_proj_data3.csv',
                  index_col='country')


#Row B
st.write('# Python for Visualisation') #st.title('')
#st.markdown("<h1 style='text-align: center; color: LightBlue;'>Python for Visualisation2</h1>", unsafe_allow_html=True)
st.markdown('''
This dashboard shows *different plot type* of several python libraries  
Data source: [Github: The Center for Systems Science and Engineering (CSSE) at JHU ](https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_time_series)
''')

#Navigation Buttons
#Row A
b1, b2 = st.columns(2)
b1.write('## Animation')
b1.markdown('[Click here to see Animated Artefact](http://143.198.68.242:5006/bokeh_animation7b)')
b2.write('## Covid Dashboard')
b2.markdown('[Click here to see Covid Dashboard](http://128.199.40.42:5006/bokeh_app_deploy2)')



#Row C
c1, c2 = st.columns(2)
#Chart 3
#st.header('Line Chart of Daily Covid cases, with Plotly')
plot2 = px.line(df_uk, x='dates', y=df_all["cases"].loc[(df_all['country']=="United Kingdom")],
                title='Line Chart of Daily Covid cases, with Plotly')
c1.plotly_chart(plot2)

#Chart 3
plot3 = px.bar(df_uk, x='dates', y='cases',
               title='Bar Chart of Daily Covid cases, with Plotly Visualisation Library' )
c2.plotly_chart(plot3)

#Row D
d1, d2 = st.columns(2)
#Chart 4
plot3 = px.line(df_all3l.iloc[50:100,:], title='Multi Line Chart of Daily Covid cases, Plotly')
d1.plotly_chart(plot3)

#Chart 5
plot4 = px.area(df_all3[:50], x="dates", y="cases", color="country", line_group="country",
                title='Area Chart Covid cases, Plotly')
#st.line_chart(df_all3l)
d2.plotly_chart(plot4)

#Row E
e1, e2 = st.columns(2)
#Chart 6
plot5 = px.bar(df_uk.iloc[50:55], x='dates', y='cases', title='Bar Chart of Covid cases, with Plotly')
e1.plotly_chart(plot5)

#Chart 7
plot6 = px.bar(df_all3.loc[(df_all3['dates']=='2021-01-30')|(df_all3['dates']=='2021-01-31')|
                           (df_all3['dates']=='2021-02-01')|(df_all3['dates']=='2021-02-02')|
                           (df_all3['dates']=='2021-02-03')], x="dates", y="cases", color="country",
               title="Stacked BarChart using Long-Form Input", text="country")
e2.plotly_chart(plot6)

#Row F
f1, f2 = st.columns(2)

#Chart 8
plot7 = px.bar(df_suu, x="dates", y="United Kingdom", color="Spain",
               title="Plotly Filtering with color",)
f1.plotly_chart(plot7)

#Chart 9
plot8 = px.histogram(df_all3[150:180], x="dates", y="cases", color='country', barmode='group', height=400,
                     title="Sum of cases recorded between aa date and previous date")
f2.plotly_chart(plot8)

#Row F
g1, g2 = st.columns(2)
#Chart 10
plot9 = px.histogram(df_all3[150:180], x="dates", y="cases", color='country', barmode='group', histfunc='avg', height=400,
                     title="The average of cases recorded between a date and previous date")
g1.plotly_chart(plot9)

#Chart 11
plot10 = go.Figure()
plot10.add_trace(go.Bar(x=df_suu.keys()[1:].to_list(), y=df_suu.iloc[8,1:].to_list(),
                base=((df_suu.iloc[8,1:])*(-1)).to_list(),
                marker_color='crimson',
                name='cases date1'))
plot10.add_trace(go.Bar(x=df_suu.keys()[1:].to_list(), y=df_suu.iloc[9,1:].to_list(),
                base=0,
                marker_color='lightslategrey',
                name='cases date2'
                ))
plot10.update_layout(title="The average of cases recorded, Showing different bases")
g2.plotly_chart(plot10)

i1, i2 = st.columns(2)
#Dual Axis Plot
plot12 = go.Figure()
plot12.add_trace(go.Scatter(x=df_suu['dates'], y=df_suu['US'],  name="UK cases"))
plot12.add_trace(go.Bar(x=df_suu['dates'], y=df_suu['United Kingdom'], name="US cases"))
plot12.update_layout(title="Dual Axis Plot of Cases in UK and US", yaxis_title="Cases Recorded",)
i1.plotly_chart(plot12)

#Pie Chart
plot13 = px.pie(dfn[4:10], values='1/4/22', names='country', title='Covid cases recorded in six countries')
i2.plotly_chart(plot13)

j1, j2 = st.columns(2)
#Sunburst Chart
sub_sectn=['St Martin', 'Wallis and Futuna', 'Sint Maarten','Isle of Man', 'British Virgin Islands', 'Jersey']
parents=['France', 'France', 'Netherlands', 'United Kingdom', 'United Kingdom', 'United Kingdom']
values=[10875,454,10537, 33821, 6941, 51792]
df_sunburst = pd.DataFrame(dict(sectors=sub_sectn, regions=parents, values=values) )
plot14 = px.sunburst(df_sunburst, path=['regions', 'sectors'], values='values', title="hierarchical Covid Cases Recorded on 6/24/22 ")
j1.plotly_chart(plot14)

#Sunburst Chart2
plot15 =go.Figure(go.Sunburst(
    labels=["United Kingdom", "British Virgin Islands", "Isle of Man", "Wolverhampton", "London", "Jersey", "Gibraltar", "Wolverhampton", "Channel Islands"],
    parents=["", "United Kingdom", "United Kingdom", "Isle of Man", "Isle of Man", "United Kingdom", "United Kingdom", "Gibraltar", "United Kingdom" ],
    values=[10, 14, 12, 10, 2, 6, 6, 4, 4],))
plot15.update_layout(margin = dict(t=0, l=0, r=0, b=0))
plot15.update_layout(title="hierarchical Covid Cases Recorded on 6/24/22 Design2")
j2.plotly_chart(plot15)

#Row K
k1, k2 = st.columns(2)
#Altair Charts2
chart_alt = alt.Chart(df_all3[150:200]).mark_circle().encode(
     x='dates', y='cases', color='country', size='country', tooltip=['cases', 'country'], ).properties(
    title="Altair Scatter Chart")
st.altair_chart(chart_alt, use_container_width=True)

#Heatmap Plotly
data = [df_suu.iloc[:,2].to_list(), df_suu.iloc[:,3].to_list(),df_suu.iloc[:,4].to_list(),
        [0, 1380, 808, 30, 2134, 1019, 1391, 1828, 1741, 1670],
        [48, 57, 49, 61, 70, 80, 79, 99, 140, 94]]
fig3 = px.imshow(data,
                 labels=dict(x="Dates of Recorded Cases",  color="Cases"),
                 x=df_suu.iloc[:,1].to_list(),
                 y=['Spain', 'US', 'UK', 'France', 'Canada']
                 )
fig3.update_xaxes(side="top")
st.plotly_chart(fig3)

#Funnel Chart
plot11 = px.funnel(df_suu, x='United Kingdom', y='dates',
                   title="Funnel Chart of Covid Cases Recorded on Different dates")
st.plotly_chart(plot11)




#Row L
#l1, l2 = st.columns(2)
#Mapbox with plotly
plot16 = px.scatter_mapbox(dfn2,
                         lon=dfn2['Long'],
                         lat = dfn2['Lat'],
                         zoom =0.5,
                         size = dfn2['1/4/22'],
                         width =700,
                         height=525,
                         title='Mapbox Covid cases map with plotly'
                         )
plot16.update_layout(mapbox_style = 'open-street-map')
plot16.update_layout(margin={"r":0, "t":50, "l":0, "b":10})
#fig2.show()
st.plotly_chart(plot16)

#Pydeck Map
st.markdown('Pydeck 3D Chart , displayed with Mapbox')
df = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon'])

st.pydeck_chart(pdk.Deck(
     map_style='mapbox://styles/mapbox/light-v9',
     initial_view_state=pdk.ViewState(
         latitude=37.76,
         longitude=-122.4,
         zoom=11,
         pitch=50,
     ),
     layers=[
         pdk.Layer(
            'HexagonLayer',
            data=df,
            get_position='[lon, lat]',
            radius=200,
            elevation_scale=4,
            elevation_range=[0, 1000],
            pickable=True,
            extruded=True,
         ),
         pdk.Layer(
             'ScatterplotLayer',
             data=df,
             get_position='[lon, lat]',
             get_color='[200, 30, 0, 160]',
             get_radius=200,
         ),
     ],
 ))
#Pydeck Map
dfn2.dropna(subset = ['Lat', 'Long'], inplace=True)

st.pydeck_chart(pdk.Deck(
     map_style='mapbox://styles/mapbox/light-v9',
     initial_view_state=pdk.ViewState(
         latitude=39,
         longitude=35,
         zoom=1,
         pitch=50,
     ),
     layers=[
         pdk.Layer(
            'ColumnLayer',
            data=dfn2,
            get_position='[Long, Lat]',
            get_elevation='1/4/22',
            radius=200_000,
            get_fill_color=[255, 165, 0, 80],
            elevation_scale=100,
            #elevation_range=[0, 1000],
            pickable=True,
            #extruded=True,
            auto_highlight=True,
         ),

     ],
 ))
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
plot = px.scatter(df_uk, x='dates', y=df_all["cases"].loc[(df_all['country']==y_axis_val)])
col = st.color_picker('Change plot color Here')
plot.update_traces(marker=dict(color=col))
st.plotly_chart(plot)
