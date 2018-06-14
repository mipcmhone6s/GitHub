# -*- coding: cp949 -*-
from urllib.request import urlopen
from xml.dom.minidom import parse, parseString #minidom 파싱함수 임포트
import xml.etree.ElementTree as elemTree

u = urlopen('http://api.visitkorea.or.kr/openapi/service/rest/KorService/areaBasedList?serviceKey=OPt4yOPTFT%2FkIL2tnYeHbROYLt3tlvJBB%2BjgIZgt0d%2FNEqLMQz%2BPJQqP7srCQwZZfXcnekixqhCrWiq7X22E1w%3D%3D&pageNo=1&startPage=1&numOfRows=100&pageSize=100&MobileApp=AppTest&MobileOS=ETC&arrange=A&contentTypeId=12&listYN=Y')
tree = parse(u)


print(tree.toxml())
items = tree.childNodes
item = items[0].childNodes
for i in item:
    if i.nodeName == "item":  # 엘리먼트를 중 book인 것을 골라 냅니다.
        subitems = i.childNodes  # book에 들어 있는 노드들을 가져옵니다.
        for atom in subitems:
            if atom.nodeName in ['title',]:
                print("title=", atom.firstChild.nodeValue)  # 책 목록을 출력 합니다.
