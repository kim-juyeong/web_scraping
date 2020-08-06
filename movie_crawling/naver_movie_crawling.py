import requests
import csv
import os
from bs4 import BeautifulSoup


# 현재 상영 영화 불러오기
#
movies = []

url = 'https://movie.naver.com/movie/running/current.nhn'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

contents = soup.select('#content > div.article > div:nth-child(1) > div.lst_wrap > ul > li')

for i in contents:
    tag = i.select_one('dl > dt > a')
    movies.append({
        'title': tag.text, 
        'code': tag['href'].split('code=')[1]
        })


# 리뷰 불러오기
# headers = {
#     'authority': 'movie.naver.com',
#     'upgrade-insecure-requests': '1',
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
#     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
#     'sec-fetch-site': 'same-origin',
#     'sec-fetch-mode': 'navigate',
#     'sec-fetch-dest': 'iframe',
#     'referer': 'https://movie.naver.com/movie/bi/mi/point.nhn?code=188909',
#     'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
#     'cookie': 'REFERER_DOMAIN="d3d3Lmdvb2dsZS5jb20="; NNB=LXP4AN3KOAVV6; csrf_token=ecc4fa05-4a6e-4c24-9fc7-58a621481d95',
# }
#
reviews = []

for i in movies:
    response = requests.get('https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn', params=(
        ('code', i['code']),
        ('type', 'after'),
        ('isActualPointWriteExecute', 'false'),
        ('isMileageSubscriptionAlready', 'false'),
        ('isMileageSubscriptionReject', 'false'),
    ))
    
    soup = BeautifulSoup(response.text, 'html.parser')
    contents = soup.select('body > div > div > div.score_result > ul > li')
    count = 0

    for j in contents:
        if j.select_one(f'span#_filtered_ment_{count} > a'):
            text = j.select_one(f'span#_filtered_ment_{count} > a').text
        else:
            text = j.select_one(f'span#_filtered_ment_{count}').text
        count += 1

        reviews.append({
            'code': i['code'],
            'star': j.select_one('div.star_score > em').text,
            'text': text.strip()
        })


# 출력 여부
#
if True:
    for i in reviews:
        print(f'({i["star"]})\t{i["text"]}')


# 파일 저장
#
if False:
    path = './data/'
    if not os.path.exists(path):
        os.mkdir(path)

    for x, y, z in zip(
        ['movies.csv', 'reviews.csv'],
        [['title', 'code'], ['code', 'star', 'text']],
        [movies, reviews]
    ):
        
        f = open(path+x, 'w', newline='', encoding='utf-8-sig')
        r = csv.DictWriter(f, fieldnames=y)
        r.writeheader()

        for i in z:
            r.writerow(i)
        f.close()