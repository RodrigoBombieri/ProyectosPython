import speech_recognition as sr
import pyttsx3
import requests

# APP para obtener el clima de una ciudad ingresada por el usuario por el micrófono


# Creo un objeto de reconocimiento de voz
listener = sr.Recognizer()
# Creo un objeto de texto a voz
engine = pyttsx3.init()

# Obtengo las voces disponibles
voices = engine.getProperty('voices')
# Selecciono una voz, en este caso la primera y la configuro para que sea la voz del asistente
engine.setProperty('voice', voices[0].id)

# Defino una función para que el asistente hable
def talk(text):    
    engine.say(text) # El asistente habla el texto que se le pase como parámetro    
    engine.runAndWait() # El asistente espera a que termine de hablar


# Defino una función para que el asistente escuche
def listen():
    rec = ""  # Inicializa rec en una cadena vacía
    indice_dispositivo = 0  # Índice del dispositivo de audio que se utilizará 
    try:
        # Abre el micrófono que le pasamos como parámetro
        with sr.Microphone(device_index=indice_dispositivo) as source:
            print("Escuchando...")           
            pc = listener.listen(source) # Escucha el micrófono y almacena el audio en pc
            # Intenta reconocer el audio y lo almacena en rec
            # Por parametro le pasamos el audio y el idioma en el que queremos que lo reconozca
            rec = listener.recognize_google(pc, language='es-ES')           
            rec = rec.lower(0) # Almaena en rec el texto reconocido en minúsculas
    except:
        pass
    print(rec)
    return rec


# Defino una función para que el asistente ejecute la accion de obtener el clima
def run_bomb():
    talk("Hola, ¿de qué ciudad quieres saber el clima?") # El asistente habla el texto que se le pase como parámetro
    rec = listen() # El asistente espera a que termine de hablar
    if rec:  # Verifica si la entrada del usuario no está vacía
        city = rec
        # Se crea la url con la ciudad ingresada por el usuario por el micrófono 
        url = "https://api.openweathermap.org/data/2.5/weather?q={city}&appid=acd84376a06d604560cda82229ed86b3&units=metric".format(city=city)
        res = requests.get(url) # Se realiza la solicitud a la API
        if res.status_code == 200:  # Verifica si la solicitud fue exitosa
            data = res.json() # Se almacena la respuesta en formato JSON
            # Validamos que la respuesta contenga los datos que necesitamos
            if 'main' in data and 'wind' in data and 'coord' in data and 'weather' in data:
                temp = data['main'].get('temp') # Se obtiene la temperatura de la respuesta JSON
                wind_speed = data['wind'].get('speed')
                latitude = data['coord'].get('lat')
                longitude = data['coord'].get('lon')
                description = data['weather'][0].get('description')

                print("Temperatura: ", temp)
                print("Velocidad del viento: ", wind_speed)
                print("Latitud: ", latitude)
                print("Longitud: ", longitude)
                print("Descripción: ", description)
                # Se verifica que los datos obtenidos no sean nulos
                if temp is not None and wind_speed is not None and latitude is not None and longitude is not None and description is not None:
                    talk("La temperatura es de " + str(float(temp)) + " ºC") # El asistente habla el texto que se le pase como parámetro
                    talk("La velocidad del viento es de " + str(float(wind_speed)) + " km/h")
                    talk("La latitud es de " + str(float(latitude)))
                    talk("La longitud es de " + str(float(longitude)))
                    talk(description)
                else:
                    talk("No se pudo obtener información del clima para la ciudad especificada.")
            else:
                talk("No se pudo obtener información del clima para la ciudad especificada.")
        else:
            talk("Error al obtener datos del servidor.")
    else:
        talk("No se detectó ninguna entrada.")
# Se ejecuta la función run_bomb
run_bomb()

