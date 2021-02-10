from numpy.lib.function_base import place
import reverse_geocoder as rg
#import pprint
import pandas as pd 


def reverseGeocode(coordinates): 
    df = pd.read_csv('hourlydata.csv')
    result = rg.search(coordinates)
    places2=[]
    #pprint.pprint(result[0].get('admin2'))
    for row in df['place']:
        places2.append(result[0].get('admin2'))
    df['places2']=places2
    df.to_csv('final copy2.csv')

if __name__=="__main__": 
    coordx=[]
    coordy=[]
    data = pd.read_csv('hourlydata.csv')
    for lat in data['latitude']:
        x=round(lat,6)
        coordx.append(x)
    for lon in data['longitude']:
        y=round(lon,6)
        coordy.append(y)
    df = pd.DataFrame(list(zip(coordx, coordy)),columns =['latitud', 'longitud']) 
    for index,row in df.iterrows():
        coordinates =(row[0], row[1]) 
        reverseGeocode(coordinates)