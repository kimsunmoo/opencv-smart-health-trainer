import tkinter as tk
import tkinter.ttk
from PIL import ImageTk, Image
import cv2
import constant

class MyFame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.setting = constant.EXER_DEFAULT
        self.ex_count = 0

        self.master = master
        self.master.title("AniWatch")
        
        menuFrm = tk.Frame(self)
        values=['스쿼트', '덤벨 컬'] 

        self.combobox=tk.ttk.Combobox(menuFrm, height=15, values=values)
        self.combobox.grid(row=0, column=0)

        self.combobox.set("운동 선택")

        lbl1 = tk.Label(menuFrm, text='횟수 : ', width=5)
        lbl1.grid(row=0, column=1)

        self.textbox = tk.ttk.Entry(menuFrm, width=15, textvariable=str)
        self.textbox.grid(row=0, column=2)

        startButton = tk.Button(menuFrm, text='start', overrelief='solid', width=15, command=self.start, repeatdelay=1000, repeatinterval=100)
        startButton.grid(row=0, column=3)

        stopButton = tk.Button(menuFrm, text='stop', overrelief='solid', width=15, command=self.stop, repeatdelay=1000, repeatinterval=100)
        stopButton.grid(row=0, column=4)

        menuFrm.grid(row=0, column=0)

        self.lbl = tk.Label(self)
        self.lbl.grid(row=1, column=0)

        self.grid(row=0, column=0)

    def video_play(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        # OpenCV 동영상
        self.lbl.imgtk = imgtk
        self.lbl.configure(image=imgtk)
        self.lbl._image_cache = imgtk

    def setFrame(self, frame):
        self.frame = frame
    
    def start(self):
        self.setting=self.combobox.current()
        self.ex_count=int(self.textbox.get())
        print(self.setting,self.ex_count)
        print('start')

    def stop(self):
        self.combobox.set("운동 선택")
        self.textbox.config(text="0")
        self.setting = constant.EXER_DEFAULT
        self.ex_count=0
        print(self.ex_name,self.ex_count)
        print('stop')