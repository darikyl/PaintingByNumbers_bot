from simpful import *
import telebot

bot = telebot.TeleBot("6794433144:AAFtN5U6HR_vO-fKgDDVWOpw78SxbEVYLsg")

# Створюємо об'єкт нечіткої системи
FS = FuzzySystem()

# Визначаємо нечіткі множини та лінгвістичні змінні
difficulty_very_easy = FuzzySet(function=Triangular_MF(a=0.3466, b=1, c=1.706), term="very_easy")
difficulty_easy = FuzzySet(function=Triangular_MF(a=1.39, b=2, c=2.58), term="easy")
difficulty_normal = FuzzySet(function=Triangular_MF(a=2.425, b=3, c=3.6), term="normal")
difficulty_difficult = FuzzySet(function=Triangular_MF(a=3.41, b=4, c=4.641), term="difficult")
difficulty_very_difficult = FuzzySet(function=Triangular_MF(a=4.412, b=5, c=5.2), term="very_difficult")
FS.add_linguistic_variable("difficulty", LinguisticVariable([difficulty_very_easy, difficulty_easy, difficulty_normal,
                                                             difficulty_difficult, difficulty_very_difficult],
                                                            universe_of_discourse=[1, 5]))

price_low = FuzzySet(function=Gaussian_MF(mu=0, sigma=65.54), term="low")
price_average = FuzzySet(function=Gaussian_MF(mu=404.3, sigma=123.9), term="average")
price_high = FuzzySet(function=Gaussian_MF(mu=1500, sigma=341), term="high")
FS.add_linguistic_variable("price",
                           LinguisticVariable([price_low, price_average, price_high], universe_of_discourse=[0, 1500]))

size_small = FuzzySet(function=Gaussian_MF(mu=40, sigma=280.5), term="small")
size_average = FuzzySet(function=Gaussian_MF(mu=1828, sigma=652.3), term="average")
size_big = FuzzySet(function=Gaussian_MF(mu=5000, sigma=1053), term="big")
FS.add_linguistic_variable("size",
                           LinguisticVariable([size_small, size_average, size_big], universe_of_discourse=[40, 5000]))

beauty_rating_bad = FuzzySet(function=Trapezoidal_MF(a=-0.1, b=0, c=1.887, d=2.38), term="bad")
beauty_rating_average = FuzzySet(function=Trapezoidal_MF(a=2.014, b=2.11, c=3.51, d=3.99), term="average")
beauty_rating_beautiful = FuzzySet(function=Trapezoidal_MF(a=3.21, b=3.853, c=5.01, d=7.26), term="beautiful")
FS.add_linguistic_variable("beauty_rating",
                           LinguisticVariable([beauty_rating_bad, beauty_rating_average, beauty_rating_beautiful],
                                              universe_of_discourse=[0, 5]))

# Визначаємо вихідні нечіткі набори та лінгвістичну змінну
decision_low = FuzzySet(function=Triangular_MF(a=-0.1, b=0, c=0.25), term="low")
decision_rather_low = FuzzySet(function=Triangular_MF(a=0.05708, b=0.1929, c=0.4429), term="rather_low")
decision_average = FuzzySet(function=Triangular_MF(a=0.2415, b=0.4915, c=0.7415), term="average")
decision_rather_high = FuzzySet(function=Triangular_MF(a=0.5465, b=0.7965, c=0.947), term="rather_high")
decision_high = FuzzySet(function=Triangular_MF(a=0.752, b=1, c=1.1), term="high")
FS.add_linguistic_variable("decision", LinguisticVariable([decision_low, decision_rather_low, decision_average,
                                                           decision_rather_high, decision_high],
                                                          universe_of_discourse=[0, 1]))

# Додаємо правила з файлу
FS.add_rules_from_file(path='rules.txt')


@bot.message_handler(commands=['help', 'start'])
def info_msg(message):
    bot.send_message(message.chat.id, "Вітаю!\n"
                                      "Цей бот може порадити вам картину по номерам на основі \nваших відповідей про "
                                      "ту чи іншу картину.\n"
                                      "Щоб почати анкетування натисність команду /run.\n"
                                      "Пройдіть опитування і отримайте рекомендацію")


@bot.message_handler(commands=['run'])
def run_quiz(message):
    bot.send_message(message.from_user.id, "Починаємо опитування\n"
                                           "Щоб зупинити опитування натисніть \n/stop\n\n"
                                           "Яка складність картини? (від 1 до 5)")
    bot.register_next_step_handler(message, get_difficulty)


def get_difficulty(message):
    if message.text.lower() == '/stop':
        bot.send_message(message.chat.id, "Опитування припинено.\nНатисність команду /run, щоб почати знову")
        return
    global difficulty
    try:
        difficulty = int(message.text)
    except ValueError:
        bot.send_message(message.chat.id, "Некоректне значення!\n"
                                          "Має бути цифра", parse_mode='Markdown')
        bot.register_next_step_handler(message, get_difficulty)
        return
    if difficulty < 1 or difficulty > 5:
        bot.send_message(message.chat.id, "Некоректне значення!\n"
                                          "Значення має бути від 1 до 5", parse_mode='Markdown')
        bot.register_next_step_handler(message, get_difficulty)
        return
    bot.send_message(message.chat.id, "Яка ціна картини в грн?", parse_mode='Markdown')
    bot.register_next_step_handler(message, get_price)


def get_price(message):
    if message.text.lower() == '/stop':
        bot.send_message(message.chat.id, "Опитування припинено.\nНатисність команду /run, щоб почати знову")
        return
    global price
    try:
        price = int(message.text)
    except ValueError:
        bot.send_message(message.chat.id, "Некоректне значення!\n"
                                          "Має бути число", parse_mode='Markdown')
        bot.register_next_step_handler(message, get_price)
        return
    if price < 0 or price > 1500:
        bot.send_message(message.chat.id, "️Некоректне значення!\n"
                                          "Вартість має бути від 0 до 1500 грн", parse_mode='Markdown')
        bot.register_next_step_handler(message, get_price)
        return
    bot.send_message(message.chat.id, "Який розмір картини? Значення введіть через пробіл", parse_mode='Markdown')
    bot.register_next_step_handler(message, get_size)


def get_size(message):
    if message.text.lower() == '/stop':
        bot.send_message(message.chat.id, "Опитування припинено.\nНатисність команду /run, щоб почати знову")
        return
    global painting_size
    global height
    global width
    input_string = message.text
    numbers = input_string.split()
    # Перевірка, чи є два числа у списку
    if len(numbers) == 2:
        try:
            height = int(numbers[0])
            width = int(numbers[1])
            if height < 0 or width < 0:
                bot.send_message(message.chat.id, "Введіть, будь ласка, додатні значення", parse_mode='Markdown')
                bot.register_next_step_handler(message, get_size)
                return
            painting_size = height * width
        except ValueError:
            bot.send_message(message.chat.id, "Введіть, будь ласка, числові значення", parse_mode='Markdown')
            bot.register_next_step_handler(message, get_size)
            return
    else:
        bot.send_message(message.chat.id, "Некоректний формат введеного рядка.\nЗначення розміру введіть через пробіл",
                         parse_mode='Markdown')
        bot.register_next_step_handler(message, get_size)
        return
    if painting_size > 5000:
        painting_size = 5000
    bot.send_message(message.chat.id, "Яка ваша особиста оцінка картини? Від 0 до 5", parse_mode='Markdown')
    bot.register_next_step_handler(message, get_beauty_rating)


def get_beauty_rating(message):
    if message.text.lower() == '/stop':
        bot.send_message(message.chat.id, "Опитування припинено.\nНатисність команду /run, щоб почати знову")
        return
    global beauty_rating
    try:
        beauty_rating = int(message.text)
    except ValueError:
        bot.send_message(message.chat.id, "Некоректне значення!\n"
                                          "Має бути число", parse_mode='Markdown')
        bot.register_next_step_handler(message, get_beauty_rating)
        return
    if beauty_rating < 0 or beauty_rating > 5:
        bot.send_message(message.chat.id, "️Некоректне значення!\n"
                                          "Вартість має бути від 0 до 5", parse_mode='Markdown')
        bot.register_next_step_handler(message, get_beauty_rating)
        return
    give_decision(message)


def give_decision(message):
    bot.send_message(message.chat.id, "_" + message.chat.first_name + ", введені дані про картину_\nСкладність: " + str(
        difficulty) + "\nЦіна: " + str(
        price) + "\nРозмір: " + str(height * width) + " см2,\nВаша оцінка: " + str(beauty_rating),
                     parse_mode='Markdown')

    variables = ["difficulty", "price", "size", "beauty_rating"]
    values = [difficulty, price, painting_size, beauty_rating]
    for variable, value in zip(variables, values):
        FS.set_variable(variable, value)
    mamdani = FS.Mamdani_inference()
    bot.send_message(message.chat.id, "Рекомендація:\n" + get_decision(mamdani.get("decision")), parse_mode='Markdown')
    bot.send_message(message.chat.id, "Опитування пройдено.\nНатисність команду /run, щоб почати нове")


def get_decision(coef):
    if 0 <= coef < 0.2:
        return "Поганий варіант для покупки, краще оберіть інший"
    elif 0.2 <= coef < 0.4:
        return "Не дуже слушний варіант для покупки, краще оберіть інший"
    elif 0.4 <= coef < 0.6:
        return "Посередній варіант для покупки, можливо краще розглянути інші варіанти"
    elif 0.6 <= coef < 0.8:
        return "Гарний варіант для покупки, має свої недоліки, але нехай це не буде заважати вашому натхненню"
    elif 0.8 <= coef < 1:
        return "Ідеальний варіант для покупки, з великою ймовірністю він принесе вам задоволення при малюванні"


@bot.message_handler(commands=['stop'])
@bot.message_handler(func=lambda msg: msg.text is not None and '/' not in msg.text)
def query_handler(message):
    bot.send_message(message.chat.id, "Опитування припинено.\nНатисність команду /run, щоб почати знову")


bot.infinity_polling()