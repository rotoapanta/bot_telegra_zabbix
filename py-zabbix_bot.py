from pyzabbix import ZabbixAPI
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CallbackContext, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
from pythonping import ping
import socket
import re

# Configuración de Zabbix
ZABBIX_URL = 'http://192.168.1.115/zabbix/'  # URL de Zabbix
ZABBIX_USER = 'rtoapanta'  # Usuario de Zabbix
ZABBIX_PASSWORD = 'TECNOLOGO'  # Contraseña de Zabbix

# Configuración de Telegram
TELEGRAM_TOKEN = '1067083332:AAGIQu8Ck8oDQtAJ0GoYRa-9xZ3hjT6OGzA'  # Token de acceso de tu bot de Telegram

# Inicializar la API de Zabbix
zabbix = ZabbixAPI(ZABBIX_URL)
zabbix.login(ZABBIX_USER, ZABBIX_PASSWORD)

def ping_host(update: Update, context: CallbackContext):
    # Enviar el mensaje de solicitud de palabras clave al usuario
    update.message.reply_text('Por favor, ingresa las palabras clave para la búsqueda del host:')


def buscar_host(update: Update, context: CallbackContext):
    # Obtener las palabras clave de la búsqueda
    palabras_clave = update.message.text

    # Buscar hosts en Zabbix
    hosts = zabbix.host.get(search={'name': palabras_clave}, output=['hostid', 'name'])

    # Verificar si se encontraron hosts
    if not hosts:
        update.message.reply_text('No se encontraron hosts.')
        return

    # Crear los botones para los hosts encontrados
    keyboard = [[InlineKeyboardButton(host['name'], callback_data=host['hostid'])] for host in hosts]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Enviar los botones como respuesta al usuario
    update.message.reply_text('Hosts encontrados:', reply_markup=reply_markup)


import re

def obtener_ping(update: Update, context: CallbackContext):
    # Obtener el ID del host seleccionado
    host_id = update.callback_query.data
    print(f"host_id: {host_id}")

    # Obtener la información del host desde Zabbix
    host = zabbix.host.get(hostids=host_id, output=['host'])
    print(f"host: {host}")

    # Obtener la dirección IP del host
    host_interfaces = zabbix.hostinterface.get(hostids=host_id, output=['ip'])
    ip_address = host_interfaces[0]['ip'] if host_interfaces else None

    if ip_address is None:
        update.callback_query.message.reply_text(f"No se pudo obtener la dirección IP del host {host[0]['host']}.")
        return

    print(f"IP: {ip_address}")

    # Obtener el ping del host utilizando pythonping
    respuesta_ping = ping(ip_address, count=5)

    # Convertir la respuesta de ping a una cadena de texto
    respuesta_ping_str = str(respuesta_ping)

    # Enviar la respuesta del ping como mensaje al usuario
    update.callback_query.message.reply_text(f"Respuesta del ping para el host {host[0]['host']} ({ip_address}):\n\n{respuesta_ping_str}")

def main():
    # Configurar el bot de Telegram
    updater = Updater(TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher

    # Manjeador para el comando /ping
    dispatcher.add_handler(CommandHandler('ping', ping_host))

    # Manjeador para la entrada de palabras clave
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, buscar_host))

    # Manjeador para las pulsaciones de botón
    dispatcher.add_handler(CallbackQueryHandler(obtener_ping))

    # Iniciar el bot de Telegram
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()