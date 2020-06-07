"""
Module containing GeoJson Dataset
"""
import json
from collections import defaultdict
import pandas as pd
from pandas.io.json import json_normalize
from h3 import h3

from .base import SpatialDataset

class GeoJsonDataset(SpatialDataset):
    """
    Class for GeoJson Datasets
    """
    def __init__(self, source, properties=None, filter_values=None, h3_resolution=11,
                 ring_distance=2, index_col='id'):
        super().__init__(source, h3_resolution, ring_distance)
        if properties is None:
            self.properties = ['name', 'amenity','cuisine',
                               'addr:housenumber',
                               'addr:street', 'addr:city',
                               'addr:state', 'addr:postcode']
        else:
            self.properties = properties

        if filter_values is None:
            self.filter_values={}
        else:
            self.filter_values = filter_values

        self.index_col = index_col


        self.read_geojson()


    def read_geojson(self):
        '''
        Read a GeoJSON file into a dataframe and drop rows with
        null geometry. Extract the latitude and longitude as
        separate columns from the geometry's coordinates
        '''

        with open(self.source) as f:
            stops_geodata = json.load(f)

        self.df = pd.DataFrame(json_normalize(stops_geodata['features']))
        self.drop_prefix("properties.")

        n_rows_orig = self.df.shape[0]

        self.df.dropna(subset=["geometry.coordinates"], inplace=True, axis=0)
        n_rows_clean = self.df.shape[0]
        print("Cleaning null geometries, eliminated ", n_rows_orig - n_rows_clean,
              " rows out of the original ", n_rows_orig, " rows")

        self.df['longitude'] = self.df["geometry.coordinates"].apply(lambda x: x[0])
        self.df['latitude'] = self.df["geometry.coordinates"].apply(lambda x: x[1])

        print(self.df.columns)
        # Remove irrelevant columns
        selection = (['id', 'latitude', 'longitude'] + self.properties)
        self.df = self.df[selection]

        # Filter records that don't match `filter_values`
        for k, v in self.filter_values.items():
            self.df = self.df.loc[self.df[k].isin(v), :]



