from locdata.dataset.geojson import GeoJsonDataset

SOURCE = "data/osm_nodes_amenities_dc_bbox.geojson"
CENTER = {"latitude": 38.882843, "longitude":-76.997509}
FILTER_VALUES = {"amenity":["restaurant", "fast_food", "cafe", 'bar', "pub"]}


def test_load_geojson():
    """
    Test to confirm GeoJson can load and be read properly
    """
    gds = GeoJsonDataset(SOURCE, filter_values=FILTER_VALUES)
    amenities_count = gds.df['amenity'].value_counts().sort_values(ascending=False)
    assert amenities_count['restaurant'] == 963
    return 0
