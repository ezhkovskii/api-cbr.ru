import requests
import datetime
import xml.etree.ElementTree as ET

def GetDateToday():
    #yesterday = datetime.datetime.today() - datetime.timedelta(days=1)
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
    DateToday = day + "/" + month + "/" + year
    return DateToday

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

def GetDateTomorrow():
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
    DateTomorrow = day + "/" + month + "/" + year
    return DateTomorrow


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

def GetGoldSilver(date):
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

Dates = [GetDateTomorrow(), GetDateToday(), GetDateYesterday()]

for date in Dates:
    Valute = GetDollarAndEuro(date)
    Metall = GetGoldSilver(date)
    print('Курсы валют и котировки драгоценных металлов на %s:' % (date))
    print('%s: %s' % ('Доллар', Valute['dollar']))
    print('%s: %s' % ('Евро', Valute['euro']))
    print('%s: %s' % ('Золото', Metall['gold']))
    print('%s: %s' % ('Серебро', Metall['silver']))
    print()

