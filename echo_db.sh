#!/bin/bash
sqlite3 users.db 'select * from users'
sqlite3 users.db 'select * from guilds'
