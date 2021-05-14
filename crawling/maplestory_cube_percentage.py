import csv
import re
import requests

from urllib.request import urlopen
from bs4 import BeautifulSoup

# 링크에 크롤링 할 데이터 링크를 list형식으로 쑤셔박기
link = ['https://maplestory.nexon.com/Guide/OtherProbability/cube/red','https://maplestory.nexon.com/Guide/OtherProbability/cube/black','https://maplestory.nexon.com/Guide/OtherProbability/cube/addi']

# 크롤링해오는 데이터 중 분류를 레어/에픽/유니크/레전 으로 분류할수 있게 리스트 지정
spec = ['rare','epic','uniq','regend']
# 구분
specrun = 0
specnum = 0
# 아이템분류:무기/엠블렘/보조(포스실드,소울링제외/포스실드,소울링/방패/모자/상의/한벌/하의/신발/장갑/망토/벨트/견장/얼장/눈장/귀고리/반지/목걸이/기계심장 으로 분류
item = ['wp','emblem','subwp','subwpadv','shield','hat','top','overall','bottom','shoes','glove','cape','belt','shoulder','face','eyes','earing','ring','neck','heart']


#for문 : hr에 list(link)데이터를 하나씩 넣고 구동
for hr in link: 
    print(hr)
    if str(hr[-3:]) == "red":
        name="redcube"
    elif hr[-5:] == "black":
        name="blackcube"
    else:
        name="addicube"

    # url 크롤링 시작
    html = urlopen(hr)
    soup = BeautifulSoup(html,"html.parser")
    div = soup.find_all("div",{"class":"contents_wrap"})
    table = div[0].find_all("table",{"class":"cube_data"})
    
    # 아이템 리스트에 따라 반복문 진행
    for t in item:     
        # 테이블 specrun : specrun+4만큼 불러옴. 4개씩 불러오는 이유는 첫번째가 레어 두번째가 에픽 세번째가 유니크 네번째가 레전 관련 테이블이기때문에 테이블 작업을 4개씩 쪼갠다.
        for i in table[specrun:(specrun+4)]:
            # 콘솔상에서 정상적으로 작동하는지 확인하려고 임시로 넣은 print문. 실제 할때는 없애도 된다.
            print(t,spec[specnum])
            # csv파일 생성.
            f = open('cubedata/{0}_{1}_{2}.csv'.format(name,t,spec[specnum]),'w',encoding='utf-8',newline='')
            # csv 첫줄 생성
            f.write('fl'+','+'fp'+','+'sl'+','+'sp'+','+'tl'+','+'tp'+'\n')
            # 크롤링 데이터 가공 시작
            tr = i.find_all('tr')
            for data in tr[1:]: #첫줄을 제외한 데이터 불러오기. 첫줄은 위에 적어둔 분류가 적혀있으니 제외함.
                td = data.find_all('td')
                fst = td[0].string
                fpr = td[1].string
                sst = td[2].string
                spr = td[3].string
                tst = td[4].string
                tpr = td[5].string

                if fst is None: #fst값이 없으면(반환값이 None이면)
                    fst = "0"
                    fpr = "0"
                else: # 데이터가 있다면
                    fpr = fpr.replace("%","") # % 문자 지우기
                    fpr = fpr.replace(".","") # . 문자 지우기
                if sst is None:
                    sst = "0"
                    spr = "0"
                else:
                    spr = spr.replace("%","")
                    spr = spr.replace(".","")
                if tst is None:
                    tst = "0"
                    tpr = "0"
                else:
                    tpr = tpr.replace("%","")
                    tpr = tpr.replace(".","")
                f.write(fst+','+fpr+','+sst+','+spr+','+tst+','+tpr+'\n')
            f.close()
            #한번 반복했을때가 레어/ 그다음이 에픽/ 그다음이 유니크 그다음이 레전으로 맞춰줄수 있도록 specnum을 1번씩 더해준다.
            specnum+=1
        #위에 for문이 끝났기때문에 여기왔을때 이전에 있던 데이터로 인해 소스가 꼬이면 안되니 다시 한번 변수를 초기화
        specnum = 0
        # for data in tr[1:] 이 끝날때마다 specrun에 4씩 더해준다.
        specrun+=4
    # 사이트가 바뀌어 다시 검색하니 specrun을 0으로 초기화
    specrun = 0
