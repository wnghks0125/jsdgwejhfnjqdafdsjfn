import asyncio
import discord
import importlib

#엠베드 만들기
async def makeembed(title, message):
    embed = discord.Embed(
        title = title,
        decription = 'EA Bot Beta',
        color = discord.Color.blue()
    )
    await message.channel.send(embed = embed)

async def get_ping(client, second):
    return {'s':round(client.latency * 1000), 'ms':f'0.{round(client.latency * 1000)}'}.get(second, 'default')

#상태메시지 바꾸기
async def bt(games, channels, client):
    await client.wait_until_ready()

    games = ["/EA도움을 입력해 명령어 확인", f'서버: {len(client.guilds)} | 체널: {channels} | 유저: {len(client.users)}', '태스트중 : 사용금지']

    while not client.is_closed():
        for game in games:
            await client.change_presence(status = discord.Status.online, activity = discord.Game(str(game)))
            await asyncio.sleep(5)

#채널 수 구하기
def get_channels(guilds):
    channels = 0

    for i in guilds:
        channels += len(i.channels)
    
    return channels

#커맨드 구하기
def get_cmd(message, prefix):
    return message.content.split(prefix)[1].split(' ')[0]

#args 구하기
def get_args(message, cmd):
    return message.content.split(cmd)[1][1:].split(' ') 

#모듈 구하기
def get_module(module):
    return importlib.import_module(module)
