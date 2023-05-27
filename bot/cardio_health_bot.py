import telebot
import objects.patient as patient
from config import TOKEN, contact_list, VALIDATION_CODE

class MyBot:
    def __init__(self):
        self.token = TOKEN
        self.bot = telebot.TeleBot(TOKEN)
        self.contact_list = contact_list
        self.users_state = {}
        self.patient_user = {}

    def enviar_mensaje(self, chat_id, mensaje):
        self.bot.send_message(chat_id, mensaje)

    def evento_externo(self, info_evento):
        # Lógica para detectar el evento externo y obtener el mensaje que se enviará
        mensaje = "EMERGENCIA: {} necesita ayuda".format(info_evento)
        return mensaje

    def manejar_evento_externo(self, info_evento):
        mensaje = self.evento_externo(info_evento)
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
        self.enviar_mensaje(chat_id, "Datos del paciente:")
        self.enviar_mensaje(chat_id, a_patient)

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
                self.enviar_mensaje(message.chat.id, "¿Cual es la edad del paciente?")
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
                    self.patient_user[message.chat.id].set_age(message.text)
                    self.enviar_mensaje(message.chat.id, "¿Cual es el sexo del paciente?")
                    self.controlar_estado_usuario(message, "analizar_paciente_sexo")
                case "analizar_paciente_sexo":
                    self.patient_user[message.chat.id].set_sex(message.text)
                    self.enviar_mensaje(message.chat.id, "¿Cual es el nivel de educacion del paciente?")
                    self.controlar_estado_usuario(message, "analizar_paciente_educacion")
                case "analizar_paciente_educacion":
                    self.patient_user[message.chat.id].set_education(message.text)
                    self.enviar_mensaje(message.chat.id, "¿Cual es el nivel de ingresos del paciente?")
                    self.controlar_estado_usuario(message, "analizar_paciente_ingresos")
                case "analizar_paciente_ingresos":
                    self.patient_user[message.chat.id].set_income(message.text)
                    self.enviar_mensaje(message.chat.id, "¿El paciente tiene lata presión?")
                    self.controlar_estado_usuario(message, "analizar_paciente_presion")
                case "analizar_paciente_presion":
                    self.patient_user[message.chat.id].set_high_blood_pressure(message.text)
                    self.enviar_mensaje(message.chat.id, "¿El paciente tiene alto colesterol?")
                    self.controlar_estado_usuario(message, "analizar_paciente_colesterol")
                case "analizar_paciente_colesterol":
                    self.patient_user[message.chat.id].set_high_cholesterol(message.text)
                    self.enviar_mensaje(message.chat.id, "¿El paciente se realizo una verificacion de colesterol?")
                    self.controlar_estado_usuario(message, "analizar_paciente_verificacion_colesterol")
                case "analizar_paciente_verificacion_colesterol":
                    self.patient_user[message.chat.id].set_cholesterol_checked(message.text)
                    self.enviar_mensaje(message.chat.id, "¿Cual es el IMC del paciente?")
                    self.controlar_estado_usuario(message, "analizar_paciente_imc")
                case "analizar_paciente_imc":
                    self.patient_user[message.chat.id].set_BMI(message.text)
                    self.enviar_mensaje(message.chat.id, "¿El paciente es fumador?")
                    self.controlar_estado_usuario(message, "analizar_paciente_fumador")
                case "analizar_paciente_fumador":
                    self.patient_user[message.chat.id].set_smoker(message.text)
                    self.enviar_mensaje(message.chat.id, "¿El paciente tiene diabetes?")
                    self.controlar_estado_usuario(message, "analizar_paciente_diabetes")
                case "analizar_paciente_diabetes":
                    self.patient_user[message.chat.id].set_diabetes(message.text)
                    self.enviar_mensaje(message.chat.id, "¿El paciente realiza actividad fisica?")
                    self.controlar_estado_usuario(message, "analizar_paciente_actividad_fisica")
                case "analizar_paciente_actividad_fisica":
                    self.patient_user[message.chat.id].set_physical_activity(message.text)
                    self.enviar_mensaje(message.chat.id, "¿Cuanta fruta consume el paciente?")
                    self.controlar_estado_usuario(message, "analizar_paciente_fruta")
                case "analizar_paciente_fruta":
                    self.patient_user[message.chat.id].set_fruits(message.text)
                    self.enviar_mensaje(message.chat.id, "¿Cuantos vegetales consume el paciente?")
                    self.controlar_estado_usuario(message, "analizar_paciente_vegetales")
                case "analizar_paciente_vegetales":
                    self.patient_user[message.chat.id].set_vegetables(message.text)
                    self.enviar_mensaje(message.chat.id, "¿El paciente consume alcohol?")
                    self.controlar_estado_usuario(message, "analizar_paciente_alcohol")
                case "analizar_paciente_alcohol":
                    self.patient_user[message.chat.id].set_alcohol(message.text)
                    self.enviar_mensaje(message.chat.id, "¿El paciente recibe cuidados de salud actualmente?")
                    self.controlar_estado_usuario(message, "analizar_paciente_cuidados_salud")
                case "analizar_paciente_cuidados_salud":
                    self.patient_user[message.chat.id].set_health_care(message.text)
                    self.enviar_mensaje(message.chat.id, "noDocbcCost")
                    self.controlar_estado_usuario(message, "analizar_paciente_costo")
                case "analizar_paciente_costo":
                    self.patient_user[message.chat.id].set_noDocbcCost(message.text)
                    self.enviar_mensaje(message.chat.id, "¿Cual es el estado general de salud del paciente?")
                    self.controlar_estado_usuario(message, "analizar_paciente_estado_salud")
                case "analizar_paciente_estado_salud":
                    self.patient_user[message.chat.id].set_general_health(message.text)
                    self.enviar_mensaje(message.chat.id, "¿Cual es el estado mental del paciente?")
                    self.controlar_estado_usuario(message, "analizar_paciente_estado_mental")
                case "analizar_paciente_estado_mental":
                    self.patient_user[message.chat.id].set_mental_health(message.text)
                    self.enviar_mensaje(message.chat.id, "¿Cual es el estado fisico del paciente?")
                    self.controlar_estado_usuario(message, "analizar_paciente_estado_fisico")
                case "analizar_paciente_estado_fisico":
                    self.patient_user[message.chat.id].set_physical_health(message.text)
                    self.enviar_mensaje(message.chat.id, "¿El paciente presenta dificultades para caminar?")
                    self.controlar_estado_usuario(message, "analizar_paciente_dificultad_caminar")
                case "analizar_paciente_dificultad_caminar":
                    self.patient_user[message.chat.id].set_walking_difficulties(message.text)
                    self.enviar_mensaje(message.chat.id, "Espere un momento por favor...")
                    self.analizar_paciente(message)
                    self.controlar_estado_usuario(message, "ninguno")
                case _:
                    self.info_bot(message)

        @self.bot.message_handler(func=lambda message: True)
        def handle_comandos_desconocidos(message):
            if message.text.startswith('/'):
                self.manejar_comando_desconocido(message)
            

        self.bot.infinity_polling()

