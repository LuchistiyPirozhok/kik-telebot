#!/bin/bash
rm ./scripts/db/users.db
sqlite3 users.db 'CREATE TABLE IF NOT EXISTS guilds (guild_name text PRIMARY KEY)'
sqlite3 users.db "insert into guilds (guild_name) values ('Коготь и клык')"