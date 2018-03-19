#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import time

from .src import InstaBot
from .src.check_status import check_status
from .src.feed_scanner import feed_scanner
from .src.follow_protocol import follow_protocol
from .src.unfollow_protocol import unfollow_protocol

from django.db import models
from django.utils import timezone



class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class InstabotDjangoModel(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    #title = models.CharField(max_length=200)
    #text = models.TextField()
    login = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    created_date = models.DateTimeField(
        default=timezone.now)
    published_date = models.DateTimeField(
       blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.login

    def RunBot(self, *args, **kwargs):
        bot = InstaBot(
            login="haw22k",
            password="mitra123",
            like_per_day=1000,
            comments_per_day=0,
            tag_list=['краснаяполяна', 'газпромлаура', 'сочи', 'совариум', 'sochi', 'krasnaypolyna', 'sovarium',
                      'фотографсочи'],
            tag_blacklist=['rain', 'thunderstorm'],
            user_blacklist={},
            max_like_for_one_tag=50,
            follow_per_day=300,
            follow_time=8 * 60,
            unfollow_per_day=300,
            unfollow_break_min=15,
            unfollow_break_max=30,
            log_mod=0,
            proxy='',
            # List of list of words, each of which will be used to generate comment
            # For example: "This shot feels wow!"
            comment_list=[["this", "the", "your"],
                          ["photo", "picture", "pic", "shot", "snapshot"],
                          ["is", "looks", "feels", "is really"],
                          ["great", "super", "good", "very good", "good", "wow",
                           "WOW", "cool", "GREAT", "magnificent", "magical",
                           "very cool", "stylish", "beautiful", "so beautiful",
                           "so stylish", "so professional", "lovely",
                           "so lovely", "very lovely", "glorious", "so glorious",
                           "very glorious", "adorable", "excellent", "amazing"],
                          [".", "..", "...", "!", "!!", "!!!"]],
            # Use unwanted_username_list to block usernames containing a string
            ## Will do partial matches; i.e. 'mozart' will block 'legend_mozart'
            ### 'free_followers' will be blocked because it contains 'free'
            unwanted_username_list=[
                'second', 'stuff', 'art', 'project', 'love', 'life', 'food', 'blog',
                'free', 'keren', 'photo', 'graphy', 'indo', 'travel', 'art', 'shop',
                'store', 'sex', 'toko', 'jual', 'online', 'murah', 'jam', 'kaos',
                'case', 'baju', 'fashion', 'corp', 'tas', 'butik', 'grosir', 'karpet',
                'sosis', 'salon', 'skin', 'care', 'cloth', 'tech', 'rental', 'kamera',
                'beauty', 'express', 'kredit', 'collection', 'impor', 'preloved',
                'follow', 'follower', 'gain', '.id', '_id', 'bags'
            ],
            unfollow_whitelist=['example_user_1', 'example_user_2'])

        while True:

            mode = 0

            if mode == 0:
                bot.new_auto_mod()
