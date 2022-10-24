

import streamlit as st
import pandas as pd
import chardet
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt
from datetime import datetime
import geopandas as gpd


    


#Creating different horizontal sections in the webpage
header = st.container() 
data= st.container()


with header:  # accesing the section for presenting the info
    st.title('Impact of Covid on Vessel waiting time') # prints the string  in the section as title

with data:# all the data is processed as 
    ## DATA IMPORT
    #file_path1 = r'Data\covid_data.csv'
    #file_path2 = r'Data\US_PortCalls_S_ST202209220924_v1.csv'

    # port data
    portcalls_file_path = "Data/Maritime data/US_PortCalls_S_ST202209220924_v1.csv"
    with open(portcalls_file_path, 'rb') as rawdata:    
        result = chardet.detect(rawdata.read(100000))
    #result

    df_port = pd.read_csv(portcalls_file_path,encoding='utf-8') # Reading the port data into 'df_ports'

    # port calls data
    portcalls_file_path_new = "Data/Maritime data/US_PortCallsArrivals_S_ST202209220927_v1.csv"
    df_port_calls = pd.read_csv(portcalls_file_path_new ,encoding='utf-8')

    # covid Data
    covid_file_path = "Data\COVID data\WHO-COVID-19-global-data.csv"
    df_covid = pd.read_csv(covid_file_path) # Reading the covid data into 'df_covid'

    # Geo data
    df_geo = gpd.read_file("Data/countries.geojson") # geojson file
    df_geo.rename(columns = {'ADMIN': 'Location', }, inplace=True)

    # Port Performance Data
    performance_path = "Data/The productivity of the ports/Container-Port-Performance-Index-2021 copy.csv"
    df_performance = pd.read_csv(performance_path)



    # Port Performance Data
    performance_path = "Data/The productivity of the ports/Container-Port-Performance-Index-2021 copy.csv"
    df_performance = pd.read_csv(performance_path)


    # DATA PROCESSING:
    # Firstly, we remove all the unnecessary fields from the data set.
    df_port = df_port.drop(columns=['Period Label','Frequency', 'Frequency Label', 'Economy', 
                                        'CommercialMarket', 'Median time in port (days) Footnote',
                                        'Average age of vessels Footnote', 'Average size (GT) of vessels Footnote',
                                        'Maximum size (GT) of vessels Footnote', 'Average cargo carrying capacity (dwt) per vessel Footnote',
                                        'Maximum cargo carrying capacity (dwt) of vessels Footnote','Average container carrying capacity (TEU) per container ship Footnote',
                                        'Maximum container carrying capacity (TEU) of container ships Footnote'])
    # we rename the column name to be easily recognizable.
    df_port.rename(columns = {'Economy Label': 'country', 'CommercialMarket Label': 'Vessel_Type', }, inplace=True)

    # the time frame in the Period column is modified to match with the date column of the covid data.
    date_change=[]
    for row in df_port['Period']:
        if row == '2018S01' :   
            date_change.append(datetime(2018,7,31))
        elif row == '2018S02':  
            date_change.append(datetime(2019,1,31))
        elif row == '2019S01':  
            date_change.append(datetime(2019,7,31))
        elif row == '2019S02':  
            date_change.append(datetime(2020,1,31))
        elif row == '2020S01':  
            date_change.append(datetime(2020,7,31))
        elif row == '2020S02':  
            date_change.append(datetime(2021,1,31))
        elif row == '2021S01':  
            date_change.append(datetime(2021,7,31))
        elif row == '2021S02':  
            date_change.append(datetime(2022,1,31))
        elif row == '2022S01':  
            date_change.append(datetime(2022,7,31))
        
        else:           
            date_change.append('Not_Rated')

    # 'Period column is removed as it has no importance in future processes and column 'date' is added
    # df_port = df_port.drop(columns=['Period'])
    df_port['date'] = date_change


    # Port Calls Data

    df_port_calls['Period Label'] = df_port_calls['Period Label'].str.replace('   ','-')
    df_port_calls = df_port_calls.drop(columns=['Period', 'Frequency', 'Frequency Label', 'Economy', 
                                        'CommercialMarket', 'Number of port calls Footnote',])
    df_port_calls.rename(columns = {'Economy Label': 'country', 'CommercialMarket Label': 'Vessel_Type', }, inplace=True)
    date_change=[]
    for row in df_port_calls['Period Label']:
        if row == 'S1-2018' :   
            date_change.append(datetime(2018,7,31))
        elif row == 'S2-2018':   
            date_change.append(datetime(2019,1,31))
        elif row == 'S1-2019':  
            date_change.append(datetime(2019,7,31))
        elif row == 'S2-2019':  
            date_change.append(datetime(2020,1,31))
        elif row == 'S1-2020':  
            date_change.append(datetime(2020,7,31))
        elif row == 'S2-2020':  
            date_change.append(datetime(2021,1,31))
        elif row == 'S1-2021':  
            date_change.append(datetime(2021,7,31))
        elif row == 'S2-2021':  
            date_change.append(datetime(2022,1,31))
        elif row == 'S1-2022':  
            date_change.append(datetime(2022,7,31))
        else:           
            date_change.append('Not_Rated')

    df_port_calls = df_port_calls.drop(columns=['Period Label'])
    df_port_calls['date'] = date_change
    df_port_calls

    #Covid Data

    df_covid = df_covid.rename({
    'Date_reported': 'date',
    'Country': 'country',
    'New_cases': 'new_cases',
    'Cumulative_cases': 'cumulative_cases'}, axis=1) 
    df_covid = df_covid.drop(labels=[
        'New_deaths', 
        'Cumulative_deaths', 
        'Country_code', 
        'WHO_region'], axis=1)

    for i in range(len(df_covid)):
        k=df_covid.iloc[i,0].split('/')
        df_covid.iloc[i,0]=datetime(int(k[0]),int(k[1]),int(k[2]))

    df_covid_new = (df_covid.groupby(['country', pd.Grouper(key='date', freq='6M')])
            .max() # gives the max value of the cumulative cases. IMP: To find 'new cases trend', use 'sum()'
            .reset_index())

    #GEO DATA:
    df_geo.rename(columns = {'Location': 'country', }, inplace=True)

    #Performance data:
    df_performance.rename(columns = {'Economy Label': 'country', }, inplace=True)
    
    #Merging Port data and Geo data:
    geo_port = pd.merge(df_geo, df_port, on = 'country')

    # Merging of port data and the covid data
    port_covid = pd.merge(df_port, df_covid_new, on=['country','date'], how='outer')
    df_combined2 =pd.merge(df_port_calls,df_covid_new,on=['country','date'], how='outer')# merging port call and covid data

    #Merging port calls data with covid data
    df_port_calls_world = df_port_calls[df_port_calls.country == 'World']
    df_covid_world = df_covid_new.groupby('date').sum()
    df_covid_world = df_covid_world.drop(['2020-01-31','2023-01-31'])

    df_combined_world_calls = pd.merge(df_port_calls_world, df_covid_world, on=['date'], how='outer')
    df_combined_world_calls

    #Filtering port covid data for the world to analyze corelation between median time and covid case in a world scale

    df_ports_world = df_port[df_port.country == 'World']
    df_covid_world = df_covid_new.groupby('date').sum()
    df_covid_world = df_covid_world.drop(['2020-01-31','2023-01-31'])


    df_combined_world =pd.merge(df_ports_world, df_covid_world, on=['date'], how='outer')

   #Merging the port data and the performance data
   #still work in progress
   
   





    st.write(port_covid.head(25))
    st.write(df_combined2.head(25))# Displaying the data on the webpage
    
    
    
    port_col, covid_col =st.columns(2) # dividing the webpage in 2 columns so you can show covid graph and port graph next to each other
    
    #CREATING a dynamic multiselect box for user to choose countries from
    country_options = port_covid['country'].unique() #converting unqiue values to list,
    #[Note:(do not use tolist() if it's already a list), in our case, it's already a list, otherwise it would be df_combined['country'].tolist().unique())
    #This list will be used as options for multiselect for user to chhose which country data he wants to see
    
    # creating a multiselect toggle option for user to choose from country_options and setting the default option as world
    country= st.multiselect('Which country data would you like to see',country_options,['Netherlands']) 
    
    
    #CREATING a dynamic dropdown box for user to choose vessel types from
    vessel_options = port_covid['Vessel_Type'].unique()
    vessel = st.selectbox('Which Vessel data would you like to see',options =vessel_options,index=0)
    # index sets the default value at the index of the list that will be displayed if nothing is selected.
    
    
    
    #filetering the data according to user's choice in both options
    df=port_covid[(port_covid['country'].isin(country)) & (port_covid['Vessel_Type']==vessel)]
    #period_options = df['Period Label'].unique()
    #period = st.selectbox('Which period data would you like to see',options=period_options,index=0)
    
    dp=df_combined2[(df_combined2['country'].isin(country)) & (df_combined2['Vessel_Type']==vessel)]
    
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
        
        fig = px.line(dp,x='date',y='Number of port calls',color='country',markers=True)
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
        
        fig = px.line(dp,x='date',y='new_cases',color='country',markers=True)
        fig.update_layout(width=400)
        st.write(fig)
        
        
# to run on the webpage : go to cmd go to the file path where this file is located using command 'cd'
#then type streamlit run port1.1.py