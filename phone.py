import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import pymysql
from PIL import Image
import pandas as pd
#import geopandas as gpd
import plotly.figure_factory as ff
myconnect = pymysql.connect(host="127.0.0.1",user='root',passwd='sv2002..',database='phonepe')
cue=myconnect.cursor() 
with st.sidebar:
    selected = option_menu(None, ["Home","Aggregated","Map","Top"],
                           default_index=0,
                           orientation="vertical",
                           styles={"nav-link": {"font-size": "20px", "text-align": "centre", "margin": "2px", 
                                                "--hover-color": "#8e44ad"},
                                   "icon": {"font-size": "30px"},
                                   "container" : {"max-width": "6000px"},
                                   "nav-link-selected": {"background-color": "#8e44ad "}})
if selected == 'Home':
    st.markdown('<p style="color: purple; font-size: 42px; font-weight: bold;">PhonePe Pulse Data Visualization</p>', unsafe_allow_html=True)
    st.markdown(
        "Welcome to PhonePe Pulse Data Visualization. This app provides insightful analysis and visualization of "
        "transaction data from the PhonePe digital payment platform."
    )
    i = Image.open(r"D:\project\phone\phone.jpg")
    st.image(i,width=700)
    st.write("\n")
    st.markdown('<p style="color: purple; font-size: 23px; font-weight: bold;">How could use this PhonePe Pulse Data Visualization</p>', unsafe_allow_html=True)
    st.write("**Payment category Analysis**: Users can analyze payment categories based on regions, years, and transaction categories. This analysis helps understand the popularity and trends of different payment categories in specific regions and over time. It can be useful for businesses and individuals to identify the most common types of transactions in different areas.")
    st.write('\n')
    st.write("**Map Transaction Analysis**: Users can analyze transactions based on regions and years. This feature allows users to explore transaction patterns and volumes in specific regions and track their changes over time.")
    st.write('\n')
    st.write("**User Activity**: Users can analyze user activity based on locations and years. This feature provides insights into user registrations and app opens in different locations. ")
    st.write('\n')
    st.write("**Top Locations based on Transaction data**:  Users can analyze the top locations based on transaction data. The app allows users to select a specific year, quarter, and region to identify the top-performing locations in terms of transaction counts.")
    st.write('\n')
    st.write("**Top Locations based on User activity data**: Users can analyze the top locations based on user activity data. By selecting a specific year, quarter, and region, users can identify the locations with the highest number of registered users. ")
if selected =='Aggregated':
    agg = st.selectbox("**From aggregated:**",['Transaction',"User"])
    if agg == "Transaction":
        st.markdown('<p style="color: purple; font-size: 20px; font-weight: bold;">Overview of table</p>', unsafe_allow_html=True)
        df = pd.read_sql_query("select * from agg_tran",myconnect)
        st.write(df)
        col1,col2,col3 = st.columns(3,gap= 'medium')
        col1.markdown("Years")
        df1 = pd.read_sql_query("select Year from agg_tran group by Year",myconnect)
        col1.write(df1)
        df2 = pd.read_sql_query("select state from agg_tran group by State",myconnect)
        col2.markdown("States")
        col2.write(df2)
        df3 = pd.read_sql_query("select transacion_type as 'Transaction type' from agg_tran group by transacion_type",myconnect)
        col3.markdown('Transaction type')
        col3.write(df3)
        fig = px.scatter(df, x='Year', y='State', animation_frame='Year',
                 animation_group='Transacion_count', size='Transacion_amount',
                 color='State', hover_name='State', range_x=[df['Year'].min(), df['Year'].max()],
                 range_y=[df['State'].min(), df['State'].max()])
        fig.update_layout(title='Animated Scatter Plot of Transaction Data',
                  xaxis_title='Year', yaxis_title='State')
        st.plotly_chart(fig)
        col4,col5= st.columns(2,gap= 'medium')
        r = col4.radio("***Select the option for visualize***",["State","Year","Transacion_type"])
        r1 = col5.radio("***Select the option for visualize***",['Transacion_count','Transacion_type','Transacion_amount','Year',"State"])
        if r1 == r :
            q1 = f'select {r} from agg_tran group by {r}'
            df5 = pd.read_sql_query(q1,myconnect)
            col4.write("\n")
            col4.write("\n")
            col4.write(df5)
        else:
            q = f"select {r},{r1} from agg_tran"
            df4 = pd.read_sql_query(q,myconnect)
            col4.write("\n")
            col4.write(df4) 
            vi = px.bar(df,x=r,y=r1,color='State')
            col5.plotly_chart(vi)
    if agg == "User":
        st.markdown('<p style="color: purple; font-size: 20px; font-weight: bold;">Overview of table</p>', unsafe_allow_html=True)
        df = pd.read_sql_query("select * from agg_user",myconnect)
        st.write(df)
        col1,col2,col3 = st.columns(3,gap= 'medium')
        df1=pd.read_sql_query("select state from agg_user group by state",myconnect)
        col1.write(df1)
        df2 = pd.read_sql_query("select year from agg_user group by year",myconnect)
        col2.write(df2)
        df3 = pd.read_sql_query("select brand from agg_user group by brand",myconnect)
        col3.write(df3)
        fig = px.scatter(df, x='year', y='count', animation_frame='year',
                 animation_group='state', color='brand', size='percentage',
                 hover_name='state', range_x=[df['year'].min(), df['year'].max()],
                 range_y=[df['count'].min(), df['count'].max()])
        fig.update_layout(title='Animated Scatter Plot of Data',
                  xaxis_title='Year', yaxis_title='Count')
        st.plotly_chart(fig)
        col4,col5= st.columns(2,gap= 'medium')
        r = col4.radio("***Select anyone for visualize***",["state","year","brand"])
        r1 = col5.radio("***Select anyone for visualize***",['state','year','brand','count','percentage'])
        if r == r1:
            q1 = f'select {r} from agg_user group by {r}'
            df5 = pd.read_sql_query(q1,myconnect)
            col4.write("\n")
            col4.write("\n")
            col4.write(df5)
        else:
            q = f"select {r},{r1} from agg_user"
            df4 = pd.read_sql_query(q,myconnect)
            col4.write("\n")
            col4.write(df4) 
            vi = px.bar(df,x=r,y=r1,color='state')
            col5.plotly_chart(vi)
if selected == "Top":
    top = st.selectbox("***From top***",['Top transaction based on district','Top transaction based on pincode','Top user based on district','Top user based on pincode'])
    if top == 'Top transaction based on district':
        st.markdown('<p style="color: purple; font-size: 20px; font-weight: bold;">Overview of table</p>', unsafe_allow_html=True)
        df = pd.read_sql_query("select * from top_trans_dis",myconnect)
        st.write(df)
        col1,col2,col3 = st.columns(3,gap= 'medium')
        df1 = pd.read_sql_query("select state as 'The district phonepe has been used' from top_trans_dis group by state",myconnect)   
        col1.write(df1)     
        df2 = pd.read_sql_query("select year as Year from top_trans_dis group by year",myconnect)
        col2.write(df2)
        df3 = pd.read_sql_query("select districts as Districts from top_trans_dis group by districts",myconnect)
        col3.write(df3)
        fig = px.scatter(df,x="year",y="registeredUsers",color='state',animation_frame='year',size = 'amount',animation_group='state',hover_name='districts',range_x=[df['year'].min(), df['year'].max()],
                 range_y=[df['registeredUsers'].min(), df['registeredUsers'].max()])
        st.plotly_chart(fig)
        col4,col5= st.columns(2,gap= 'medium')
        r = col4.radio("***Select any option for visualize***",['state','year'])
        r1 = col5.radio("***Select any option for visualize***",['districts','registeredUsers','amount'])
        if r == r1:
            q1 = f'select {r} from top_trans_dis group by {r}'
            df5 = pd.read_sql_query(q1,myconnect)
            col4.write("\n")
            col4.write("\n")
            col4.write(df5)
        else:
            q = f"select {r},{r1} from top_trans_dis"
            df4 = pd.read_sql_query(q,myconnect)
            col4.write("\n")
            col4.write(df4) 
            vi = px.bar(df,x=r,y=r1,color='state')
            col5.plotly_chart(vi)
    if top == 'Top transaction based on pincode':
        st.markdown('<p style="color: purple; font-size: 20px; font-weight: bold;">Overview of table</p>', unsafe_allow_html=True)
        df = pd.read_sql_query("select * from top_trans_pin",myconnect)
        st.write(df)
        col1,col2,col3 = st.columns(3,gap= 'medium')
        df1 = pd.read_sql_query("select state from top_trans_pin group by state",myconnect)
        col1.write(df1)
        df2 = pd.read_sql_query("select year from top_trans_pin group by year",myconnect)
        col2.write(df2)
        df3 = pd.read_sql_query("select Pincode from top_trans_pin group by Pincode",myconnect)
        col3.write(df3)
        fig = px.scatter(df,x="year",y="count",color='state',animation_frame='year',size = 'amount',animation_group='state',hover_name='Pincode',range_x=[df['year'].min(), df['year'].max()],
                 range_y=[df['count'].min(), df['count'].max()])
        st.plotly_chart(fig)
        col4,col5= st.columns(2,gap= 'medium')
        r = col4.radio("***Select any option to visualize***",['state','year'])
        r1 = col5.radio("***Select any option to visualize***",['Pincode','count','amount'])
        q = f"select {r},{r1} from top_trans_pin"
        df5 = pd.read_sql_query(q,myconnect)
        col4.write(df5)
        vi = px.bar(df,x=r,y=r1,color='state')
        col5.plotly_chart(vi)
    if top == 'Top user based on district':
        st.markdown('<p style="color: purple; font-size: 20px; font-weight: bold;">Overview of table</p>', unsafe_allow_html=True)
        df = pd.read_sql_query("select * from top_user_dis",myconnect)
        st.write(df)
        col1,col2,col3 = st.columns(3,gap= 'medium')
        df1 = pd.read_sql_query("select state from top_user_dis group by state",myconnect)
        col1.write(df1)
        df2 = pd.read_sql_query("select year from top_user_dis group by year",myconnect)
        col2.write(df2)
        df3 = pd.read_sql_query("select districts from top_user_dis group by districts",myconnect)
        col3.write(df3)
        fig = px.scatter(df,x="year",y="registeredUsers",color='state',animation_frame='year',animation_group='state',hover_name='districts',range_x=[df['year'].min(), df['year'].max()],
                 range_y=[df['registeredUsers'].min(), df['registeredUsers'].max()])
        st.plotly_chart(fig)
        col4,col5= st.columns(2,gap= 'medium')
        r = col4.radio("***Select any option to visualize***",['state','year'])
        r1 = col5.radio("***Select any option to visualize***",['districts','registeredUsers'])
        q = f"select {r},{r1} from top_user_dis"
        df5 = pd.read_sql_query(q,myconnect)
        col4.write(df5)
        vi = px.bar(df,x=r,y=r1,color='state')
        col5.plotly_chart(vi)
    if top =="Top user based on pincode":
        st.markdown('<p style="color: purple; font-size: 20px; font-weight: bold;">Overview of table</p>', unsafe_allow_html=True)
        df = pd.read_sql_query("select * from top_user_pin",myconnect)
        st.write(df)
        col1,col2,col3 = st.columns(3,gap= 'medium')
        df1 = pd.read_sql_query("select state from top_user_pin group by state",myconnect)
        col1.write(df1)
        df2 = pd.read_sql_query("select year from top_user_pin group by year",myconnect)
        col2.write(df2)
        df3 = pd.read_sql_query("select pincode from top_user_pin group by pincode",myconnect)
        col3.write(df3)
        fig = px.scatter(df,x="year",y="registeredUsers",color='state',animation_frame='year',animation_group='state',hover_name='pincode',range_x=[df['year'].min(), df['year'].max()],
                 range_y=[df['registeredUsers'].min(), df['registeredUsers'].max()])
        st.plotly_chart(fig)
        col4,col5= st.columns(2,gap= 'medium')
        r = col4.radio("***Select any option to visualize***",['state','year'])
        r1 = col5.radio("***Select any option to visualize***",['pincode','registeredUsers'])
        q = f"select {r},{r1} from top_user_pin"
        df5 = pd.read_sql_query(q,myconnect)
        col4.write(df5)
        vi = px.bar(df,x=r,y=r1,color='state')
        col5.plotly_chart(vi)
if selected == "Map":
    mp = st.selectbox("**From Map:**",['Transaction',"User"])
    if mp == 'Transaction':
        st.markdown('<p style="color: purple; font-size: 20px; font-weight: bold;">Overview of table</p>', unsafe_allow_html=True)
        df = pd.read_sql_query("select * from map_tran",myconnect)
        st.write(df)
        col1,col2,col3= st.columns(3,gap= 'medium')
        df1 = pd.read_sql_query("select year from map_tran group by year",myconnect)
        col1.write(df1)
        df2 = pd.read_sql_query("select state from map_tran group by state",myconnect)
        col2.write(df2)
        df3 = pd.read_sql_query("select district from map_tran group by district",myconnect)
        col3.write(df3)
        m = pd.read_csv(r"D:\project\phone\map.csv")
        #st.plotly_chart(fig.show())
        ma = st.selectbox("Select anyone for Map visualize",['Map Transcation based in amount','Map transcation based on count'])
        st.markdown('<p style="color: purple; font-size: 20px; font-weight: bold;">Map of data</p>', unsafe_allow_html=True)
        if ma == 'Map Transcation based in amount':
            fig = px.choropleth(m,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",featureidkey='properties.ST_NM',locations='state',color='amount',color_continuous_scale='Reds')
            st.plotly_chart(fig.update_geos(fitbounds="locations", visible=False))
        if ma =='Map transcation based on count':
            fig = px.choropleth(m,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",featureidkey='properties.ST_NM',locations='state',color='count',color_continuous_scale='Reds')
            st.plotly_chart(fig.update_geos(fitbounds="locations", visible=False))
        st.markdown('<p style="color: purple; font-size: 20px; font-weight: bold;">Comparison of data</p>', unsafe_allow_html=True)
        col4,col5= st.columns(2,gap= 'medium')
        r = col4.radio("***Select any option to visualize***",['state','year','district'])
        r1 = col5.radio("***Select a option for visualize***",['transactions_done','transaction_value','district'])
        if r == r1:
            q1 = f'select {r} from map_tran group by {r}'
            df5 = pd.read_sql_query(q1,myconnect)
            col4.write("\n")
            col4.write("\n")
            col4.write(df5)
        else:
            q = f"select {r},{r1} from map_tran"
            df4 = pd.read_sql_query(q,myconnect)
            col4.write("\n")
            col4.write(df4) 
            vi = px.bar(df,x=r,y=r1,color='state')
            col5.plotly_chart(vi)
    if mp == 'User':
        st.markdown('<p style="color: purple; font-size: 20px; font-weight: bold;">Overview of table</p>', unsafe_allow_html=True)
        col1,col2,col3= st.columns(3,gap= 'medium')
        df = pd.read_sql_query("select * from map_use",myconnect)
        st.write(df)
        col1,col2,col3= st.columns(3,gap= 'medium')
        df1 = pd.read_sql_query("select state from map_use group by state",myconnect)
        col1.write(df1)
        df2 = pd.read_sql_query("select distirct from map_use group by distirct",myconnect)
        col2.write(df2)
        df3 = pd.read_sql_query("select year from map_use group by year",myconnect)
        col3.write(df3)
        p = pd.read_csv(r"D:\project\phone\map_u.csv")
        ma = st.selectbox("Select anyone for Map visualize",['Map User based in amount','Map User based on count'])
        st.markdown('<p style="color: purple; font-size: 20px; font-weight: bold;">Map of data</p>', unsafe_allow_html=True)
        if ma == 'Map User based in amount':
            fig = px.choropleth(p,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",featureidkey='properties.ST_NM',locations='state',color='open',color_continuous_scale='Reds')
            st.plotly_chart(fig.update_geos(fitbounds="locations", visible=False))
        if ma =='Map User based on count':
            fig = px.choropleth(p,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",featureidkey='properties.ST_NM',locations='state',color='user',color_continuous_scale='Reds')
            st.plotly_chart(fig.update_geos(fitbounds="locations", visible=False))
        st.markdown('<p style="color: purple; font-size: 20px; font-weight: bold;">Comparison of data</p>', unsafe_allow_html=True)
        col4,col5= st.columns(2,gap= 'medium')
        r = col4.radio("***Select any option to visualize***",['state','year','distirct'])
        r1 = col5.radio("***Select a option for visualize***",['App_open','No_of_App_open','distirct'])
        if r == r1:
            q1 = f'select {r} from map_use group by {r}'
            df5 = pd.read_sql_query(q1,myconnect)
            col4.write("\n")
            col4.write("\n")
            col4.write(df5)
        else:
            q = f"select {r},{r1} from map_use"
            df4 = pd.read_sql_query(q,myconnect)
            col4.write("\n")
            col4.write(df4) 
            vi = px.bar(df,x=r,y=r1,color='state')
            col5.plotly_chart(vi)   