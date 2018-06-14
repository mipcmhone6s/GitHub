# -*- coding: cp949 -*-
from urllib.request import urlopen
from xml.dom.minidom import parse, parseString #minidom �Ľ��Լ� ����Ʈ
import xml.etree.ElementTree as elemTree

u = urlopen('http://api.visitkorea.or.kr/openapi/service/rest/KorService/areaBasedList?serviceKey=OPt4yOPTFT%2FkIL2tnYeHbROYLt3tlvJBB%2BjgIZgt0d%2FNEqLMQz%2BPJQqP7srCQwZZfXcnekixqhCrWiq7X22E1w%3D%3D&pageNo=1&startPage=1&numOfRows=100&pageSize=100&MobileApp=AppTest&MobileOS=ETC&arrange=A&contentTypeId=12&listYN=Y')
tree = parse(u)


print(tree.toxml())
items = tree.childNodes
item = items[0].childNodes
for i in item:
    if i.nodeName == "item":  # ������Ʈ�� �� book�� ���� ��� ���ϴ�.
        subitems = i.childNodes  # book�� ��� �ִ� ������ �����ɴϴ�.
        for atom in subitems:
            if atom.nodeName in ['title',]:
                print("title=", atom.firstChild.nodeValue)  # å ����� ��� �մϴ�.
