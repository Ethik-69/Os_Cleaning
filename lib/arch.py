#! /usr/bin/python
# -*- coding:utf-8 -*-
"""
Un petit script pour nettoyer votre ArchLinux =)
Ligne 26 -> votre nom d'utilisateur
"""
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


class ArchClean:
    def __init__(self, user_name):
        self.child = pexpect.spawn('pacman -Scc', timeout=5)
        self.user_name = user_name
        self.browser_list = ['mozilla', 'chromium', 'chrome']

    def clean_pacman_cache(self):
        print('[*] Clean Pacman Cache')
        ret = self.child.expect([pexpect.EOF, '.*[Oo/Nn]', '.*[Yy/Nn]'])

        if ret == 0:
            print('[--] Error While Cleaning Pacman Cache')
            sys.exit(0)

        if ret == 1:
            self.child.sendline('O')

        if ret == 2:
            self.child.sendline('Y')

        ret = self.child.expect([pexpect.EOF, '.*[Oo/Nn]', '.*[Yy/Nn]'])

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

    def clean_unsed_dependencies(self):
        print('[*] Clean Unused Dependencies')
        self.child.sendline('pacman -Rs `pacman -Qqtd | grep -Fv -f <(pacman -Qqtdm)`')
        #self.child.sendline('pacman -Rns $(pacman -Qtdq)')
        ret = self.child.expect([pexpect.EOF, '.*[Oo/Nn]', '.*[Yy/Nn]', '$'])

        if ret == 0:
            print('[--] Error While Cleaning Unused Dependencies')
            sys.exit(0)

        if ret == 1:
            self.child.sendline('O')
            print('[*] Unused Dependencies Has Been Removed')

        if ret == 2:
            self.child.sendline('Y')
            print('[*] Unused Dependencies Has Been Removed')

        if ret == 3:
            print('[*] No Unused Dependencies')

    def clean_thumbnails(self):
        print('[*] Clean Thumbnails')
        path_to_thumbnails = '/home/' + self.user_name + '/.thumbnails/'
        for folder in os.listdir(path_to_thumbnails):
            try:
                shutil.rmtree(path_to_thumbnails + folder + '/')
            except:
                shutil.rmtree(path_to_thumbnails + folder)

        path_to_thumbnails = '/home/' + self.user_name + '/.cache/thumbnails/'
        for folder in os.listdir(path_to_thumbnails):
            try:
                shutil.rmtree(path_to_thumbnails + folder + '/')
            except:
                shutil.rmtree(path_to_thumbnails + folder)

    def clean_trash(self):
        print('[*] Clean Trash')
        path_to_trash = '/home/' + self.user_name + '/.local/share/Trash/'
        for folder in os.listdir(path_to_trash):
            shutil.rmtree(path_to_trash + folder + '/')

    def optimize_pacman_db(self):
        print('[*] Optimizing Pacman Data-Base')
        self.child.sendline('pacman-optimize')
        ret = self.child.expect([pexpect.EOF, '$'])

        if ret == 0:
            print('[--] Error While Optimizing the DB')

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

    def read_output(self, display=False):
        log_before = self.child.before.decode('utf-8').strip().split('\\r\\n')
        log_after = self.child.after.decode('utf-8').strip().split('\\r\\n')
        if display:
            print('-' * 15 + ' Before ' + '-' * 15)
            for line in log_before:
                print(line)

            print('-' * 15 + ' After ' + '-' * 15)
            for line in log_after:
                print(line)

            print('-' * 15 + ' ReadLines ' + '-' * 15)
            for line in self.child.readlines():
                print(line.decode('utf-8'))

            print('-' * 15 + ' End Of Display ' + '-' * 15)

    def main(self):
        self.clean_pacman_cache()
        self.clean_os_cache()
        self.clean_unsed_dependencies()
        self.clean_thumbnails()
        self.clean_trash()
        self.optimize_pacman_db()
        self.clean_browser_cache()
        self.child.kill(1)
