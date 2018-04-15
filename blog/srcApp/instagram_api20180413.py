# -*- coding: utf-8 -*-
from InstagramAPI import InstagramAPI

login = 'haw22k'
password = 'Mitra123'

def initialize_api(login,password):
    api = InstagramAPI(login, password)
    api.login()
    return api

def get_total_followers(user_ids):
    api = initialize_api(login,password)

    followers_quantities = []

    for user_id in user_ids:
            followers = []
            next_max_id = True
            while next_max_id:
                # first iteration hack
                if next_max_id is True:
                    next_max_id = ''

                    #api.s.get('https://www.instagram.com/haw22k/?__a1')
                    #api.s.get('https://api.instagram.com/v1/users/search?q=haw2k&access_token=WbnklO47eHmCV2C6rVbzWViVReA6ghx0')

                _ = api.getUserFollowers(user_id, maxid=next_max_id)
                followers.extend(api.LastJson.get('users', []))
                next_max_id = api.LastJson.get('next_max_id', '')
                followers_quantities.append(len(followers))

    return followers_quantities

def get_total_followers(user_ids):
    api = initialize_api(login,password)

    followers_quantities = []

    for user_id in user_ids:
            followers = []
            next_max_id = True
            while next_max_id:
                # first iteration hack
                if next_max_id is True:
                    next_max_id = ''

                    #api.s.get('https://www.instagram.com/haw22k/?__a1')
                    #api.s.get('https://api.instagram.com/v1/users/search?q=haw2k&access_token=WbnklO47eHmCV2C6rVbzWViVReA6ghx0')

                _ = api.getUserFollowers(user_id, maxid=next_max_id)
                followers.extend(api.LastJson.get('users', []))
                next_max_id = api.LastJson.get('next_max_id', '')
                followers_quantities.append(len(followers))

    return followers_quantities

if __name__ == "__main__":
    get_total_followers(['haw22k','haw2k'])

