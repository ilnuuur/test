import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import sqlite3
import folium
from .models import Restaurant

def load_data():

    bk = Restaurant.objects.filter(name__iexact='BurgerKing')
    other = Restaurant.objects.exclude(name__iexact='BurgerKing')

    bk_df = pd.DataFrame(list(bk.values()), columns=['name', 'long', 'lat'])
    other_df = pd.DataFrame(list(other.values()), columns=['name', 'long', 'lat'])

    return bk_df, other_df


def to_geopand(dataframe):

    geopand_df = gpd.GeoDataFrame(geometry=gpd.points_from_xy(dataframe.long, dataframe.lat), crs=4326) 
    
    return geopand_df

def get_mos_rests(gdf):

    moscow = gpd.read_file('app/static/app/mo.geojson')
    moscow['city'] = ['Moscow']*moscow.shape[0]
    moscow_polygon = moscow.dissolve(by='city').geometry.Moscow

    mask = gdf.within(moscow_polygon)
    mos_rests = gdf[mask]

    return mos_rests.reset_index(drop=True)


def n_competitors(gdf1, gdf2, radius=2000):
    
    gpd1 = gdf1.to_crs(epsg=3857).copy()
    gpd2 = gdf2.to_crs(epsg=3857).copy()
    
    def within_radius(x):
        dists = gpd2.distance(x)
        nearby = (dists <= radius).astype(int)
        return sum(nearby)
    
    gpd1['n_competitors'] = gpd1.geometry.apply(within_radius)
    
    return gpd1.to_crs(epsg=4326)

def plot(results):

    folium_map = folium.Map(location=[results.geometry.y.mean(), results.geometry.x.mean()],
                            zoom_start=13) 
    for i in range(len(results)):
            folium.Marker(location=[results.loc[i,'geometry'].y, results.loc[i,'geometry'].x], tooltip=str(results.loc[i, 'n_competitors'])).add_to(folium_map)
    return folium_map


def show():

    d1, d2 = load_data()

    gdf1 = to_geopand(d1)
    gdf2 = to_geopand(d2)

    gdf1 = get_mos_rests(gdf1).copy()
    gdf2 = get_mos_rests(gdf2).copy()

    results = n_competitors(gdf1, gdf2)

    return results, plot(results)






