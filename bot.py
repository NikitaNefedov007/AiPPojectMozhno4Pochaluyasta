# telebot - библиотека для подлючения к боту в телеграмме
# requests библиотека для взаимодействия с web приложениями
# sting - библиотека для работы со строками
# BeautifulSoup - библиотека для получения html кода сайта и последующего его анализа
import telebot;
import requests;
import string;
from bs4 import BeautifulSoup
bot = telebot.TeleBot('5043775880:AAEZ1P0kk9m0mIh2mZYWt2KqC39bwLY5O4Y')  # импортируем токен бота
weapon=''  # переменная типа str будет использована для дальнейшей работы с сылкой, в неё записывается наименование оружия
name=''  # переменная типа str будет использована для дальнейшей работы с сылкой, в неё записывается раскраска оружия
URL=''  # переменная типа str в неё будет записана сама ссылка на просматриваемую страницу сайта

# В URL_1 записывается фиксированная ссылка, которая в дальшейшем будет изменяться, но уже в переменнной URL
URL_1 = 'https://market.csgo.com/?s=price&t=all&search=awp%20%7C%20asiimov&sd=asc'
# Headers необоходима для имитации работы браузера
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36', 'accept': '*/*' }

@bot.message_handler(commands=['start','help'],content_types=['text','images','photo'])
def get_text_messages(message):

        """
        message -- команда от пользователя.
        функция получает на вход переменную message.
        если значение переменной = /start, то бот отправлят сообщения, затем вызывается функция wep_id, 
        ей передаётся значение message"""

    if message.text == "/start":
        bot.send_message(message.from_user.id, "Привет! Начинаю работу!")
        bot.send_message(message.from_user.id, "Подключаюсь к сервисам...")
        bot.send_message(message.from_user.id, "Введите название оружия:")
        bot.register_next_step_handler(message,wep_id)

def wep_id(message):
    
    """
    message -- команда от пользователя.
    функция получает на вход переменную message, её значение записывается в глобальную переменную weapon типа str, затем
    бот отправляет сообщение, и вызывается следющая функция wep_sk, которой передаётся значение message"""

    global weapon
    weapon=message.text
    bot.send_message(message.from_user.id, "Введите скин оружия:")
    bot.register_next_step_handler(message,wep_sk)

def wep_sk(message):
    
    """
    message -- команда от пользователя.
    функция полуает на вход переменную message, оно записывается в глобальную переменную name типа str
    В дальнейшем именно эта функция будет отправлять значения, полученные в процессе работы функции get_content()
    guns_vs1,guns_vs2 - переменные типа list. gun3,guns4,guns5,guns6 переменные типа str,а так же переменна kartinka типа str
    функция вызывает следующую функцию links"""

    global name
    name=message.text
    name=name.replace(' ','%20')
    guns_vs1,guns_vs2,guns_vs3,guns_vs4,guns_vs5,guns_vs6,kartinka=links()
    bot.send_photo(message.from_user.id,kartinka)
    bot.send_message(message.from_user.id,guns_vs1+'  '+guns_vs2)
    bot.send_message(message.from_user.id,guns_vs3+'  '+guns_vs4)
    bot.send_message(message.from_user.id,guns_vs5+'  '+guns_vs6)

def links():
    
    """"в функции происходит обращение к глобальным переменным weapon и name. Методом replace изменяется исходное значение в 
    переменной URL. она возвращает get_content. (Отпарсенную страницу) затем в parse() передаётся ссылка, вызывается get_content и извлекаются данные.
    """
        
    global URL
    URL=URL_1.replace('awp',weapon)
    URL=URL.replace('asiimov',name)
    return parse()

def get_html(url, params=None):
    
        """
        params -- опциональный аргумент, (по умолчанию = None)
        url -- страницы с которой необходимо получить контент
        функция на вход получает url (url - переменная типа str) страницы с которой необходимо получить контент. далее выполняется get запрос, 
        который записывается в переменную r и в конце своей работы, функция возвращает эту переменную"""
    
        r = requests.get(url, headers=HEADERS, params=params)
        return r
    
    
def get_content(html):
    
    """
    html -- весь код страницы в текстовом виде. переменная типа str.
    функция вызывается функцией parse и получает переменную html. Объекту soup передаются переменная html и тип переменной с которой предстоит работа.
    также задаются переменные которые возвращает функция: списки: guns1,guns2 и строки: guns3,guns4,guns5,guns6 и задаётся глобальная переменная kartinka.
    Задачей функции является обработка html кода страницы и выявление значений по заданным параметрам"""
    
    soup=BeautifulSoup(html,'html.parser')
    items=soup.find_all('a', class_="item hot")
    guns1=[]
    guns2=[]
    guns3=''
    guns4=''
    guns5=''
    guns6=''
    global kartinka
    kartinka1=''
    for item in items:
        kartinka1=item.find('div', class_="image")
        guns1.append(item.find('div', class_="name").get_text().replace('\n','').replace('ё','е').replace(' |',''))
        guns2.append(item.find('div', class_="price").get_text().replace('\xa0','').replace(' ',''))
    if guns1!=[]:
        print(guns1[0],guns2[0])
        for m in range(0,len(guns1)):
            if guns1[m]==guns1[m+1] and m<len(guns1)-1:
                m=m
            else:
                m=m+1
                break
        guns3=(guns1[m])
        guns4=(guns2[m])
        for m in range(m,len(guns1)):
            if guns1[m]==guns1[m+1] and m<len(guns1)-1:
                m=m
            else:
                m=m+1
                break
        guns5=(guns1[m])
        guns6=(guns2[m])
        kartinka1=kartinka1.__str__().replace('<div class="image" style="background-image: url(', "")
        kartinka1=kartinka1.__str__().replace(');"></div>', "")
        kartinka=kartinka1
        return guns1[0],guns2[0],guns3,guns4,guns5,guns6,kartinka
    else:
        print('ошибка')

def parse():
    
    """функция parse() обращается к сайту по глобальной переменной (URL) типа str получение которой было описано выше, затем возвращается html код страницы сайта
    или сообщаетcя об ошибке подлючения."""
    
        html= get_html(URL)
        if html.status_code==200:
            return get_content(html.text)
            
        else:
            print('ошибка подключения')

bot.polling(none_stop=True, interval=0)
