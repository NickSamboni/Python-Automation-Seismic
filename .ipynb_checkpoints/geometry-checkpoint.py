import pandas as pd
from osgeo import ogr,osr
import os

coordx=[]
coordy=[]
data = pd.read_csv('final.csv')
for lat in data['latitude']:
    x=round(lat,6)
    coordx.append(x)
for lon in data['longitude']:
    y=round(lon,6)
    coordy.append(y)
df = pd.DataFrame(list(zip(coordx, coordy)),columns =['latitud', 'longitud']) 
print(df.shape)

spatialRef1 = osr.SpatialReference()
spatialRef1.ImportFromEPSG(4326)

# Input data
fieldName = 'test'
fieldType = ogr.OFTString
fieldValue = 'test'
outSHPfn = 'Seismos.shp'

# Create the output shapefile
shpDriver = ogr.GetDriverByName("ESRI Shapefile")
if os.path.exists(outSHPfn):
    shpDriver.DeleteDataSource(outSHPfn)
outDataSource = shpDriver.CreateDataSource(outSHPfn)
outLayer = outDataSource.CreateLayer(outSHPfn,spatialRef1, geom_type=ogr.wkbPoint )

# create a field
idField = ogr.FieldDefn(fieldName, fieldType) #estas dos lineas son necesarias segun el numero de atributos
outLayer.CreateField(idField)

# Create the feature and set values
for index,row in df.iterrows():
    point=ogr.Geometry(ogr.wkbPoint)
    point.AddPoint(row[1],row[0])
    ptos=point.ExportToWkt()
    geom=ogr.CreateGeometryFromWkt(ptos)
    #point.Transform(trans)
    featureDefn = outLayer.GetLayerDefn()
    outFeature = ogr.Feature(featureDefn)
    outFeature.SetGeometry(point)
    outFeature.SetField(fieldName, fieldValue)
    outLayer.CreateFeature(outFeature)
    outFeature = None
