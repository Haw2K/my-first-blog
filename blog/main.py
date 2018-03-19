from kivy.app import App
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
import os
import time
import random
from functools import partial

from src import InstaBot
from src.check_status import check_status
from src.feed_scanner import feed_scanner
from src.follow_protocol import follow_protocol
from src.unfollow_protocol import unfollow_protocol

from connected import Connected


def LikeOnShedule(bot, key, *largs):
    if len(bot.media_by_tag) == 0:
        bot.get_media_id_by_tag(random.choice(bot.tag_list))
        bot.this_tag_like_count = 0
        bot.max_tag_like_count = random.randint(
            1, bot.max_like_for_one_tag)
        bot.remove_already_liked()
    # ------------------- Like -------------------
    bot.new_auto_mod_like()

def my_callback(value, key, *largs):
    fdfd=1
    pass




class Login(Screen):
    def do_login(self, loginText, passwordText):
        app = App.get_running_app()

        app.username = loginText
        app.password = passwordText

        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'connected'

        app.config.read(app.get_application_config())
        app.config.write()

        app.initialBot()
        if app.bot.login_status:
            app.RunBot()
        else:
            Window.close()
            app.stop()


    def resetForm(self):
        self.ids['login'].text = ""
        self.ids['password'].text = ""

    def logoutBot(self):
        app = App.get_running_app()
        app.logoutBot()




class LoginApp(App):
    username = StringProperty(None)
    password = StringProperty(None)
    bot = ObjectProperty(None)
    event = ObjectProperty(None)

    #def on_stop(self):
        #self.bot.logout()

    def build(self):
        manager = ScreenManager()

        manager.add_widget(Login(name='login'))
        manager.add_widget(Connected(name='connected'))

        return manager

    def get_application_config(self):
        if(not self.username):
            return super(LoginApp, self).get_application_config()

        conf_directory = self.user_data_dir + '/' + self.username

        if(not os.path.exists(conf_directory)):
            os.makedirs(conf_directory)

        return super(LoginApp, self).get_application_config(
            '%s/config.cfg' % (conf_directory)
        )
    def initialBot(self):
        self.bot = InstaBot(
            login=self.username,
            password=self.password,
            like_per_day=1000,
            comments_per_day=0,
            tag_list=['краснаяполяна', 'газпромлаура', 'сочи', 'совариум', 'sochi', 'krasnaypolyna', 'sovarium',
                      'фотографсочи'],
            tag_blacklist=['rm'],
            user_blacklist={},
            max_like_for_one_tag=50,
            follow_per_day=0,
            follow_time=1 * 60,
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

    def logoutBot(self):
        #Clock.unschedule(LikeOnShedule(self.bot))
        self.event.cancel()
        self.bot.logout()
        self.stop()

    def RunBot(self):
        #self.event = Clock.schedule_interval(partial(LikeOnShedule,self.bot, 60)
        #Clock.schedule_interval(partial(my_callback, 'my value', 'my key'), 0.5)
        self.event = Clock.schedule_interval(partial(LikeOnShedule, self.bot, 'my key'), 60)





if __name__ == '__main__':
    LoginApp().run()
