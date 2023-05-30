from decouple import config
import json
from media_kaktus import data_news
import telebot
from telebot import types


bot = telebot.TeleBot(config('TOKEN'))


@bot.message_handler(commands=['start'])
def start(message:types.Message):
    
    bot.send_message(message.chat.id, text="Добро пожаловать!\nПодождите идет загрузка...🕗")
    data_news()
    data_base(message)
    
def data_base(message:types.Message): 
    global data   
    with open ('data.json') as file:
        data = json.load(file)
    
    for nums,item in enumerate(data,1):
        bot.send_message(message.chat.id, text=str(nums)+'. '+item['title'])
    
    
    start_buttons_nums = ['💳'+str(i) for i in range(1,21)]
    keybord_nums = types.ReplyKeyboardMarkup(row_width=5,resize_keyboard=True)
    keybord_nums.add(*start_buttons_nums)
    
    message2 = bot.send_message(message.chat.id, "Выбери номер новости: ", reply_markup=keybord_nums)
    bot.register_next_step_handler(message2, handle_text)
    
def handle_text(message):
    global number_news
    global keybord_chose
    number_news = int(message.text[-1])
    keybord_chose = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1  = types.KeyboardButton("Description")
    button2 = types.KeyboardButton('Photo')
    button3 = types.KeyboardButton('Quit')
    keybord_chose.add(button1,button2,button3)
    message2 = bot.send_message(message.chat.id, "You can see Description of this news and Photo", reply_markup=keybord_chose)
    bot.register_next_step_handler(message2, chose)
    
def chose(message):
    if message.text == 'Description':
        bot.send_message(message.chat.id, text=data[number_news-1]['description'],reply_markup=types.ReplyKeyboardRemove())
        keybord = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1  = types.KeyboardButton("Yes")
        button2 = types.KeyboardButton('NO')
        keybord.add(button1,button2)
        bot.send_message(message.chat.id, text='Читать полностью: '+ data[number_news-1]['link'])
        message2 = bot.send_message(message.chat.id, "Хотите посмотреть другие новости?", reply_markup=keybord)
        bot.register_next_step_handler(message2,end)

        
    elif message.text == 'Photo':
        bot.send_photo(message.chat.id, data[number_news-1]['photo'],reply_markup=types.ReplyKeyboardRemove())
        message2 = bot.send_message(message.chat.id, "You can see Description of this news and Photo", reply_markup=keybord_chose)
        bot.register_next_step_handler(message2, chose)
        
    elif message.text == 'Quit':
        bot.send_message(message.chat.id, text="До свидания",reply_markup=types.ReplyKeyboardRemove())
        
    else:
        bot.send_message(message.chat.id, text="Такой команды нету!",reply_markup=types.ReplyKeyboardRemove())
        message2 = bot.send_message(message.chat.id, "You can see Description of this news and Photo", reply_markup=keybord_chose)
        bot.register_next_step_handler(message2, chose)

def end(message:types.Message):
    if message.text == "Yes":
        data_base(message)
    else:
        bot.send_message(message.chat.id, text="До свидания",reply_markup=types.ReplyKeyboardRemove())


def main():
    bot.polling()
   
if __name__ == '__main__':
    main()