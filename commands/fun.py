import discord
import sqlite3
import asyncio
import functions
import random

aliases = ['말해', '전송', '건의', '제안', '무단침입', '채널전송', '채널침입', '디엠', '디엠전송', '전송디엠', '투표', '찬반투표', '주사위']

async def run(client, message, args, vip, admin, cmd):
    if cmd in ['말해', '전송']:
        msg = message.content.split(cmd)[1][1:]
        if msg == '':
            await functions.makeembed('봇이 할 말을 입력해주세요', message)
            return
        try:
            await message.delete()
            await message.channel.send(msg)
        except discord.errors.Forbidden:
            await message.channel.send(msg)
    if cmd in ['건의', '제안']:
        msg = message.content[4:]
        user = client.get_user(695608812328976525)
        embed = discord.Embed(
            title = msg, 
            description = f'{message.author}님의 건의사항입니다',
            colour = discord.Colour.blue()
        )
        await user.send(embed = embed)
        await functions.makeembed('건의사항이 성공적으로 전송되었습니다', message)
    if cmd in ['무단침입', '채널전송', '채널침입']:
        if args[0] == '':
            await functions.makeembed('채널을 입력해주세요', message)
            return
        try:
            channel = client.get_channel(int(args[0].split('<#')[1].split('>')[0]))
        except IndexError:
            try:
                channel = client.get_channel(int(args[0]))
            except ValueError:
                await functions.makeembed('채널을 입력해주세요', message)
                return
            except IndexError:
                await functions.makeembed('채널을 입력해주세요', message)
                return
        msg = message.content.split(str(channel.id))[1][1:]
        try:
            if args[1] == '':
                await functions.makeembed('내용을 입력해주세요', message)
                return
        except IndexError:
            await functions.makeembed('내용을 입력해주세요', message)
            return
        try:
            try:
                await message.delete()
            except discord.errors.Forbidden:
                pass
            await channel.send(msg)   
        except discord.errors.Forbidden:
            functions.makeembed('권한이 없네요', message)     
            return
    if cmd in ['디엠', '디엠전송', '전송디엠']:
        if args[0] == '':
            await functions.makeembed('디엠을 보낼 유저를 맨션해주세요', message)
            return
        try:
            user = message.guild.get_member(int(args[0].split('<@!')[1].split('>')[0]))
        except IndexError:
            try:
                user = message.guild.get_member(int(args[0]))
            except ValueError:
                await functions.makeembed('디엠을 보낼 유저를 맨션해주세요', message)
                return
            except IndexError:
                await functions.makeembed('디엠을 보낼 유저를 맨션해주세요', message)
                return
        try:
            if args[1] == '':
                await functions.makeembed('내용을 입력해주세요', message)
                return
        except IndexError:
            await functions.makeembed('내용을 입력해주세요', message)
            return
        msg = message.content.split(str(user.id))[1][1:]
        embed = discord.Embed(
            title = msg,
            description = f'{message.author}님의 메시지', 
            color = discord.Color.blue()
        )
        await user.send(embed = embed)
        await functions.makeembed('성공적으로 메시지를 전송했습니다', message)
    if cmd in ['투표', '찬반투표']:
        msg = message.content.split(cmd)[1][1:]
        if args[0] == '':
            await functions.makeembed('투표 주제를 입력해주세요', message)
            return
        if not '&&' in msg:
            embed = discord.Embed(
                title = msg, 
                color = discord.Color.blue()
            )
            mesg = await message.channel.send(embed = embed)
            await mesg.add_reaction('👍')
            await mesg.add_reaction('👎')
            return
        msg = msg.split('&&')
        try:
            if msg[1] == '':
                await functions.makeembed('투표 항목은 2개 이상이여야 합니다', message)
                return
            if msg[2] == '':
                await functions.makeembed('투표 항목은 2개 이상이여야 합니다', message)
                return
        except IndexError:
            await functions.makeembed('투표 항목은 2개 이상이여야 합니다', message)
            return
        string = ''
        for i in range(len(msg) ):
            if i == 0:
                continue
            if i >= 10:
                await functions.makeembed('투표 항목은 10개 이하여야 합니다', message)
                return
            string += f'{i}. {msg[i]}\n'
        embed = discord.Embed(
            title = msg[0],
            description = string, 
            color = discord.Color.blue()
        )
        mesg = await message.channel.send(embed = embed)
        for i in range(len(msg)):
            if i == 0:
                continue
            await mesg.add_reaction({1:'1️⃣', 2:'2️⃣', 3:'3️⃣', 4:'4️⃣', 5:'5️⃣', 6:'6️⃣', 7:'7️⃣', 8:'8️⃣', 9:'9️⃣', 10:'🔟', }.get(i, 'default'))
    if cmd in ['주사위']:
        await functions.makeembed(f'주사위 값: {random.randint(1, 6)}', message)
