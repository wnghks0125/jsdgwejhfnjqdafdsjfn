import json
import discord
import requests
import bs4
from urllib.request import urlopen, Request
import urllib
import env
from bs4 import BeautifulSoup
from googletrans import Translator
import functions
import smtplib
from email.mime.text import MIMEText
import os
import env
import wikipediaapi

aliases = ['응용도움', '실시간검색어', '네이버실검', '네이버실시간검색어', '실검', '날씨', '현재날씨', '미세', '날', '미세먼지', '온도', '링크', '단축', '단축링크', '영화순위', '영화', '네이버영화', '네이버영화순위', '번역', '한영번역', '영한번역', '음악순위', '맬론', '맬론차트', '맬론차트순위', '이메일전송', '이메일', '메일', '위키', '위키백과', '위키피디아', '롤', '롤전적', '리그오브레전드', '마크서버', '코로나', '코로나19', '우한폐렴', '코로나바이러스']

async def run(client, message, args, admin, vip, cmd):

    if cmd in ['실검', '실시간검색어', '네이버실검', '네이버실시간검색어']:
        try:
            if args[0] == '':
                first = 1
            first = int(args[0])
            if first < 1:
                await functions.makeembed('0위 갓에아-에아', message)
                return
            if  first > 20:
                await functions.makeembed('1000000000000000000000000000000000000000위 바보에아-에아', message)
                return
        except ValueError:
            await functions.makeembed('자연수를 입력해주세요', message)
            return
        except IndexError:
            first = 1
        try:
            if args[1] == '':
                last = 10
            last = int(args[1])
            if last < 1:
                await functions.makeembed('0위 갓에아', message)
                return
            if last > 20:
                await functions.makeembed('1000000000000000000000000000000000000000위 바보에아', message)
                return
            if last < first:
                await functions.makeembed('사용법\nㅋ실검 [첫번째 순위] [마지막 순위]', message)
                return
        except ValueError:
            await functions.makeembed('자연수를 입력해주세요', message)
            return
        except IndexError:
            last = 20
        json = requests.get('https://www.naver.com/srchrank?frm=main').json()
        embed = discord.Embed(
            title = '네이버 실시간검색어',
            description = f'{first}위~{last}위',
            colour = discord.Colour.blue()
        )

        for r in json.get('data'):
            if int(r.get("rank")) < first or int(r.get("rank")) > last:
                continue
            embed.add_field(name = f'{r.get("rank")}위', value = r.get('keyword'), inline = False)
    
        await message.channel.send(embed = embed)
    
    elif cmd in ['날씨', '현재날씨', '미세', '날', '미세먼지', '온도']:
        try:
            location = args[0]
        except IndexError:
            await functions.makeembed('사용법\nㅋ날씨 [도시이름]', message)
            return
        
        try:
            enc_location = urllib.parse.quote(location+'날씨')
            hdr = {'User-Agent': 'Mozilla/5.0'} 
            url = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=' + enc_location
            req = Request(url, headers=hdr)
            html = urllib.request.urlopen(req)
            bsObj = bs4.BeautifulSoup(html, "html.parser")
            todayBase = bsObj.find('div', {'class': 'main_info'})
            todayTemp1 = todayBase.find('span', {'class': 'todaytemp'})
            todayTemp = todayTemp1.text.strip() 
            todayValueBase = todayBase.find('ul', {'class': 'info_list'})
            todayValue2 = todayValueBase.find('p', {'class': 'cast_txt'})
            todayValue = todayValue2.text.strip()  
            todayFeelingTemp1 = todayValueBase.find('span', {'class': 'sensible'})
            todayFeelingTemp = todayFeelingTemp1.text.strip()  
            todayMiseaMongi1 = bsObj.find('div', {'class': 'sub_info'})
            todayMiseaMongi2 = todayMiseaMongi1.find('div', {'class': 'detail_box'})
            todayMiseaMongi3 = todayMiseaMongi2.find('dd')
            todayMiseaMongi = todayMiseaMongi3.text  
            tomorrowBase = bsObj.find('div', {'class': 'table_info weekly _weeklyWeather'})
            tomorrowTemp1 = tomorrowBase.find('li', {'class': 'date_info'})
            tomorrowTemp2 = tomorrowTemp1.find('dl')
            tomorrowTemp3 = tomorrowTemp2.find('dd')
            tomorrowTemp = tomorrowTemp3.text.strip()  
            tomorrowAreaBase = bsObj.find('div', {'class': 'tomorrow_area'})
            tomorrowMoring1 = tomorrowAreaBase.find('div', {'class': 'main_info morning_box'})
            tomorrowMoring2 = tomorrowMoring1.find('span', {'class': 'todaytemp'})
            tomorrowMoring = tomorrowMoring2.text.strip()  
            tomorrowValue1 = tomorrowMoring1.find('div', {'class': 'info_data'})
            tomorrowValue = tomorrowValue1.text.strip()  
            tomorrowAreaBase = bsObj.find('div', {'class': 'tomorrow_area'})
            tomorrowAllFind = tomorrowAreaBase.find_all('div', {'class': 'main_info morning_box'})
            tomorrowAfter1 = tomorrowAllFind[1]
            tomorrowAfter2 = tomorrowAfter1.find('p', {'class': 'info_temperature'})
            tomorrowAfter3 = tomorrowAfter2.find('span', {'class': 'todaytemp'})
            tomorrowAfterTemp = tomorrowAfter3.text.strip() 
            tomorrowAfterValue1 = tomorrowAfter1.find('div', {'class': 'info_data'})
            tomorrowAfterValue = tomorrowAfterValue1.text.strip()
            embed = discord.Embed(
                title=location + ' 날씨',
                description=location + ' 날씨입니다.',
                colour=discord.Colour.blue()
            )
            embed.add_field(name='현재온도', value=todayTemp+'˚', inline = False)  # 현재온도
            embed.add_field(name='체감온도', value=todayFeelingTemp, inline = False)  # 체감온도
            embed.add_field(name='현재상태', value=todayValue, inline=False)  # 밝음,어제보다 ?도 높거나 낮음을 나타내줌
            embed.add_field(name='현재 미세먼지 상태', value=todayMiseaMongi, inline=False)  # 오늘 미세먼지
            embed.add_field(name='오늘 오전/오후 날씨', value=tomorrowTemp, inline=False)  # 오늘날씨 # color=discord.Color.blue()
            embed.add_field(name='**----------------------------------**',value='**----------------------------------**', inline=False)  # 구분선
            embed.add_field(name='내일 오전온도', value=tomorrowMoring+'˚', inline=False)  # 내일오전날씨
            embed.add_field(name='내일 오전날씨상태, 미세먼지 상태', value=tomorrowValue, inline=False)  # 내일오전 날씨상태
            embed.add_field(name='내일 오후온도', value=tomorrowAfterTemp + '˚', inline=False)  # 내일오후날씨
            embed.add_field(name='내일 오후날씨상태, 미세먼지 상태', value=tomorrowAfterValue, inline=False)  # 내일오후 날씨상태
            await message.channel.send(embed = embed)
        except AttributeError:
            await functions.makeembed('에아봇이 그 도시의 날씨를 가져올수 없습니다', message)
            return
    elif cmd in ['링크', '단축', '단축링크']:
        try:
            target = args[0]
            if target == '':
                await functions.makeembed('사용방법\nㅋ단축 [링크]', message)
                return
        except IndexError:
            await functions.makeembed('사용방법\nㅋ단축 [링크]', message)
            return
        client_id = env.shorturl_client_id
        client_secret = env.shorturl_client_secret
        header = {'X-Naver-Client-Id': client_id, 'X-Naver-Client-Secret': client_secret}
        naver = 'https://openapi.naver.com/v1/util/shorturl'
        data = {'url': target}
        try:
            maker = requests.post(url = naver, data = data, headers = header)
            maker.close()
            output = maker.json()['result']['url']
        except ValueError:
            await functions.makeembed('재데로된 링크를 입력해주세요', message)
            return

        embed = discord.Embed(
            title = output,
            url = output,
            colour = discord.Colour.blue()
        )   
        await message.channel.send(embed = embed)
    
    elif cmd in ['영화순위', '영화', '네이버영화', '네이버영화순위']:
        try:
            first = args[0]
            if args[0] == '':
                first = 1
        except IndexError:
            first = 1
        try:
            first = int(first)
            if first < 1:
                await functions.makeembed('0위 갓에아', message)
                return
            if  first > 25:
                await functions.makeembed('1000000000000000000000000000000000000000위 바보에아', message)
                return
        except ValueError:
            await functions.makeembed('자연수를 입력해주세요', message)
            return
        try:
            last = args[1]
            if args[1] == '':
                last = 10
        except IndexError:
            last = 10
        try:
            last = int(last)
            if last < 1:
                await functions.makeembed('0위 갓에아', message)
                return
            if last > 25:
                await functions.makeembed('1000000000000000000000000000000000000000위 바보에아-에아', message)
                return
            if last < first:
                await functions.makeembed('사용법\nㅋ영화 [첫번째 순위] [마지막 순위]', message)
                return
        except ValueError:
            await functions.makeembed('자연수를 입력해주세요', message)
            return
        url = urlopen('https://movie.naver.com/movie/running/current.nhn')
        bs = BeautifulSoup(url, 'html.parser')
        body = bs.body
        target = body.find(class_ = "lst_detail_t1")
        embed = discord.Embed(title = "영화 순위", description = "네이버 영화에서 크롤링", colour = discord.Colour.blue())
        list = target.find_all('li')
        no = first
        for n in range(first - 1, last):
            title = list[n].find(class_ = 'tit').find('a').text
            try:
                director = list[n].find(class_ = 'info_txt1').find_all('dd')[1].find_all('a')
                directorList = [director.text.strip() for director in director]
            except IndexError:
                directorList = '정보 없음'
            try:
                cast = list[n].find(class_="lst_dsc").find("dl", class_="info_txt1").find_all("dd")[2].find(class_="link_txt").find_all("a")
                castList = [cast.text.strip() for cast in cast]
            except IndexError:
                castList="정보 없음"
            embed.add_field(name=f'{no}등', value=f"영화 제목:  {title}\n제작 감독:  {directorList}\n출연 배우:  {castList}", inline=False)
            no += 1
        await message.channel.send(embed = embed)
    if cmd in ['번역', '한영번역', '영한번역']:
        translator = Translator()
        try:
            index = args[0]
            if args[0] == '':
                await functions.makeembed('번역할 문장이나 단어를 입력해주세요', message)
                return
        except IndexError:
            await functions.makeembed('번역할 문장이나 단어를 입력해주세요', message)
            return
        index = message.content.split(cmd)[1][1:]
        lang = translator.detect(index).lang
        if str(lang) == 'ko':
            await functions.makeembed(f'{index}를 ko에서 영어로 변경\n값: {translator.translate(index, src = lang, dest = "en").text}', message)
            return
        await functions.makeembed(f'{index}를 {lang}에서 한국어로 변경\n값: {translator.translate(index, src = lang, dest = "ko").text}', message)
    elif cmd in ['음악순위', '맬론', '맬론차트', '맬론차트순위']:
        try:
            first = args[0]
            if args[0] == '':
                first = 1
        except IndexError:
            first = 1
        try:
            first = int(first)
            if first < 1:
                await functions.makeembed('0위 갓에아', message)
                return
            if  first > 25:
                await functions.makeembed('1000000000000000000000000000000000000000위 바보에아', message)
                return
        except ValueError:
            await functions.makeembed('자연수를 입력해주세요', message)
            return
        try:
            last = args[1]
            if args[1] == '':
                last = first + 9
        except IndexError:
            last = first + 9
        try:
            last = int(last)
            if last < 1:
                await functions.makeembed('0위 갓에아', message)
                return
            if last > 25:
                await functions.makeembed('1000000000000000000000000000000000000000위 바보에아', message)
                return
            if last < first:
                await functions.makeembed('사용법\n맬론차트 (첫번째 순위) (마지막 순위)', message)
                return
        except ValueError:
            await functions.makeembed('자연수를 입력해주세요', message)
            return
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}
        req = requests.get('https://www.melon.com/chart/index.htm', headers = header)
        html = req.text
        parse = BeautifulSoup(html, 'html.parser')
        titles = parse.find_all('div', {'class': 'ellipsis rank01'})
        songs = parse.find_all('div', {'class': 'ellipsis rank02'})
        title = []
        song = []
        embed = discord.Embed(
            title = f'맬론차트 {first} ~ {last}위',
            color = discord.Colour.blue()
        )
        for i in titles:
            title.append(i.find('a').text)
        for i in songs:
            song.append(i.find('span', {'class': 'checkEllipsis'}).text)
        for i in range(first - 1, last):
            embed.add_field(name = f'{i + 1}위', value = f'{title[i]} - {song[i]}', inline = False)
        await message.channel.send(embed = embed)
    if cmd in ['이메일전송', '이메일', '메일']:
        msg = message.content.split(cmd)[1][1:]
        if msg == '':
            await functions.makeembed('이메일을 입력해주세요', message)
            return
        email = msg.split(' ')[0]
        msg = msg.split(email)[1][1:]
        if email in msg:
            await functions.makeembed('내용에 이메일이 들어가면 에아봇에 에러가 납니다', message)
            return
        if msg == '':
            await functions.makeembed('내용을 입력해주세요', message)
            return
        s = smtplib.SMTP('smtp.gmail.com',587)
        s.starttls()
        s.login('happykiki7000@gmail.com', env.stmp)
        m2sg = MIMEText(msg)
        m2sg['Subject'] = f'{message.author}님의 메시지'
        s.sendmail('happykiki7000@gmail.com', email, m2sg.as_string())
        s.quit()
        await functions.makeembed('이메일 전송 성공입니다', message)
    if cmd in ['위키', '위키백과', '위키피디아']:
        wiki = wikipediaapi.Wikipedia(language = 'ko', extract_format = wikipediaapi.ExtractFormat.WIKI)
        learn = message.content.split(cmd)[1][1:]
        if learn == '':
            await functions.makeembed('문서 이름을 입력해주세요', message)
            return
        if not wiki.page(learn).exists():
            await functions.makeembed('없는 문서입니다', message)
            return
        embed = discord.Embed(
            title = learn,
            description = wiki.page(learn).text[0:2000],
            color = discord.Color.blue()
        )
        await message.author.send(embed = embed)
        await functions.makeembed('문서 내용을 성공적으로 보냈습니다(2000글자 까지)', message)
    if cmd in ['마크서버']:
        server = args[0]
        if server == '':
            await functions.makeembed('서버 주소를 입력해주세요', message)
            return
        url = 'https://mcsrvstat.us/server/' + str(server)
        res = requests.get(url)
        soup = BeautifulSoup(res.content, 'html.parser')
        clas = soup.findAll('h2')   
        try:
            a = clas[1]
            if a == None:
                return
        except IndexError:
            await functions.makeembed('서버가 온라인입니다', message)
            return
        await functions.makeembed('서버가 오프라인입니다', message)
    if cmd in ['롤', '롤전적', '리그오브레전드']:
        Name = args[0]
        if Name == '':
            await functions.makeembed('소환사 이름을 입력해주세요', message)
            return
        SummonerName = "" 
        TierUnranked = "" 
        LeagueType = [] 
        Tier = [] 
        LP = [] 
        Wins = [] 
        Losses = [] 
        Ratio = []
        url = 'https://www.op.gg/summoner/userName=' + Name 
        hdr = {'Accept-Language': 'ko_KR,en;q=0.8', 'User-Agent': ('Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Mobile Safari/537.36')} 
        req = requests.get(url, headers=hdr) 
        html = req.text 
        soup = BeautifulSoup(html, 'html.parser')
        for i in soup.select('div[class=SummonerName]'): 
            SummonerName = i.text 
        TierUnranked = soup.select('div.Cell')
        for i in soup.select('div[class=LeagueType]'): 
            LeagueType.append(i.text) 
        for i in soup.select('div[class=Tier]'): 
            Tier.append(i.text)
        for i in soup.select('div[class=LP]'): 
            LP.append(i.text) 
        for i in soup.select('span[class=Wins]'): 
            Wins.append(i.text) 
        for i in soup.select('span[class=Losses]'): 
            Losses.append(i.text) 
        for i in soup.select('span[class=Ratio]'): 
            Ratio.append(i.text)
        embed = discord.Embed(
            title='롤 정보',
            description='응용 기능',
            colour=discord.Colour.blue()
        )
        if SummonerName != "":
            if 'Unranked' in str(TierUnranked[0]): 
                embed.add_field(name = '솔로랭크', value = 'Unranked', inline = False)
            else: 
                asdf=Tier[0].strip('\n\t')
                embed.add_field(name = '솔로랭크', value = f'티어: {asdf}\nLP: {LP[0]}\n승/패: {Wins[0]}/{Losses[0]}\n승률: {Ratio[0]}', inline = False)
            if 'Unranked' in str(TierUnranked[1]): 
                embed.add_field(name = '자유랭크', value = 'Unranked', inline = False)
            else: 
                asdf=Tier[1].strip('\n\t')
                embed.add_field(name = '자유랭크', value = f'티어: {asdf}\nLP: {LP[1]}\n승/패: {Wins[1]}/{Losses[1]}\n승률: {Ratio[1]}', inline = False)
        else:
            embed.add_field(name = "에러", value = "사용자 정보 없음")
        await message.channel.send( embed=embed)
    if cmd in ['코로나', '코로나19', '우한폐렴', '코로나바이러스']:
        url = 'https://coronamap.site/'
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')
        hwagjin = soup.find('div', class_ = 'content').find('div').text
        dead = str(soup.find('div', class_ = 'content1 clear')).split('</div>')[5].split('<div>')[1]
        noknow = BeautifulSoup(requests.get('https://search.naver.com/search.naver?sm=top_hty&fbm=0&ie=utf8&query=%EC%BD%94%EB%A1%9C%EB%82%98').text, 'html.parser').find('div', class_ = 'graph_view').find('div', class_ = 'circle orange level5').find('strong', class_ = 'num').text
        none = str(soup.find('div', class_ = 'content1 clear')).split('</div>')[1].split('<div>')[1]
        embed = discord.Embed(
            title = '코로나19 현황',
            color = discord.Color.blue(),
            description = f'확진자: {hwagjin}\n검사진행: {noknow}\n사망자: {dead}\n격리해제: {none}'
        )
        await message.channel.send(embed = embed)
