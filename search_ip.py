import requests
import telebot
import time
from config import bot_id


bot = telebot.TeleBot(bot_id) #Enter your bot id


def get_info_ip(ip: str = '127.0.0.1') -> str:

    try:
        response = requests.get(url=f'http://ip-api.com/json/{ip}').json()
        status = response.get('status')
        if status == "success":
            global lat, lon
            lat = response.get('lat')
            lon = response.get('lon')
            user_data = {
                '[IP]': response.get('query'),
                '[Int provider]': response.get('isp'),
                '[Organization]': response.get('org'),
                '[Country]': response.get('country'),
                '[Region Name]': response.get('regionName'),
                '[City]': response.get('city'),
                '[ZIP]': response.get('zip'),
            }
            result = ''

            for k, v in user_data.items():
                result += k[1:-1] + ': ' + str(v) + '\n'
            return result

        else:
            return f'[!] Status: {status}'

    except requests.exceptions.ConnectionError:
        return '[!] Check your connection!'


def ip_correct_checker(ip: str) -> bool:
    try:
        ip_list = ip.split('.')
        if len(ip_list) == 4:
            for num in ip_list:
                if not 0 <= int(num) <= 255:
                    return False
        else:
            return False
        return True
    except ValueError:
        return False


@bot.message_handler(commands=["start"])
def start(m, res=False):
    if m.from_user.last_name:
        bot.send_message(m.chat.id, text=f"Hello, {m.from_user.first_name} {m.from_user.last_name}!"
                                         f" I am IP-CheckerBot. If you want to know about target"
                                         f" IP address - let's do it together!")
    else:
        bot.send_message(m.chat.id, text=f"Hello, {m.from_user.first_name}!"
                                         f" I am IP-CheckerBot. If you want to know about target"
                                         f" IP address - let's do it together!")
    time.sleep(5)
    bot.send_message(m.chat.id, text="I can find out internet provider, organization,"
                                     " country region, city, zip code and user location!")
    time.sleep(5)
    bot.send_sticker(m.chat.id, "CAACAgIAAxkBAAEEGm5iKcGxM3agYeCbxaqAOsoiRB7NsQACqAIAAi8P8AaI2qBqs3F_0yME")
    time.sleep(1)
    bot.send_message(m.chat.id, text="Send me IP address: ")


@bot.message_handler(content_types=["text"])
def handle_text(message):
    if ip_correct_checker(message.text):
        data = get_info_ip(ip=message.text)
        if 'Status' not in data:
            bot.send_message(message.chat.id, data)
            bot.send_location(message.chat.id, latitude=lat, longitude=lon)
        else:
            bot.send_message(message.chat.id, text="IP address information not available.")
            time.sleep(0.7)
            bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAEEGo9iKdK7VK0I2gv7UT1dGMDs0VPTdgAC2wgAAnlc4gnjh-VCkUOrwyME")
    else:
        bot.send_message(message.chat.id, text="Check the IP-address: it must be integer in"
                                               " 0 to 255 range with points split"
                                               " ('97.98.99.100' for example)")


bot.polling(none_stop=True, interval=0)
