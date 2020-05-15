import discord
import sqlite3
import command       
import env 
import importlib
import functions
import youtube_dl
import datetime
import re
import os

#다른것이와요


client = discord.Client()   
token = env.token
prefix = '/ea'
chattingprefix = '에아야'

print('EA BOT 부팅중...')

commands = command.run()

admin = [0]
black = [0]
vip = [0]
users = [0]

cur = sqlite3.connect('commands/database.db').cursor()
cur.execute('SELECT * FROM USERS')

for element in cur:
    if element[4] == 1:
        vip.append(str(element[0]))

    if element[5] == 1:
        black.append(str(element[0]))
        
    if element[7] == 1:
        admin.append(str(element[0]))

#봇 시작
@client.event
async def on_ready():
    channels = functions.get_channels(client.guilds)
    games = ["/EA도움을 입력해 명령어 확인", f'서버: {len(client.guilds)} | 체널: {channels} | 유저: {len(client.users)}', '리라중: 사용금지']

    print('================================================================================')
    print(f'Client ID: {client.user.id}')
    print(f'Client Name: {client.user.name}')
    print('================================================================================')
    await functions.bt(games, channels, client)

@client.event
async def on_message(message):
    if message.content.startswith(chattingprefix) and str(message.channel.type) == 'text' and not message.author.bot: 
        print(f'{message.author.name}: {str(message.content.split(chattingprefix)[1][1:])}')
        await command.chattinghandler(message, str(message.content.split(chattingprefix)[1][1:]))
        return
    if not message.content.startswith(prefix): return
    if str(message.channel.type) != 'text': return
    if message.author.bot: return
    if str(message.author.id) in black: return
    if len(message.content) == 1: return
    if message.content[1] == 'ㅋ': return
    cmd = functions.get_cmd(message, prefix)   
    args = functions.get_args(message, cmd)

    print(f'{message.author.name}: {cmd} {args}')

    for i in commands:
        if cmd in i[0]: 
            mod = functions.get_module(str(i[1]))
            await mod.run(client, message, args, vip, admin, cmd)
            break
            
client.run(token)       
