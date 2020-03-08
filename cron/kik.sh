#!/bin/bash
source /root/.bash_profile
if [ $(pgrep python3) ]; then
    echo -e "main.py script was already running."
    exit 0
else
    cd /var/bot/kik-telebot
    /bin/bash /var/bot/kik-telebot/run.sh 
fi
