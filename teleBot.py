import psycopg2
import telebot
from telebot import types

bot = telebot.TeleBot("6417568746:AAHkFkvCh4A5n3hbY0fvxBKegdXX__9czt4")

# В этой части мы создаем все переменные, которые будут нуджны для того, чтобы сохранять
# предметы и прочую информаию об абитуриенте. || Здесь же я предлагаю подключить базу данных с предметами.

#подключаем БД
conn = psycopg2.connect('postgresql://gen_user:8s%25%25esY%3F)FCIsB@147.45.151.87:5432/default_db')
cursor = conn.cursor()
cursor.execute("set search_path to speciality_bot_schema")


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

#Функция проверки. Набрал ли человек пороговые баллы для поступления в ВУЗ
def check(subject1, score1, subject2, score2, subject3, score3):
    is_passing = False
    cursor.execute("select passing_score from subjects where name = %s", (subject1,))
    passing_score1 = cursor.fetchone()[0]
    cursor.execute("select passing_score from subjects where name = %s", (subject2,))
    passing_score2 = cursor.fetchone()[0]
    cursor.execute("select passing_score from subjects where name = %s", (subject3,))
    passing_score3 = cursor.fetchone()[0]
    if (score1 >= passing_score1 and score2 >= passing_score2 and score3 >= passing_score3):
        is_passing = True
    return(is_passing)

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
    bot.send_message(message.from_user.id, 'По ', subject1 + mark1)
    # bot.register_next_step_handler(message, )

    # В этой части мы прописываем клавиши, которые подтверждают информацию о предметах.

    # Создается  виртуальная "клавиатура"
    markup = types.InlineKeyboardMarkup()

    # Добавляются кнопки взаимодействия
    # button_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
    # button_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
    # markup.add(button_yes, button_no)

    question = 'Давайте убедимся, всё ли верно. ' + person1.name + ' ' + person1.surname + ', предметы, которые вы сдавали: ' + person1.subject1 + ' ' + person1.subject2 + ' верно?'
    question2 = 'Давайте убедимся, всё ли верно. ' + person1.name + ' ' + person1.surname + ', предметы, которые вы сдавали: ' + person1.subject1 + ' ' + person1.subject2 + ' ' + person1.subject3 + ' верно?'
    bot.send_message(message.from_user.id, text=question, reply_markup=markup)

    bot.register_next_step_handler()


# Теперь, когда мы знаем, какие предметы сдавал абитурент, можно спросить его о баллах.


def sub1_mark(message):
    global mark1
    mark1 = message.text
    bot.send_message(message, 'Ваша оценка, по предмету: ' + person1.subject1 + ' ' + mark1)


#Если пороговые баллы по всем предметам набраны начинаем выбирать специальность
if (check(person1.subject1, mark1, person1.subject2, mark2, person1.subject3, mark3)):
    #заполняем массив предметов.он хранит айдишники сданных предметов
    cursor.execute("select id from subjects where name in (%s, %s, %s)",(person1.subject1,person1.subject2,person1.subject3,))
    subjects = cursor.fetchall()
    s = list(map(lambda s: s[0],subjects))

    #выбираем специальности, для которых подходит данный набор предметов, пока не учитываем сумму баллов
    cursor.execute("select specialities_id from specialities_subjects where subjects_id in (%s, %s, %s) group by specialities_id having count(distinct subjects_id) = 3", (subjects[0], subjects[1], subjects[2],))
    sp_id = cursor.fetchall()
    sp_id = list(map(lambda s: s[0],sp_id))
    #массив specialities будет хранить все специальности, подходящие по сумме баллов и предметам.
    #сеты passing_faculty, passing_degree факультеты и степени(бакалавр и тд) этих специальностей
    specialities = []
    passing_faculty = set()
    passing_degree = set()
    #заполняем массив, сравнивая сумму баллов с проходным прошлого года
    score = mark1 + mark2 + mark3
    for i in sp_id:
        cursor.execute("select name, faculty, degree from specialities where id = %s and passing_score <= %s", (i,score,))
        x = cursor.fetchone()
        if x != None:
            specialities.append(x)
            passing_faculty.add(x[1])
            passing_degree.add(x[2])

    #по сумме баллов подходит 0 специальностей. пишем что подходящих специальностей нет
    if len(specialities) == 0:
        print('no suitable specialities')

    # по сумме баллов подходит несколько специальностей
    elif len(specialities) > 1 and len(passing_faculty) > 1:
        #бот спрашивает предпочтения человека и заносит факультеты в массив faculty
        faculty = ['инженерной механики', 'комплексной безопасности ТЭК']
        #массив, хранящий специальности, с учетом выбранных факультетов
        sp_faculty = []
        for i in specialities:
            if i[1] in faculty:
                sp_faculty.append(i)

        #если есть выбор спец/бакалавр спрашиваем
        if len(sp_faculty) > 1 and len(passing_degree) > 1:
            # массив, хранящий специальности, с учетом выбранных факультетов и уровня подготовки(спец/бакалавр)
            dg_sp_faculty = []
            degree = ['Специалитет']
            for i in specialities:
                if i[2] in degree:
                    dg_sp_faculty.append(i)
            for i in dg_sp_faculty:
                print(i[0])

        #выбор с/б отсутствует
        else:
            print(sp_faculty)

    #по сумме баллов подходит 1 специальность .выводим ее
    else:
        print(specialities[0][0], 'факультет', specialities[0][0])

#Пороговые баллы не набраны
else:
    print("too small score")


conn.close()
bot.infinity_polling()