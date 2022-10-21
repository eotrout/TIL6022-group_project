

import streamlit as st
import pandas as pd
import chardet
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt
from datetime import datetime


#Creating different horizontal sections in the webpage
header = st.container() 
data= st.container()


with header:  # accesing the section for presenting the info
    st.title('Impact of Covid on Vessel waiting time') # prints the string  in the section as title

with data:# all the data is processed as 
    file_path1 = r'Data\covid_data.csv'
    file_path2 = r'Data\US_PortCalls_S_ST202209220924_v1.csv'

    df = pd.read_csv(file_path1)
    df = df.rename({'Date_reported': 'date','Country': 'country','New_cases': 'new_cases','Cumulative_cases': 'cumulative_cases'}, axis=1) 
    df = df.drop(labels=['New_deaths','Cumulative_deaths','Country_code','WHO_region'], axis=1)

    df_port = pd.read_csv(file_path2,encoding='utf-8')
    df_port = df_port.drop(columns=['Period Label','Year','Frequency', 'Frequency Label', 'Economy', 
                                      'CommercialMarket', 'Median time in port (days) Footnote',
                                      'Average age of vessels Footnote', 'Average size (GT) of vessels Footnote',
                                      'Maximum size (GT) of vessels Footnote', 'Average cargo carrying capacity (dwt) per vessel Footnote',
                                      'Maximum cargo carrying capacity (dwt) of vessels Footnote','Average container carrying capacity (TEU) per container ship Footnote',
                                      'Maximum container carrying capacity (TEU) of container ships Footnote'])
    df_port.rename(columns = {'Economy Label': 'country', 'CommercialMarket Label': 'Vessel_Type', }, inplace=True)

    for i in range(len(df)):
        k=df.iloc[i,0].split('-')
        df.iloc[i,0]=datetime(int(k[0]),int(k[1]),int(k[2]))

    df_new = (df.groupby(['country', pd.Grouper(key='date', freq='6M')]).max().reset_index())
    date_change=[]
    for row in df_port['Period']:
        if row == '2018S01' :   date_change.append(datetime(2018,7,31))
        elif row == '2018S02':   date_change.append(datetime(2019,1,31))
        elif row == '2019S01':  date_change.append(datetime(2019,7,31))
        elif row == '2019S02':  date_change.append(datetime(2020,1,31))
        elif row == '2020S01':  date_change.append(datetime(2020,7,31))
        elif row == '2020S02':  date_change.append(datetime(2021,1,31))
        elif row == '2021S01':  date_change.append(datetime(2021,7,31))
        elif row == '2021S02':  date_change.append(datetime(2022,1,31))
        elif row == '2022S01':  date_change.append(datetime(2022,7,31))
    
        else:      
            date_change.append('Not_Rated')


    df_port = df_port.drop(columns=['Period'])
    df_port['date'] = date_change
    df_combined=pd.merge(df_port,df_new,on=['country','date'],how = 'outer' )#Median port time and covid
    
    st.write(df.head(25)) # Displaying the data on the webpage
    
    
    
    port_col, covid_col =st.columns(2) # dividing the webpage in 2 columns so you can show covid graph and port graph next to each other
    
    #CREATING a dynamic multiselect box for user to choose countries from
    country_options = df_combined['country'].unique() #converting unqiue values to list,
    #[Note:(do not use tolist() if it's already a list), in our case, it's already a list, otherwise it would be df_combined['country'].tolist().unique())
    #This list will be used as options for multiselect for user to chhose which country data he wants to see
    
    # creating a multiselect toggle option for user to choose from country_options and setting the default option as Austrailia
    country= st.multiselect('Which country data would you like to see',country_options,['Australia']) 
    
    
    #CREATING a dynamic dropdown box for user to choose vessel types from
    vessel_options = df_combined['Vessel_Type'].unique()
    vessel = st.selectbox('Which Vessel data would you like to see',options =vessel_options,index=0)
    # index sets the default value at the index of the list that will be displayed if nothing is selected.
    
    
    
    #filetering the data according to user's choice in both options
    df=df_combined[(df_combined['country'].isin(country)) & (df_combined['Vessel_Type']==vessel)]
    #period_options = df['Period Label'].unique()
    #period = st.selectbox('Which period data would you like to see',options=period_options,index=0)
    
    
   # Accessing port_col vertical section of the webpage and plotting different port graphs
    with port_col:
        fig = px.line(df,x='date',y='Median time in port (days)',color='country',markers=True)
        fig.update_layout(width=400)
        st.write(fig)
        
        fig = px.line(df,x='date',y='Average age of vessels',color='country',markers=True)
        fig.update_layout(width=400)
        st.write(fig)
        
        fig = px.line(df,x='date',y='Average cargo carrying capacity (dwt) per vessel',color='country',markers=True)
        fig.update_layout(width=400)
        st.write(fig)
        
        fig = px.line(df,x='date',y='Average size (GT) of vessels',color='country',markers=True)
        fig.update_layout(width=400)
        st.write(fig)
        
        
        
        # Accessing covid_col vertical section of the webpage and plotting different covid graphs next to port graphs
    with covid_col:
        fig = px.line(df,x='date',y='new_cases',color='country',markers=True)
        fig.update_layout(width=400)
        st.write(fig)
        
        fig = px.line(df,x='date',y='new_cases',color='country',markers=True)
        fig.update_layout(width=400)
        st.write(fig)
        
        fig = px.line(df,x='date',y='new_cases',color='country',markers=True)
        fig.update_layout(width=400)
        st.write(fig)
        
        fig = px.line(df,x='date',y='new_cases',color='country',markers=True)
        fig.update_layout(width=400)
        st.write(fig)
        
# to run on the webpage : go to cmd go to the file path where this file is located using command 'cd'
#then type streamlit run port1.1.py