'''
    이 소스는 discord bot에서 활용하기 위한 목적으로 만드는 소스임.
    그렇기 때문에 아직 소스코드가 전부 완성된것은 아님.
    
    이 소스코드의 목적은 아래와 같음.
    
    1. 부위별 옵션에 대한 확률값과 그에 대한 수치값 범위를 지정
    2. 해당 부위에서 특정옵션에 대한 중복값이 나오면 안되기 때문에 해당 데이터에 대한 연산/csv값에 등록
    
    --21.05.15. 현재까지 진행상황
    1. 부위별 옵션에 대한 확률값과 그에 대한 수치값 범위를 지정/저장
    
    --해야할일 : 
      모든 스킬레벨 증가
      피격 후 무적시간 증가
      이 2번째 3번째 줄에서 예외확률 추가 및 예외확률에 대한 %값을 각각 범위로 지정한 데이터 생성

      몬스터 방어율 무시 +%
      피격 시 일정 확률로 데미지 % 무시
      피격 시 일정 확률로 일정 시간 무적
      보스 몬스터 공격 시 데미지 +%
      아이템 드롭률 +%
      이 1,2번째 줄에서 나왔을 때 3번째 줄에서 예외확률 추가 및 예외확률이 빠진만큼 다른 확률값에 각각 소분해서 더한값을 데이터로 생성
      
'''

import csv
import re
import requests

from urllib.request import urlopen
from bs4 import BeautifulSoup

# 링크에 크롤링 할 데이터 링크를 list형식으로 쑤셔박기
link = ['https://maplestory.nexon.com/Guide/OtherProbability/cube/red','https://maplestory.nexon.com/Guide/OtherProbability/cube/black','https://maplestory.nexon.com/Guide/OtherProbability/cube/addi']

# 크롤링해오는 데이터에서 레어/에픽/유니크/레전드리를 1,2,3,4 으로 분류
spec = ['rare','epic','uniq','regend']
# 구분
specrun = 0
specnum = 0
# 아이템분류
item = ['wp','emblem','subwp','subwpadv','shield','hat','top','overall','bottom','shoes','glove','cape','belt','shoulder','face','eyes','earing','ring','neck','heart']
for hr in link: #for문 : hr에 list(link)데이터를 하나씩 넣고 구동
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
    
    #아이템에 따라 반복
    for t in item:     
        # 테이블 specrun : specrun+4만큼 불러옴.
        for i in table[specrun:(specrun+4)]:
            print(t,spec[specnum])
            f = open('cubedata/{0}_{1}_{2}.csv'.format(name,t,spec[specnum]),'w',encoding='utf-8',newline='')
            # csv 첫줄 생성
            f.write('첫옵션'+','+'첫확률'+','+'첫확률시작'+','+'첫확률끝'+','+'둘옵션'+','+'둘확률'+','+'둘시작'+','+'둘확률끝'+','+'셋옵션'+','+'셋확률'+','+'셋확률시작'+','+'셋확률끝'+'\n')
            # 크롤링 데이터 가공 시작
            tr = i.find_all('tr')

            fprs = 1 #확률시작
            fpre = 1 #확률끝
            sprs = 1 #확률시작
            spre = 1 #확률끝
            tprs = 1 #확률시작
            tpre = 1 #확률끝
            for data in tr[1:]: #첫줄을 제외한 데이터 불러오기. 첫줄은 위에 적어둔 분류가 적혀있으니 제외함.
                td = data.find_all('td')
                fst = td[0].string #첫줄옵션
                fpr = td[1].string #첫줄확률
                sst = td[2].string #가운데옵션
                spr = td[3].string #가운데확률
                tst = td[4].string #끝옵션
                tpr = td[5].string #끝확률

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
                if fpr == "0":
                    fpre = 999999999999
                else:
                    fpre +=int(fpr)
                if spr == "0":
                    spre = 999999999999
                else:
                    spre +=int(spr)
                if tpr == "0":
                    tpre = 999999999999
                else:
                    tpre +=int(tpr)
                f.write(fst+','+fpr+','+str(fprs)+','+str(fpre)+','+sst+','+spr+','+str(sprs)+','+str(spre)+','+tst+','+tpr+','+str(tprs)+','+str(tpre)+'\n')
                if fpr == "0":
                    fprs = 999999999999
                else:
                    fprs +=int(fpre)
                if spr == "0":
                    sprs = 999999999999
                else:
                    sprs +=int(spre)
                if tpr == "0":
                    tprs = 999999999999
                else:
                    tprs +=int(tpre)
            f.close()
            specnum+=1
        specnum = 0
        specrun+=4
    specrun = 0
