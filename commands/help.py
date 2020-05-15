import discord
import sqlite3
import functions

aliases = ['도움', '도움말', '명령어도움', '명령어도움말']

async def run(client, message, args, admin, vip, cmd):
    typeofhelp = message.content.split(cmd)[1][1:]
    if args[0] == '':
        embed = discord.Embed(
            title = '에아봇 도움말',
            color = discord.Color.blue()
        )
        for i in [['/ea도움 돈', '에아봇 돈 사용 명령어들을 확인합니다'], ['/ea도움 크롤링', '에아봇 크롤링 사용 명령어들을 확인합니다'], ['/ea도움 서버관리', '에아봇 서버관리 명령어들을 확인합니다'], ['/ea도움 관리자', '에아봇 관리자만 사용 가능한 명령어들을 확인합니다'], ['/ea도움 정보', '에아봇 정보를 알려주는 명령어들을 확인합니다'], ['/ea도움 놀이', '에아봇 재미있는 명령어를 확인합니다'], ['/ea도움 [특정 명령어]', '그 명령어를 확인합니다']]:
            embed.add_field(name = i[0], value = i[1])
        await message.channel.send(embed = embed)
        return
    cur = sqlite3.connect('commands/database.db').cursor()
    if typeofhelp in ['돈', '크롤링', '서버관리', '관리자', '정보', '놀이']:
        cur.execute(f'SELECT * FROM HELP WHERE type=\'{typeofhelp}\'')
        embed = discord.Embed(
            title = f'{typeofhelp} 명령어 도움말',
            description = f'대괄호([]) 안에 들어있는거는 필수, 소괄호(())안에 들어있는거는 선택',
            color = discord.Color.blue()
        )
        for element in cur:
            embed.add_field(name = element[3], value = element[1])
        await message.channel.send(embed = embed)
        return
    cur.execute(f'SELECT * FROM HELP WHERE howtocall=\'{typeofhelp}\'')
    i = 1
    for element in cur:
        i += 1
        a = element
    if i == 1:
        await functions.makeembed('명령어를 못찾습니다', message)
        return
    embed = discord.Embed(
        title = f'{a[3]} 명령어 도움말',
        description = f'사용 방법: {a[1]}\n설명: {a[2]}',
        color = discord.Color.blue()
    )
    await message.channel.send(embed = embed)
    
