"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
from app import plot_map
from app import save_to_bd



def home(request):
    """Renders the home page."""

    #assert savesave_to_bd.save_to_bd()
    save_to_bd.save_to_bd()

    assert isinstance(request, HttpRequest)

    table, folium_map = plot_map.show()

    return render(
        request,
        'app/index.html',
        {
            'map':   folium_map._repr_html_(),
            'table': table,
            'title':'Map',
            'year':datetime.now().year,
        }
    )
