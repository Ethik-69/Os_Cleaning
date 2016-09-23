#! /usr/bin/python
# -*- coding:utf-8 -*-
import os
import sys

try:
    import shutil
except Exception as e:
    print(e)
    print('[--] Import Error: shutil require !')

try:
    import pexpect
except Exception as e:
    print(e)
    print('[--] Import Error: pexpect require !')


class DebianClean:
    def __init__(self, user_name):
        self.child = pexpect.spawn('apt-get autoclean', timeout=5)
        self.user_name = user_name
        self.browser_list = ['mozilla', 'chromium', 'chrome']

    def clean_apt(self):
        print('[*] Clean Aptitude')
        finish = False
        awaiting_cmd = 1

        while not finish:

            ret = self.child.expect([pexpect.EOF, '.*[Oo/Nn]', '.*[Yy/Nn]', '$'])

            if ret == 0:
                print('[--] Error While Cleaning Aptitude')

            if ret == 1:
                self.child.sendline('O')

            if ret == 2:
                self.child.sendline('Y')

            if ret == 3:
                if awaiting_cmd == 1:
                    self.child.sendline('apt-get clean')
                    awaiting_cmd += 1
                elif awaiting_cmd == 2:
                    self.child.sendline('apt-get autoremove')
                    awaiting_cmd += 1
                elif awaiting_cmd == 3:
                    finish = True

    def clean_orphan(self):
        print('[*] Clean Oprhans')
        self.child.sendline('deborphan | xargs apt-get -y remove --purge')
        ret = self.child.expect([pexpect.EOF, '.*[Oo/Nn]', '.*[Yy/Nn]', '$'])

        if ret == 0:
            print('[--] Error While Cleaning Aptitude')

        if ret == 1:
            self.child.sendline('O')

        if ret == 2:
            self.child.sendline('Y')

    def clean_os_cache(self):
        print('[*] Clean Os Cache')
        self.child.sendline('sync | tee /proc/sys/vm/drop_caches')
        ret = self.child.expect([pexpect.EOF, '$'])

        if ret == 0:
            print('[--] Error When Cleaning Cache')
            sys.exit(0)

    def clean_thumbnails(self):
        print('[*] Clean Thumbnails')
        path_to_thumbnails = '/home/' + self.user_name + '/.thumbnails/'
        for folder in os.listdir(path_to_thumbnails):
            try:
                shutil.rmtree(path_to_thumbnails + folder + '/')
            except:
                os.remove(path_to_thumbnails + folder)

        path_to_thumbnails = '/home/' + self.user_name + '/.cache/thumbnails/'
        for folder in os.listdir(path_to_thumbnails):
            try:
                shutil.rmtree(path_to_thumbnails + folder + '/')
            except:
                os.remove(path_to_thumbnails + folder)

    def clean_trash(self):
        print('[*] Clean Trash')
        path_to_trash = '/home/' + self.user_name + '/.local/share/Trash/'
        for folder in os.listdir(path_to_trash):
            shutil.rmtree(path_to_trash + folder + '/')

    def clean_browser_cache(self):
        ask = True
        clean = False

        while ask:

            print('[?] May I Clean Your Browser ? [y/N]')
            user_choice = input()
            if user_choice == '' or user_choice in 'Nn':
                clean = False
                ask = False
            elif user_choice in 'Yy':
                clean = True
                ask = False
            else:
                print('[-|°\|°\[]|°\ Can\'t Understand What You Said !')

        if clean:

            for browser in self.browser_list:
                try:
                    path_to_moz = '/home' + self.user_name + '/.cache/' + browser + '/'
                    for folder in os.listdir(path_to_moz):
                        shutil.rmtree(path_to_moz + folder + '/')
                    print('[*] Clean %s' % browser)
                except:
                    pass

    def main(self):
        self.clean_apt()
        self.clean_orphan()
        self.clean_os_cache()
        self.clean_thumbnails()
        self.clean_trash()
        self.clean_browser_cache()
        self.child.kill(1)
