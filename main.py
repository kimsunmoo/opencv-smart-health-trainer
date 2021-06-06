import ui
import videocap
import constant
import tkinter as tk
import time
import threading

#myFrame 객체와 video 객체 사이에 정보를 전달하는 스레드의 메인 함수
def play():
    #초기화 되지 않은 메모리 접근 방지
    time.sleep(1)  

    while video.cap.isOpened():
        #Tkinter의 버튼이 눌렸을 때 작동
        if myFrame.pressed == True:
            video.setState(myFrame.setting, myFrame.ex_count)
            myFrame.pressed = False

        #운동이 완료되었을 때 Tkinter 위젯 초기화
        if (video.isComplete() == True):
            myFrame.combobox.set("운동 선택")
            myFrame.textbox.delete(0, "end")
            myFrame.ex_count = 0

        #video 객체에서 처리된 frame을 Tkinter로 넘김
        myFrame.video_play(video.getFrame())

        #중복된 frame 전송 방지
        time.sleep(0.01)

def main():
    global myFrame
    global video

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