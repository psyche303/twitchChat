import threading, time
from tkinter import *
from tkinter import StringVar
from bs4 import BeautifulSoup
from selenium import webdriver
import os

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
            def crawl():
                # 채팅창 CSS
                print("crawl 실행 전")
                result = soup.find('div', {'class': 'tw-flex-grow-1 tw-full-height tw-pd-b-1'})
                return result
            global confirm
            confirm = 1

            # 구글드라이버
            options = webdriver.ChromeOptions();
            options.add_argument('headless')
            options.add_argument('window-size=1920x540')
            options.add_argument("--disable-popup-blocking")
            options.add_argument("settings.tts.speech_volume")
            # 화면 사용여부
            # options.add_argument('disable-gpu')
            #드라이버 전역변수 선언(Ender 쓰레드에서도 써야함)
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

            # 타이머 리셋, 시작
            sw.Reset()
            sw.Start()

            #크롤링 파트
            while True:
                if confirm == 1:
                    # 페이지 elements 모두 가져오기
                    html = driver.page_source
                    timeS = timeStamp()
                    # BeautifulSoup 사용
                    soup = BeautifulSoup(html, "html.parser")
                    global result2
                    result2 = crawl()
                    # print(timeS)
                    # print(result2.getText())
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
                else :
                    print("break 실행")
                    break
        startT()


class Ender(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        def stop():
            global confirm
            confirm = 0
            # 크롬 드라이버 종료
            driver.quit()
            # 파일 저장 경로
            path = "C:\\twitchChat\\"
            if not os.path.isdir(path):
                os.mkdir(path)
            # 파일 이름
            fileName = path + e2.get()
            # 파일 열기(W모드)
            writeText = open(fileName + ".txt", 'w', encoding="UTF-8")
            # 줄바꿈을 넣어서 리스트 단위로 작성, 저장
            writeText.writelines("\n".join(timeList))
            writeText.close()
        stop()

# 초시계 클래스
class StopWatch(Frame):
    """ Implements a stop watch frame widget. """
    def __init__(self, parent=None, **kw):
        Frame.__init__(self, parent, kw)
        self._start = 0.0
        self._elapsedtime = 0.0
        self._running = 0
        self.timestr = StringVar()
        self.makeWidgets()

    def makeWidgets(self):
        """ Make the time label. """
        l = Label(self, textvariable=self.timestr)
        self._setTime(self._elapsedtime)
        l.pack(fill=X, expand=NO, pady=2, padx=2)

    def _update(self):
        """ Update the label with elapsed time. """
        self._elapsedtime = time.time() - self._start
        self._setTime(self._elapsedtime)
        self._timer = self.after(50, self._update)

    def _setTime(self, elap):
        """ Set the time string to Minutes:Seconds:Hundreths """
        minutes = int(elap/60)
        seconds = int(elap - minutes*60.0)
        hseconds = int((elap - minutes*60.0 - seconds)*100)
        self.timestr.set('%02d:%02d:%02d' % (minutes, seconds, hseconds))

    def Start(self):
        """ Start the stopwatch, ignore if running. """
        if not self._running:
            self._start = time.time() - self._elapsedtime
            self._update()
            self._running = 1

    def Stop(self):
        """ Stop the stopwatch, ignore if stopped. """
        if self._running:
            self.after_cancel(self._timer)
            self._elapsedtime = time.time() - self._start
            self._setTime(self._elapsedtime)
            self._running = 0

    def Reset(self):
        """ Reset the stopwatch. """
        self._start = time.time()
        self._elapsedtime = 0.0
        self._setTime(self._elapsedtime)

def startA():
    print("start clicked")
    t = HtmlGetter()
    t.start()

def stop():
    print("stop clicked")
    sw.Stop()
    e = Ender()
    e.start()


window = Tk()
confirm = 1
l1 = Label(window, text="방송 주소")
l1.grid(row=0, column=0)
l2 = Label(window, text="파일명")
l2.grid(row=1, column=0)
e1 = Entry(window, width=50)
e1.grid(row=0, column=1)
e2 = Entry(window, width=50)
e2.grid(row=1, column=1)
str = StringVar()
b1 = Button(window, text="Start", command=startA, width = 10)
b2 = Button(window, text="Stop & Save", command=stop)
b1.grid(row=0, column=2)
b2.grid(row=1, column=2)

sw = StopWatch(window)
sw.grid(row=2,columnspan=2)

window.mainloop()


