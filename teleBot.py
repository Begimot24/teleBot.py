import telebot
from telebot import types


bot = telebot.TeleBot("6417568746:AAHkFkvCh4A5n3hbY0fvxBKegdXX__9czt4")

#В этой части мы создаем все переменные, которые будут нуджны для того, чтобы сохранять
# предметы и прочую информаию об абитуриенте. || Здесь же я предлагаю подключить базу данных с предметами.

name = ''
surname = ''
age = 0
subject1 = ''
subject2 = ''
subject3 = ''

yes_no = ''
third_subject = False


#Ниже расположены функции, которые управляют начальным диалогом бота с польлзователем.


@bot.message_handler(content_types=['text'])
def start(message):
	if message.text == '/reg':
		bot.send_message(message.from_user.id, "Здравствуйте, как ваше имя?")
		bot.register_next_step_handler(message, get_name)
	else:
		bot.send_message(message.from_user.id, 'Здравствуйте, напишите пожалуйста /reg, чтобы начать работу')


def get_name(message):
	global name
	name = message.text
	bot.send_message(message.from_user.id, 'Очень приятно, ' + name + '. А как ваша фамилия?')
	bot.register_next_step_handler(message, get_surname)


def get_surname(message):
	global surname
	surname = message.text
	bot.send_message(message.from_user.id, 'Приятно познакомиться ' + surname + ' ' + name + '. Какие предметы вы сдавали? Назовите их по порядку, пожалуйста')
	bot.register_next_step_handler(message, get_subject1)


def get_subject1(message):
	global subject1
	subject1 = message.text
	bot.send_message(message.from_user.id, 'Хорошо, ваш первый предмет - ' + subject1 + '. А второй?')
	bot.register_next_step_handler(message, get_subject2)


def get_subject2(message):
	global subject2
	subject2 = message.text
	bot.send_message(message.from_user.id, 'Ваш второй предмет - ' + subject2 + '. Сдавали ли вы какой-нибудь третий предмет?' )
	bot.register_next_step_handler(message, choice)


def choice(message):
	global third_subject
	global yes_no
	loop_key = 0

	yes_no = message.text

	while loop_key == 0:
		if yes_no == 'Да' or yes_no == 'да':
			bot.reply_to(message, 'Какой ваш третий предмет?')
			bot.register_next_step_handler(message, get_subject3)
			third_subject = True
			loop_key = 1
		elif yes_no == 'Нет' or yes_no == 'нет':
			#bot.register_next_step_handler(message, )
			pass
			loop_key = 1
		else:
			bot.reply_to(message, 'Извините, я не до конца понимаю ваш ответ.')


def get_subject3(message):
	global subject3
	subject3 = message.text
	bot.send_message(message.from_user.id, 'Ваш третий предмет - ' + subject3)
	#bot.register_next_step_handler(message, )



	keyboard = types.InlineKeyboardMarkup()
	key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
	keyboard.add(key_yes)
	key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
	keyboard.add(key_no)
	question = 'Давайте убедимся, что всё верно. ' + name + ' ' + surname + ', предметы, которые вы сдавали: ' + subject1 + ' ' + subject2 + ' верно?'
	question2 = 'Давайте убедимся, что всё верно. ' + name + ' ' + surname + ', предметы, которые вы сдавали: ' + subject1 + ' ' +  subject2 + ' ' + subject3 + ' верно?'
	bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)

bot.infinity_polling()
