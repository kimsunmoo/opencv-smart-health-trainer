import ui
import videocap
import tkinter as tk
import time
import threading

def play():
    time.sleep(1)  
    while video.cap.isOpened():
        if myFrame.pressed == True:
            video.setState(myFrame.setting, myFrame.ex_count)
            myFrame.pressed = False
            print(myFrame.setting, myFrame.ex_count)
        myFrame.video_play(video.getFrame())
        time.sleep(0.01)
    print('play therad exit')

def main():
    global myFrame
    global video

    global exerciseDetector

    capture = True

    window = tk.Tk()

    myFrame = ui.MyFame(window)

    video = videocap.VideoCap()
    video.daemon = True
    video.start()

    t = threading.Thread(target=play)
    t.daemon = True
    t.start()

    window.mainloop()

    video.cap.release()


if __name__ == '__main__':
    main()