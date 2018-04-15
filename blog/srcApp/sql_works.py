# -*- coding: utf-8 -*-
import sqlite3
import MySQLdb
from datetime import datetime, timedelta


tasks_db_name = 'tasks_db.db'
tasks_table_name = 'modx_insta_likes'

def check_create():
    try:
        tasks_db = sqlite3.connect(tasks_db_name, detect_types=sqlite3.PARSE_DECLTYPES, timeout=0, isolation_level=None)
        #db = pyodbc.connect(driver='{SQL Server Native Client 10.0}',
         #                   server='TESTSRVR', database='TESTDB',
          #                  trusted_connection='yes')
        #print
        #pformat(db.cursor().execute("select * from dbo.datetest").description)
        tasks_db_c = tasks_db.cursor()
        tasks_db_c.execute('''CREATE TABLE IF NOT EXISTS insta_tasks (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, task_id int(10) NOT NULL,
                           user_id int(10) NOT NULL, account_id int(10) NOT NULL, type_id int(2) NOT NULL,
                           date_start timestamp NOT NULL, date_end timestamp, subscribers_start int(10),
                           subscribers_end int(10))''')
        return tasks_db_c, tasks_db
    except:
        return 0

def check_working_task(tasks_db_c,task_values):

    if task_values[6] != '':
        task_values_end = [task_values[0], task_values[4], None, task_values[5], None, 3, task_values[7],
                           task_values[8], task_values[9], task_values[1], task_values[2], task_values[3],
                           task_values[6]]
        return task_values_end

    tasks_db_c.execute('''SELECT id, task_id, date_start, subscribers_start from insta_tasks where task_id = ? and
    date(date_start) < ? and date_end is  null''', (task_values[0], task_values[4]))
            #date(date_start, '+1 day') < ? and date_end is  null''', (task_values[0], task_values[4]))

    data = tasks_db_c.fetchall()
    if data.__len__() > 0:
        #close task if it work 24 hours
        tasks_db_c.execute('''UPDATE insta_tasks SET date_end = ?, subscribers_end = ? WHERE ID = ?''',
                           (task_values[4], task_values[5], data[0][0]))
        #open new task
        tasks_db_c.execute('''INSERT INTO insta_tasks(task_id, user_id, account_id, type_id, date_start, subscribers_start)
                         VALUES (?,?,?,?,?,?)''', (task_values[0], task_values[1], task_values[2], task_values[3], task_values[4], task_values[5]))

        # task_id, date_start, date_end, subscribers_start, subscribers_end, new_task
        task_values_end = [task_values[0], data[0][2], task_values[4], data[0][3], task_values[5], 0, task_values[7],
                           task_values[8], task_values[9], task_values[1], task_values[2], task_values[3], task_values[6]]
        return task_values_end
    else:
        #mb it new task
        tasks_db_c.execute('''SELECT id, task_id, date_start, subscribers_start from insta_tasks where task_id = ?''',
                           (task_values[0],))
        data = tasks_db_c.fetchall()
        if data.__len__() == 0:
            tasks_db_c.execute('''INSERT INTO insta_tasks(task_id, user_id, account_id, type_id, date_start, subscribers_start)
                            VALUES (?,?,?,?,?,?)''', (task_values[0], task_values[1], task_values[2], task_values[3], task_values[4], task_values[5]))
            # task_id, date_start, date_end, subscribers_start, subscribers_end, new_task, login, password, tags, user_id, account_id, type_id, error_text
            task_values_end = [task_values[0], task_values[4], None, task_values[5], None, 1, task_values[7],
                               task_values[8], task_values[9], task_values[1], task_values[2], task_values[3], task_values[6]]
            return task_values_end
        else:
            task_values_end = [task_values[0], task_values[4], None, task_values[5], None, 2, task_values[7],
                               task_values[8], task_values[9], task_values[1], task_values[2], task_values[3],
                               task_values[6]]
            return task_values_end

def task_manager(insta_tasks):

    tasks_db_c, tasks_db = check_create()
    if tasks_db_c != 0:

        tasks_to_start = []
        for task_values in insta_tasks:

            backend_task = check_working_task(tasks_db_c,task_values)
            if backend_task != 0:
                backend_task.append(task_values[10])
                if backend_task[12] == '':
                    backend_task[12] = 0
                tasks_to_start.append(backend_task)

        tasks_db.close()
        return tasks_to_start
    else:
        return 'connection backend tasks DB error'

def delete_task(task_id):
    tasks_db_c = check_create()
    if tasks_db_c != 0:
        tasks_db_c = check_create()
        tasks_db_c.execute('''DELETE FROM insta_tasks WHERE ID = '''+task_id)
        return 1
    else:
        return 0

def create_task(tasks_db_c,task_values):

    tasks_db_c.execute('''INSERT INTO insta_tasks(task_id, user_id, account_id, type_id, date_start, subscribers_start)
    VALUES (?,?,?,?,?,?)''', task_values )

#mysql databases
def get_tasks_front():
    db = MySQLdb.connect(host="egorit.beget.tech", user="egorit_instalike", passwd="&HWIHj9Z", db="egorit_instalike",
                         charset='utf8')
    cursor = db.cursor()

    # '''SELECT '' as accounts_id, modx_insta_likes.id as likes_id
    # FROM modx_insta_likes
    #
    # union all
    #
    # SELECT modx_insta_accounts.id, ''
    #  FROM modx_insta_accounts'''

    sql = '''SELECT modx_insta_likes.id, modx_insta_likes.account_id, modx_insta_likes.type_id, modx_insta_likes.tags,
              modx_insta_accounts.user_id, modx_insta_accounts.login, modx_insta_accounts.password
              FROM modx_insta_likes
              LEFT JOIN modx_insta_accounts ON modx_insta_likes.account_id = modx_insta_accounts.id      
              where modx_insta_likes.active = "1"
              and modx_insta_likes.id IS NOT NULL and modx_insta_likes.account_id IS NOT NULL
              and modx_insta_likes.type_id IS NOT NULL and modx_insta_accounts.user_id IS NOT NULL
              and modx_insta_accounts.login IS NOT NULL and modx_insta_accounts.password IS NOT NULL'''
    #check not null because front testing

    cursor.execute(sql)
    # task_id, account_id, type_id, tags, user_id, login, password
    results = cursor.fetchall()

    db.close()
    return results

def return_statictic_to_front(insta_backend_tasks, DDarray = 1):
    db = MySQLdb.connect(host="egorit.beget.tech", user="egorit_instalike", passwd="&HWIHj9Z", db="egorit_instalike",
                         charset='utf8')
    cursor = db.cursor()

    if DDarray == 1:
        for row in insta_backend_tasks:
            #errors and end tasks
            if row[5] == 3 or row[5] == 0:
                #task_id, date_start, date_end, subscribers_start, subscribers_end, new_task, login, password, tags, user_id, account_id, type_id, error_text
                cursor.execute('''INSERT INTO insta_tasks_results(user_id, account_id, type_id, date_start,
                                    date_end, subscribers_start, subscribers_end, taskId, errors_log) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)''',
                                                (row[9], row[10], row[11], row[1], row[2], row[3], row[4], row[0], row[12],))
                                               #insta_tasks_results columns: id, user_id, account_id, type_id, date_start, date_end, subscribers_start,
                                               #subscribers_end, errors_log, taskId


    else:
        # errors and end tasks
        row = insta_backend_tasks
        if row[5] == 3 or row[5] == 0:
            # task_id, date_start, date_end, subscribers_start, subscribers_end, new_task, login, password, tags, user_id, account_id, type_id, error_text
            cursor.execute('''INSERT INTO insta_tasks_results(user_id, account_id, type_id, date_start,
                                            date_end, subscribers_start, subscribers_end, taskId, errors_log) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)''',
                           (row[9], row[10], row[11], row[1], row[2], row[3], row[4], row[0], row[12],))
            # insta_tasks_results columns: id, user_id, account_id, type_id, date_start, date_end, subscribers_start,
            # subscribers_end, errors_log, taskId




    db.commit()
    db.close()





