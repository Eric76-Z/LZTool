import tkinter
from PIL import ImageGrab, ImageTk
from PySide2.QtGui import QPixmap

from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QFileDialog, QApplication

from src.common.setting import main_ui_path, start_ui_path

Flag = False
radius = 20


def selectBox():
    box = (345, 281, 600, 500)
    return box


def loopGrab():
    Falg = True
    box = selectBox()
    subIm = ImageGrab.grab(box)
    subIm = subIm.resize((radius * 20, radius * 20))
    # subIm = subIm.resize((radius * 20, radius * 20))  # 放大该图像
    # subIm = ImageTk.PhotoImage(subIm)
    startwindow.ui.label_pic.setPixmap(subIm)


def startPlay():
    loopGrab()
    startwindow.ui.show()


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

    def signalConnect(self):
        self.ui.pushButton_select.clicked.connect(lambda: selectBox())
        self.ui.pushButton_start.clicked.connect(lambda: startPlay())

class Ui_StartWindows():
    def __init__(self):
        self.ui = QUiLoader().load(start_ui_path)


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
