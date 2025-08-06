from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import requests
from collections import Counter
from datetime import datetime
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    response = requests.get(settings.API_URL)
    posts = response.json()

    # Número total de respuestas
    total_responses = len(posts)

    # Extraer productos y fechas
    productos = []
    fechas = []
    tabla = []

    for item in posts.values():
        producto = item.get("ProductoID", "Desconocido")
        timestamp = item.get("timestamp", "")
        
        productos.append(producto)
        fechas.append(timestamp)
        
        tabla.append({
            "producto": producto,
            "fecha": datetime.fromisoformat(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        })

    # Indicador 2: número de productos distintos
    productos_unicos = len(set(productos))

    # Indicador 3: producto más frecuente
    producto_mas_frecuente = Counter(productos).most_common(1)[0][0]

    # Indicador 4: último timestamp registrado
    fecha_mas_reciente = max(datetime.fromisoformat(f) for f in fechas).strftime('%Y-%m-%d %H:%M:%S')

    # Datos para el gráfico: conteo por día
    conteo_por_dia = Counter(f[:10] for f in fechas)  # YYYY-MM-DD
    fechas_ordenadas = sorted(conteo_por_dia.keys())
    cantidades = [conteo_por_dia[fecha] for fecha in fechas_ordenadas]

    data = {
        "title": "Landing Page' Dashboard",
        "total_responses": total_responses,
        "productos_unicos": productos_unicos,
        "producto_mas_frecuente": producto_mas_frecuente,
        "fecha_mas_reciente": fecha_mas_reciente,
        "tabla": tabla,
        "labels": fechas_ordenadas,     # eje x del gráfico
        "values": cantidades            # eje y del gráfico
    }

    return render(request, 'dashboard/index.html', data)
