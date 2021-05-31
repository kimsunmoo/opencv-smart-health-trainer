import tkinter as tk
import tkinter.ttk
from PIL import ImageTk, Image
import cv2

class MyFame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.master = master
        self.master.title("AniWatch")
        
        menuFrm = tk.Frame(self)
        values=['스쿼트', '덤벨 컬'] 

        combobox=tk.ttk.Combobox(menuFrm, height=15, values=values)
        combobox.grid(row=0, column=0)

        combobox.set("운동 선택")

        lbl1 = tk.Label(menuFrm, text='횟수 : ', width=5)
        lbl1.grid(row=0, column=1)

        textbox = tk.ttk.Entry(menuFrm, width=15, textvariable=str)
        textbox.grid(row=0, column=2)

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

    def setFrame(self, frame):
        self.frame = frame
    
    def start(self):
        print('start')

    def stop(self):
        print('stop')