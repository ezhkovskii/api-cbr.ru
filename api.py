import requests
import datetime
import xml.etree.ElementTree as ET


'''
Функция возвращает текущую дату в формате 01/01/1900
'''
def get_date_today():
    today = datetime.datetime.today()
    if today.day < 10:
        day = '0' + str(today.day)
    else:
        day = str(today.day)
    if today.month < 10:
        month = '0' + str(today.month)
    else:
        month = str(today.month)
    year = str(today.year)
    date_today = day + "/" + month + "/" + year
    return date_today


'''
Функция возвращает вчерашнюю дату в формате 01/01/1900
'''
def get_date_yesterday():
    yesterday = datetime.datetime.today() - datetime.timedelta(days=1)
    if yesterday.day < 10:
        day = '0' + str(yesterday.day)
    else:
        day = str(yesterday.day)
    if yesterday.month < 10:
        month = '0' + str(yesterday.month)
    else:
        month = str(yesterday.month)
    year = str(yesterday.year)
    date_yesterday = day + "/" + month + "/" + year
    return date_yesterday


'''
Функция возвращает завтрашнюю дату в формате 01/01/1900
'''
def get_date_tomorrow():
    tomorrow = datetime.datetime.today() + datetime.timedelta(days=1)
    if tomorrow.day < 10:
        day = '0' + str(tomorrow.day)
    else:
        day = str(tomorrow.day)
    if tomorrow.month < 10:
        month = '0' + str(tomorrow.month)
    else:
        month = str(tomorrow.month)
    year = str(tomorrow.year)
    date_tomorrow = day + "/" + month + "/" + year
    return date_tomorrow


'''
Функция возвращает словарь с элементами доллар и евро
'''
def get_dollar_and_euro(date):
    result = {
        'dollar': '',
        'euro': '',
    }
    r = requests.get('http://www.cbr.ru/scripts/XML_daily.asp?date_req=%s' % (date))
    structure = ET.fromstring(r.content)
    try:
        dollar = structure.find("./*[@ID='R01235']/Value")
        result['dollar'] = dollar.text.replace(',', '.')
        euro = structure.find("./*[@ID='R01239']/Value")
        result['euro'] = euro.text.replace(',', '.')
        return result
    except:
        result['dollar'] = 'Неизвестно'
        result['euro'] = 'Неизвестно'
        return result


'''
Функция возвращает словарь с элементами золото и серебро
'''
def get_gold_and_silver(date):
    result = {
        'gold': '',
        'silver': '',
    }
    r = requests.get('http://www.cbr.ru/scripts/xml_metall.asp?date_req1=%s&date_req2=%s' % (date, date))
    structure = ET.fromstring(r.content)
    try:
        gold = structure.find("./*[@Code='1']/Sell")
        result['gold'] = gold.text.replace(',', '.')
        silver = structure.find("./*[@Code='2']/Sell")
        result['silver'] = silver.text.replace(',', '.')
        return result
    except:
        result['gold'] = 'Неизвестно'
        result['silver'] = 'Неизвестно'
        return result


'''
Процедура выводит курсы валют и котировки драгоценных металлов на определенную дату
'''
def print_currency_and_metall(currency, metall, date):
    # Вывод ввиде таблицы
    result = "%10s\t%10s\t%10s\t%10s\t%10s" % (
    date, currency['dollar'], currency['euro'], metall['gold'], metall['silver'])
    print(result)

    '''
    print('Курсы валют и котировки драгоценных металлов на %s:' % (date))
    print('%s: %s' % ('Доллар', currency['dollar']))
    print('%s: %s' % ('Евро', currency['euro']))
    print('%s: %s' % ('Золото', metall['gold']))
    print('%s: %s' % ('Серебро', metall['silver']))
    print()
    '''


if __name__ == "__main__":

    dates = [get_date_tomorrow(), get_date_today(), get_date_yesterday()]

    print("%10s\t%10s\t%10s\t%10s\t%10s" % ("Дата", "Доллар", "Евро", "Золото", "Серебро"))
    for date in dates:
        currency = get_dollar_and_euro(date)
        metall = get_gold_and_silver(date)

        print_currency_and_metall(currency, metall, date)
