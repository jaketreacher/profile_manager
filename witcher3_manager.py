#!/usr/bin/python3

import os
import subprocess
import sys
import time

# Get user argument
try:
    index = sys.argv.index('-user')
    index += 1
    user = sys.argv[index]
except ValueError:
    user = False
except IndexError:
    print('Must specify -user <user>')
    sys.exit()

# Read/create settings
settings = {}
root_dir = os.path.dirname(os.path.realpath(__file__))
settings_path = os.path.join(root_dir, 'settings.txt')
if os.path.exists(settings_path):
    with open(settings_path, 'r') as file:
        for line in file:
            line = line.replace('\n', '')
            args = line.split('=')
            settings[args[0]] = args[1]
else:
    with open(settings_path, 'w') as file:
        settings_default = ('SAVE=/absolute/path/to/documents/save/folder\n'
                            'GAME=/absolute/path/to/witcher3.exe\n'
                            'PROFILE=/absolute/path/to/profile/root/dir\n')
        file.write(settings_default)
    print('Configure settings.txt to continue')
    sys.exit()

# Verify settings
required_keys = ['SAVE', 'GAME', 'PROFILE']
for key in required_keys:
    if key not in settings.keys():
        print('Settings contains invalid keys. Delete the file to reset.')
        sys.exit()

# Ommit trailing / from all settings
for key,value in settings.items():
    value = os.path.dirname(os.path.join(value, ''))
    settings[key] = value

if not os.path.exists(settings['GAME']):
    print("GAME not found!")
    sys.exit()

# Get profiles in PROFILE directory
if os.path.exists(settings['PROFILE']):
    files = os.listdir(settings['PROFILE'])
    folders = list(filter(lambda file:
                          os.path.isdir(os.path.join(
                              settings['PROFILE'], file)),
                          files))
else:
    print("PROFILE not found!")
    sys.exit()

# If program run without arguments, create batch shortcuts for all profiles
batch_path = os.path.dirname(os.path.abspath(__file__))
batch_path = os.path.join(batch_path, 'launch.bat')
if not os.path.exists(batch_path):
    game_path = os.path.dirname(settings['GAME'])
    game_file = os.path.basename(settings['GAME'])

    batch = []
    batch.append('@echo off\n')
    batch.append('cd "{}"\n'.format(game_path))
    batch.append('start {}\n'.format(game_file))
    batch.append('exit')
    batch = "".join(batch)

    with open(batch_path, 'w') as file:
        file.write(batch)

if not user:
    sys.exit()

# Check if profile matches argument
active_profile = None
if user in folders:
    active_profile = os.path.join(settings['PROFILE'], user)
    active_profile = os.path.join(active_profile, '')
else:
    print("Profile '{}' not found!".format(user))
    sys.exit()

# Check if current save folder is directory or link
if os.path.isdir(settings['SAVE']) and not os.path.islink(settings['SAVE']):
    # Backup old files
    now = int(time.time())
    current_dir = os.path.dirname(os.path.join(settings['SAVE'], ''))
    backup_dir = "{}_{}_backup".format(current_dir, now)

    os.rename(current_dir, backup_dir)
    print("Backup current profiles to: {}".format(backup_dir))

if os.path.islink(settings['SAVE']):
    os.remove(settings['SAVE'])
    print("Removed previous save link")

# Create Link
os.symlink(active_profile, settings['SAVE'])
print("Swapped to profile '{}'".format(user))

print("Launching {}".format(settings['GAME']))
subprocess.Popen(batch_path)