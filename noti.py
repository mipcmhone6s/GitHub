#!/usr/bin/python
# coding=utf-8

import sys
import time
import sqlite3
import telepot
from pprint import pprint
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from datetime import date, datetime, timedelta
import traceback

from tkinter import *
from tkinter import font
import http.client
from xml.dom.minidom import parse, parseString

key = 'OPt4yOPTFT%2FkIL2tnYeHbROYLt3tlvJBB%2BjgIZgt0d%2FNEqLMQz%2BPJQqP7srCQwZZfXcnekixqhCrWiq7X22E1w%3D%3D&pageNo=1&startPage=1&numOfRows=100&pageSize=100&MobileApp=AppTest&MobileOS=ETC&arrange=A&contentTypeId='
TOKEN = '600412514:AAGTegsX0z47BjN0vaSpIkjnEb41TYkEXaY'
MAX_MSG_LENGTH = 300
baseurl = 'http://api.visitkorea.or.kr/openapi/service/rest/KorService/areaBasedList?serviceKey='+key
bot = telepot.Bot(TOKEN)

def getData(RememberContentCode, RememberAreaCode, RememberSubAreaCode):
    url = baseurl + str(RememberContentCode) + "&areaCode=" + RememberAreaCode + "&sigunguCode=" + str(
        RememberSubAreaCode) + "&listYN=Y"
    res_list = []

    #print(url)
    res_body = urlopen(url).read()
    #print(res_body)
    soup = BeautifulSoup(res_body, 'html.parser')
    items = soup.findAll('item')

    conn = http.client.HTTPConnection("api.visitkorea.or.kr")
    conn.request("GET",
                 "/openapi/service/rest/KorService/areaBasedList?serviceKey=uAZ4kkFChL5d%2FLnSAxDGp6wkFCgE%2BovQ6W%2FC8gk5%2FA2%2BxhIRSXALj%2FV3SppGEippCgUluNCQ9mT9XdkQXbO1jg%3D%3D&pageNo=1&startPage=1&numOfRows=100&pageSize=100&MobileApp=AppTest&MobileOS=ETC&arrange=A&contentTypeId=" + str(RememberContentCode) + "&areaCode=" + RememberAreaCode + "&sigunguCode=" + str(RememberSubAreaCode) + "&listYN=Y")
    req = conn.getresponse()
    if req.status == 200:
        BooksDoc = req.read().decode('utf-8')
        if BooksDoc == None:
            print("에러")
        else:
            parseData = parseString(BooksDoc)
            GeoInfoLibrary = parseData.childNodes
            AreaData = GeoInfoLibrary[0].childNodes[1].childNodes[0].childNodes
            cnt = 0
            for item in AreaData:
                cnt += 1
                nTitle = 0
                nTel = 0
                nAddr2 = 0
                nImage = 0
                lengthofChildNodes = len(item.childNodes)
                while nTitle < lengthofChildNodes:
                    if item.childNodes[nTitle].nodeName == 'title':
                        break
                    nTitle += 1
                while nTel < lengthofChildNodes:
                    if item.childNodes[nTel].nodeName == 'tel':
                        break
                    nTel += 1
                while nAddr2 < lengthofChildNodes:
                    if item.childNodes[nAddr2].nodeName == 'addr2':
                        break
                    nAddr2 += 1
                while nImage < lengthofChildNodes:
                    if item.childNodes[nImage].nodeName == 'firstimage':
                        break
                    nImage += 1
                ##############################################
                row = "[" + str(cnt) +"]" + item.childNodes[0].childNodes[0].nodeValue
                if nTitle < lengthofChildNodes :
                    row += " " + item.childNodes[nTitle].childNodes[0].nodeValue
                else:
                    row += " " + '-'
                if nAddr2 < lengthofChildNodes :
                    row += " " + item.childNodes[nAddr2].childNodes[0].nodeValue
                else:
                    row += " " + '-'
                if nTel < lengthofChildNodes:
                    row += " " + item.childNodes[nTel].childNodes[0].nodeValue
                else:
                    row += " " + '-'
                if nImage < lengthofChildNodes:
                    row += " " + item.childNodes[nImage].childNodes[0].nodeValue
                else:
                    row += " " + '-'
                row = str(row)
                if row:
                    res_list.append(row)
    return res_list

def sendMessage(user, msg):
    try:
        bot.sendMessage(user, msg)
    except:
        traceback.print_exc(file=sys.stdout)

# def run(date_param, param='11710'):
#     conn = sqlite3.connect('logs.db')
#     cursor = conn.cursor()
#     cursor.execute('CREATE TABLE IF NOT EXISTS logs( user TEXT, log TEXT, PRIMARY KEY(user, log) )')
#     conn.commit()
#
#     user_cursor = sqlite3.connect('users.db').cursor()
#     user_cursor.execute('CREATE TABLE IF NOT EXISTS users( user TEXT, location TEXT, PRIMARY KEY(user, location) )')
#     user_cursor.execute('SELECT * from users')
#
#     for data in user_cursor.fetchall():
#         user, param = data[0], data[1]
#         print(user, date_param, param)
#         res_list = getData( param, date_param )
#         msg = ''
#         for r in res_list:
#             try:
#                 cursor.execute('INSERT INTO logs (user,log) VALUES ("%s", "%s")'%(user,r))
#             except sqlite3.IntegrityError:
#                 # 이미 해당 데이터가 있다는 것을 의미합니다.
#                 pass
#             else:
#                 print( str(datetime.now()).split('.')[0], r )
#                 if len(r+msg)+1>MAX_MSG_LENGTH:
#                     sendMessage( user, msg )
#                     msg = r+'\n'
#                 else:
#                     msg += r+'\n'
#         if msg:
#             sendMessage( user, msg )
#     conn.commit()

if __name__=='__main__':
    today = date.today()
    # current_month = today.strftime('%Y%m')

    print( '[',']received token :', TOKEN )

    pprint( bot.getMe() )

    # run(current_month)
