import pandas as pd
from osgeo import ogr,osr

"""
import reverse_geocoder as rg
import pprint

def reverseGeocode(coordinates):
    result = rg.search(coordinates)
    pprint.pprint(result[0].get('admin2'))


if __name__=="__main__": 
    coordinates =(42.8, -3.6) 
    reverseGeocode(coordinates)

"""

data = pd.read_csv('final.csv')

driver = ogr.GetDriverByName("ESRI Shapefile")
data_source = driver.CreateDataSource("/Users/nickramos/Desktop/Coding/seismos/seismos.shp")
srs = osr.SpatialReference() #WGS84
srs.ImportFromEPSG(4326)

layer = data_source.CreateLayer("Eventos Sismicos", srs, ogr.wkbPoint)

field_name = ogr.FieldDefn("Id", ogr.OFTString)
field_name.SetWidth(24)
layer.CreateField(field_name)
field_region = ogr.FieldDefn("Place", ogr.OFTString)
field_region.SetWidth(24)
layer.CreateField(field_region)
layer.CreateField(ogr.FieldDefn("Time", ogr.OFTDate))
layer.CreateField(ogr.FieldDefn("Latitude", ogr.OFTReal))
layer.CreateField(ogr.FieldDefn("Longitude", ogr.OFTReal))
layer.CreateField(ogr.FieldDefn("Mag", ogr.OFTReal))
layer.CreateField(ogr.FieldDefn("Depth", ogr.OFTReal))

for index,row in data.iterrows():
  feature = ogr.Feature(layer.GetLayerDefn())
  feature.SetField("Id", row['id'])
  feature.SetField("Place", row['place'])
  feature.SetField("Time", row['time'])
  feature.SetField("Latitude", row['latitude'])
  feature.SetField("Longitude", row['longitude'])
  feature.SetField("Mag", row['mag'])
  feature.SetField("Depth", row['depth'])
  wkt = "POINT(%f %f)" %  (float(row['longitude']) , float(row['latitude']))
  
  point = ogr.CreateGeometryFromWkt(wkt)
  feature.SetGeometry(point)
  layer.CreateFeature(feature)
  feature = None

data_source = None