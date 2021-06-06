#참고한 자료 : 
import tkinter as tk
import tkinter.ttk
from PIL import ImageTk, Image
import cv2

import constant

class MyFame(tk.Frame):
    #Tkinter의 위젯 배치 및 변수 초기화
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        #setting : 운동 종류를 지정하는 변수
        self.setting = constant.EXER_DEFAULT
        
        #ex_count : 목표 운동 횟수 지정
        self.ex_count = 0

        #pressed : 버튼이 눌렸을 때만 작동하도록 하기위해 사용되는 변수
        self.pressed = False

        self.master = master
        self.master.title("Smart Health Trainer")
        
        menuFrm = tk.Frame(self)
        values=['스쿼트', '덤벨 컬 (오른손)', '덤벨 컬 (왼손)'] 

        self.combobox=tk.ttk.Combobox(menuFrm, width=26, height=15, values=values)
        self.combobox.grid(row=0, column=0)

        self.combobox.set("운동 선택")

        lbl1 = tk.Label(menuFrm, text='횟수 : ', width=5)
        lbl1.grid(row=0, column=1)

        self.textbox = tk.ttk.Entry(menuFrm, width=26, textvariable=str)
        self.textbox.grid(row=0, column=2)

        startButton = tk.Button(menuFrm, text='start', overrelief='solid', width=26, command=self.start, repeatdelay=1000, repeatinterval=100)
        startButton.grid(row=0, column=3)

        stopButton = tk.Button(menuFrm, text='stop', overrelief='solid', width=26, command=self.stop, repeatdelay=1000, repeatinterval=100)
        stopButton.grid(row=0, column=4)

        menuFrm.grid(row=0, column=0)

        self.lbl = tk.Label(self)
        self.lbl.grid(row=1, column=0)

        self.grid(row=0, column=0)

    #영상 처리가 완료된 frame을 받아서 tkinter에 띄우는 함수
    def video_play(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)

        # OpenCV 동영상
        self.lbl.imgtk = imgtk
        self.lbl.configure(image=imgtk)
        self.lbl._image_cache = imgtk
    
    #start 버튼을 눌렀을 때 호출되는 함수 (입력한 정보를 변수에 저장)
    def start(self):
        self.setting=self.combobox.current()
        self.ex_count=int(self.textbox.get())
        self.pressed = True
        print('start')
    
    #stop 버튼을 눌렀을 때 호출되는 함수 (변수 초기화)
    def stop(self):
        self.combobox.set("운동 선택")
        self.textbox.delete(0, "end")
        self.setting = constant.EXER_DEFAULT
        self.ex_count=0
        self.pressed = True
        print('stop')