from tkinter import *
from tkinter import font
import tkinter.messagebox
import folium

window = Tk()

SearchString = ""
SearchEntry = None
SearchListBox1 = None
SearchListBox2 = None
SearchTextBox1 = None
SearchTextBox2 = None
SearchTextBox3 = None

RememberAreaCode = -1
RememberContentCode = -1
RememberSubAreaCode = -1
RememberMapx = -1
RememberMapy = -1
RememberTitle = ""
def FindinMap():
    global RememberMapx, RememberMapy, RememberTitle
    RememberMapx = float(RememberMapx)
    RememberMapy = float(RememberMapy)
    # 위도 경도 지정
    map_osm = folium.Map(location=[RememberMapy, RememberMapx], zoom_start=17)
    # 마커 지정
    folium.Marker([RememberMapy, RememberMapx], popup=RememberTitle).add_to(map_osm)
    # html 파일로 저장
    map_osm.save(RememberTitle + '.html')

def InitHeadLine():
    HeadLineFont = font.Font(window, size=20, weight='bold')
    HeadLine = Label(window, font = HeadLineFont, text="국문 관광정보 서비스 App")
    HeadLine.grid(row = 0, column = 0)

def InitLabels():
    l1 = Label(window, text="지역")
    l2 = Label(window, text="시군구")
    l1.pack()
    l2.pack()

def InitSearchEntry():
    global SearchEntry

    SearchEntry = Entry(window)
    SearchEntry.grid(row = 1, column = 0)

def InitSearchButton():
    SearchButton = Button(window, text = "검색" ,  command = SearchButtonAction)
    SearchButton.place(x = 455, y = 35)

    SearchButton = Button(window, text="검색", command=SearchButtonAction1)
    SearchButton.grid(row = 4, column = 3)

    SearchButton = Button(window, text="검색", command=SearchButtonAction2)
    SearchButton.grid(row=5, column=3)

def InitSearchText():
    global SearchTextBox1, SearchTextBox2

    SearchTextScrollbar1 = Scrollbar(window)
    SearchTextScrollbar1.grid(row=4, column=1)

    SearchTextBox1 = Text(window, width=80, height=10, borderwidth=7, relief='ridge', yscrollcommand=SearchTextScrollbar1.set)
    SearchTextBox1.grid(row = 4, column = 0)

    SearchTextScrollbar2 = Scrollbar(window)
    SearchTextScrollbar2.grid(row=5, column=1)

    SearchTextBox2 = Text(window, width=80, height=10, borderwidth=7, relief='ridge', yscrollcommand=SearchTextScrollbar2.set)
    SearchTextBox2.grid(row=5, column = 0 )

def SearchButtonAction1():
    import http.client
    from xml.dom.minidom import parse, parseString
    global SearchListBox1, SearchString, SearchTextBox1, RememberAreaCode, RememberContentCode, RememberSubAreaCode, RememberMapx, RememberMapy, RememberTitle

    SearchTextBox1.configure(state='normal')
    SearchTextBox1.delete(0.0, END)

    RememberSubAreaCode = SearchListBox1.curselection()[0] + 1

    conn = http.client.HTTPConnection("api.visitkorea.or.kr")
    conn.request("GET",
                 "/openapi/service/rest/KorService/areaBasedList?serviceKey=uAZ4kkFChL5d%2FLnSAxDGp6wkFCgE%2BovQ6W%2FC8gk5%2FA2%2BxhIRSXALj%2FV3SppGEippCgUluNCQ9mT9XdkQXbO1jg%3D%3D&pageNo=1&startPage=1&numOfRows=100&pageSize=100&MobileApp=AppTest&MobileOS=ETC&arrange=A&contentTypeId=" + str(RememberContentCode) + "&areaCode=" + RememberAreaCode + "&sigunguCode=" + str(RememberSubAreaCode) + "&listYN=Y")
    req = conn.getresponse()

    if req.status == 200:
        BooksDoc = req.read().decode('utf-8')
        if BooksDoc == None:
            print("에러")
        else:
            parseData = parseString(BooksDoc)
            GeoInfoLibrary = parseData.childNodes
            AreaData = GeoInfoLibrary[0].childNodes[1].childNodes[0].childNodes
            cnt = 0
            for item in AreaData:
                cnt += 1
                nTitle = 0
                nTel = 0
                nAddr2 = 0
                nMapx = 0
                nMapy = 0
                lengthofChildNodes = len(item.childNodes)

                while nTitle < lengthofChildNodes:
                    if item.childNodes[nTitle].nodeName == 'title':
                        break
                    nTitle += 1
                while nTel < lengthofChildNodes:
                    if item.childNodes[nTel].nodeName == 'tel':
                        break
                    nTel += 1
                while nAddr2 < lengthofChildNodes:
                    if item.childNodes[nAddr2].nodeName == 'addr2':
                        break
                    nAddr2 += 1
                while nMapx < lengthofChildNodes:
                    if item.childNodes[nMapx].nodeName == 'mapx':
                        break
                    nMapx += 1
                while nMapy < lengthofChildNodes:
                    if item.childNodes[nMapy].nodeName == 'mapy':
                        break
                    nMapy += 1

                SearchTextBox1.insert(INSERT, "[")
                SearchTextBox1.insert(INSERT, cnt)
                SearchTextBox1.insert(INSERT, "] ")
                SearchTextBox1.insert(INSERT, '명칭 : ')
                SearchTextBox1.insert(INSERT, item.childNodes[nTitle].childNodes[0].nodeValue) #이름
                SearchTextBox1.insert(INSERT, '\n')
                SearchTextBox1.insert(INSERT, '주소 : ')
                SearchTextBox1.insert(INSERT, item.childNodes[0].childNodes[0].nodeValue) #주소1
                SearchTextBox1.insert(INSERT, '\n')
                SearchTextBox1.insert(INSERT, '상세 : ')

                if nAddr2 < lengthofChildNodes :
                    SearchTextBox1.insert(INSERT, item.childNodes[nAddr2].childNodes[0].nodeValue) #주소2
                else:
                    SearchTextBox1.insert(INSERT, '-')

                SearchTextBox1.insert(INSERT, '\n')
                SearchTextBox1.insert(INSERT, '전화번호 : ')

                if nTel < lengthofChildNodes :
                    SearchTextBox1.insert(INSERT, item.childNodes[nTel].childNodes[0].nodeValue) #전화번호
                else :
                    SearchTextBox1.insert(INSERT, '-')

                SearchTextBox1.insert(INSERT, '\n')
                SearchTextBox1.insert(INSERT, '\n')
                #지도----------------------------------------
                RememberTitle = item.childNodes[nTitle].childNodes[0].nodeValue
                RememberMapx = item.childNodes[nMapx].childNodes[0].nodeValue
                RememberMapy = item.childNodes[nMapy].childNodes[0].nodeValue
                FindinMap()

def SearchButtonAction2():
    import http.client
    from xml.dom.minidom import parse, parseString
    global SearchListBox2, SearchString, SearchTextBox2, RememberAreaCode, RememberContentCode, RememberSubAreaCode, RememberMapx, RememberMapy, RememberTitle

    SearchTextBox2.configure(state='normal')
    SearchTextBox2.delete(0.0, END)

    if SearchListBox2.curselection()[0] == 0:
        RememberContentCode = 12
    elif SearchListBox2.curselection()[0] == 1:
        RememberContentCode = 14
    elif SearchListBox2.curselection()[0] == 2:
        RememberContentCode = 15
    elif SearchListBox2.curselection()[0] == 3:
        RememberContentCode = 25
    elif SearchListBox2.curselection()[0] == 4:
        RememberContentCode = 28
    elif SearchListBox2.curselection()[0] == 5:
        RememberContentCode = 32
    elif SearchListBox2.curselection()[0] == 6:
        RememberContentCode = 38
    elif SearchListBox2.curselection()[0] == 7:
        RememberContentCode = 39

    conn = http.client.HTTPConnection("api.visitkorea.or.kr")
    conn.request("GET",
                 "/openapi/service/rest/KorService/areaBasedList?serviceKey=uAZ4kkFChL5d%2FLnSAxDGp6wkFCgE%2BovQ6W%2FC8gk5%2FA2%2BxhIRSXALj%2FV3SppGEippCgUluNCQ9mT9XdkQXbO1jg%3D%3D&pageNo=1&startPage=1&numOfRows=100&pageSize=100&MobileApp=AppTest&MobileOS=ETC&arrange=A&contentTypeId=" + str(
                     RememberContentCode) + "&areaCode=" + RememberAreaCode + "&sigunguCode=" + str(
                     RememberSubAreaCode) + "&listYN=Y")
    req = conn.getresponse()

    if req.status == 200:
        BooksDoc = req.read().decode('utf-8')
        if BooksDoc == None:
            print("에러")
        else:
            parseData = parseString(BooksDoc)
            GeoInfoLibrary = parseData.childNodes
            AreaData = GeoInfoLibrary[0].childNodes[1].childNodes[0].childNodes
            cnt = 0
            for item in AreaData:
                cnt += 1
                nTitle = 0
                nTel = 0
                nAddr2 = 0
                nMapx = 0
                nMapy = 0
                lengthofChildNodes = len(item.childNodes)

                while nTitle < lengthofChildNodes:
                    if item.childNodes[nTitle].nodeName == 'title':
                        break
                    nTitle += 1

                while nTel < lengthofChildNodes:
                    if item.childNodes[nTel].nodeName == 'tel':
                        break
                    nTel += 1

                while nAddr2 < lengthofChildNodes:
                    if item.childNodes[nAddr2].nodeName == 'addr2':
                        break
                    nAddr2 += 1
                while nMapx < lengthofChildNodes:
                    if item.childNodes[nMapx].nodeName == 'mapx':
                        break
                    nMapx += 1
                while nMapy < lengthofChildNodes:
                    if item.childNodes[nMapy].nodeName == 'mapy':
                        break
                    nMapy += 1

                SearchTextBox2.insert(INSERT, "[")
                SearchTextBox2.insert(INSERT, cnt)
                SearchTextBox2.insert(INSERT, "] ")
                SearchTextBox2.insert(INSERT, '명칭 : ')
                SearchTextBox2.insert(INSERT, item.childNodes[nTitle].childNodes[0].nodeValue)  # 이름
                SearchTextBox2.insert(INSERT, '\n')
                SearchTextBox2.insert(INSERT, '주소 : ')
                SearchTextBox2.insert(INSERT, item.childNodes[0].childNodes[0].nodeValue)  # 주소1
                SearchTextBox2.insert(INSERT, '\n')
                SearchTextBox2.insert(INSERT, '상세 : ')

                if nAddr2 < lengthofChildNodes:
                    SearchTextBox2.insert(INSERT, item.childNodes[nAddr2].childNodes[0].nodeValue)  # 주소2
                else:
                    SearchTextBox2.insert(INSERT, '-')

                SearchTextBox2.insert(INSERT, '\n')
                SearchTextBox2.insert(INSERT, '전화번호 : ')

                if nTel < lengthofChildNodes:
                    SearchTextBox2.insert(INSERT, item.childNodes[nTel].childNodes[0].nodeValue)  # 전화번호
                else:
                    SearchTextBox2.insert(INSERT, '-')

                SearchTextBox2.insert(INSERT, '\n')
                SearchTextBox2.insert(INSERT, '\n')
                #지도----------------------------------------
                RememberTitle = item.childNodes[nTitle].childNodes[0].nodeValue
                RememberMapx = item.childNodes[nMapx].childNodes[0].nodeValue
                RememberMapy = item.childNodes[nMapy].childNodes[0].nodeValue
                FindinMap()

def SearchButtonAction():
    global SearchEntry, SearchString, RememberAreaCode, SearchListBox2, RememberContentCode
    import http.client
    from xml.dom.minidom import parse, parseString

    SearchString = SearchEntry.get()

    if SearchListBox2.curselection()[0] == 0:
        RememberContentCode = 12
    elif SearchListBox2.curselection()[0] == 1:
        RememberContentCode = 14
    elif SearchListBox2.curselection()[0] == 2:
        RememberContentCode = 15
    elif SearchListBox2.curselection()[0] == 3:
        RememberContentCode = 25
    elif SearchListBox2.curselection()[0] == 4:
        RememberContentCode = 28
    elif SearchListBox2.curselection()[0] == 5:
        RememberContentCode = 32
    elif SearchListBox2.curselection()[0] == 6:
        RememberContentCode = 38
    elif SearchListBox2.curselection()[0] == 7:
        RememberContentCode = 39

    conn = http.client.HTTPConnection("api.visitkorea.or.kr")
    conn.request("GET",
                 "/openapi/service/rest/KorService/areaCode?serviceKey=uAZ4kkFChL5d%2FLnSAxDGp6wkFCgE%2BovQ6W%2FC8gk5%2FA2%2BxhIRSXALj%2FV3SppGEippCgUluNCQ9mT9XdkQXbO1jg%3D%3D&numOfRows=17&pageSize=17&pageNo=1&startPage=1&MobileOS=ETC&MobileApp=AppTest")
    req = conn.getresponse()

    ListData = []

    if req.status == 200:
        BooksDoc = req.read().decode('utf-8')
        if BooksDoc == None:
            print("에러")
        else:
            parseData = parseString(BooksDoc)
            GeoInfoLibrary = parseData.childNodes
            AreaData = GeoInfoLibrary[0].childNodes[1].childNodes[0].childNodes

            for item in AreaData:
                if item.childNodes[1].firstChild.nodeValue == SearchString:
                    RememberAreaCode = item.childNodes[0].childNodes[0].nodeValue
                    break

    if not RememberAreaCode == -1:
        SetSearchListBox()

def InitSearchListBox():
    global SearchListBox1, SearchListBox2
    ListBoxScrollbar = Scrollbar(window)
    ListBoxScrollbar.place(x = 395, y = 62)

    TempFont = font.Font(window, size=15, weight='bold', family='Consolas')
    SearchListBox1 = Listbox(window, font=TempFont, activestyle='none',
                            width=15, height=1, borderwidth=7, relief='ridge',
                            yscrollcommand=ListBoxScrollbar.set)

    SearchListBox1.grid(row = 2,column = 0)
    ListBoxScrollbar.config(command=SearchListBox1.yview)

    #---구분선

    ListBoxScrollbar = Scrollbar(window)
    ListBoxScrollbar.grid(row=2, column=3)

    TempFont = font.Font(window, size=15, weight='bold', family='Consolas')
    SearchListBox2 = Listbox(window, font=TempFont, activestyle='none',
                            width=15, height=1, borderwidth=7, relief='ridge',
                            yscrollcommand=ListBoxScrollbar.set)

    SearchListBox2.insert(1, "관광지")
    SearchListBox2.insert(2, "문화시설")
    SearchListBox2.insert(3, "축제/행사/공연")
    SearchListBox2.insert(4, "여행코스")
    SearchListBox2.insert(5, "레포츠")
    SearchListBox2.insert(6, "숙박")
    SearchListBox2.insert(7, "쇼핑")
    SearchListBox2.insert(8, "음식점")

    SearchListBox2.grid(row=2, column=2)
    ListBoxScrollbar.config(command=SearchListBox2.yview)

def SetSearchListBox():
    import http.client
    from xml.dom.minidom import parse, parseString
    global SearchString, SearchListBox1

    conn = http.client.HTTPConnection("api.visitkorea.or.kr")
    conn.request("GET", "/openapi/service/rest/KorService/areaCode?serviceKey=uAZ4kkFChL5d%2FLnSAxDGp6wkFCgE%2BovQ6W%2FC8gk5%2FA2%2BxhIRSXALj%2FV3SppGEippCgUluNCQ9mT9XdkQXbO1jg%3D%3D&numOfRows=25&pageSize=25&pageNo=1&startPage=1&MobileOS=ETC&MobileApp=AppTest&areaCode=" + str(RememberAreaCode))
    req = conn.getresponse()

    ListData = []

    if req.status == 200:
        BooksDoc = req.read().decode('utf-8')
        if BooksDoc == None:
            print("에러")
        else:
            parseData = parseString(BooksDoc)
            GeoInfoLibrary = parseData.childNodes
            AreaData = GeoInfoLibrary[0].childNodes[1].childNodes[0].childNodes

            for item in AreaData:
                subitems = item.childNodes[1]
                ListData.append(subitems.firstChild.nodeValue)

    ListBoxScrollbar = Scrollbar(window)
    ListBoxScrollbar.place(x=395, y=62)

    TempFont = font.Font(window, size=15, weight='bold', family='Consolas')
    SearchListBox1 = Listbox(window, font=TempFont, activestyle='none',
                            width=15, height=1, borderwidth=7, relief='ridge',
                            yscrollcommand=ListBoxScrollbar.set)

    for i in range(len(ListData)):
        SearchListBox1.insert(i, ListData[i])

    SearchListBox1.grid(row = 2,column = 0)
    ListBoxScrollbar.config(command=SearchListBox1.yview)

InitHeadLine()
InitSearchEntry()
InitSearchButton()
InitSearchListBox()
InitSearchText()

window.mainloop()