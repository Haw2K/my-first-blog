# -*- coding: utf-8 -*-
import sqlite3
from datetime import datetime, timedelta

tasks_db_name = 'tasks_db.db'


def check_create():
    try:
        tasks_db = sqlite3.connect(tasks_db_name, timeout=0, isolation_level=None)
        tasks_db_c = tasks_db.cursor()
        tasks_db_c.execute('''CREATE TABLE IF NOT EXISTS insta_tasks (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, task_id int(10) NOT NULL,
                           user_id int(10) NOT NULL, account_id int(10) NOT NULL, type_id int(2) NOT NULL,
                           date_start timestamp NOT NULL, date_end timestamp, subscribers_start int(10),
                           subscribers_end int(10))''')
        return tasks_db_c
    except:
        return 0

#return 0 if no need create new insta task or list end task values
def task_manager(task_values):
    tasks_db_c = check_create()
    #create_task(tasks_db_c, task_values)
    if tasks_db_c != 0:
        #datetime_end = task_values[4] + timedelta(days=1)
        #query_values = [task_values[0], datetime_start, task_values[4]]
        #find tasks need to end (work more 24 hours)
        tasks_db_c.execute('''SELECT id, task_id, date_start, subscribers_start from insta_tasks where task_id = ? and
        date(date_start, '+1 day') < ? and date_end is  null''', (task_values[0], task_values[4]))
        #datetime(date_start, '+1 day') < ?''', (task_values[0], datetime_end))
        #tasks_db_c.execute("SELECT * from insta_tasks where id =?", ('1'))
        #tasks_db_c.execute("SELECT id, date_start, (date_start + 86400)  from insta_tasks where id = %s", (task_values[0],))

        data = tasks_db_c.fetchall()
        if data.__len__() > 0:
            tasks_db_c.execute('''UPDATE insta_tasks SET date_end = ?, subscribers_end = ? WHERE ID = ?''', (task_values[4], task_values[5], data[0][0]))
            tasks_db_c.execute('''INSERT INTO insta_tasks(task_id, user_id, account_id, type_id, date_start, subscribers_start)
                VALUES (?,?,?,?,?,?)''', task_values)
            #task_id, date_start, date_end, subscribers_start, subscribers_end, new_task
            task_values_end = [task_values[0], data[0][2], task_values[4], data[0][3], task_values[5],0]
            return task_values_end
        else:
            #mb it new tasks need create
            tasks_db_c.execute('''SELECT id, task_id, date_start, subscribers_start from insta_tasks where task_id = ?''', (task_values[0],))
            data = tasks_db_c.fetchall()
            if data.__len__() == 0:
                tasks_db_c.execute('''INSERT INTO insta_tasks(task_id, user_id, account_id, type_id, date_start, subscribers_start)
                                VALUES (?,?,?,?,?,?)''', task_values)
                # task_id, date_start, date_end, subscribers_start, subscribers_end, new_task
                task_values_end = [task_values[0], data[0][2], task_values[4], data[0][3], task_values[5],1]
                return task_values_end
            else:
                return 0
        #
        # for rec in data:
        #     ff=1
        #     if ff==1:
        #         return 1
        #     else:
        #         return 0
        # query_result = tasks_db_c.execute('''SELECT modx_insta_likes.id, modx_insta_likes.account_id, modx_insta_likes.type_id, modx_insta_likes.tags,
        # modx_insta_accounts.user_id, modx_insta_accounts.login, modx_insta_accounts.password
        # FROM modx_insta_likes
        # LEFT JOIN modx_insta_accounts ON modx_insta_likes.account_id = modx_insta_accounts.id
        # where modx_insta_likes.active = "1"''')
    else:
        return 'connect to task DB error'

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


#task_values = [1,1,1,1,datetime.now(),1]
#task_manager(task_values)




