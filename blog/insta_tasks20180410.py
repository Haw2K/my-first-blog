#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import time
import MySQLdb
from src import InstaBot
from src.check_status import check_status
from src.feed_scanner import feed_scanner
from src.follow_protocol import follow_protocol
from src.unfollow_protocol import unfollow_protocol
from src.userinfo import UserInfo

from srcApp import sql_works
from srcApp import instagram_api
from datetime import datetime


#initialize variables
#api = instagram_api.initialize_api('haw22k','Mitra123')


if __name__ == "__main__":

    db = MySQLdb.connect(host="egorit.beget.tech", user="egorit_instalike", passwd="&HWIHj9Z", db="egorit_instalike", charset='utf8')
    cursor = db.cursor()

    sql = '''SELECT modx_insta_likes.id, modx_insta_likes.account_id, modx_insta_likes.type_id, modx_insta_likes.tags,
          modx_insta_accounts.user_id, modx_insta_accounts.login, modx_insta_accounts.password
          FROM modx_insta_likes
          LEFT JOIN modx_insta_accounts ON modx_insta_likes.account_id = modx_insta_accounts.id      
          where modx_insta_likes.active = "1"'''

    cursor.execute(sql)
    data = cursor.fetchall()

    for rec in data:
        # it is more readable
        dist_task_values = {'task_id': rec[0], 'account_id': rec[1], 'type_id': rec[2], 'tags': rec[3],
                            'user_id': rec[4], \
                            'login': rec[5], 'password': rec[6]}

        if dist_task_values['user_id'] == None:
            continue

        try:
            ui = UserInfo()
            user_id = ui.get_user_id_by_login(rec[5])

            subscribers_now = 0
            #subscribers_now = instagram_api.get_total_followers(api,user_id)
            #task_id, user_id, account_id, type_id, date_start, subscribers_now
            task_values = [rec[0], rec[4], rec[1], rec[2], datetime.now(), subscribers_now]
            #task_id, date_start, date_end, subscribers_start, subscribers_end
            task_values_end = sql_works.task_manager(task_values)

            if task_values_end != 0:
                dist_task_values.update({'date_start': task_values_end[1], 'date_end': task_values_end[2],
                                         'subscribers_start': task_values_end[3],
                                         'subscribers_end': task_values_end[4]})
                #update front table
                if task_values_end[5] == 0:
                    cursor.execute('''INSERT INTO insta_tasks_results(user_id, account_id, type_id, date_start,
                    date_end, subscribers_start, subscribers_end, taskId) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)''',
                    (dist_task_values['user_id'],dist_task_values['account_id'],dist_task_values['type_id'],
                    dist_task_values['date_start'],dist_task_values['date_end'],dist_task_values['subscribers_start'],
                    dist_task_values['subscribers_end'],dist_task_values['task_id'],))
                    #insta_tasks_results columns: id, user_id, account_id, type_id, date_start, date_end, subscribers_start,
                    #subscribers_end, errors_log, taskId

                bot = InstaBot(
                login=rec[5],
                password=rec[6],
                like_per_day=1000,
                comments_per_day=0,
                tag_list=rec[3].split(', '),
                tag_blacklist=[],
                user_blacklist={},
                max_like_for_one_tag=50,
                follow_per_day=300,
                follow_time=24 * 60+1,
                unfollow_per_day=300,
                unfollow_break_min=15,
                unfollow_break_max=30,
                log_mod=1,
                proxy='',
                # List of list of words, each of which will be used to generate comment
                # For example: "This shot feels wow!"
                comment_list=[["this", "the", "your"],
                              ["photo", "picture", "pic", "shot", "snapshot"],
                              ["is", "looks", "feels", "is really"],
                              ["great", "super", "good", "very good", "good", "wow",
                               "WOW", "cool", "GREAT","magnificent", "magical",
                               "very cool", "stylish", "beautiful", "so beautiful",
                               "so stylish", "so professional", "lovely",
                               "so lovely", "very lovely", "glorious","so glorious",
                               "very glorious", "adorable", "excellent", "amazing"],
                              [".", "..", "...", "!", "!!", "!!!"]],
                # Use unwanted_username_list to block usernames containing a string
                ## Will do partial matches; i.e. 'mozart' will block 'legend_mozart'
                ### 'free_followers' will be blocked because it contains 'free'
                unwanted_username_list=[],
                unfollow_whitelist=[])
                while True:
                    bot.new_auto_mod()
        except:
            cursor.execute('''INSERT INTO insta_tasks_results(user_id, account_id, type_id, date_start,
                                errors_log, taskId) VALUES (%s,%s,%s,%s,%s,%s)''',
                           (dist_task_values['user_id'], dist_task_values['account_id'], dist_task_values['type_id'],
                            datetime.now(), 'some1 error', dist_task_values['task_id'],))
            #return 'error'

    db.commit()
    db.close()
