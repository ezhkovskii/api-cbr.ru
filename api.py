import requests
import datetime
import xml.etree.ElementTree as ET

def GetDateYesterday():
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
    DateYesterday = day + "/" + month + "/" + year
    return DateYesterday


def GetDollarAndEuro(date):
    result = {
        'dollar': '',
        'euro': '',
    }
    r = requests.get('http://www.cbr.ru/scripts/XML_daily.asp?date_req=%s'  % (date))
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

def GetGold(date):
    result = {
        'gold': '',
        'silver': '',
    }
    r = requests.get('http://www.cbr.ru/scripts/xml_metall.asp?date_req1=%s&date_req2=%s' % (date,date))
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

DateYesterday = GetDateYesterday()

Valute = GetDollarAndEuro(DateYesterday)
Metall = GetGold(DateYesterday)

print('Курсы валют на %s:' % (DateYesterday))
print('%s: %s' % ('Доллар', Valute['dollar']))
print('%s: %s' % ('Евро', Valute['euro']))

print('Котировки драгоценных металлов на %s:' % (DateYesterday))
print('%s: %s' % ('Золото', Metall['gold']))
print('%s: %s' % ('Евро', Metall['silver']))