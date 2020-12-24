import overpy
import numpy as np
import requests
import re
from .models import Restaurant

def get_from_OSM(name='KFC|КФС', city='Москва'):
    """
    
Parameters
----------
    
name : str, retaurant name  with format 'name in RU|name in En'
city : string, city name in Ru
    
-------
    
Get coordinates of restaurants from OpenStreetMap

    -------
Returns

List of objects
    
"""
    api = overpy.Overpass()
    query = """area["name"="{0}"]; 
                node["name"~"{1}"](area);
                out;""".format(name, city)
    answer = api.query(query)

    #restaurants = [Restaurant(name=name.split('|')[0], long=float(node.lon), lat= float(node.lat)) for node in answer.nodes]
        
    #return restaurants

    for node in answer.nodes:
        r = Restaurant(name=name, long=float(node.lon), lat= float(node.lat)).save()
        r.save()


def get_from_web_page(name, url):
    """
    
    Parameters
    ----------
    
    name : str, retaurant name  in En
    url: str, 

    -------
    
    Get coordinates of restaurants from web page code

    -------
    Returns

    List of objects

    """
    response = requests.get(url)


    lat = re.findall(r'latitude:"(\d+.\d+)"', response.text)
    long = re.findall(r'longitude:"(\d+.\d+)"', response.text)

    #restaurants = [Restaurant(name=name, *args) for args in zip(long, lat)]
    #return restaurants

    for x, y in zip(long, lat):
        r = Restaurant(name=name, long=float(x), lat= float(y))
        r.save()


def save_to_bd():

    KFC_coords = get_from_OSM(name='KFC|КФС', city='Москва')
    McD_coords = get_from_web_page(name = 'McDonald', url='https://mcdonalds.ru/restaurants/map')
    BK_coords = get_from_web_page(name = 'BurgerKing', url = "https://burgerking.ru/restaurant-locations-json-reply-new/")

    #all_coords = np.concatenate((BK_coords, KFC_coords, McD_coords))

    #try:
        #Restaurant.objects.bulk_create(all_coords)
        #return True
    #except:
        #return False
        #raise Exception('bd')




 