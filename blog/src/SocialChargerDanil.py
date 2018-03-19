#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import time
import atexit
import itertools
import logging
import signal
import sys
import sqlite3
import time
import requests
from fake_useragent import UserAgent
from datetime import datetime
import json
import random
import time


def check_and_update(self):
    """ At the Program start, i does look for the sql updates """
    self.follows_db_c.execute("CREATE TABLE IF NOT EXISTS usernames (username varchar(300))")
    self.follows_db_c.execute("CREATE TABLE IF NOT EXISTS medias (media_id varchar(300))")
    table_info = self.follows_db_c.execute("pragma table_info(medias)")
    table_column_status = [o for o in table_info if o[1] == "status"]
    if not table_column_status:
        self.follows_db_c.execute("ALTER TABLE medias ADD COLUMN status integer")
    table_info = self.follows_db_c.execute("pragma table_info(medias)")
    table_column_status = [o for o in table_info if o[1] == "datetime"]
    if not table_column_status:
        self.follows_db_c.execute("ALTER TABLE medias ADD COLUMN datetime TEXT")
    table_info = self.follows_db_c.execute("pragma table_info(medias)")
    table_column_status = [o for o in table_info if o[1] == "code"]
    if not table_column_status:
        self.follows_db_c.execute("ALTER TABLE medias ADD COLUMN code TEXT")
    table_info = self.follows_db_c.execute("pragma table_info(usernames)")
    table_column_status = [o for o in table_info if o[1] == "username_id"]
    if not table_column_status:
        qry = """
            CREATE TABLE "usernames_new" ( `username_id` varchar ( 300 ), `username` TEXT  );
            INSERT INTO "usernames_new" (username_id) Select username from usernames;
            DROP TABLE "usernames";
            ALTER TABLE "usernames_new" RENAME TO "usernames";
              """
        self.follows_db_c.executescript(qry)
    table_info = self.follows_db_c.execute("pragma table_info(usernames)")
    table_column_status = [o for o in table_info if o[1] == "unfollow_count"]
    if not table_column_status:
        self.follows_db_c.execute("ALTER TABLE usernames ADD COLUMN unfollow_count INTEGER DEFAULT 0")
    table_info = self.follows_db_c.execute("pragma table_info(usernames)")
    table_column_status = [o for o in table_info if o[1] == "last_followed_time"]
    if not table_column_status:
        self.follows_db_c.execute("ALTER TABLE usernames ADD COLUMN last_followed_time TEXT")
    table_info = self.follows_db_c.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='settings';").fetchone()
    if not table_info:
        qry = """
            CREATE TABLE "settings" ( `settings_name` TEXT, `settings_val` TEXT  );
              """
        self.follows_db_c.execute(qry)
        # table_column_status = [o for o in table_info if o[1] == "last_followed_time"]
        # if not table_column_status:
        #    self.follows_db_c.execute("ALTER TABLE usernames ADD COLUMN last_followed_time TEXT")


def check_already_liked(self, media_id):
    """ controls if media already liked before """
    if self.follows_db_c.execute("SELECT EXISTS(SELECT 1 FROM medias WHERE media_id='" +
                                         media_id + "' LIMIT 1)").fetchone()[0] > 0:
        return 1
    return 0

def insert_media(self, media_id, status):
    """ insert media to medias """
    now = datetime.now()
    self.follows_db_c.execute("INSERT INTO medias (media_id, status, datetime) VALUES('" +
                              media_id + "','" + status + "','" + str(now) + "')")

def get_user_id_by_login(self, user_name):
        url_info = "https://www.instagram.com/%s/?__a=1" % (user_name)
        info = self.s.get(url_info)
        all_data = json.loads(info.text)
        id_user = all_data['user']['id']
        return id_user


class InstagramBot:
    accept_language = 'en-US,en;q=0.5'
    like_counter = 0
    media_max_like = 50
    media_min_like = 0
    max_like_for_one_tag = 5

    # If instagram ban you - query return 400 error.
    error_400 = 0
    # If you have 3 400 error in row - looks like you banned.
    error_400_to_ban = 3
    # If InstaBot think you are banned - going to sleep.
    ban_sleep_time = 2 * 60 * 60

    def __init__(self,
                 login,
                 password):
        self.follows_db = sqlite3.connect('follows_db.db', timeout=0, isolation_level=None)
        self.follows_db_c = self.follows_db.cursor()

        ua = UserAgent()
        check_and_update(self)
        self.user_agent = ua.random
        self.time_in_day = 24 * 60 * 60
        self.like_per_day = 1000
        self.like_delay = self.time_in_day / self.like_per_day
        self.timeLastLike = 0
        self.media_by_tag = []

        self.tag_list = ['краснаяполяна', 'газпромлаура', 'сочи', 'совариум', 'sochi', 'krasnaypolyna', 'sovarium', 'фотографсочи']
        self.s = requests.Session()
        #self.user_login = "shotaowl"
        #self.user_password = "Danil5891"
        self.user_login = login.lower()
        self.user_password = password
        self.login()
       # self.logout()

    def login(self):
        self.login_post = {
            'username': self.user_login,
            'password': self.user_password
        }

        self.s.headers.update({
            'Accept': '*/*',
            'Accept-Language': self.accept_language,
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Content-Length': '0',
            'Host': 'www.instagram.com',
            'Origin': 'https://www.instagram.com',
            'Referer': 'https://www.instagram.com/',
            'User-Agent': self.user_agent,
            'X-Instagram-AJAX': '1',
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Requested-With': 'XMLHttpRequest'
        })

        r = self.s.get('https://www.instagram.com/')
        self.s.headers.update({'X-CSRFToken': r.cookies['csrftoken']})
        time.sleep(5 * random.random())
        login = self.s.post(
            'https://www.instagram.com/accounts/login/ajax/', data=self.login_post, allow_redirects=True)
        self.s.headers.update({'X-CSRFToken': login.cookies['csrftoken']})
        self.csrftoken = login.cookies['csrftoken']
        #ig_vw=1536; ig_pr=1.25; ig_vh=772;  ig_or=landscape-primary;
        self.s.cookies['ig_vw'] = '1536'
        self.s.cookies['ig_pr'] = '1.25'
        self.s.cookies['ig_vh'] = '772'
        self.s.cookies['ig_or'] = 'landscape-primary'
        time.sleep(5 * random.random())

        if login.status_code == 200:
            r = self.s.get('https://www.instagram.com/')
            finder = r.text.find(self.user_login)
            if finder != -1:

                self.user_id = get_user_id_by_login(self, self.user_login)
                self.login_status = True
                print('login')
            else:
                self.login_status = False
        else:
            self.login_status = False

    def logout(self):
        try:
            logout_post = {'csrfmiddlewaretoken': self.csrftoken}
            logout = self.s.post('https://www.instagram.com/accounts/logout/', data=logout_post)
            print('logout')
            ff=3
        except:
            ff=2

    def get_media_id_by_tag(self, tag):

        if self.login_status:
            if self.login_status == 1:
                url_tag = 'https://www.instagram.com/explore/tags/%s/?__a=1' % (tag)
                try:
                    r = self.s.get(url_tag)
                    all_data = json.loads(r.text)
                    self.media_by_tag = list(all_data['graphql']['hashtag']['edge_hashtag_to_media']['edges'])
                except:
                    self.logout()
                    self.media_by_tag = []
            else:
                self.logout()
                return 0

    def remove_already_liked(self):
        x = 0
        while x < len(self.media_by_tag):
            if check_already_liked(self, media_id=self.media_by_tag[x]['node']['id']) == 1:
                self.media_by_tag.remove(self.media_by_tag[x])
            else:
                x += 1

    def new_auto_mod_like(self):
        if time.time() > self.timeLastLike and self.like_per_day != 0 \
                and len(self.media_by_tag) > 0:
            # You have media_id to like:
            if self.like_all_exist_media(media_size=1, delay=False):
                # If like go to sleep:
                self.timeLastLike = time.time() + self.like_delay * 0.9 + self.like_delay * 0.2 * random.random()
                # Count this tag likes:
                self.this_tag_like_count += 1
                if self.this_tag_like_count >= self.max_tag_like_count:
                    self.media_by_tag = [0]
            # Del first media_id
            del self.media_by_tag[0]

    def like(self, media_id):
        """ Send http request to like media by ID """
        if self.login_status:
            url_likes = 'https://www.instagram.com/web/likes/%s/like/' % (media_id)
            try:
                like = self.s.post(url_likes)
                last_liked_media_id = media_id
                print('like media %s' % (self.like_counter))
            except:
                like = 0
            return like

    def like_all_exist_media(self, media_size=-1, delay=True):
        """ Like all media ID that have self.media_by_tag """

        if self.login_status:
            if self.media_by_tag != 0:
                i = 0
                for d in self.media_by_tag:
                    # Media count by this tag.
                    if media_size > 0 or media_size < 0:
                        media_size -= 1
                        l_c = self.media_by_tag[i]['node']['edge_liked_by']['count']
                        if ((l_c <= self.media_max_like and
                             l_c >= self.media_min_like) or
                            (self.media_max_like == 0 and
                             l_c >= self.media_min_like) or
                            (self.media_min_like == 0 and
                             l_c <= self.media_max_like) or
                            (self.media_min_like == 0 and
                             self.media_max_like == 0)):
                            if self.media_by_tag[i]['node']['owner'][
                                    'id'] == self.user_id:
                                return False
                            if check_already_liked(self, media_id=self.media_by_tag[i]['node']['id']) == 1:
                                return False
                            try:
                                if (len(self.media_by_tag[i]['node']['edge_media_to_caption']['edges']) > 1):
                                    caption = self.media_by_tag[i]['node']['edge_media_to_caption'][
                                        'edges'][0]['node']['text'].encode(
                                            'ascii', errors='ignore')
                                    if sys.version_info[0] == 3:
                                        tags = {
                                            str.lower(
                                                (tag.decode('ASCII')).strip('#'))
                                            for tag in caption.split()
                                            if (tag.decode('ASCII')
                                                ).startswith("#")
                                        }
                                    else:
                                        tags = {
                                            unicode.lower(
                                                (tag.decode('ASCII')).strip('#'))
                                            for tag in caption.split()
                                            if (tag.decode('ASCII')
                                                ).startswith("#")
                                        }
                            except:
                                return False


                            like = self.like(self.media_by_tag[i]['node']['id'])

                            if like != 0:
                                if like.status_code == 200:
                                    # Like, all ok!
                                    self.error_400 = 0
                                    self.like_counter += 1
                                    insert_media(self,
                                                 media_id=self.media_by_tag[i]['node']['id'],
                                                 status="200")
                                elif like.status_code == 400:

                                    insert_media(self,
                                                 media_id=self.media_by_tag[i]['node']['id'],
                                                 status="400")
                                    # Some error. If repeated - can be ban!
                                    if self.error_400 >= self.error_400_to_ban:
                                        # Look like you banned!
                                        time.sleep(self.ban_sleep_time)
                                    else:
                                        self.error_400 += 1
                                else:
                                    insert_media(self,
                                                 media_id=self.media_by_tag[i]['node']['id'],
                                                 status=str(like.status_code))
                                    return False
                                    # Some error.
                                i += 1
                                if delay:
                                    time.sleep(self.like_delay * 0.9 +
                                               self.like_delay * 0.2 *
                                               random.random())
                                else:
                                    return True
                            else:
                                return False
                        else:
                            return False
                    else:
                        return False
            else:
                fdfd=1


InstagramBot = InstagramBot(
    login="haw22k",
    password="Mitra123")

while True:



    if len(InstagramBot.media_by_tag) == 0:
        InstagramBot.this_tag_like_count = 0
        InstagramBot.max_tag_like_count = random.randint(
            1, InstagramBot.max_like_for_one_tag)
        InstagramBot.get_media_id_by_tag(random.choice(InstagramBot.tag_list))
        InstagramBot.remove_already_liked()
    # ------------------- Like -------------------
    InstagramBot.new_auto_mod_like()


ff=1
bot.logout()
