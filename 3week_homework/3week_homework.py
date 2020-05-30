import requests
from bs4 import BeautifulSoup

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://www.genie.co.kr/chart/top200?ditc=D&ymd=20200403&hh=23&rtm=N&pg=1',headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')

songs = soup.select('table.list-wrap > tbody > tr')

for song in songs: 
    ex_num = song.select_one('td.number').text # 숫자 / 곡제목 / 가수 

    if ex_num is not None:
        title_data = song.select_one('td.info > a.title.ellipsis')
        artist_data = song.select_one('td.info > a.artist.ellipsis')

        title = title_data.text
        artist = artist_data.text
        
        num = ex_num[0:2]
        print(num.strip(), title.strip(), artist.strip())