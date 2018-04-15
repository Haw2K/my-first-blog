#!/usr/bin/python
# -*- coding: utf-8

import MySQLdb
import string
import json
import datetime



# подключаемся к базе данных (не забываем указать кодировку, а то в базу запишутся иероглифы)
db = MySQLdb.connect(host="egorit.beget.tech", user="egorit_instalike", passwd="&HWIHj9Z", db="egorit_instalike", charset='utf8')
# формируем курсор, с помощью которого можно исполнять SQL-запросы
cursor = db.cursor()


#SHOW TABLES [FROM db_name]; -  список таблиц в базе
#SHOW COLUMNS FROM таблица [FROM db_name];

#cursor.execute('SHOW TABLES')
#tables =cursor.fetchall()

#for rec in tables:

    #fff=1

#cursor.execute('SHOW COLUMNS FROM insta_tasks_results')
#tables =cursor.fetchall()

#for rec in tables:
#    fff=1

#'modx_insta_likes'
#'modx_users'
#modx_insta_accounts
#insta_tasks_results
# запрос к БД
sql = """SELECT * FROM insta_tasks_results"""

# sql = '''SELECT modx_insta_likes.id, modx_insta_likes.account_id, modx_insta_likes.type_id, modx_insta_likes.tags,
#       modx_insta_accounts.user_id, modx_insta_accounts.login, modx_insta_accounts.password
#       FROM modx_insta_likes
#       LEFT JOIN modx_insta_accounts ON modx_insta_likes.account_id = modx_insta_accounts.id
#       where modx_insta_likes.active = "1"'''
#'errors_log'
#'taskId'


#SELECT ID, Name, Phone
#FROM Table1
#LEFT JOIN Table2 ON Table1.ID = Table2.ID
#WHERE Table1.ID = 12 AND Table2.IsDefault = 1
# выполняем запрос
cursor.execute(sql)
#
# # получаем результат выполнения запроса
data = cursor.fetchall()
# # перебираем записи
for rec in data:
    # извлекаем данные из записей - в том же порядке, как и в SQL-запросе
    #intags = json.loads(rec[25])['intags']
    fdf=1
    # выводим информацию

#json.dumps([1, 2, 3, {'4': 5, '6': 7}], separators=(',', ':'))

'sdfasf, sdfaetgt, sjhtiv'
#CREATE TABLE insta_logs (id VARCHAR(20), owner VARCHAR(20),
 #   -> species VARCHAR(20), sex CHAR(1), birth DATE, death DATE);
#createTableSql = '''CREATE TABLE insta_tasks_results (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
#user_id int(10) unsigned NOT NULL, account_id int(10) NOT NULL, type_id int(2),
#date_start DATETIME, date_end DATETIME, subscribers_start int(10), subscribers_end int(10))'''
#cursor.execute(createTableSql)
#<class 'tuple'>: ('user_id', 'int(10) unsigned', 'NO', '', None, '')

#addColumn = 'ALTER TABLE insta_tasks_results ADD taskId int(10) NOT NULL'
#cursor.execute(addColumn)
# закрываем соединение с БД
#
# cursor.execute('''INSERT INTO modx_insta_accounts(user_id, login, password) VALUES (%s,%s,%s)''',
#                             (1, 'haw2k', 'Mitra123',))
# #(1, 'haw22k', 'Mitra123',))
#
# #cursor.execute('''UPDATE modx_insta_likes SET active = 1 WHERE ID = 5''')
# #
# cursor.execute("""SELECT id FROM modx_insta_accounts WHERE user_id = %s and login = %s and password = %s""",(1, 'haw2k', 'Mitra123',))
# data = cursor.fetchall()
# for rec in data:
#     account_id=rec[0]
# #
# cursor.execute('''INSERT INTO modx_insta_likes(account_id, type_id, tags, active) VALUES (%s,%s,%s,1)''',
#                             (account_id, 1, 'code, sleep, repeat',))
# #
# db.commit()
db.close()