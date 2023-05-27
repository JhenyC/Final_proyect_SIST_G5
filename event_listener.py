import cardio_health_bot as chb
import threading as th

bot = chb.MyBot()

def eventos_bot():
    #Controlador de eventos externos
    #por ahora solo se maneja por linea de comandos
    while True:
        command = input("Ingrese el comando a ejecutar: ")
        if command == "1":
            bot.manejar_evento_externo()
        elif command == "2":
            print("nada")

thread = th.Thread(target=eventos_bot)
thread.start()

bot.run()
    