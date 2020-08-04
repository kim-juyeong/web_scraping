import requests
from bs4 import BeautifulSoup


url = 'https://movie.naver.com/movie/running/current.nhn'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

movies = []

contents = soup.select('#content > div.article > div:nth-child(1) > div.lst_wrap > ul > li')

for movie in contents:
    tag = movie.select_one('dl > dt > a')
    movies.append({'title': tag.text, 'code': tag['href'].split('code=')[1]})

print(movies)