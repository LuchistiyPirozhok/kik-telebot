#!/bin/bash
rm -f ./scripts/users.db

sqlite3 scripts/users.db 'CREATE TABLE IF NOT EXISTS guilds (guild_name text PRIMARY KEY)'
sqlite3 scripts/users.db "insert into guilds (guild_name) values ('Коготь и клык')"
sqlite3 scripts/users.db 'CREATE TABLE IF NOT EXISTS users (telegram_id text PRIMARY KEY, character_name text, phone text, subscribed int, guild_name text, reg_code text, status int default 0)'
sqlite3 scripts/users.db "insert into users (telegram_id,character_name,reg_code,status) values ('463808631','Дорим','000001','4')"
