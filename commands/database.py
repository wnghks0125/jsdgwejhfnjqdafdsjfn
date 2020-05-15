import json
import discord
import requests
import sqlite3
import functions
import random
import time
import asyncio

con = sqlite3.connect('commands/database.db')
cur = con.cursor()

aliases = ['가입', '로그인', '회원가입', '커명추가', '커명사용', '커스텀명령어추가', '커스텀명령어사용', '배워', '커스텀명령어티켓사용', '커명티사용', '커명티켓사용', '구입', '구매', '사', 'buy', '물건구매', '인벤', '인벤토리', '가방', '내물건', '내가방', '물건', '지갑', '내돈', '돈', '머니', '마이돈', '배팅', '올인', '도박', '돈도박', '나쁜짓', '이상한짓', '돈줘', '돈받기', '돈내놔', '깁미돈', '내돈내놔', '돈돌려줘', '돈주라니까', '돈받아', '랭킹', '돈랭킹', '순위', '돈순위', '리더보드', '돈리더보드']

async def run(client, message, args, admin, vip, cmd):
    if cmd in ['가입', '로그인', '회원가입']:
        try:
            cur.execute(f'INSERT INTO USERS VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (str(message.author.id), str(message.author.name), 0, 0, 0, 0, 0, 0, random.randint(1, 4), 0))
        except sqlite3.IntegrityError:
            await functions.makeembed('이미 가입되어있습니다', message)
            return
        except sqlite3.OperationalError:
            await functions.makeembed('데이터베이스에 문제가 생겼습니다', message)
            return
        con.commit()
        await functions.makeembed('성공적으로 가입했습니다', message)
    if cmd in ['커명추가', '커명사용', '커스텀명령어추가', '커스텀명령어사용', '배워', '커스텀명령어티켓사용', '커명티사용', '커명티켓사용']:
        msg = message.content.split(cmd)[1][1:]
        if msg == '':
            await functions.makeembed('입력을 입력해주세요',  message)
            return
        if not '&&' in msg:
            await functions.makeembed('출력을 입력해주세요',  message)
            return
        q = msg.split('&&')[0]
        a = msg.split('&&')[1]
        if q == '':
            await functions.makeembed('입력을 입력해주세요',  message)
            return
        cur.execute(f'SELECT * FROM USERS WHERE id=\'{str(message.author.id)}\'')
        i = 0
        for row in cur:
            i += 1
            user = row
        if i == 0:
            await notlogin(message)
            return
        if user[3] < 1:
            await functions.makeembed('커스텀명령어 티켓이 필요합니다', message)
            return
        cur.execute(f'UPDATE USERS SET customcommands={user[3] - 1} WHERE id=\'{user[0]}\'')
        con.commit()    
        cur.execute(f'INSERT INTO CUSTOMCOMMANDS VALUES (?, ?, ?, ?)', (str(q), str(a), str(message.author.id), str(message.author.name)))
        con.commit()
        await functions.makeembed(f'{q}를 말하면 {a}를 말할게요', message)
    if cmd in ['구입', '구매', '사', 'buy', '물건구매']:
        value = args[0]
        if value == '':
            await functions.makeembed('물건 이름을 입력해주세요', message)
            return
        i = 0
        cur.execute(f'SELECT * FROM USERS WHERE id=\'{message.author.id}\'')
        for row in cur:
            user = row
            i += 1
        if i == 0:
            await notlogin(message)
            return
        if value in ['커명', '커스텀명령어티켓', '커스텀명령어', '커명티켓']:
            if user[2] < 5000:
                await nomoney(message)
                return
            cur.execute(f'UPDATE USERS SET money={user[2] - 5000}, customcommands={user[3] + 10} WHERE id=\'{user[0]}\'')
            con.commit()
            await buyed(message)
            return
        if value in ['VIP', 'VIP권', 'vip', 'vip권']:
            if user[2] < 1000000:
                await nomoney(message)
                return
            if user[4] != 0:
                await functions.makeembed('이미 VIP입니다', message)
                return
            cur.execute(f'UPDATE USERS SET money={user[2] - 1000000}, vip={1} WHERE id=\'{user[0]}\'')
            con.commit()
            await buyed(message)
            return
        await functions.makeembed('상점에 등록되지 않은 물건 입니다', message)
    if cmd in ['인벤', '인벤토리', '가방', '내물건', '내가방', '물건']:
        if args[0] == '':
            user = message.author
            a = True
        else:
            a = False
        try:
            if not a:
                user = message.guild.get_member(int(args[0].split('<@!')[1].split('>')[0]))
        except IndexError:
            try:
                user = message.guild.get_member(int(args[0]))
            except ValueError:
                await functions.makeembed('인벤토리를 확인할 유저를 맨션해주세요', message)
                return
            except IndexError:
                await functions.makeembed('인벤토리를 확인할 유저를 맨션해주세요', message)
                return
        i = 0
        cur.execute(f'SELECT * FROM USERS WHERE id=\'{user.id}\'')
        for row in cur:
            i += 1
            user2 = row
        if i == 0:
            await notlogin(message)
            return
        await functions.makeembed(f'{user.name}님의 인벤토리\n\n커스텀명령어 티켓: {user2[3]}\nVIP권: {user2[4]}', message)
    if cmd in ['지갑', '내돈', '돈', '머니', '마이돈']:
        if args[0] == '':
            user = message.author
            a = True
        else:
            a = False
        try:
            if not a:
                user = message.guild.get_member(int(args[0].split('<@!')[1].split('>')[0]))
        except IndexError:
            try:    
                user = message.guild.get_member(int(args[0]))
            except ValueError:
                await functions.makeembed('돈을 확인할 유저를 맨션해주세요', message)
                return
            except IndexError:
                await functions.makeembed('돈을 확인할 유저를 맨션해주세요', message)
                return
        cur.execute(f'SELECT * FROM USERS WHERE id=\'{user.id}\'')
        i = 0
        for row in cur:
            i += 1
            user2 = row
        if i == 0:
            await notlogin(message)
            return
        await functions.makeembed(f'{user.name}님의 돈: {user2[2]}~~K~~', message)
    if cmd in ['배팅', '올인', '도박', '돈도박', '나쁜짓', '이상한짓']:
        i = 0
        cur.execute(f'SELECT * FROM USERS WHERE id=\'{message.author.id}\'')
        for row in cur:
            user = row
            i += 1
        if i == 0:
            await notlogin(message)
            return
        if args[0] == '':
            money = user[2]
        else:
            if int(args[0]) > user[2] or int(args[0]) < 0:
                await functions.makeembed('가진 돈보다 큰 돈을 도박하시면 망해요', message)
                return
            money = int(args[0])
        embed = discord.Embed(
            title = f'정말로 {money}라는 돈을 가지고 도박을 하시겠습니까?',
            color = discord.Color.blue()
        )
        msg = await message.channel.send(embed = embed)
        await msg.add_reaction('⭕')
        def check(reaction, user2):
            return user2 == message.author and str(reaction.emoji) == '⭕'
        try:
            user2 = await client.wait_for('reaction_add', timeout = 60.0, check = check)
        except asyncio.TimeoutError:
            await msg.edit('도박이 취소되었습니다')
            try:
                await msg.clear_reactions()
            except Exception:
                pass
        else:
            try:
                await msg.clear_reactions()
            except Exception:
                pass
            if user[4] != 0:
                randmoney = random.randint(1, 3)
            else:
                randmoney = random.randint(1, 2)
            if randmoney == 1 or randmoney == 3:
                getmoney = money * 2
            else:
                getmoney = money * -1
            cur.execute(f'UPDATE USERS SET money={user[2] + getmoney} WHERE id=\'{user[0]}\'')
            if randmoney == 1 or randmoney == 3:
                await functions.makeembed('성공했습니다!!', message)
            else:
                await functions.makeembed('실패했어요ㅠㅠ', message)
            con.commit()
            return
    if cmd in ['돈줘', '돈받기', '돈내놔', '깁미돈', '내돈내놔', '돈돌려줘', '돈주라니까', '돈받아']:
        i = 0
        cur.execute(f'SELECT * FROM USERS WHERE id=\'{message.author.id}\'')
        for row in cur:
            user = row
            i += 1
        if i == 0:
            await notlogin(message)
            return
        if not int(user[9] + 3600 - time.time()) <= 0:
            await functions.makeembed(f'{int(user[9] + 3600 - time.time())}초 동안 쿨타임이 적용되어있습니다', message)
            return
        randmoney = random.randint(1, 1000)
        cur.execute(f'UPDATE USERS SET money={user[2] + randmoney}, cooltime={time.time()} WHERE id=\'{user[0]}\'')
        con.commit()
        await functions.makeembed(f'{randmoney}~~K~~ 획득', message)
        return
        
