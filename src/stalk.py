#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import subprocess

def command_usage():
    to_print = """
**** Need to be run inside the directory where you manage.py is
#### usage :
        stalk.py directory_to_watch CMD

        e.g.
            stalk.py authorization ./manage.py test authorization/
    """
    print(to_print)
    return False

# font : StampatStandardello
running_test_text_short = """
                         _                                                             _
  _ __ _   _ _ __  _ __ (_)_ __   __ _    ___ ___  _ __ ___  _ __ ___   __ _ _ __   __| |
 | '__| | | | '_ \| '_ \| | '_ \ / _` |  / __/ _ \| '_ ` _ \| '_ ` _ \ / _` | '_ \ / _` |
 | |  | |_| | | | | | | | | | | | (_| | | (_| (_) | | | | | | | | | | | (_| | | | | (_| |_ _ _
 |_|   \__,_|_| |_|_| |_|_|_| |_|\__, |  \___\___/|_| |_| |_|_| |_| |_|\__,_|_| |_|\__,_(_|_|_)
                                 |___/
"""
waiting_text_short = """
              _ _   _              __              _
 __ __ ____ _(_) |_(_)_ _  __ _   / _|___ _ _   __| |_  __ _ _ _  __ _ ___
 \ V  V / _` | |  _| | ' \/ _` | |  _/ _ \ '_| / _| ' \/ _` | ' \/ _` / -_)
  \_/\_/\__,_|_|\__|_|_||_\__, | |_| \___/_|   \__|_||_\__,_|_||_\__, \___|
                          |___/                                  |___/
"""

error_text_short = """
  _____                        ___      ____  _                          _
 | ____|_ __ _ __ ___  _ __   ( _ )    / ___|| |__   __ _ _ __ ___   ___| |
 |  _| | '__| '__/ _ \| '__|  / _ \/\  \___ \| '_ \ / _` | '_ ` _ \ / _ \ |
 | |___| |  | | | (_) | |    | (_>  <   ___) | | | | (_| | | | | | |  __/_|
 |_____|_|  |_|  \___/|_|     \___/\/  |____/|_| |_|\__,_|_| |_| |_|\___(_)

"""

success_text_short = """
   _.._..,_,_    __     ___      _                                      _    ____ _                  _
  (          )   \ \   / (_) ___| |_  ___  _ __ _   _    __ _ _ __   __| |  / ___| | ___  _ __ _   _| |
   ]~,"-.-~~[     \ \ / /| |/ __| __|/ _ \| '__| | | |  / _` | '_ \ / _` | | |  _| |/ _ \| '__| | | | |
 .=])' (;  ([      \ V / | | (__| |_| (_) | |  | |_| | | (_| | | | | (_| | | |_| | | (_) | |  | |_| |_|
 | ]:: '    [       \_/  |_|\___|\__|\___/|_|   \__, |  \__,_|_| |_|\__,_|  \____|_|\___/|_|   \__, (_)
 '=]): .)  ([                                   |___/                                          |___/
    ~~----~~
"""

def colorized(string, color, bold='2'):
    colors = {
        "Black": "0;30",
        "Blue": "0;34",
        "Green": "0;32",
        "Cyan": "0;36",
        "Red": "0;31",
        "Purple": "0;35",
        "Brown": "0;33",
        "Light Gray": "0;37",
        "Dark Gray": "1;30",
        "Light Blue": "1;34",
        "Light Green": "1;32",
        "Light Cyan": "1;36",
        "Light Red": "1;31",
        "Light Purple": "1;35",
        "Yellow": "1;33",
        "White": "1;37",
    }

    b = bold if bold in ['1', '2'] else '2'
    s = '\x1b[%s;%sm%s\x1b[0m' % (colors.get(color, colors.get("White")), b, string)
    return s

def watch_app_for_py_change(path, cmd):
    tree = {}
    basepath = os.path.abspath(path)
    while True:
        something_has_changed = False
        for root, dirs, files in os.walk(basepath):
            for file in files:
                if file[0] == '.' or file[-3:] != '.py':
                    continue
                fullpath = os.path.join(root, file)
                unique_key = fullpath.replace('/', '_').replace('.', '_')
                last_time_modified = os.stat(fullpath).st_mtime
                last_time_tested = tree.get(unique_key, 0)
                if last_time_modified > last_time_tested:
                    something_has_changed = True
                    print('file changed : %s ' % fullpath)
                    tree[unique_key] = last_time_modified
        if something_has_changed:
            cmd()
            print(colorized(waiting_text_short, "Light Blue"))
        time.sleep(1)


def launch_cmd(path, cmd):
    os.system("clear")
    print(colorized(running_test_text_short, "Light Blue"))
    returncode = os.system(cmd)

    if returncode != 0:
        print("%s" % colorized(error_text_short, "Light Red", '1'))
        return returncode
    print(colorized(success_text_short, "Green"))



def setup_required_param(argv):
    if len(argv) < 3:
        command_usage()
        exit()
    cmd_sp = ' '
    return { 'cmd': cmd_sp.join(argv[2:]),
             'path': './',
             'watch_path': argv[1] }


def setup_cmd(path, cmd):
    def closure():
        launch_cmd(path, cmd)
    return closure

if __name__ == "__main__":
    settings = setup_required_param(sys.argv)

    cmd = setup_cmd(settings.get("path"), settings.get("cmd"))
    if settings:
        watch_app_for_py_change(settings['watch_path'], cmd)

