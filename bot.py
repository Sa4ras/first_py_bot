import config
import telebot
from telebot import types

import requests
import speech_recognition as sr
import soundfile as sf
from gtts import gTTS
import os

bot = telebot.TeleBot(config.token)

def buttons_start(message):
    markup = types.ReplyKeyboardMarkup(row_width=1)
    markup.row('Main menu')
    markup.row('Help')
    bot.send_message(message.chat.id, "Welcome, " + message.from_user.first_name + '!', reply_markup=markup)

def buttons_menu(message):
    markup = types.ReplyKeyboardMarkup(row_width=1)
    markup.row('Send me a random meme please')
    markup.row('Text to voice')
    markup.row('Voice to text')
    bot.send_message(message.chat.id, "Choose one: ", reply_markup=markup)

def random_meme_function(message):
    api_link = ['https://api.memeload.us/v1/random', 'https://some-random-api.ml/meme']
    contents = requests.get(api_link[1]).json() #сделать обработку случаев, если апи не отвечает
    url = contents['image']
    bot.send_photo(message.chat.id, url)

def text_to_voice(message):
    language = 'en'
    myobj = gTTS(text=message.text, lang=language, slow = False)
    myobj.save("user.mp3")
    audio = open('user.mp3', 'rb')
    bot.send_audio(message.chat.id, audio)
    audio.close()
    os.remove("user.mp3")

def voice_to_text_function(user_voice):
    with open("usaudio.wav", "wb") as file:
        file.write(user_voice.voice)
    '''r = sr.Recognizer()
    with user_voice as source:
        audio = r.listen(user_voice)
    sound = user_voice.voice
    #try:
    text = r.recognize_google(sound)
    bot.send_message(user_voice.chat.id, text)
    #except:
     #   bot.send_message(user_voice.chat.id, "Sorry, I can't recognize anything(")
    '''
@bot.message_handler(commands=['start'])
def repeat_all_messages(message):
    buttons_start(message)

@bot.message_handler(regexp='Help')
def button_help(message):
    bot.send_message(message.chat.id, config.help_text)

@bot.message_handler(regexp='Main menu')
def button_reply(message):
    buttons_menu(message)

    @bot.message_handler(regexp='Send me a random meme please')
    def button_send_meme(message):
        random_meme_function(message)

    @bot.message_handler(regexp='Voice to text')
    def button_voice_to_text(message):
        bot.send_message(message.chat.id, "Send me a voice message")

        @bot.message_handler(content_types=['voice'])
        def audio_handler(message):
            bot.send_message(message.chat.id, type(message.voice))
            voice_to_text_function(message)

    @bot.message_handler(regexp='Text to voice')
    def button_text_to_voice(message):
        bot.send_message(message.chat.id, "Send me a text:")

        @bot.message_handler(content_types=['text'])
        def push_text_to_func(content):
            text_to_voice(content)




if __name__ == '__main__':
    bot.polling(none_stop=True)