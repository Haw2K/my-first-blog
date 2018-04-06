#!/usr/bin/python
# -*- coding: utf-8

import MySQLdb
import string
import json



# подключаемся к базе данных (не забываем указать кодировку, а то в базу запишутся иероглифы)
db = MySQLdb.connect(host="egorit.beget.tech", user="egorit_instalike", passwd="&HWIHj9Z", db="egorit_instalike", charset='utf8')
# формируем курсор, с помощью которого можно исполнять SQL-запросы
cursor = db.cursor()


# запрос к БД
sql = """SELECT * FROM `modx_user_attributes`"""
# выполняем запрос
cursor.execute(sql)

# получаем результат выполнения запроса
data = cursor.fetchall()
# перебираем записи
for rec in data:
    # извлекаем данные из записей - в том же порядке, как и в SQL-запросе
    intags = json.loads(rec[25])['intags']
    # выводим информацию

#json.dumps([1, 2, 3, {'4': 5, '6': 7}], separators=(',', ':'))
# закрываем соединение с БД
db.close()