#!/bin/bash
sqlite3 scripts/users.db 'select * from users'
sqlite3 scripts/users.db 'select * from guilds'
