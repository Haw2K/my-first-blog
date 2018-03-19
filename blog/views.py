#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post
from .forms import PostForm
from django.shortcuts import redirect
from .models import InstabotDjangoModel
from .forms import PostInstabotDjangoModel

import os
import time

from .src import InstaBot

def post_list(request):
    #posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    posts = InstabotDjangoModel.objects.all().order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(InstabotDjangoModel, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
    # if request.method == "POST":
    #     form = PostInstabotDjangoModel(request.POST)
    #     if form.is_valid():
    #         post = form.save(commit=False)
    #         post.author = request.user
    #         post.published_date = timezone.now()
    #         post.save()
    #         return redirect('post_detail', pk=post.pk)
    # else:
    #     form = PostInstabotDjangoModel()
    # form = PostInstabotDjangoModel()
    # return render(request, 'blog/post_edit.html', {'form': form})
    bot = InstaBot(
        login="shotaowl",
        password="Danil5891",
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
        bot.new_auto_mod()

def post_edit(request, pk):
    post = get_object_or_404(InstabotDjangoModel, pk=pk)
    if request.method == "POST":
        form = PostInstabotDjangoModel(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostInstabotDjangoModel(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})
