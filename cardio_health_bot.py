import telebot
from config import TOKEN, contact_list

class MyBot:
    def __init__(self):
        self.token = TOKEN
        self.bot = telebot.TeleBot(TOKEN)
        self.contact_list = contact_list

    def enviar_mensaje(self, chat_id, mensaje):
        self.bot.send_message(chat_id, mensaje)

    def evento_externo(self):
        # Lógica para detectar el evento externo y obtener el mensaje que se enviará
        mensaje = "Este es un mensaje automático en respuesta a un evento externo"
        return mensaje

    def manejar_evento_externo(self):
        mensaje = self.evento_externo()
        for chat_id in self.contact_list:
            self.enviar_mensaje(chat_id, mensaje)

    def inicio(self, mensaje):
        chat_id = mensaje.chat.id
        nombre_usuario = mensaje.from_user.first_name
        mensaje = "Hola {}, bienvenido al bot de prueba".format(nombre_usuario)
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

    def run(self):
        @self.bot.message_handler(commands=['start'])
        def handle_start(message):
            self.inicio(message)

        @self.bot.message_handler(func=lambda message: True)
        def handle_comandos_desconocidos(message):
            if message.text.startswith('/'):
                self.manejar_comando_desconocido(message)

        self.bot.infinity_polling()

