import discord
import functions
import asyncio
import sqlite3

aliases = ['잡명령어도움', '청소', '삭제', '메시지삭제', 'clear', 'delete', '메시지청소', '유저차단', '차단', '서버차단', '유저추방', '추방', '서버추방', '서버가입', '공지등록', '공지채널', '공지받기', '우체통', '서버우체통', '초대코드', '채널초대', '서버초대', '초대코드생성', '초대링크']

async def run(client, message, args, admin, vip, cmd):

    con = sqlite3.connect('commands/database.db')
    cur = con.cursor()

    if cmd in ['청소', '삭제', '메시지삭제', 'clear', 'delete', '메시지청소']:
        if args[0] == '':
            await functions.makeembed('삭제할 메시지의 양을 입력해주세요', message)
            return
        if not message.author.guild_permissions.manage_messages:
            await functions.makeembed('유저에게 권한이 없네요', message)
            return
        try:
            if int(args[0]) > 100:
                await functions.makeembed('봇이 100개 이하의 메시지만 삭제 가능합니다', message)
                return
        except ValueError:
            await functions.makeembed('정수를 입력해주세요', message)
            return
        try:
            delete = await message.channel.purge(limit = int(args[0]) + 1)
        except discord.errors.Forbidden:
            await functions.makeembed('봇에게 권한이 없네요', message)
            return
        msg = await message.channel.send(embed = discord.Embed(title = f'메시지 {len(delete) - 1}개 삭제 완료!', colour = discord.Colour.blue()))
        await asyncio.sleep(5)
        await msg.delete()
    
    if cmd in ['유저차단', '차단', '서버차단']:
        if args[0] == '':
            await functions.makeembed('차단할 유저를 맨션해주세요', message)
            return
        try:
            user = message.guild.get_member(int(args[0].split('<@!')[1].split('>')[0]))
        except IndexError:
            try:
                user = message.guild.get_member(int(args[0]))
            except ValueError:
                await functions.makeembed('차단할 유저를 맨션해주세요', message)
                return
            except IndexError:
                await functions.makeembed('차단할 유저를 맨션해주세요', message)
                return
        if not message.author.guild_permissions.ban_members:
            await functions.makeembed('유저에게 권한이 없네요', message)
            return
        try:
            await message.guild.ban(user)
        except discord.errors.Forbidden:
            await functions.makeembed('봇에게 권한이 없네요', message)
            return
        await functions.makeembed(f'성공적으로 {user.name}님을 차단했습니다', message)
    if cmd in ['유저추방', '추방', '서버추방']:
        if args[0] == '':
            await functions.makeembed('추방할 유저를 맨션해주세요', message)
            return
        try:
            user = message.guild.get_member(int(args[0].split('<@!')[1].split('>')[0]))
        except IndexError:
            try:
                user = message.guild.get_member(int(args[0]))
            except ValueError:
                await functions.makeembed('추방할 유저를 맨션해주세요', message)
                return
            except IndexError:
                await functions.makeembed('추방할 유저를 맨션해주세요', message)
                return
        if not message.author.guild_permissions.kick_members:
            await functions.makeembed('유저에게 권한이 없네요', message)
            return
        try:
            await message.guild.ban(user)
        except discord.errors.Forbidden:
            await functions.makeembed('봇에게 권한이 없네요', message)
            return
        await functions.makeembed(f'성공적으로 {user.name}님을 추방했습니다', message)
    if cmd in ['서버가입', '공지등록', '공지채널', '공지받기', '우체통', '서버우체통']:
        if args[0] == '':
            await functions.makeembed('공지를 받을 채널을 입력해주세요', message)
            return
        try:
            channel = client.get_channel(int(args[0].split('<#')[1].split('>')[0]))
        except IndexError:
            try:
                channel = client.get_channel(int(args[0]))
            except ValueError:
                await functions.makeembed('공지를 받을 채널을 입력해주세요', message)
                return
            except IndexError:
                await functions.makeembed('공지를 받을 채널을 입력해주세요', message)
                return
        print(channel)
        try:
            cur.execute(f'INSERT INTO SERVERS VALUES (?, ?, ?, ?)', (str(message.guild.id), str(message.guild.name), str(channel.id), 0))
        except sqlite3.IntegrityError:
            cur.execute(f'UPDATE SERVERS SET channelid=\'{channel.id}\' WHERE id=\'{message.guild.id}\'')
        con.commit()
        await functions.makeembed('성공적으로 서버 가입을 했습니다', message)
    if cmd in ['초대코드', '채널초대', '서버초대', '초대코드생성', '초대링크']:
        if args[0] == '':
            await functions.makeembed('초대할 채널을 입력해주세요', message)
            return
        try:
            channel = client.get_channel(int(args[0].split('<#')[1].split('>')[0]))
        except IndexError:
            try:
                channel = client.get_channel(int(args[0]))
            except ValueError:
                await functions.makeembed('초대할 채널을 입력해주세요', message)
                return
            except IndexError:
                await functions.makeembed('초대할 채널을 입력해주세요', message)
                return
        try:
            url = await channel.create_invite(reason = f'{message.author.display_name}님이 생성')
        except discord.errors.Forbidden:
            await functions.makeembed('봇에게 권한이 없습니다', message)
            return
        embed = discord.Embed(
            title = f'{channel.name} 채널 초대링크',
            url = str(url), 
            colour = discord.Colour.blue()
        )
        await message.channel.send(embed = embed)
            
            

        
