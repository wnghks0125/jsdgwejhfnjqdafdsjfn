import json
import discord
import requests
import sqlite3
import random
import functions
import os
import sys
import asyncio

aliases = ['관리자도움', '데이터베이스', '데이터베이스조회', '디비조회', '디비', '블랙추가', '블랙리스트추가', '나쁜인간추가', '나쁜유저추가', '나쁜사람추가', '금지유저추가', '공지', '모든서버공지', '도움말추가', '도움추가', '핼프추가', '핼프말추가', '컴파일', '소스컴파일', '코드컴파일', 'evaluation', 'eval', '테스트', '실험', '코드테스트', '코드실험', '스크립트재시작', '스크립트시작', '봇재시작', '봇시작', '재시작', '봇재시작', '모든서버초대', '모든서버초대링크']

con = sqlite3.connect('commands/database.db')
cur = con.cursor()

async def run(client, message, args, vip, admin, cmd):
    if not str(message.author.id) in admin:
        await functions.makeembed(f'⛔관리자 전용 명령어입니다', message)
        return

    if cmd in ['데이터베이스', '데이터베이스조회', '디비조회', '디비']:
        db = sqlite3.connect('commands/database.db').cursor()
        try:
            name = args[0]
        except IndexError:
            await functions.makeembed('데이터베이스 이름을 입력해주세요', message)
            return
        if name == '서버':
            name = 'SERVERS'
        elif name == '유저':
            name = 'USERS'
        elif name == '기억':
            name = 'CUSTOMCOMMANDS'
        elif name == '도움말':
            name = 'HELP'
        else:
            await functions.makeembed('그 데이터베이스를 못찾겠습니다', message)
            return
        value = ""
        db.execute(f'SELECT * FROM {name}')
        for row in db:
            value += f'{str(row)}\n'

        embed = discord.Embed(
            title = f'TABLE {name} 값',
            description = f'{value}',
            colour = discord.Colour.blue()
        )

        await message.channel.send(embed = embed)

    elif cmd in ['블랙추가', '블랙리스트추가', '나쁜인간추가', '나쁜유저추가', '나쁜사람추가', '금지유저추가']:
        try:
            user = message.guild.get_member(int(args[0].split('<@!')[1].split('>')[0]))
        except IndexError:
            try:
                user = message.guild.get_member(int(args[0]))
            except ValueError:
                await functions.makeembed('블랙리스트에 추가할 유저를 맨션해주세요', message)
                return
            except IndexError:
                await functions.makeembed('블랙리스트에 추가할 유저를 맨션해주세요', message)
                return
        userall = cur.execute('SELECT * FROM USERS')
        for row in userall:
            if str(message.author.id) == str(row[0]):
                cur.execute(f'UPDATE USERS SET black=1 WHERE id={user.id}')
                await functions.makeembed('블랙리스트에 유저를 추가했습니다\n리부팅을 해야합니다', message)
                con.commit()
                return
        await functions.makeembed('다행히(?) 이 사람은 에아봇 서비스에 가입이 되어 있지 않네요', message)
    elif cmd in ['블랙해제', '블랙리스트해제', '나쁜인간해제', '나쁜유저해제', '나쁜사람해제', '금지유저해제']:
        try:
            user = message.guild.get_member(int(args[0].split('<@!')[1].split('>')[0]))
        except IndexError:
            try:
                user = message.guild.get_member(int(args[0]))
            except ValueError:
                await functions.makeembed('블랙리스트에 해제할 유저를 맨션해주세요', message)
                return
            except IndexError:
                await functions.makeembed('블랙리스트에 해제할 유저를 맨션해주세요', message)
                return
        userall = cur.execute('SELECT * FROM USERS')
        for row in userall:
            if str(message.author.id) == str(row[0]):
                cur.execute(f'UPDATE USERS SET black=0 WHERE id={user.id}')
                await functions.makeembed('블랙리스트에 유저를 해제했습니다\n리부팅을 해야합니다', message)
                con.commit()
                return
        await functions.makeembed('이 사람은 에아봇 서비스에 가입이 되어 있지 않네요', message)
    elif cmd in ['공지', '모든서버공지']:
        serverall = cur.execute('SELECT * FROM SERVERS')
        try:
            mesg = message.content.split(f"{message.content.split(' ')[0]} ")[1]
        except IndexError: 
            await functions.makeembed('공지 내용을 써주세요!!', message)
            return
        embed = discord.Embed(
            title = '에아봇 공지',
            description = mesg + '\n\n[에아봇 서포트](https://discord.gg/tRfm3ZP)\n[봇 개발자들의 소통방](없는뒈 따로 감귤#7777 문의 기릿)',
            color = discord.Color.blue()
        )
        announcechannels = [[0, 0]]
        i = 1
        for row in serverall:
            if row[2]:
                announcechannels.append([row[0], client.get_channel(int(row[2]))])
                i += 1
        for server in client.guilds:
            alla = True
            arr = [0]
            z = 0
            if server.id in announcechannels:
                await announcechannels.index(str(server.id))[1].send(embed = embed)
                continue
            for channel in server.channels:
                if str(channel.type) == 'text':
                    arr.append(channel)
                    z += 1
                    try:
                        if not '에아봇-공지X' in channel.topic:
                            if '봇-공지' in channel.name or '에아봇' in channel.name or '봇_공지' in channel.name or '에아봇-공지' in channel.topic:
                                await channel.send(embed = embed)
                                alla = False
                                break
                    except TypeError:
                        try:
                            if '봇-공지' in channel.name or '에아봇' in channel.name or '봇_공지' in channel.name or '에아봇-공지' in channel.topic:
                                await channel.send(embed = embed)
                                alla = False
                                break
                        except TypeError:
                            if '봇-공지' in channel.name or '에아봇' in channel.name or '봇_공지' in channel.name:
                                await channel.send(embed = embed)
                                alla = False
                                break
                    except Exception:
                        pass
        if alla:
            if not z < 2:
                rand = random.randrange(1, z)
                await arr[rand].send(embed = embed)
        await functions.makeembed('공지 전송을 완료했습니다', message)
    if cmd in ['도움말추가', '도움추가', '핼프추가', '핼프말추가']:
        try:
            a = message.content.split(cmd)[1][1:].split('&&')
            if a[0] == '':
                await functions.makeembed('타입을 입력해주세요', message)
                return
            if a[1] == '':
                await functions.makeembed('입력을 입력해주세요', message)
                return
            if a[2] == '':
                await functions.makeembed('출력을 입력해주세요', message)
                return
            if a[3] == '':
                await functions.makeembed('명칭을 입력해주세요', message)
                return
        except IndexError:
            await functions.makeembed('형식에 맞춰서 입력해주세요', message)
            return
        try:
            cur.execute('INSERT INTO HELP VALUES (?, ?, ?, ?)', (str(a[0]), str(a[1]), str(a[2]), str(a[3])))
        except sqlite3.IntegrityError:
            await functions.makeembed('이미 있는 명령어입니다', message)
            return
        await functions.makeembed('도움말을 성공적으로 등록했습니다', message)
        con.commit()
    if cmd in ['컴파일', '소스컴파일', '코드컴파일', 'evaluation', 'eval', '테스트', '실험', '코드테스트', '코드실험']:
        if str(message.author.id) != '695608812328976525':
            await functions.makeembed('이 메시지는 총관리자밖에 사용이 불가합니다', message)
            return
        code = message.content.split(cmd)[1][1:]
        if code == '':
            await functions.makeembed('코드를 입력해주세요', message)
            return
        if 'token' in code: return
        
        #source = f'import discord\nimport functions\nimport sqlite3\n\n{code}'
        try:
            output = eval(str(code))
        except Exception as e:
            embed = discord.Embed(
                title = '에아봇 코드 컴파일 결과',
                description = f'**입력**\n\
```py\n\
import discord\n\
import functions\n\n\
{code}\n\
```\n\n\
**출력**\n\
 ```py\n\
{e}\n\
```\n\n\
**타입**\n\
```py\n\
Exception\n\
```',
                color = discord.Colour.blue()
            )
            await message.channel.send(embed = embed)
        typeofeval = type(output)
        try:
            embed = discord.Embed(
                title = '에아봇 코드 컴파일 결과',
                description = f'**입력**\n\
```py\n\
import discord\n\
import functions\n\n\
{code}\n\
```\n\n\
**출력**\n\
 ```py\n\
{output}\n\
```\n\n\
**타입**\n\
```py\n\
{typeofeval}\n\
```',
                color = discord.Colour.blue()
            )
            await message.channel.send(embed  = embed)
        except Exception as e:
            embed = discord.Embed(
                title = '에아봇 코드 컴파일 결과',
                description = f'**입력**\n\
```py\n\
import discord\n\
import functions\n\n\
{code}\n\
```\n\n\
**출력**\n\
 ```py\n\
{e}\n\
```\n\n\
**타입**\n\
```py\n\
Exception\n\
```',
                color = discord.Colour.blue()
            )
            await message.channel.send(embed = embed)
        
    if cmd in ['스크립트재시작', '스크립트시작', '봇재시작', '봇시작', '재시작', '봇재시작']:
        await functions.makeembed('현재 점검중인 코드입니다', message)
        await message.add_reaction('👌')
        await functions.makeembed('봇을 재시작시키는중입니다', message)
        executeable = sys.executable
        args2 = sys.argv[:]
        args2.insert(0, sys.executable)
        os.execvp(executeable, args2)
        client.logout()
        client.close()
    elif cmd in ['모든서버초대', '모든서버초대링크']:
        for server in client.guilds:
            #a = True
            arr = [0]
            for channel in server.channels:
                if str(channel.type) == 'text':
                    try:
                        await message.author.send(str(await channel.create_invite()))
                        break
                    except discord.errors.Forbidden:
                        pass
                    except discord.errors.HTTPException:
                        pass
            await asyncio.sleep(1)
        await functions.makeembed('초대링크 전송을 완료했습니다', message)
