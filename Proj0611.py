from tkinter import *
from tkinter import font
import tkinter.messagebox
import folium
from email.mime.text import MIMEText

window = Tk()
window.title("국문관광정보 프로그램 by 희동민")
window.geometry('1200x600+0+0')

SearchString = ""
SearchEntry1 = None #상위지역 검색
SearchEntry2 = None #이메일
SearchEntry3 = None #키워드(사진) 검색
SearchListBox1 = None
SearchListBox2 = None
SearchTextBox1 = None
SearchTextBox2 = None
SearchTextBox3 = None
SearchComboBox = None
PrintEmailDataString = ""

RememberAreaCode = -1
RememberContentCode = -1
RememberSubAreaCode = -1
RememberMapx = -1
RememberMapy = -1
RememberTitle = ""
RememberImageArr = []
RememberImage = None
def NoPic():
    from io import BytesIO
    import urllib
    import urllib.request
    from PIL import Image, ImageTk

    # openapi로 이미지 url을 가져옴.
    url = 'http://www.belimoseoul.com/data/3/44e7b453a54068b6ceab684322cdd5d5.jpg'
    with urllib.request.urlopen(url) as u:
        raw_data = u.read()

    im = Image.open(BytesIO(raw_data))
    image = ImageTk.PhotoImage(im)

    label = Label(window, image=image, height=300, width=500)
    label.place(x=650, y=20)
    window.mainloop()

def StickPic():
    global RememberImage
    from io import BytesIO
    import urllib
    import urllib.request
    from PIL import Image, ImageTk

    # openapi로 이미지 url을 가져옴.
    url = RememberImage
    with urllib.request.urlopen(url) as u:
        raw_data = u.read()

    im = Image.open(BytesIO(raw_data))
    image = ImageTk.PhotoImage(im)

    label = Label(window, image=image, height=300, width=500)
    label.place(x=650, y=20)
    window.mainloop()
def StickMap():
    global RememberImage, RememberTitle
    from io import BytesIO
    import urllib
    import urllib.request
    from PIL import Image, ImageTk

    # openapi로 이미지 url을 가져옴.
    url = 'file:///D:/pythonProject/TermProject/' + '강남' + '.html'
    with urllib.request.urlopen(url) as u:
        raw_data = u.read()

    im = Image.open(BytesIO(raw_data))
    image = ImageTk.PhotoImage(im)

    label = Label(window, image=image, height=300, width=500)
    label.place(x=650, y=550)
    window.mainloop()
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
    l1 = Label(window, text="상위지역")
    l2 = Label(window, text="하위지역")
    l3 = Label(window, text = "E-Mail")
    l4 = Label(window, text = "Contents Type")
    l5 = Label(window, text = "사진 검색")

    l1.place(x = 10, y = 40)
    l2.place(x = 10, y = 75)
    l3.place(x = 10 , y = 150)
    l4.place(x = 350, y = 40)
    l5.place(x = 350, y = 75)

def InitSearchEntry():
    global SearchEntry1, SearchEntry2, SearchEntry3

    SearchEntry1 = Entry(window)
    SearchEntry1.place(x = 100, y = 40)

    SearchEntry2 = Entry(window, width = 30)
    SearchEntry2.place(x = 100, y = 150)

    SearchEntry3 = Entry(window, width = 23)
    SearchEntry3.place(x=450, y=75)


def InitSearchButton():
    SearchButton = Button(window, text = "상위지역 + 콘텐츠1" ,  command = SearchButtonAction)
    SearchButton.place(x = 300, y = 180)

    SearchButton = Button(window, text="하위지역 + 텍스트1", command=SearchButtonAction1)
    SearchButton.place(x = 300, y = 220)

    SearchButton = Button(window, text="콘텐츠2 + 텍스트2", command=SearchButtonAction2)
    SearchButton.place( x = 450, y = 180)

    SearchButton = Button(window, text="이메일 보내기", command=SearchButtonAction3)
    SearchButton.place(x = 450, y = 220)

    SearchButton = Button(window, text="키워드 검색(사진)", command=SearchButtonAction4)
    SearchButton.place(x=450, y=140)

def InitSearchText():
    global SearchTextBox1, SearchTextBox2

    SearchTextScrollbar1 = Scrollbar(window)
    SearchTextScrollbar1.place(x = 580 , y = 300)

    SearchTextBox1 = Text(window, width=80, height=10, borderwidth=7, relief='ridge', yscrollcommand=SearchTextScrollbar1.set)
    SearchTextBox1.place(x = 0 , y = 250)

    SearchTextScrollbar2 = Scrollbar(window)
    SearchTextScrollbar2.place(x=580, y=450)

    SearchTextBox2 = Text(window, width=80, height=10, borderwidth=7, relief='ridge', yscrollcommand=SearchTextScrollbar2.set)
    SearchTextBox2.place(x=0, y=400)

def SearchButtonAction1():
    import http.client
    from xml.dom.minidom import parse, parseString
    global SearchListBox1, SearchString, SearchTextBox1, RememberAreaCode, RememberContentCode, RememberSubAreaCode, RememberMapx, RememberMapy, RememberTitle, RememberImage
    global PrintEmailDataString

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
                nImage = 0
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
                while nImage < lengthofChildNodes:
                    if item.childNodes[nImage].nodeName == 'firstimage':
                        break
                    nImage += 1

                PrintEmailDataString += "[" + str(cnt) + "]" + "명칭 : " + str(item.childNodes[nTitle].childNodes[0].nodeValue) + "\n"
                PrintEmailDataString += "주소 : " + item.childNodes[0].childNodes[0].nodeValue + "\n"

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
                    PrintEmailDataString += "상세 : " + item.childNodes[nAddr2].childNodes[0].nodeValue + "\n"
                else:
                    SearchTextBox1.insert(INSERT, '-')
                    PrintEmailDataString += "상세 : " + "-" + "\n"

                SearchTextBox1.insert(INSERT, '\n')
                SearchTextBox1.insert(INSERT, '전화번호 : ')
                PrintEmailDataString += "전화번호 : "

                if nTel < lengthofChildNodes :
                    SearchTextBox1.insert(INSERT, item.childNodes[nTel].childNodes[0].nodeValue) #전화번호
                    PrintEmailDataString += item.childNodes[nTel].childNodes[0].nodeValue + "\n\n\n"
                else :
                    SearchTextBox1.insert(INSERT, '-')
                    PrintEmailDataString += "-" + "\n\n\n"

                SearchTextBox1.insert(INSERT, '\n')
                SearchTextBox1.insert(INSERT, '\n')
                #지도----------------------------------------
                if nMapx < lengthofChildNodes - 1:
                    RememberTitle = item.childNodes[nTitle].childNodes[0].nodeValue
                    RememberMapx = item.childNodes[nMapx].childNodes[0].nodeValue
                    RememberMapy = item.childNodes[nMapy].childNodes[0].nodeValue
                    FindinMap()
                #사진----------------------------------------
                if nImage < lengthofChildNodes - 1:
                    RememberImageArr.append(item.childNodes[nImage].childNodes[0].nodeValue)
                else:
                    RememberImageArr.append(-1)

def SearchButtonAction2():
    import http.client
    from xml.dom.minidom import parse, parseString
    global SearchString, SearchTextBox2, RememberAreaCode, RememberContentCode, RememberSubAreaCode, RememberMapx, RememberMapy, RememberTitle
    global PrintEmailDataString, SearchComboBox


    if SearchComboBox.current() == 0:
        RememberContentCode = 12
    elif SearchComboBox.current() == 1:
        RememberContentCode = 14
    elif SearchComboBox.current() == 2:
        RememberContentCode = 15
    elif SearchComboBox.current() == 3:
        RememberContentCode = 25
    elif SearchComboBox.current() == 4:
        RememberContentCode = 28
    elif SearchComboBox.current() == 5:
        RememberContentCode = 32
    elif SearchComboBox.current() == 6:
        RememberContentCode = 38
    elif SearchComboBox.current() == 7:
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

            PrintEmailDataString += "==============================구분===============================\n\n"

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

                PrintEmailDataString += "[" + str(cnt) + "]" + "명칭 : " + str(
                    item.childNodes[nTitle].childNodes[0].nodeValue) + "\n"
                PrintEmailDataString += "주소 : " + item.childNodes[0].childNodes[0].nodeValue + "\n"

                if nAddr2 < lengthofChildNodes:
                    SearchTextBox2.insert(INSERT, item.childNodes[nAddr2].childNodes[0].nodeValue)  # 주소2
                    PrintEmailDataString += "상세 : " + item.childNodes[nAddr2].childNodes[0].nodeValue + "\n"
                else:
                    SearchTextBox2.insert(INSERT, '-')
                    PrintEmailDataString += "상세 : " + "-" + "\n"

                SearchTextBox2.insert(INSERT, '\n')
                SearchTextBox2.insert(INSERT, '전화번호 : ')
                PrintEmailDataString += "전화번호 : "

                if nTel < lengthofChildNodes:
                    SearchTextBox2.insert(INSERT, item.childNodes[nTel].childNodes[0].nodeValue)  # 전화번호
                    PrintEmailDataString += "전화번호 : " + item.childNodes[nTel].childNodes[0].nodeValue + "\n\n\n"
                else:
                    SearchTextBox2.insert(INSERT, '-')
                    PrintEmailDataString += "전화번호 : " + "-" + "\n\n\n"

                SearchTextBox2.insert(INSERT, '\n')
                SearchTextBox2.insert(INSERT, '\n')
                #지도----------------------------------------
                RememberTitle = item.childNodes[nTitle].childNodes[0].nodeValue
                RememberMapx = item.childNodes[nMapx].childNodes[0].nodeValue
                RememberMapy = item.childNodes[nMapy].childNodes[0].nodeValue
                FindinMap()

def SearchButtonAction3():
    import smtplib
    from email.mime.text import MIMEText

    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.ehlo()  # say Hello
    smtp.starttls()  # TLS 사용시 필요
    smtp.login('hidong801@gmail.com', 'tmzmflqxmdjsdj!')

    msg = MIMEText(PrintEmailDataString)
    msg['Subject'] = '국문관광정보'
    msg['To'] = 'all_family@naver.com'
    smtp.sendmail('hidong801@gmail.com', 'all_family@naver.com', msg.as_string())

    smtp.quit()

def SearchButtonAction4(): #사진
    global RememberImageArr, RememberImage, SearchString, SearchEntry3
    SearchString = SearchEntry3.get()
    RememberImage = RememberImageArr[int(SearchString) - 1]
    if RememberImage != -1:
        StickPic()
        StickMap()
    else :
        NoPic()

def SearchButtonAction():
    global SearchEntry1, SearchString, RememberAreaCode, RememberContentCode, SearchComboBox
    import http.client
    from xml.dom.minidom import parse, parseString

    SearchString = SearchEntry1.get()

    if SearchComboBox.current() == 0:
        RememberContentCode = 12
    elif SearchComboBox.current() == 1:
        RememberContentCode = 14
    elif SearchComboBox.current() == 2:
        RememberContentCode = 15
    elif SearchComboBox.current() == 3:
        RememberContentCode = 25
    elif SearchComboBox.current() == 4:
        RememberContentCode = 28
    elif SearchComboBox.current() == 5:
        RememberContentCode = 32
    elif SearchComboBox.current() == 6:
        RememberContentCode = 38
    elif SearchComboBox.current() == 7:
        RememberContentCode = 39

    conn = http.client.HTTPConnection("api.visitkorea.or.kr")
    conn.request("GET",
                 "/openapi/service/rest/KorService/areaCode?serviceKey=uAZ4kkFChL5d%2FLnSAxDGp6wkFCgE%2BovQ6W%2FC8gk5%2FA2%2BxhIRSXALj%2FV3SppGEippCgUluNCQ9mT9XdkQXbO1jg%3D%3D&numOfRows=17&pageSize=17&pageNo=1&startPage=1&MobileOS=ETC&MobileApp=AppTest")
    req = conn.getresponse()

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
    ListBoxScrollbar.place(x = 280, y = 70)

    TempFont = font.Font(window, size=15, weight='bold', family='Consolas')
    SearchListBox1 = Listbox(window, font=TempFont, activestyle='none',
                            width=15, height=1, borderwidth=7, relief='ridge',
                            yscrollcommand=ListBoxScrollbar.set)

    SearchListBox1.place( x = 95, y = 75)
    ListBoxScrollbar.config(command=SearchListBox1.yview)

def InitComboBox():
    from tkinter import ttk
    global SearchComboBox
    str = StringVar()

    SearchComboBox = ttk.Combobox(window, width=20, textvariable=str)
    SearchComboBox['values'] = ('관광지', '문화시설', '축제/행사/공연', '여행코스', '레포츠', '숙박', '쇼핑', '음식점')
    SearchComboBox.place(x = 450, y = 38)
    SearchComboBox.current(0)

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
    ListBoxScrollbar.place(x=280, y=70)

    TempFont = font.Font(window, size=15, weight='bold', family='Consolas')
    SearchListBox1 = Listbox(window, font=TempFont, activestyle='none',
                            width=15, height=1, borderwidth=7, relief='ridge',
                            yscrollcommand=ListBoxScrollbar.set)

    for i in range(len(ListData)):
        SearchListBox1.insert(i, ListData[i])

    SearchListBox1.place(x=95, y=75)
    ListBoxScrollbar.config(command=SearchListBox1.yview)

InitHeadLine()
InitLabels()
InitSearchEntry()
InitComboBox()
InitSearchButton()
InitSearchListBox()
InitSearchText()

window.mainloop()