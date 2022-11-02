import streamlit as st
import pandas as pd
import chardet
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt

header = st.container()
data= st.container()

with header:
    st.title('Impact of Covid on Vessel waiting time')

with data:
    st.header('Dataset')
    #st.text()
    #st.subhead()
    file_path = r"Data/US_PortCalls_S_ST202209220924_v1.csv"
    df = pd.read_csv(file_path,encoding='utf-8')
    df['Period Label'] = df['Period Label'].str.replace('   ','-')
    df = df.drop(columns=['Period', 'Frequency', 'Frequency Label', 'Economy', 
                                      'CommercialMarket', 'Median time in port (days) Footnote',
                                      'Average age of vessels Footnote', 'Average size (GT) of vessels Footnote',
                                      'Maximum size (GT) of vessels Footnote', 'Average cargo carrying capacity (dwt) per vessel Footnote',
                                      'Maximum cargo carrying capacity (dwt) of vessels Footnote','Average container carrying capacity (TEU) per container ship Footnote',
                                      'Maximum container carrying capacity (TEU) of container ships Footnote'])
    df.rename(columns = {'Economy Label': 'Location', 'CommercialMarket Label': 'Vessel_Type', }, inplace=True)
    df=df[['Period Label','Location','Median time in port (days)','Vessel_Type']]
    st.write(df.head(25))
    
    #country_options = sel_col.selectbox('What country data would you like to see',options = ['India','China','Netherlands','dataframe'],index =3)
    # index sets the default value at the index of the list
    
    country_options = df['Location'].unique() #converting unqiue values to list, do not use tolis() if it's already a list
    #country= st.selectbox('Which country data would you like to see',options =country_options,index=0)
    country= st.multiselect('Which country data would you like to see',country_options,['World'])
    vessel_options = df['Vessel_Type'].unique()
    vessel = st.selectbox('Which Vessel data would you like to see',options =vessel_options,index=0)
    #df=df[(df['Location']==country) & (df['Vessel_Type']==vessel)]
    df=df[(df['Location'].isin(country)) & (df['Vessel_Type']==vessel)]
    #period_options = df['Period Label'].unique()
    #period = st.selectbox('Which period data would you like to see',options=period_options,index=0)
    fig = px.line(df,x='Period Label',y='Median time in port (days)',color='Location',markers=True)
    fig.update_layout(width=800)
    st.write(fig)


