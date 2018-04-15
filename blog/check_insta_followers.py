#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Use text editor to edit the script and type in valid Instagram username/password

from InstagramAPI import InstagramAPI

InstagramAPI = InstagramAPI("accName", "accPass!")
InstagramAPI.login() # login

InstagramAPI.getSelfUserFollowers()
followers = InstagramAPI.LastJson
print (len(followers['users']))