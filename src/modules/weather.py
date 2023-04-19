import requests, os, datetime
import matplotlib.pyplot as plt
import numpy as np

def get_weather_forecasts():
    print("[+] Preparing weather data forecast...")
    api_key=os.getenv('OPEN_WEATHER_TOKEN')
    lat=os.getenv('LATITUDE')
    lon=os.getenv('LONGITUDE')
    url = f'https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&appid={api_key}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        today = data["hourly"]

        # Crear una lista de horas como objetos de fecha y hora
        hours = [datetime.datetime.fromtimestamp(t["dt"], datetime.timezone.utc) for t in today]

        # Convertir los objetos de fecha y hora a la zona horaria UTC+2
        hours_cest = [h.astimezone(datetime.timezone(datetime.timedelta(hours=2))) for h in hours]

        # Crear una lista de temperaturas en grados Celsius
        temperatures = [t["temp"] - 273.15 for t in today]
        labels = [h.strftime('%H:00') for h in hours_cest]

        # Crear una lista de probabilidades de lluvia
        rain_probs = [t["pop"] * 100 for t in today]

        # Crear el gráfico
        fig, ax1 = plt.subplots(figsize=(12, 6))  # Ajustar el tamaño del gráfico

        # Crear el subgráfico para la línea de temperatura
        color = 'tab:red'
        ax1.set_xlabel('Hora')
        ax1.set_ylabel('Temperatura (°C)', color=color)

        # Limitar el rango del eje x a las próximas 48 horas
        now_cest = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=2)))
        future_cest = now_cest + datetime.timedelta(hours=48)
        ax1.set_xlim(now_cest, future_cest)

        # Formatear las etiquetas de tiempo
        labels = [h.strftime('%H:00') for h in hours_cest]
        ax1.set_xticks(hours_cest[::2])
        ax1.set_xticklabels(labels[::2], rotation=45, ha='right')
        ax1.plot(hours_cest, temperatures, color=color)
        ax1.tick_params(axis='y', labelcolor=color)

        # Crear el subgráfico para el histograma de probabilidad de lluvia
        ax2 = ax1.twinx() 
        color = 'tab:blue'
        ax2.set_ylabel('Probabilidad de lluvia', color=color)
        ax2.plot(hours_cest, rain_probs, color=color)
        ax2.tick_params(axis='y', labelcolor=color)

        # Agregar una línea vertical separando los días
        for i, h in enumerate(hours_cest):
            if i > 0 and h.day != hours_cest[i-1].day:
                ax1.axvline(x=h, color='gray', linestyle='--')
                ax1.annotate(h.strftime('%d %b'), xy=(h, ax1.get_ylim()[1]), xytext=(h, ax1.get_ylim()[1]+1), ha='center', va='bottom', fontsize=10, color='gray', annotation_clip=False)

        fig.tight_layout()

        # guardar gráfico en un archivo png
        plt.savefig('weather.png')

        return data["current"]
    else:
        print(response)
        return 'No se pudieron obtener los datos meteorológicos.'