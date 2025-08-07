from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import requests # type: ignore
from collections import Counter
from datetime import datetime
from django.contrib.auth.decorators import login_required
import json

@login_required
# dashboard/views.py
def index(request):
    response = requests.get(settings.API_URL)
    posts = response.json()

    total_responses = len(posts)

    # Extraer productoID y timestamp
    tabla_datos = []
    for key, val in posts.items():
        tabla_datos.append({
            "id": key,
            "producto": val["ProductoID"],
            "fecha": val["timestamp"]
        })

    # Indicadores
    productos = [val["ProductoID"] for val in posts.values()]
    productos_unicos = len(set(productos))
    producto_mas_frecuente = max(set(productos), key=productos.count)
    ultima_fecha = max(
        datetime.fromisoformat(val["timestamp"]).strftime("%Y-%m-%d")
        for val in posts.values()
    )


    # Gráfico: conteo por producto
    conteo_productos = Counter(productos) # Ej: Counter({'Producto 1': 5, 'Producto 2': 3})
    chart_labels = list(conteo_productos.keys())  # Ej: ["Producto 1", "Producto 2"]
    chart_values = list(conteo_productos.values())  # Ej: [5, 3]


    data = {
        'title': "Landing Page' Dashboard",
        'total_responses': total_responses,
        'productos_unicos': productos_unicos,
        'producto_mas_frecuente': producto_mas_frecuente,
        'ultima_fecha': ultima_fecha,
        'tabla_datos': tabla_datos,
        'chart_labels': json.dumps(chart_labels),
        'chart_values': json.dumps(chart_values),
    }

    return render(request, 'dashboard/index.html', data)

