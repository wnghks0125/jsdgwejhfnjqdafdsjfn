import os
import importlib
import sqlite3
import functions
import random

def run():
    arr = []
    for filename in os.listdir('./commands'):
        if filename.endswith('.py'):
            mod = importlib.import_module(f'commands.{filename.split(".py")[0]}')
            arr.extend([[mod.aliases, f'commands.{filename.split(".py")[0]}']])
    return arr  
async def chattinghandler(message, cmd):
    if cmd == '':
        await functions.makeembed(random.choice(['안녕하세요 인공지능 에아입니다', '왜불러요', '안녕하세요', 'ZZZZZZ', '쿠쿠루쿠쿠']), message)
        return
    con = sqlite3.connect('commands/database.db')
    cur = con.cursor()
    cur.execute(f'SELECT * FROM CUSTOMCOMMANDS WHERE input=\'{cmd}\'')
    commands = []
    i = 0
    for row in cur:
        i += 1
        commands.append(row)
    if i == 0:
        await functions.makeembed('***(갸우뚱)***', message)
        return
    await functions.makeembed(random.choice(commands)[1], message)
