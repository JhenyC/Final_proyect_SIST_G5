import telebot
import objects.patient as patient
import objects.classifier as classifier
from config import TOKEN, contact_list, VALIDATION_CODE

class MyBot:
    def __init__(self):
        self.token = TOKEN
        self.bot = telebot.TeleBot(TOKEN)
        self.contact_list = contact_list
        self.users_state = {}
        self.patient_user = {}
        self.classifier = classifier.Classifier()

    def enviar_mensaje(self, chat_id, mensaje):
        self.bot.send_message(chat_id, mensaje)

    def evento_externo(self, nombre, habitacion):
        # Lógica para detectar el evento externo y obtener el mensaje que se enviará
        mensaje = "EMERGENCIA: {} en la habitacion {} necesita ayuda".format(nombre, habitacion)
        return mensaje

    def manejar_evento_externo(self, nombre, habitacion):
        mensaje = self.evento_externo(nombre, habitacion)
        for chat_id in self.contact_list:
            self.enviar_mensaje(chat_id, mensaje)

    def manejar_comando_desconocido(self, mensaje):
        chat_id = mensaje.chat.id
        mensaje = "Lo siento, no conozco ese comando"
        self.enviar_mensaje(chat_id, mensaje)

    def imprimir_info_usuario(self, message):
        print("Información del usuario:")
        print(f"ID de chat: {message.chat.id}")
        print(f"Nombre de usuario: {message.from_user.username}")
        print(f"Nombre completo: {message.from_user.first_name} {message.from_user.last_name}")
        print(f"Mensaje: {message.text}")
        print("")

    def agregar_contacto(self, message):
        chat_id = message.chat.id
        if(self.leer_codigo_seguridad(message)):
            mensaje = "Código de validación correcto"
            self.enviar_mensaje(chat_id, mensaje)
            if chat_id not in self.contact_list:
                self.contact_list.append(chat_id)
                mensaje = "Contacto agregado"
            else:
                mensaje = "El contacto ya existe"
            self.enviar_mensaje(chat_id, mensaje)
        else:
            mensaje = "Código de validación incorrecto"
            self.enviar_mensaje(chat_id, mensaje)

    def eliminar_contacto(self, message):
        chat_id = message.chat.id
        if(self.leer_codigo_seguridad(message)):
            mensaje = "Código de validación correcto"
            self.enviar_mensaje(chat_id, mensaje)
            if chat_id in self.contact_list:
                self.contact_list.remove(chat_id)
                mensaje = "Contacto eliminado"
            else:
                mensaje = "El contacto no existe"
            self.enviar_mensaje(chat_id, mensaje)
        else:
            mensaje = "Código de validación incorrecto"
            self.enviar_mensaje(chat_id, mensaje)

    def analizar_paciente(self, message):
        chat_id = message.chat.id
        a_patient = self.patient_user[chat_id]
        df = a_patient.data_frame_format()
        prediction = self.classifier.classify(df)
        if prediction[0] == 1:
            mensaje = "Es probable que el paciente sufra alguna enfermedad cardiaca"
        else:
            mensaje = "Es poco probable que el paciente sufra alguna enfermedad cardiaca"
        self.enviar_mensaje(chat_id, mensaje)
    
    def enviar_mensaje_botones(self, chat_id, mensaje, botones):
        markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
        for boton in botones:
            markup.add(telebot.types.KeyboardButton(boton))
        self.bot.send_message(chat_id, mensaje, reply_markup=markup)

    def estandarizar_respuestas(self, mensaje):
        if mensaje == "Si":
            return 1
        elif mensaje == "No":
            return 0
        else:
            return mensaje

    def info_bot(self, message):
        chat_id = message.chat.id
        mensaje = "Hola {}, soy cardio_health_bot ¿en que puedo ayudarte?".format(message.from_user.first_name)
        self.enviar_mensaje(chat_id, mensaje)
        mensaje = "Puedes usar los siguientes comandos: \n /agregar_contacto: Agrega un nuevo contacto a mi lista de contactos, en caso de emergencia enviare un mensaje a todos mis contactos \n /eliminar_contacto: Elimina un contacto de mi lista de contactos \n /analizar_paciente: Responde unas preguntas sobre el paciente para predecir si el paciente puede sufrir de alguna enfermedad cárdiaca \n/start: Inicia el bot \n Los comandos /agregar_contacto y /eliminar_contacto requieren un código de validación"
        self.enviar_mensaje(chat_id, mensaje)

    def autenticar_usuario(self, message):
        chat_id = message.chat.id
        if chat_id in self.contact_list:
            return True
        else:
            return False
        
    def leer_codigo_seguridad(self, message):   
        if  message.text == VALIDATION_CODE:
            return True
        else:
            return False
        
    def controlar_estado_usuario(self, message, estado):
        chat_id = message.chat.id
        self.users_state[chat_id] = estado
        print(self.users_state)

    def run(self):
        @self.bot.message_handler(commands=['start'])
        def handle_start(message):
            self.info_bot(message)

        @self.bot.message_handler(commands=['agregar_contacto'])
        def handle_agregar_contacto(message):
            self.enviar_mensaje(message.chat.id, "Ingrese el código de validación")
            self.controlar_estado_usuario(message, "agregar_contacto")

        @self.bot.message_handler(commands=['eliminar_contacto'])
        def handle_eliminar_contacto(message):
            self.enviar_mensaje(message.chat.id, "Ingrese el código de validación")
            self.controlar_estado_usuario(message, "eliminar_contacto")

        @self.bot.message_handler(commands=['analizar_paciente'])
        def handle_analizar_paciente(message):
            if(self.autenticar_usuario(message)):
                self.patient_user[message.chat.id] = patient.Patient()
                self.enviar_mensaje(message.chat.id, "Muy bien, ahora ingresa los datos del paciente")
                self.enviar_mensaje(message.chat.id, "¿Cual es la edad del paciente? \n(en años completos sin decimales Ejemplo de respuesta: \"20\")")
                self.controlar_estado_usuario(message, "analizar_paciente_edad")
            else:
                self.enviar_mensaje(message.chat.id, "No tienes permiso para usar este comando")

        @self.bot.message_handler(func=lambda m: True)
        def handle_all_messages(message):
            state = ""
            if(message.text == "Gracias"):
                self.enviar_mensaje(message.chat.id, "De nada" + u'\U0001F600')
            if("Por Favor" in message.text):
                self.enviar_mensaje(message.chat.id, "Claro que si :)")
            if(message.chat.id in self.users_state):
                state = self.users_state[message.chat.id]
            match state:
                case "agregar_contacto":
                    self.agregar_contacto(message)
                    self.controlar_estado_usuario(message, "ninguno")
                case "eliminar_contacto":
                    self.eliminar_contacto(message)
                    self.controlar_estado_usuario(message, "ninguno")
                case "analizar_paciente_edad":
                    try:
                        self.patient_user[message.chat.id].set_age(message.text)
                        self.enviar_mensaje_botones(message.chat.id, "¿Cual es el sexo del paciente?", ["Hombre", "Mujer"])
                        self.controlar_estado_usuario(message, "analizar_paciente_sexo")
                    except:
                        self.enviar_mensaje(message.chat.id, "Por favor ingrese un numero entero")
                        self.enviar_mensaje(message.chat.id, "¿Cual es la edad del paciente? \n(en años completos sin decimales Ejemplo de respuesta: \"20\")")
                case "analizar_paciente_sexo":
                    try:
                        self.patient_user[message.chat.id].set_sex(1 if message.text == "Hombre" else 0)
                        self.enviar_mensaje_botones(message.chat.id, "¿El paciente tiene presion arterial alta? (Pacientes adultos que hayan recibido un diagnostico de presion alta por un profesional de la salud)", ["Si", "No"])
                        self.controlar_estado_usuario(message, "analizar_paciente_presion")
                    except:
                        self.enviar_mensaje(message.chat.id, "Por favor ingrese una respuesta valida")
                        self.enviar_mensaje_botones(message.chat.id, "¿Cual es el sexo del paciente?", ["Hombre", "Mujer"])
                case "analizar_paciente_presion":
                    try:
                        self.patient_user[message.chat.id].set_high_blood_pressure(self.estandarizar_respuestas(message.text))
                        self.enviar_mensaje_botones(message.chat.id, "¿El paciente tiene alto colesterol? (Pacientes adultos que hayan recibido diagnostico de colesterol alto por un profesional de la salud)", ["Si", "No"])
                        self.controlar_estado_usuario(message, "analizar_paciente_colesterol")
                    except:
                        self.enviar_mensaje(message.chat.id, "Por favor ingrese una respuesta valida")
                        self.enviar_mensaje_botones(message.chat.id, "¿El paciente tiene presion arterial alta? (Pacientes adultos que hayan recibido un diagnostico de presion alta por un profesional de la salud)", ["Si", "No"])
                case "analizar_paciente_colesterol":
                    try:
                        self.patient_user[message.chat.id].set_high_cholesterol(self.estandarizar_respuestas(message.text))
                        self.enviar_mensaje(message.chat.id, "¿Cual es el IMC del paciente? \n(En caso de no saberlo, puedes calcularlo en https://www.calculadoraimc.com/) \n (Ejemplo de respuesta: \"20.5\")")
                        self.controlar_estado_usuario(message, "analizar_paciente_imc")
                    except:
                        self.enviar_mensaje(message.chat.id, "Por favor ingrese una respuesta valida")
                        self.enviar_mensaje_botones(message.chat.id, "¿El paciente tiene alto colesterol? (Pacientes adultos que hayan recibido diagnostico de colesterol alto por un profesional de la salud)", ["Si", "No"])
                case "analizar_paciente_imc":
                    try:
                        self.patient_user[message.chat.id].set_BMI(message.text)
                        self.enviar_mensaje_botones(message.chat.id, "¿El paciente es fumador? (¿El paciente fumó al menos 100 cigarros en toda su vida? NOTA: 5 paquetes = 100 cigarros)", ["Si", "No"])
                        self.controlar_estado_usuario(message, "analizar_paciente_fumador")
                    except:
                        self.enviar_mensaje(message.chat.id, "Por favor ingrese un numero decimal")
                        self.enviar_mensaje(message.chat.id, "¿Cual es el IMC del paciente? \n(En caso de no saberlo, puedes calcularlo en https://www.calculadoraimc.com/) \n (Ejemplo de respuesta: \"20.5\")")
                case "analizar_paciente_fumador":
                    try:
                        self.patient_user[message.chat.id].set_smoker(self.estandarizar_respuestas(message.text))
                        self.enviar_mensaje_botones(message.chat.id, "¿El paciente tiene diabetes? ", ["Diabetes tipo 1", "Diabetes tipo 2", "No"])
                        self.controlar_estado_usuario(message, "analizar_paciente_diabetes")
                    except:
                        self.enviar_mensaje(message.chat.id, "Por favor ingrese una respuesta valida")
                        self.enviar_mensaje_botones(message.chat.id, "¿El paciente es fumador? (¿El paciente fumó al menos 100 cigarros en toda su vida? NOTA: 5 paquetes = 100 cigarros)", ["Si", "No"])
                case "analizar_paciente_diabetes":
                    try:
                        self.patient_user[message.chat.id].set_diabetes(2 if message.text == "Diabetes tipo 2" else 1 if message.text == "Diabetes tipo 1" else 0)
                        self.enviar_mensaje_botones(message.chat.id, "¿El paciente realiza actividad fisica? (Pacientes adultos que reporten actividad fisica regular en los utlimos 30 días)", ["Si", "No"])
                        self.controlar_estado_usuario(message, "analizar_paciente_actividad_fisica")
                    except:
                        self.enviar_mensaje(message.chat.id, "Por favor ingrese una respuesta valida")
                        self.enviar_mensaje_botones(message.chat.id, "¿El paciente tiene diabetes? ", ["Diabetes tipo 1", "Diabetes tipo 2", "No"])
                case "analizar_paciente_actividad_fisica":
                    try:
                        self.patient_user[message.chat.id].set_physical_activity(self.estandarizar_respuestas(message.text))
                        self.enviar_mensaje_botones(message.chat.id, "¿El paciente consume alcohol? (Hombres adultos que beban 14 bebidas alcoholicas o mas por semana y mujeres adultas que beban mas de 7 bebidas alcoholicas por semana)", ["Si", "No"])
                        self.controlar_estado_usuario(message, "analizar_paciente_alcohol")
                    except:
                        self.enviar_mensaje(message.chat.id, "Por favor ingrese una respuesta valida")
                        self.enviar_mensaje_botones(message.chat.id, "¿El paciente realiza actividad fisica? (Pacientes adultos que reporten actividad fisica regular en los utlimos 30 días)", ["Si", "No"])
                case "analizar_paciente_alcohol":
                    try:
                        self.patient_user[message.chat.id].set_alcohol(self.estandarizar_respuestas(message.text))
                        self.enviar_mensaje_botones(message.chat.id, "¿Cual es el estado general de salud del paciente?", ["Pesimo","Malo", "Regular", "Bueno", "Excelente"])
                        self.controlar_estado_usuario(message, "analizar_paciente_estado_salud")
                    except:
                        self.enviar_mensaje(message.chat.id, "Por favor ingrese una respuesta valida")
                        self.enviar_mensaje_botones(message.chat.id, "¿El paciente consume alcohol? (Hombres adultos que beban 14 bebidas alcoholicas o mas por semana y mujeres adultas que beban mas de 7 bebidas alcoholicas por semana)", ["Si", "No"])
                case "analizar_paciente_estado_salud":
                    try:
                        self.patient_user[message.chat.id].set_general_health(1 if message.text == "Pesimo" else 2 if message.text == "Malo" else 3 if message.text == "Regular" else 4 if message.text == "Bueno" else 5 if message.text == "Excelente" else 0)
                        self.enviar_mensaje(message.chat.id, "¿Cual es el estado mental del paciente? (¿En cuantos de los ultimos 30 días el paciente se ha sentido deprimido, ansioso o emocionalmente inestable? \n Ejemplo de respuesta: \"10\"")
                        self.controlar_estado_usuario(message, "analizar_paciente_estado_mental")
                    except:
                        self.enviar_mensaje(message.chat.id, "Por favor ingrese una respuesta valida")
                        self.enviar_mensaje_botones(message.chat.id, "¿Cual es el estado general de salud del paciente?", ["Pesimo","Malo", "Regular", "Bueno", "Excelente"])
                case "analizar_paciente_estado_mental":
                    try:
                        self.patient_user[message.chat.id].set_mental_health(message.text)
                        self.enviar_mensaje(message.chat.id, "¿Cual es el estado fisico del paciente? (¿En cuantos de los ultimos 30 días el paciente ha tenido problemas para realizar sus actividades diarias debido a problemas de salud fisica?) \n Ejemplo de respuesta: \"10\"")
                        self.controlar_estado_usuario(message, "analizar_paciente_estado_fisico")
                    except:
                        self.enviar_mensaje(message.chat.id, "Por favor ingrese una respuesta valida")
                        self.enviar_mensaje(message.chat.id, "¿Cual es el estado mental del paciente? (¿En cuantos de los ultimos 30 días el paciente se ha sentido deprimido, ansioso o emocionalmente inestable? \n Ejemplo de respuesta: \"10\"")
                case "analizar_paciente_estado_fisico":
                    try:
                        self.patient_user[message.chat.id].set_physical_health(message.text)
                        self.enviar_mensaje_botones(message.chat.id, "¿El paciente se realizo un chequeo de colesterol?", ["Si", "No"])
                        self.controlar_estado_usuario(message, "analizar_paciente_colesterol_chequeo")
                    except:
                        self.enviar_mensaje(message.chat.id, "Por favor ingrese una respuesta valida")
                        self.enviar_mensaje(message.chat.id, "¿Cual es el estado fisico del paciente? (¿En cuantos de los ultimos 30 días el paciente ha tenido problemas para realizar sus actividades diarias debido a problemas de salud fisica?) \n Ejemplo de respuesta: \"10\"")
                case "analizar_paciente_colesterol_chequeo":
                    try:
                        self.patient_user[message.chat.id].set_chol_checked(self.estandarizar_respuestas(message.text))
                        self.enviar_mensaje_botones(message.chat.id, "¿El paciente sufrió algun ataque cardiaco en el pasado?", ["Si", "No"])
                        self.controlar_estado_usuario(message, "analizar_paciente_ataque_cardiaco")
                    except:
                        self.enviar_mensaje(message.chat.id, "Por favor ingrese una respuesta valida")
                        self.enviar_mensaje_botones(message.chat.id, "¿El paciente se realizo un chequeo de colesterol?", ["Si", "No"])
                case "analizar_paciente_ataque_cardiaco":
                    try:
                        self.patient_user[message.chat.id].set_stroke(self.estandarizar_respuestas(message.text))
                        self.enviar_mensaje_botones(message.chat.id, "¿En los ultimos 30 dias el paciente requirio tratamiento que no pudo pagar?", ["Si", "No"])
                        self.controlar_estado_usuario(message, "analizar_paciente_costo_medico")
                    except:
                        self.enviar_mensaje(message.chat.id, "Por favor ingrese una respuesta valida")
                        self.enviar_mensaje_botones(message.chat.id, "¿El paciente sufrió algun ataque cardiaco en el pasado?", ["Si", "No"])
                case "analizar_paciente_costo_medico":
                    try:
                        self.patient_user[message.chat.id].set_noDocbcCost(self.estandarizar_respuestas(message.text))
                        self.enviar_mensaje_botones(message.chat.id, "¿El paciente esta pasando por algun tratamiento médico actualmente?", ["Si", "No"])
                        self.controlar_estado_usuario(message, "analizar_paciente_tratamiento_medico")
                    except:
                        self.enviar_mensaje(message.chat.id, "Por favor ingrese una respuesta valida")
                        self.enviar_mensaje_botones(message.chat.id, "¿En los ultimos 30 dias el paciente requirio tratamiento que no pudo pagar?", ["Si", "No"])
                case "analizar_paciente_tratamiento_medico":
                    try:
                        self.patient_user[message.chat.id].set_health_care(self.estandarizar_respuestas(message.text))
                        self.enviar_mensaje_botones(message.chat.id, "¿El paciente suele consumir vegetales?", ["Si", "No"])
                        self.controlar_estado_usuario(message, "analizar_paciente_vegetales")
                    except:
                        self.enviar_mensaje(message.chat.id, "Por favor ingrese una respuesta valida")
                        self.enviar_mensaje_botones(message.chat.id, "¿El paciente esta pasando por algun tratamiento médico actualmente?", ["Si", "No"])
                case "analizar_paciente_vegetales":
                    try:
                        self.patient_user[message.chat.id].set_veggies(self.estandarizar_respuestas(message.text))
                        self.enviar_mensaje_botones(message.chat.id, "¿El paciente suele consumir frutas?", ["Si", "No"])
                        self.controlar_estado_usuario(message, "analizar_paciente_frutas")
                    except:
                        self.enviar_mensaje(message.chat.id, "Por favor ingrese una respuesta valida")
                        self.enviar_mensaje_botones(message.chat.id, "¿El paciente suele consumir vegetales?", ["Si", "No"])
                case "analizar_paciente_frutas":
                    try:
                        self.patient_user[message.chat.id].set_fruits(self.estandarizar_respuestas(message.text))
                        self.enviar_mensaje_botones(message.chat.id, "¿El paciente tiene alguna dificultad para caminar?", ["Si", "No"])
                        self.controlar_estado_usuario(message, "analizar_paciente_dificultad_caminar")
                    except:
                        self.enviar_mensaje(message.chat.id, "Por favor ingrese una respuesta valida")
                        self.enviar_mensaje_botones(message.chat.id, "¿El paciente suele consumir frutas?", ["Si", "No"])
                case "analizar_paciente_dificultad_caminar":
                    try:
                        self.patient_user[message.chat.id].set_walking_difficulty(self.estandarizar_respuestas(message.text))
                        self.enviar_mensaje(message.chat.id, "Espere un momento por favor, estamos analizando los datos...")
                        self.analizar_paciente(message)
                        self.controlar_estado_usuario(message, "ninguno")
                    except:
                        self.enviar_mensaje(message.chat.id, "Por favor ingrese una respuesta valida")
                        self.enviar_mensaje_botones(message.chat.id, "¿El paciente tiene alguna dificultad para caminar?", ["Si", "No"])
                case _:
                    self.info_bot(message)

        @self.bot.message_handler(func=lambda message: True)
        def handle_comandos_desconocidos(message):
            if message.text.startswith('/'):
                self.manejar_comando_desconocido(message)
            

        self.bot.infinity_polling()

