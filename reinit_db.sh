#!/bin/bash
rm -f ./scripts/users.db

sqlite3 scripts/users.db 'CREATE TABLE IF NOT EXISTS guilds (guild_name text PRIMARY KEY)'
sqlite3 scripts/users.db "insert into guilds (guild_name) values ('Коготь и клык')"
