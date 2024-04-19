import telebot
from telebot import types

bot = telebot.TeleBot("6417568746:AAHkFkvCh4A5n3hbY0fvxBKegdXX__9czt4")

# В этой части мы создаем все переменные, которые будут нуджны для того, чтобы сохранять
# предметы и прочую информаию об абитуриенте. || Здесь же я предлагаю подключить базу данных с предметами.


yes_no = ''


class Person:
    def __init__(self, name='', surname='', age=0, subject1='', subject2='', subject3=''):
        self.name = name
        self.age = age
        self.surname = surname
        self.subject1 = subject1
        self.subject2 = subject2
        self.subject3 = subject3


database = [Person() for i in range(20000)]

isThirdSubjectAsked = False
isRegistered = False
askForThirdSubject = False
last_message_id = 0
mark1 = 0
mark2 = 0
mark3 = 0
person1 = Person()


# Ниже расположены функции, которые управляют начальным диалогом бота с польлзователем.

@bot.message_handler(content_types=['text'])
def start(message):
    global isRegistered
    global isThirdSubjectAsked
    global askForThirdSubject
    global last_message_id
    if message.text == '/reset' and isRegistered:
        person1.name = ''
        person1.surname = ''
        person1.subject1 = ''
        person1.subject2 = ''
        person1.subject3 = ''
        isThirdSubjectAsked = False
        isRegistered = False
        askForThirdSubject = False
    elif not isRegistered and message.text != '/reg':
        bot.send_message(message.from_user.id, 'Здравствуйте, напишите пожалуйста /reg, чтобы начать работу')

    elif message.text == '/reg' and person1.name == '':
        isRegistered = True
        bot.send_message(message.from_user.id, "Давайте приступим.")
        bot.send_message(message.from_user.id, "Как ваше имя?")

    elif person1.name == '':
        person1.name = message.text
        bot.send_message(message.from_user.id, "Здравствуйте " + message.text)
        bot.send_message(message.from_user.id, "А как ваша фамилия?")

    elif person1.surname == '':
        person1.surname = message.text
        bot.send_message(message.from_user.id, "Приятно познакомиться " + person1.name + " " + person1.surname)
        bot.send_message(message.from_user.id,
                         "Чтобы подобрать наиболее подходящую для Вас специальность, мне нужно узнать какие предметы вы сдавали на ЕГЭ. Из представленного ниже списка выберите пожалуйста сдаваемые вами предметы.")

    elif person1.subject1 == '':
        person1.subject1 = message.text
        bot.send_message(message.from_user.id, "Первый: " + message.text)
        bot.send_message(message.from_user.id, "Второй какой")

    elif person1.subject2 == '':
        person1.subject2 = message.text
        bot.send_message(message.from_user.id, "Второй: " + message.text)
        bot.send_message(message.from_user.id, "Ты третий сдавал? (Да/Нет)")

    elif person1.subject3 == '' and not isThirdSubjectAsked:
        if message.text == 'Нет' or message.text == 'нет':
            isThirdSubjectAsked = True
            bot.send_message(message.from_user.id, "Не сдавал, ok.")
        elif message.text == 'Да' or message.text == 'да':
            isThirdSubjectAsked = True
            askForThirdSubject = True
            bot.send_message(message.from_user.id, "И какой?")
        else:
            bot.send_message(message.from_user.id, "Извините, я не распознал Вашего ответа. Выберите (Да/Нет)")
    elif person1.subject3 == '' and askForThirdSubject:
        person1.subject3 = message.text
        bot.send_message(message.from_user.id, "Третий: " + person1.subject3)
        markup = types.InlineKeyboardMarkup()
        button_correct = types.InlineKeyboardButton(text='Да', callback_data='yes')
        button_incorrect = types.InlineKeyboardButton(text='Нет', callback_data='no')
        markup.add(button_correct, button_incorrect)
        bot.send_message(message.from_user.id,
                         "Давайте сверим данные. " + person1.name + " " + person1.surname + "\n Вы сдавали: " + person1.subject1 + ", " + person1.subject2 + ", " + person1.subject3, reply_markup=markup)
        bot.register_next_step_handler()

    else:
        markup = types.InlineKeyboardMarkup()
        button_correct = types.InlineKeyboardButton(text='Да', callback_data='yes')
        button_incorrect = types.InlineKeyboardButton(text='Нет', callback_data='no')
        markup.add(button_correct, button_incorrect)
        bot.send_message(message.from_user.id,
                         "Давайте сверим данные. " + person1.name + " " + person1.surname + "\n Вы сдавали: " + person1.subject1 + ", " + person1.subject2 + ", " + person1.subject3, reply_markup=markup)


def answer_check(callback):
    if callback.message:
        if callback.data == 'yes':
            bot.send_message(callback.message.chat.id, 'Отлично, теперь давайте узнаем, какие у вас баллы по этим предметам')
            bot.register_next_step_handler(callback, )
        elif callback.date == 'no':
            bot.send_message(callback.message.chat.id, 'Хоршо, давайте начнём с начала')
            bot.register_next_step_handler(callback, start)


def get_subject_score(message):
    global subject1
    global mark1
    mark1 = message.text
    bot.send_message(message.from_user.id, 'По ' subject1 + mark1)
    # bot.register_next_step_handler(message, )

    # В этой части мы прописываем клавиши, которые подтверждают информацию о предметах.

    # Создается  виртуальная "клавиатура"
    markup = types.InlineKeyboardMarkup()

    # Добавляются кнопки взаимодействия
    # button_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
    # button_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
    # markup.add(button_yes, button_no)

    question = 'Давайте убедимся, всё ли верно. ' + person1.name + ' ' + person1.surname + ', предметы, которые вы сдавали: ' + person1.subject1 + ' ' + person1.subject2 + ' верно?'
    question2 = 'Давайте убедимся, всё ли верно. ' + person1.name + ' ' + person1.surname + ', предметы, которые вы сдавали: ' + person1.subject1 + ' ' + person1.subject2 + ' ' + subject3 + ' верно?'
    bot.send_message(message.from_user.id, text=question, reply_markup=markup)

    bot.register_next_step_handler()


# Теперь, когда мы знаем, какие предметы сдавал абитурент, можно спросить его о баллах.


def sub1_mark(message):
    global mark1
    mark1 = message.text
    bot.send_message(message, 'Ваша оценка, по предмету: ' + person1.subject1 + ' ' + mark1)


bot.infinity_polling()
