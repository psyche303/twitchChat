import threading, requests, time
from tkinter import *
from tkinter import StringVar
from bs4 import BeautifulSoup
from selenium import webdriver


class HtmlGetter (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        def timeStamp():
            # 현재 시각 출력
            now = time.localtime()
            printNow = "%04d-%02d-%02d %02d:%02d:%02d" % (
                now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
            return printNow

        def startT():
            print("OK Click")

            def crawl():
                # 채팅창 CSS
                print("crawl 실행 전")
                result = soup.find('div', {'class': 'tw-flex-grow-1 tw-full-height tw-pd-b-1'})
                return result

            # 구글드라이버
            options = webdriver.ChromeOptions();
            options.add_argument('headless')
            options.add_argument('window-size=1920x540')
            # 화면 사용여부
            # options.add_argument('disable-gpu')
            options.add_argument("--disable-popup-blocking")
            options.add_argument("settings.tts.speech_volume")

            # options.add_argument('--disable-gpu')

            # driver = webdriver.Chrome("C:\\Users\\Administrator\\Desktop\\test\\chromedriver.exe", chrome_options=options)
            global driver
            driver = webdriver.Chrome("./chromedriver", chrome_options=options)

            # 페이지 URL
            driver.get(e1.get())
            # 페이지 로딩까지 대기
            time.sleep(1)
            # 메시지 리스트 생성
            global mList
            mList = list()
            # 시간+메시지 리스트 생성
            global timeList
            timeList = list()

            # 수집시간
            # crawlTime = 30

            # for i in range(crawlTime):
            while True:
            # for i in range(30):
                # 페이지 elements 모두 가져오기
                html = driver.page_source
                timeS = timeStamp()
                # BeautifulSoup 사용
                soup = BeautifulSoup(html, "html.parser")
                global result2
                result2 = crawl()
                print(timeS)
                print(result2.getText())
                for n in result2:
                    # 삭제된 메시지면 원본유지
                    if "<메시지가 삭제되었습니다>" in n.getText():
                        continue
                    # 이미 등록된 메시지면 다음 줄로
                    elif n.getText() in mList:
                        continue
                    else:
                        # 메시지 리스트에 추가
                        mList.append(n.getText())

                        # 시간+메시지 리스트에 추가
                        timeList.append(timeS + " " + n.getText())

                        # 콘솔에 확인
                        print(timeList[-1])
                # 다음 1초 후 Element 읽어옴
                time.sleep(1)

        startT()

class Ender(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        def stop():
            print("Cancel Click")
            # 크롬 드라이버 종료
            driver.quit()
            # 파일 저장 경로
            path = "C:\\Users\\2-10\\Desktop\\크롤링테스트\\"
            # 파일 이름
            fileName = "data"
            # 파일 열기(W모드)
            writeText = open(path + fileName + ".txt", 'w', encoding="UTF-8")
            # 줄바꿈을 넣어서 리스트 단위로 작성, 저장
            writeText.writelines("\n".join(timeList))
            writeText.close()
        stop()




def startA():
    print("start clicked")
    t = HtmlGetter()
    t.start()

def stop():
    print("stop clicked")
    e = Ender()
    e.start()


window = Tk()
l1 = Label(window, text="방송 주소")
l1.grid(row=0, column=0)
e1 = Entry(window, width=50)
e1.grid(row=0, column=1)
str = StringVar()
b1 = Button(window, text="Start", command=startA)
b2 = Button(window, text="Stop", command=stop)
b1.grid(row=0, column=2)
b2.grid(row=0, column=3)

window.mainloop()


