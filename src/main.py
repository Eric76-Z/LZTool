import tkinter
from threading import Thread
from time import sleep

import win32api
import win32con
import win32gui
import win32ui
from PIL import ImageGrab, ImageTk, Image
from PySide2 import QtGui
from PySide2.QtCore import QObject, Signal
from PySide2.QtGui import QPixmap

from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QFileDialog, QApplication, QLabel

from src.common.setting import main_ui_path, start_ui_path

Flag = False
radius = 20


class MySignals(QObject):
    # 定义一种信号，因为有文本框和进度条两个类，此处要四个参数，类型分别是： QPlainTextEdit 、 QProgressBar、字符串和整形数字
    # 调用 emit方法发信号时，传入参数必须是这里指定的参数类型
    # 此处也可分开写两个函数，一个是文本框输出的，一个是给进度条赋值的
    text_print = Signal(QLabel, str, int)


def window_capture():
    winType = mainwindow.ui.lineEdit_type.text()
    winTitle = mainwindow.ui.lineEdit_title.text()
    # 获取后台窗口的句柄，注意后台窗口不能最小化
    hWnd = win32gui.FindWindow(winType, winTitle)  # 窗口的类名可以用Visual Studio的SPY++工具获取
    # 获取句柄窗口的大小信息
    left, top, right, bot = win32gui.GetWindowRect(hWnd)
    width = right - left
    height = bot - top
    # 返回句柄窗口的设备环境，覆盖整个窗口，包括非客户区，标题栏，菜单，边框
    hWndDC = win32gui.GetWindowDC(hWnd)
    # 创建设备描述表
    mfcDC = win32ui.CreateDCFromHandle(hWndDC)
    # 创建内存设备描述表
    saveDC = mfcDC.CreateCompatibleDC()
    # 创建位图对象准备保存图片
    saveBitMap = win32ui.CreateBitmap()
    # 为bitmap开辟存储空间
    saveBitMap.CreateCompatibleBitmap(mfcDC, 200, 50)
    # 将截图保存到saveBitMap中
    saveDC.SelectObject(saveBitMap)
    # 保存bitmap到内存设备描述表
    saveDC.BitBlt((0, 0), (width, height), mfcDC, (0, 30), win32con.SRCCOPY)
    # 保存图像
    # 方法一：windows api保存
    ##保存bitmap到文件
    saveBitMap.SaveBitmapFile(saveDC, "img/toplay.png")
    # ##方法二(第一部分)：PIL保存
    # ###获取位图信息
    # bmpinfo = saveBitMap.GetInfo()
    # bmpstr = saveBitMap.GetBitmapBits(True)
    # ###生成图像
    # im_PIL = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1)
    # im_PIL.save("img/toplay.png")  # 保存


class Ui_Mainwindows():
    def __init__(self):
        # 从文件中加载UI定义
        # 从 UI 定义中动态 创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性了
        self.ui = QUiLoader().load(main_ui_path)
        self.process()

    def process(self):
        # pushButton连接
        self.signalConnect()

    def widgetInit(self):
        if self.ui.lineEdit_type.text() == '' or self.ui.lineEdit_title.text() == '':
            self.ui.pushButton_start.setEnabled(False)
        else:
            self.ui.pushButton_start.setEnabled(True)



    def signalConnect(self):
        self.ui.pushButton_select.clicked.connect(lambda: self.selectBox())
        self.ui.pushButton_start.clicked.connect(lambda: startwindow.process())

    def selectBox(self):
        box = (345, 281, 600, 500)
        return box


class Ui_StartWindows():
    def __init__(self):
        self.ui = QUiLoader().load(start_ui_path)

    def process(self):
        th = Thread(target=self.loopGrab)
        th.start()
        startwindow.ui.show()

    def playImg(self):
        pixmap = QtGui.QPixmap('img/toplay.png')
        self.ui.label_pic.setPixmap(pixmap)
        self.ui.label_pic.setScaledContents(True)  # 让图片自适应label大小

    def loopGrab(self):
        Flag = True
        while Flag == True:
            window_capture()
            # subIm = ImageGrab.grab(box)
            # subIm = subIm.resize((radius * 20, radius * 20))
            # subIm.save('img/toplay.jpg', 'jpeg')
            self.playImg()
            # subIm = subIm.resize((radius * 20, radius * 20))  # 放大该图像
            # subIm = ImageTk.PhotoImage(subIm)
            sleep(0.1)


def main():
    app = QApplication([])
    global mainwindow
    global startwindow
    mainwindow = Ui_Mainwindows()
    startwindow = Ui_StartWindows()
    mainwindow.ui.show()
    app.exec_()


if __name__ == '__main__':
    # 抓取选定区域屏幕，并最大化
    # 1、选定截屏区域
    # 2、循环截屏
    # 3、放入画布
    # 4、配置pygui
    main()
