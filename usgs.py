import schedule
import time
import urllib.request
import pandas as pd
import re

def scrapping():
    print('Starting....') #Mensaje de terminal 
    #URL del archivo donde se encuentran los datos
    url = 'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.csv'
    #Acceso al archivo de datos, descarga del archivo actual de la web
    urllib.request.urlretrieve(url,'HourlyData.csv')
    #Leer el archivo descargado,
    df = pd.read_csv('hourlydata.csv')
    print('file downloaded') #Mensaje de terminal
    #generamos archivo record de todos los cambios que haya en la web
    #si no existe se crea el archivo, si existe se van añadiendo datos 
    with open('record.csv','a') as f:
        df.to_csv(f,header=f.tell()==0)
    #Leemos el archivo record y depuramos los datos en formato dataframe Pandas
    #no duplicados, ordenar por tiempo, modificar indexacion 
    raw_data = pd.read_csv('record.csv').drop_duplicates(keep='first',subset=['latitude','longitude']).sort_values(by='time').reset_index(drop=True)
    print('record read successfully')  
    #Extraer datos segun el lugar (California) identificado en los datos de origen por (CA) dentro de la columna Place
    state=[]
    for row in raw_data['place']:
        x=re.split(',',row)
        state.append(x[-1])
    raw_data['state']=state
    #Eliminar una columna 'index' creada al escribir y leer un archivo csv
    index_names=raw_data[raw_data['state']!=' CA'].index
    #Eliminar columnas innecesarias
    raw_data.drop(columns=['Unnamed: 0','locationSource','magSource','status','magType','nst','gap','dmin','rms','net','magNst'],index=index_names).to_csv('final.csv')
    print('Process Done!') #Mensaje de terminal
    print('          ') #Mensaje de terminal

#Iterador de la funcion cada cierto tiempo (pudiendo expresarlo en hh,mm ó ss)  
schedule.every(15).minutes.do(scrapping)
while True:
    schedule.run_pending()
    time.sleep(2)
