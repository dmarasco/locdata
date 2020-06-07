
import pandas as pd
from h3 import h3

class SpatialDataset():
    """
    """
    def __init__(self, source, h3_resolution, ring_distance):
        self.name = "Abstract Spatial Dataset"
        self.source=source
        self.h3_resolution = h3_resolution
        self.ring_distance = ring_distance
        self.df = pd.DataFrame()

    def drop_prefix(self, prefix):
        print("Before: ",self.df.columns)
        self.df.columns = self.df.columns.str.replace(prefix,"")
        print("After: ", self.df.columns)

    def index_df(self):
        """
        add h3 index to dataset
        """
        self.df[f'hex_id{self.h3_resolution}'] =self.df.apply(lambda row: h3.geo_to_h3(row["latitude"], row["longitude"],
                                               self.h3_resolution), axis=1)
