import json
import discord
import requests
import sqlite3
import functions
import sys
import pkg_resources
import sqlite3

aliases = ['정보도움', '서버정보', '섭정보', '서버인포', '서버', '섭정', '내정보', '유저정보', '정보', '내인포', '마이인포', '유저인포', '봇정보', '봇인포', '키키봇정보', '핑', '퐁', '내프사', '내아바타', '프사', '아바타']

async def run(client, message, args, admin, vip, cmd):
    con = sqlite3.connect('commands/database.db')
    cur = con.cursor()

    if cmd in ['서버정보', '섭정보', '서버인포', '서버', '섭정']:
        i = 0
        cur.execute(f'SELECT * FROM SERVERS WHERE id=\'{str(message.guild.id)}\'')
        for row in cur:
            i += 1
            server = row
        embed = discord.Embed(
            colour = discord.Colour.blue()
        )
        embed.set_thumbnail(url = message.guild.icon_url)
        embed.set_author(name = f'{message.guild.name} 정보')
    
        embed.set_author(name = f'서버 정보 - {message.guild.name}')
        embed.set_thumbnail(url = message.guild.icon_url)
        embed.add_field(name = "이름", value = message.guild.name, inline = False)
        embed.add_field(name = "아이디", value = message.guild.id, inline = False)
        embed.add_field(name = "나라", value = str(message.guild.region).title(), inline = False)
        embed.add_field(name = "주인", value = f'{message.guild.owner.display_name} (ID: {message.guild.owner_id})', inline = False)
        embed.add_field(name = "멤버 수", value = f'전체 유저: {len(message.guild.members)} ( 봇: {len(list(filter(lambda x: x.bot, message.guild.members)))} | 유저: {len(list(filter(lambda x: not x.bot, message.guild.members)))} )', inline = False)
        embed.add_field(name = "채널 수", value = f'전체 채널: {len(message.guild.channels)} ( 채팅채널: {len(message.guild.text_channels)} | 음성채널: {len(message.guild.voice_channels)} | 카테고리: {len(message.guild.categories)} )', inline = False)
        embed.add_field(name = "생긴 날짜", value = message.guild.created_at.strftime("20%y년 %m월 %d일"), inline = False)
    
        if message.guild.afk_channel != None:
            embed.add_field(name = f'잠수 채널', value = f'{message.guild.afk_channel.name} (타이머: {message.guild.afk_timeout})', inline = False)

        if message.guild.system_channel != None:
            embed.add_field(name = f'시스템 채널', value = f'{message.guild.system_channel.name}', inline = False)
        if not i == 0:
            embed.add_field(name = f'공지 채널', value = f'{client.get_channel(int(server[2])).name} (ID: {server[2]})', inline = False)
        await message.channel.send(embed = embed)
    
    if cmd in ['내정보', '유저정보', '정보', '내인포', '마이인포', '유저인포']:
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
                await functions.makeembed('프로필을 확인할 유저를 맨션해주세요', message)
                return
            except IndexError:
                await functions.makeembed('프로필을 확인할 유저를 맨션해주세요', message)
                return
        roles = [role for role in user.roles]
        embed = discord.Embed(
            color = discord.Colour.blue()
        )
        embed.set_author(name = f'유저정보 - {user.display_name}')
        embed.set_thumbnail(url = user.avatar_url)
        embed.add_field(name = '아이디', value = user.id, inline = False)
        embed.add_field(name = '계정 생성 시간', value = user.created_at.strftime('%a, %#d %B %Y, %I:%M %p UTC'), inline = False)
        embed.add_field(name = '가입 시간', value = user.joined_at.strftime('%a, %#d %B %Y, %I:%M %p UTC'), inline = False)
        embed.add_field(name = f'가진 역할들 ({len(roles)})', value = ' '.join([role.mention for role in roles][1:]), inline = False)
        embed.add_field(name = '가장 높은 역할', value = user.top_role.mention, inline = False)
        embed.add_field(name = '상태', value = user.status, inline = False)
        if 'Custom Status' in str(user.activity):
            embed.add_field(name = '하는 게임', value = user.activity.state, inline = False)
        else:
            embed.add_field(name = '하는 게임', value = user.activity, inline = False)
        cur.execute(f'SELECT * FROM USERS WHERE id=\'{str(user.id)}\'')
        i = 0
        for row in cur:
            i += 1
            user2 = row
        if not i == 0:
            embed.add_field(name = '돈', value = str(user2[2]) + '~~K~~', inline = False)
            embed.add_field(name = '커스텀커맨드 티켓', value = str(user2[3]) + '개', inline = False)
            embed.add_field(name = '소속사', value = {1: 'KI', 2: 'IK', 3: 'BO', 4:'OT'}.get(user2[8], 'default'), inline = False)
            if user2[4] == 1:
                embed.add_field(name = 'VIP 회원', value = 'True', inline = False)
            if user2[7] == 1:
                embed.add_field(name = '봇 관리자', value = 'True', inline = False)
            if user2[0] == '647630912795836437':
                embed.add_field(name = '봇 총관리자', value = 'True', inline = False)
        await message.channel.send(embed = embed)
    if cmd in ['봇정보', '봇인포', '에아봇정보']:
        embed = discord.Embed(
            title = 'EA BOT 정보',
            description = f'> 봇 이름: EA\n\
> 봇 id: {client.user.id}\n\
> 봇 탄생: 2020년 05월 15일 ||빼액||\n\
> 개발자: 감귤#7777\n\
> 사이트: 없는디?\n\n\
> 서버 수: {len(client.guilds)}\n\
> 유저 수: {len(client.users)}\n\n\
> 파이썬 버전: {sys.version.split(" ")[0]}\n\
> discord.py 버전: {pkg_resources.get_distribution("discord.py").version}',
            color = discord.Color.blue()
        ).set_thumbnail(url = client.user.avatar_url)
        await message.channel.send(embed = embed)
    if cmd in ['핑', '퐁']:
        await functions.makeembed(f'에아봇 핑\n세컨드 단위: {await functions.get_ping(client, "ms")}\n밀리세컨드 단위: {await functions.get_ping(client, "s")}', message)
    if cmd in ['내프사', '내아바타', '프사', '아바타']:
        if args[0] == '':
            embed = discord.Embed(
            title = f'{message.author.name}님의 프사',
            color = discord.Color.blue()
            ).set_image(url = message.author.avatar_url)
            await message.channel.send(embed = embed)
            return
        try:
            user = message.guild.get_member(int(args[0].split('<@!')[1].split('>')[0]))
        except IndexError:
            try:
                user = message.guild.get_member(int(args[0]))
            except ValueError:
                await functions.makeembed('프사를 확인할 유저를 맨션해주세요', message)
                return
            except IndexError:
                await functions.makeembed('프사를 확인할 유저를 맨션해주세요', message)
                return
        embed = discord.Embed(
            title = f'{user.name}님의 프사',
            color = discord.Color.blue()
        ).set_image(url = user.avatar_url)
        await message.channel.send(embed = embed)
