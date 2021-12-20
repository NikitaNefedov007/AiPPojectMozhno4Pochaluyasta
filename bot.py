import telebot;
import requests;
import string;
from bs4 import BeautifulSoup
bot = telebot.TeleBot('5043775880:AAEZ1P0kk9m0mIh2mZYWt2KqC39bwLY5O4Y')
weapon=''
name=''
URL=''
perem1=''
perem2=0
indx=0
kart='https://cdn.csgo.com//item/AWP+%7C+%D0%90%D0%B7%D0%B8%D0%BC%D0%BE%D0%B2+%28%D0%97%D0%B0%D0%BA%D0%B0%D0%BB%D1%91%D0%BD%D0%BD%D0%BE%D0%B5+%D0%B2+%D0%B1%D0%BE%D1%8F%D1%85%29/100.png'
URL_1 = 'https://market.csgo.com/?s=price&t=all&search=awp%20%7C%20asiimov&sd=asc'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36', 'accept': '*/*' }

@bot.message_handler(commands=['start','help'],content_types=['text','images','photo'])
def get_text_messages(message):

    """функция получает команду от пользоваталя (/start) и отправляет сообщения о готовности бота к работе"""

    if message.text == "/start":
        bot.send_message(message.from_user.id, "Привет! Начинаю работу!")
        bot.send_message(message.from_user.id, "Подключаюсь к сервисам...")
        bot.send_message(message.from_user.id, "Введите название оружия:")
        bot.register_next_step_handler(message,wep_id)

    """функция получает сообщение от пользователя содержащее наимневание искомого оружия и значение присваивается глобальной переменной weapon"""

def wep_id(message):
    global weapon
    weapon=message.text
    bot.send_message(message.from_user.id, "Введите скин оружия:")
    bot.register_next_step_handler(message,wep_sk)

    """функция полуает сообщение содержащее название раскраски искомого оружия, оно записывается в глобальную переменную name
    пробел в названии скина меняется на %20. В дальнейшем именно эта функция будет отправлять износ оружия(guns_vs1,guns_vs3
    guns_vs5) и их актуальные цены(guns_vs2,guns_vs4,guns_vs6),а так жекартинку самого предмета (kartinka)"""

def wep_sk(message):
    global name
    name=message.text
    name=name.replace(' ','%20')
    guns_vs1,guns_vs2,guns_vs3,guns_vs4,guns_vs5,guns_vs6,kartinka=links()
    bot.send_photo(message.from_user.id,kartinka)
    bot.send_message(message.from_user.id,guns_vs1+'  '+guns_vs2)
    bot.send_message(message.from_user.id,guns_vs3+'  '+guns_vs4)
    bot.send_message(message.from_user.id,guns_vs5+'  '+guns_vs6)

    """"в функции links() ссылка изначально указанная в переменной URL_1 изменяется на необходиую, это получается за счёт замены 
    названия и раскраски оружия в строке, обозначающей ссылку"""

def links():
    global URL
    URL=URL_1.replace('awp',weapon)
    URL=URL.replace('asiimov',name)
    return parse()

    """в функции get_htm происходят основные вычисления: код html, полученый в функции parse() обрабатывается и сортируется: в массивы
    guns1 и guns2 заносятся название и стоимость оружия соответсвенно, а в переменную kartinka1 заносится сыллка на изображение оружия, 
    затем удаляются лишние элементы и в глобальную переменную kartinka заносится прямая ссылка на картинку. Далее происходит поиск списков
    на отличающиеся значения в названии оружия """

def get_html(url, params=None):
        r = requests.get(url, headers=HEADERS, params=params)
        return r
def get_content(html):
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

"""функция parse() обращается к сайту по переменной (URL) получение которой было описано выше, затем возвращается html код страницы сайта"""

def parse():
        html= get_html(URL)
        if html.status_code==200:
            return get_content(html.text)
            
        else:
            print('ошибка подключения')

bot.polling(none_stop=True, interval=0)
