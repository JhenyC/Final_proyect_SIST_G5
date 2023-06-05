import cardio_health_bot as chb
import threading as th
import simulation.simulation as sim
import numpy as np
import time 
import random as rd

bot = chb.MyBot()
simulator = sim.PatientSimulator()
nombres_hombre = ['Juan', 'Pedro', 'Pablo', 'Jose', 'Luis', 'Carlos', 'Jorge', 'Alberto', 'Ricardo', 'Roberto', 'Miguel', 'Raul', 'Fernando', 'Santiago', 'Diego', 'Daniel', 'Alejandro', 'Andres', 'Felipe', 'Manuel', 'Rafael', 'Sebastian', 'Gabriel', 'Antonio', 'David', 'Jose Luis', 'Jose Manuel', 'Francisco', 'Javier', 'Eduardo', 'Enrique', 'Alvaro', 'Adrian', 'Oscar', 'Jesus', 'Mario', 'Tomas', 'Juan Carlos', 'Juan Jose']
nombres_mujer = ['Maria', 'Carmen', 'Josefa', 'Isabel', 'Ana', 'Laura', 'Francisca', 'Antonia', 'Dolores', 'Paula', 'Elena', 'Lucia', 'Mercedes', 'Sara', 'Rosa', 'Concepcion', 'Julia', 'Manuela', 'Rocio', 'Marina', 'Teresa', 'Beatriz', 'Nuria', 'Sonia', 'Raquel', 'Cristina', 'Silvia', 'Patricia', 'Eva', 'Marta', 'Pilar', 'Alicia', 'Catalina', 'Luisa', 'Natalia', 'Angela', 'Mar', 'Juana', 'Alba', 'Maria Jose', 'Maria Carmen', 'Maria Dolores', 'Maria Pilar', 'Maria Isabel', 'Maria Teresa', 'Maria Angeles', 'Maria Jesus', 'Maria Antonia', 'Maria Luisa', 'Maria Fernanda', 'Maria Victoria', 'Maria Francisca', 'Maria Rosa', 'Maria Elena', 'Maria Mercedes', 'Maria Mar', 'Maria Belen', 'Maria Nieves', 'Maria Soledad', 'Maria Concepcion', 'Maria Salud', 'Maria Rosario', 'Maria Lourdes', 'Maria Amparo', 'Maria Cristina', 'Maria Josefa', 'Maria Montserrat', 'Maria Angeles', 'Maria Asuncion', 'Maria Milagros', 'Maria Inmaculada', 'Maria Mar', 'Maria Aranzazu', 'Maria Fatima', 'Maria Remedios', 'Maria Candelaria', 'Maria Encarnacion', 'Maria Milagros', 'Maria Asuncion', 'Maria Soledad', 'Maria Rosario', 'Maria Lourdes', 'Maria Amparo', 'Maria Cristina', 'Maria Josefa', 'Maria Montserrat', 'Maria Angeles', 'Maria Asuncion', 'Maria Milagros', 'Maria Inmaculada', 'Maria Mar', 'Maria Aranzazu', 'Maria Fatima', 'Maria Remedios', 'Maria Candelaria', 'Maria Encarnacion', 'Maria Milagros', 'Maria Asuncion', 'Maria Soledad', 'Maria Rosario', 'Maria Lourdes', 'Maria Amparo', 'Maria Cristina', 'Maria Josefa', 'Maria Montserrat', 'Maria Angeles']
def eventos_bot():
    #Controlador de eventos externos
    #por ahora solo se maneja por linea de comandos
    nombre = "Juan"
    habitacion = 1
    while True:
        command = input("Ingrese el comando a ejecutar: ")
        if command == "1":
            bot.manejar_evento_externo(nombre, habitacion)
        elif command == "2":
            print("nada")

def simulacion_pacientes():
    lambda_param = 1/2
    while True:
        tiempo_de_espera = np.random.exponential(1/lambda_param, 1)[0]*60
        time.sleep(tiempo_de_espera)

        #Generar paciente
        patient= simulator.generate_patient()
        patient_data_dataframe = patient.data_frame_format()
        print(patient_data_dataframe)
        
        #Nombre y habitacion del paciente
        if patient.get_sex() == 1:
            nombre = rd.choice(nombres_hombre)
        else:
            nombre = rd.choice(nombres_mujer)

        habitacion = rd.randint(1, 10)

        print("Paciente: ", nombre, " Habitacion: ", habitacion)

        prediction = bot.classifier.classify(patient_data_dataframe)
        print(prediction)
        if prediction == 1:
            bot.manejar_evento_externo(nombre, habitacion)

threadManual = th.Thread(target=eventos_bot)
threadManual.start()
thread = th.Thread(target=simulacion_pacientes)
thread.start()
print("Simulacion de pacientes iniciada")

print("Bot iniciado")
bot.run()

    