import json
import pandas as pd
from pandas.io.json import json_normalize

from .base import SpatialDataset

class GeoJsonDataset(SpatialDataset):
    def __init__(self, source, properties=[]):
        super().__init__(source)
        print(self.source)
        if not len(properties):
            self.properties = ['name','amenity','cuisine',
                               'addr:housenumber',
                               'addr:street','addr:city',
                               'addr:state','addr:postcode']
        else:
            self.properties = properties
        self.df = self._read_geojson()


    def _read_geojson(self):
        '''
        Read a GeoJSON file into a dataframe and drop rows with
        null geometry. Extract the latitude and longitude as
        separate columns from the geometry's coordinates
        '''
    
        with open(self.source) as f:
            stops_geodata = json.load(f)
        
        df = pd.DataFrame(json_normalize(stops_geodata['features']))
        n_rows_orig = df.shape[0]
        
        df.dropna(subset=["geometry.coordinates"], inplace = True, axis = 0)
        n_rows_clean = df.shape[0]
        print("Cleaning null geometries, eliminated ", n_rows_orig - n_rows_clean, 
            " rows out of the original ",n_rows_orig, " rows")
        
        df['longitude'] = df["geometry.coordinates"].apply(lambda x: x[0]) 
        df['latitude'] = df["geometry.coordinates"].apply(lambda x: x[1]) 
        
        selection = (['id', 'latitude', 'longitude'] +
            [f"properties.{p}" for p in self.properties])
        df = df[selection]
        return df