# -*- coding: utf-8 -*-
from InstagramAPI import InstagramAPI

def initialize_api(login,password):
    api = InstagramAPI(login, password)
    api.login()
    return api

def get_total_followers(api, user_id):
    followers = []
    next_max_id = True
    while next_max_id:
        # first iteration hack
        if next_max_id is True:
            next_max_id = ''

        _ = api.getUserFollowers(user_id, maxid=next_max_id)
        followers.extend(api.LastJson.get('users', []))
        next_max_id = api.LastJson.get('next_max_id', '')
    return len(followers)
