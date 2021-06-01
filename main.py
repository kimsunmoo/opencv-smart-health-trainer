import ui
import videocap
import tkinter as tk
import time
import threading

def play():
    time.sleep(1)
    while video.cap.isOpened():
        myFrame.video_play(video.frame)
        time.sleep(0.05)
    print('play therad exit')

def main():
    global myFrame
    global video
    global exerciseDetector

    capture = True

    window = tk.Tk()

    myFrame = ui.MyFame(window)

    video = videocap.VideoCap()
    video.start()

    t = threading.Thread(target=play)
    t.start()

    window.mainloop()
    video.cap.release()
    t.join()
    video.join()

if __name__ == '__main__':
    main()