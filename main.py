import telebot
from telebot import types
from ssh_connection import Connection


# Replace with your bot token
TOKEN = 'YOU_TOKEN'
bot = telebot.TeleBot(TOKEN)

# Список разрешённых пользователей по их Telegram ID
ALLOWED_USERS = ['USER_ID_TO_TL', 'USER_ID_TO_TL']  # Вставьте сюда Telegram ID пользователей, которые могут использовать бота

# Define the keyboard layout
keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
button1 = types.KeyboardButton("Minecraft ON")
button2 = types.KeyboardButton("Minecraft OFF")
button3 = types.KeyboardButton("ARK ON")
button4 = types.KeyboardButton("ARK OFF")
button5 = types.KeyboardButton("SERVER RESTART")
button6 = types.KeyboardButton("TOP")

# Add buttons to the keyboard
keyboard.add(button6)
keyboard.add(button1, button3)
keyboard.add(button2, button4)
keyboard.add(button5)

# Функция проверки, разрешён ли пользователь
def is_allowed(user_id):
    return user_id in ALLOWED_USERS

# Command to start the bot
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    if not is_allowed(user_id):
        # Заблокировать пользователя и отправить сообщение
        bot.send_message(message.chat.id, "You are not authorized to use this bot.")
        bot.ban_chat_member(message.chat.id, user_id)
    else:
        bot.send_message(message.chat.id, "Hi! This is a bot with a keyboard for server administration.", reply_markup=keyboard)

# Функция для выполнения SSH-команд
def execute_ssh_command(command):
    try:
        result = Connection().connect(ip='SERVER_IP', username='SERVER_username', password='YOU_PASSWORD', port=22, comande=command)
        return f"Command output:\n{result}"
    except Exception as e:
        # Логирование ошибки (псевдокод, замените print на ваш метод логирования)
        print(f"Error occurred while executing command '{command}': {e}")
        return f"SSH connection failed: {e}"
# Handling button presses
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    if not is_allowed(user_id):
        # Заблокировать пользователя при любой активности
        bot.send_message(message.chat.id, "You are not authorized to use this bot.")
        bot.ban_chat_member(message.chat.id, user_id)
    else:

        if message.text == "Minecraft ON":
            response = execute_ssh_command('source myvenv/bin/activate && python3 main.py')
            bot.send_message(message.chat.id, response)
        elif message.text == "Minecraft OFF":
             response = execute_ssh_command('pkill python3')
             bot.send_message(message.chat.id, response)
        elif message.text == "ARK ON":
            bot.send_message(message.chat.id, "You have pressed Button ARK ON")
        elif message.text == "ARK OFF":
            bot.send_message(message.chat.id, "You have pressed Button ARK OFF")
        elif message.text == "SERVER RESTART":
            bot.send_message(message.chat.id, "You have pressed Button SERVER RESTART")
        elif message.text == "TOP":
            bot.send_message(message.chat.id, "You have pressed Button TOP")
        else:
            bot.send_message(message.chat.id, "Unknown command")

# Start polling (listening for messages)
bot.polling(none_stop=True)
