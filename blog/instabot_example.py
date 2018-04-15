#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import time
from src import InstaBot
from src.check_status import check_status
from src.feed_scanner import feed_scanner
from src.follow_protocol import follow_protocol
from src.unfollow_protocol import unfollow_protocol
from src.userinfo import UserInfo

from srcApp import sql_works
import sys
from datetime import datetime


def insta_bot_start(task):

    #task: task_id, date_start, date_end, subscribers_start, subscribers_end, new_task, login, password, tags, user_id, account_id, type_id, user_id
    try:
        bot = InstaBot(
                    login=task[6],
                    password=task[7],
                    user_id_take=task[13],
                    like_per_day=1000,
                    comments_per_day=0,
                    tag_list=task[8].split(':'),
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
        error_task = task[:]
        error_task[5] = 3
        error_task[12] = 'cant run intagrambot example'
        if error_task[1] != 'None':
            error_task[1] = datetime.fromtimestamp(int(arg_task[1].timestamp()))
        if error_task[2] != 'None':
            error_task[2] = datetime.fromtimestamp(int(arg_task[2].timestamp()))
        sql_works.return_statictic_to_front(error_task, 0)



if __name__ == "__main__":

    #print('Number of arguments:', len(sys.argv), 'arguments.')
    #print('Argument List:', str(sys.argv))
    #task = '6 1523706403.852221 1523706735.63401 4 5 0 haw22k Mitra123 code:sleep:repeat 2 4 1 0 7134637717'.split(' ')

    task = sys.argv[1:]
    insta_bot_start(task)
