#!/bin/bash
/usr/bin/sqlite3 /var/bot/kik-telebot/users.db 'select * from users'
/usr/bin/sqlite3 /var/bot/kik-telebot/users.db 'select * from guilds'
