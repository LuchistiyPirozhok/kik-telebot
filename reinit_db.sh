#!/bin/bash
rm -f ./scripts/users.db

CREATE_TABLE_COMMAND=$(cat <<-END
CREATE TABLE IF NOT EXISTS users (telegram_id text PRIMARY KEY,
                                                           character_name text,
                                                           phone text,
                                                           subscribed int,
                                                           guild_name text,
                                                           reg_code text,
                                                           status int default 0,
                                                           boss_mask int default 0,
                                                           last_update int default 0)
END
)

sqlite3 scripts/users.db 'CREATE TABLE IF NOT EXISTS guilds (guild_name text PRIMARY KEY)'
sqlite3 scripts/users.db "insert into guilds (guild_name) values ('Коготь и клык')"
sqlite3 scripts/users.db "$CREATE_TABLE_COMMAND"
#sqlite3 scripts/users.db "insert into users (telegram_id,character_name,reg_code,status) values ('463808631','Дорим','000001','4')"
sqlite3 scripts/users.db "insert into users (telegram_id,character_name,subscribed,guild_name,reg_code,status) values ('463808631','Дорим','1','Коготь и Клык','000001','4')"
