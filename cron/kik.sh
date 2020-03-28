#!/bin/bash
source /root/.bash_profile_orig
if [ $(ps -ef | grep "main.py" | grep -v grep | wc -l) = 1 ]; then
    echo -e "main.py script was already running."
    exit 0
elif [ $(ps -ef | grep "main.py" | grep -v grep | wc -l) = 0 ]; then
    echo -e "script was down, starting again"
    date +"%T"
    cd /var/bot/kik-telebot
    /bin/bash /var/bot/kik-telebot/run.sh
else
    echo -e "a lot's of main.py scripts"
    date +"%T"
    #cd /var/bot/kik-telebot
    #/bin/bash /var/bot/kik-telebot/run.sh
fi
