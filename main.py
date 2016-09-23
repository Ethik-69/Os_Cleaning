#! /usr/bin/python
# -*- coding:utf-8 -*-
import sys, os
from lib.arch import ArchClean
from lib.debian import *

user_name = 'thesystem'


#  Check root permission
if os.geteuid() != 0:
    print('[*] Please Launch This With sudo !')
    sys.exit(0)

print('')
print("""
    ________________________________________
    < Keep Calm and Let Me Clean your System >
    ----------------------------------------
            \   ^__^
             \  (oo)\_________
                (__)\         )\/\\
                     || ----w|
                     ||     ||
    """)

print('')
print('-' * 10 + ' This Script Has Been Writen For a Personnal Use ' + '-' * 10)
print('-' * 10 + '       Normaly It Won\'t Break Your System        ' + '-' * 10)
print('-' * 10 + '             But.... We Never Know               ' + '-' * 10)
print('-' * 10 + '            Use It At Your Own Risk !            ' + '-' * 10)
print('')


#  Gather User Name
if user_name is None:
    print('[*] Please Give Me You User Name:')
    user_name = input('')
    print('[*] If you don\'t want to do this again, just add your username at the start of this file =)')


#  Gather OS Info
print('[*] Supported OS are:')
print('         1. Debian/Ubuntu/Mint')
print('         2. ArchLinux/Manjaro')
print('')
print('[?] What\'s your\'s ? [1/2]')
user_os = int(input())

if user_os == 1:
    cleaner = DebianClean(user_name)
elif user_os == 2:
    cleaner = ArchClean(user_name)
else:
    print('[-|°\|°\[]|°\ Can\'t understand what you said !')
    sys.exit(0)


#  If User Is Ready
print('[?] I Have All I Need, Launch Cleaning ? [Y/n]')
user_choice = input()

if user_choice == '':
    pass
elif user_choice in 'Nno':
    sys.exit(0)


#  Gather Avaiable space on Disk
disk = os.statvfs('/')
avaiable_disk_space = disk.f_bsize * disk.f_bavail


cleaner.main()

print('[*] You system is clean')


#  Print Release Disk Space
change_on_disk = (disk.f_bsize * disk.f_bavail - avaiable_disk_space) / 1.048576e6
print('[/*\] %s Mb were liberated on your disk' % change_on_disk)
