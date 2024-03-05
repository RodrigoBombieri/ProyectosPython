import requests

# APP para obtener el clima de una ciudad ingresada por el usuario por el teclado

city = input("Ingrese la ciudad: ")


url= "https://api.openweathermap.org/data/2.5/weather?q={city}&appid=acd84376a06d604560cda82229ed86b3&units=metric".format(city=city)

res = requests.get(url)

data = res.json()

temp = data['main']['temp']
wind_speed = data['wind']['speed']
latitude = data['coord']['lat']
longitude = data['coord']['lon']
description = data['weather'][0]['description']

print("Temperatura: ", temp)
print("Velocidad del viento: ", wind_speed)
print("Latitud: ", latitude)
print("Longitud: ", longitude)
print("Descripción: ", description)

