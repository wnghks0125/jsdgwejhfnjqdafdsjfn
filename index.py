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


def check_queue(qid, channel):
    if queues[qid]:
        player = queues[qid].pop(0)
        del musiclist[0]
        embed = discord.Embed(title="재생하겠느니라!!", description=player.title + "\n" + player.url)
        say = client.send_message(client.get_channel(channel), embed=embed)
        asyncio.run_coroutine_threadsafe(say, client.loop)
        player.volume = 0.5
        player.start()

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

    if message.author.bot:
        return None

    if message.content == '종료':
        try:
            for key in queues:
                if key == server.id:
                    del queues[server.id]
        except RuntimeError:
            for key in queues:
                if key == server.id:
                    del queues[server.id]
        if musiclist:
            musiclist.clear()
        try:
            voice_client = client.voice_client_in(server)
            await voice_client.disconnect()
            await client.send_message(message.channel, '종료했느니라!!')
        except discord.DiscordException:
            return

    # 음악 재생
    if message.content.startswith("재생"):
        if len(players) == 0 or players[0].is_playing() == 0:
            if client.voice_client_in(server) is None:
                await client.join_voice_channel(message.author.voice.voice_channel)
            voice_client = client.voice_client_in(server)
            msg1 = message.content.split(' ')
            url = msg1[1]
            try:
                player = await voice_client.create_ytdl_player(url,
                                                               after=lambda: check_queue(server.id, message.channel.id),
                                                               before_options="-reconnect 1 -reconnect_streamed 1 "
                                                                              "-reconnect_delay_max 5")
                player.volume = 0.5
                player.start()
                if len(players) == 0:
                    players.append(player)
                else:
                    players[0] = player
                embed = discord.Embed(title="재생하겠느니라!!", description=player.title + "\n" + player.url)
                await client.send_message(message.channel, embed=embed)
            except Exception:
                await client.send_message(message.channel, '유튜브 링크가 아니거나 재생할 수 없는 주소 이니라...')

    # 음악 예약
    if message.content.startswith('예약'):
        try:
            msg1 = message.content.split(' ')
            url = msg1[1]
            voice_client = client.voice_client_in(server)
            player = await voice_client.create_ytdl_player(url,
                                                           after=lambda: check_queue(server.id, message.channel.id),
                                                           before_options="-reconnect 1 "
                                                                          "-reconnect_streamed 1 "
                                                                          "-reconnect_delay_max 5")
            if server.id in queues:
                queues[server.id].append(player)
            else:
                queues[server.id] = [player]
            await client.send_message(message.channel, '예약 완료 했느니라!')
            musiclist.append(player.title + "\n" + url)
        except discord.DiscordException:
            await client.send_message(message.channel, '음성방에 들어가있지 않으면 예약이 불가능하니라...')

    # 음악 큐
    if message.content.startswith('큐'):
        msg1 = message.content.split(" ")
        check = msg1[1]
        # 큐 보기
        if check == '보기':
            for i in range(0, len(musiclist)):
                resings = resings + str(i + 1) + '번 예약곡' + '-' + ' ' + musiclist[i] + '\n\n'
            embed = discord.Embed(title='대기중인 곡들이니라~', description=resings, color=0xf7cac9)
            await client.send_message(message.channel, embed=embed)
        # 큐에 있는 음악 삭제
        if check == '삭제':
            del musiclist[int(msg1[2]) - 1]
            del queues[server.id][int(msg1[2]) - 1]
            await client.send_message(message.channel, msg1[2] + '번 예약곡을 취소 했느니라!')
 

client.run('token')       
