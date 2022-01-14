from threading import Thread
from time import sleep
import win32con
import win32gui
import win32ui
from PySide2 import QtGui
from PySide2.QtCore import QObject, Signal, Qt, QPoint, QSize, QRect
from PySide2.QtGui import QMouseEvent, QPen, QPainter
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QLabel, QWidget, QMenu, QAction, QGridLayout

from src.common.setting import main_ui_path


class MySignals(QObject):
    # 定义一种信号，因为有文本框和进度条两个类，此处要四个参数，类型分别是： QPlainTextEdit 、 QProgressBar、字符串和整形数字
    # 调用 emit方法发信号时，传入参数必须是这里指定的参数类型
    # 此处也可分开写两个函数，一个是文本框输出的，一个是给进度条赋值的
    text_print = Signal(QLabel, str, int)

class MyLabel(QLabel):
    x0 = 0
    y0 = 0
    x1 = 0
    y1 = 0
    flag = False

    # 鼠标点击事件
    def mousePressEvent(self, event):
        self.flag = True
        self.x0 = event.x()
        self.y0 = event.y()

    # 鼠标释放事件
    def mouseReleaseEvent(self, event):
        self.flag = False

    # 鼠标移动事件
    def mouseMoveEvent(self, event):
        if self.flag:
            self.x1 = event.x()
            self.y1 = event.y()
            self.update()

    # 绘制事件
    def paintEvent(self, event):
        super().paintEvent(event)
        rect = QRect(self.x0, self.y0, abs(self.x1 - self.x0), abs(self.y1 - self.y0))
        painter = QPainter(self)
        painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
        painter.drawRect(rect)




def window_capture():
    winType = mainwindow.ui.lineEdit_type.text()
    winTitle = mainwindow.ui.lineEdit_title.text()
    winType = 'Q360SafeMainClass'
    winTitle = '360安全卫士'

    # 获取后台窗口的句柄，注意后台窗口不能最小化
    hWnd = win32gui.FindWindow(winType, winTitle)  # 窗口的类名可以用Visual Studio的SPY++工具获取
    # 获取句柄窗口的大小信息
    try:
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
        saveDC.BitBlt((0, 0), (width, height), mfcDC, (20, 30), win32con.SRCCOPY)
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
        startwindow.rightWin = True
    except:
        startwindow.rightWin = False


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
        pixmap = QtGui.QPixmap('img/bgc.png')
        self.ui.label_img.setPixmap(pixmap)
        self.ui.label_img.setScaledContents(True)  # 让图片自适应label大小

    def signalConnect(self):
        self.ui.pushButton_select.clicked.connect(lambda: drawing.process())
        self.ui.pushButton_start.clicked.connect(lambda: startwindow.process())

    def selectBox(self):
        drawing.show()
        box = (345, 281, 600, 500)
        return box


class Drawing(QWidget):
    defultsize = 600
    x0 = 0
    y0 = 0
    x1 = 0
    y1 = 0
    flag = False
    def __init__(self, parent=None):
        super(Drawing, self).__init__(parent)
        self.resize(600, 400)
        self.setWindowTitle('拖拽绘制矩形')
        # self.setFixedSize(QSize(self.defultsize, self.defultsize))

        self.label_pic = MyLabel(self)  # 重定义的label

        self.label_pic.setAutoFillBackground(True)
        self.label_pic.resize(self.width(), self.height())
        self.label_pic.setScaledContents(True)  # 让图片自适应label大小
        self.label_pic.setCursor(Qt.CrossCursor)
        self.label_pic.setGeometry(QRect(30, 30, 511, 541))

        grid = QGridLayout()
        grid.addWidget(self.label_pic)
        self.setLayout(grid)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)  # 无边框


    def process(self):
        self.createSelectTh()
        self.show()

    def createSelectTh(self):
        self.Flag = True
        self.th = Thread(target=self.selectTarget)
        self.th.start()

    def selectTarget(self):
        window_capture()
        if startwindow.rightWin == True:
            pixmap = QtGui.QPixmap('img/toplay.png')
        else:
            pixmap = QtGui.QPixmap('img/errorwin.png')
        self.label_pic.setPixmap(pixmap)

    def contextMenuEvent(self, evt):  # 连接菜单事件
        menu = QMenu(self)
        confirm = QAction("确认区域", menu)
        confirm.triggered.connect(lambda: self.confirmArea())
        showfullscreen = QAction("全屏", menu)
        showfullscreen.triggered.connect(lambda: self.clickFullScreen())
        showdefault = QAction("默认显示", menu)
        showdefault.triggered.connect(lambda: self.clickDefultSize())
        showmax = QAction("最大化", menu)
        showmax.triggered.connect(lambda: self.clickMaximize())
        showmini = QAction("最小化", menu)
        showmini.triggered.connect(lambda: self.clickMinimize())
        exit_action = QAction("退出", menu)
        exit_action.triggered.connect(lambda: self.clickExit())

        menu.addAction(confirm)
        menu.addAction(showfullscreen)
        menu.addAction(showdefault)
        menu.addAction(showmax)
        menu.addAction(showmini)
        menu.addSeparator()
        menu.addAction(exit_action)
        menu.exec_(evt.globalPos())

    def clickFullScreen(self):
        self.showFullScreen()

    def clickDefultSize(self):
        self.showNormal()

    def clickMaximize(self):
        self.showMaximized()

    def clickMinimize(self):
        self.showMinimized()

    def clickExit(self):
        self.close()

    def confirmArea(self):
        print(drawing.label_pic.x0)
        print(drawing.label_pic.x1)
        print('wwwwww')


class Ui_StartWindows(QWidget):
    # def __init__(self):
    #     super().__init__()
    #     self.ui = QUiLoader().load(start_ui_path)
    #     self._startPos = None
    #     self._endPos = None
    #     self._tracking = False
    #     # 窗体置顶(窗体置顶，仅仅为了方便测试)，去边框
    #     self.ui.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
    #     # 窗体透明，控件不透明
    #     # self.setAttribute(Qt.WA_TranslucentBackground)
    _startPos = None
    _endPos = None
    _isTracking = False
    defultsize = 600
    Flag = False
    rightWin = False

    def __init__(self):
        super().__init__()
        grid = QGridLayout()
        self.setFixedSize(QSize(self.defultsize, self.defultsize))
        self.label_pic = QLabel(self)
        self.label_pic.setAutoFillBackground(True)
        self.label_pic.resize(self.width(), self.height())
        self.label_pic.setScaledContents(True)  # 让图片自适应label大小
        grid.addWidget(self.label_pic)
        self.setLayout(grid)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)  # 无边框

    def process(self):
        self.createPlayTh()
        self.show()

    def createPlayTh(self):
        self.Flag = True
        self.th = Thread(target=self.loopGrab)
        self.th.start()

    def loopGrab(self):
        while self.Flag == True:
            window_capture()
            self.playImg()
            sleep(0.05)

    def playImg(self):
        if self.rightWin == True:
            pixmap = QtGui.QPixmap('img/toplay.png')
        else:
            pixmap = QtGui.QPixmap('img/errorwin.png')
        self.label_pic.setPixmap(pixmap)

    def mouseMoveEvent(self, e: QMouseEvent):  # 重写移动事件
        self._endPos = e.pos() - self._startPos
        self.move(self.pos() + self._endPos)

    def mousePressEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._isTracking = True
            self._startPos = QPoint(e.x(), e.y())

    def mouseReleaseEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._isTracking = False
            self._startPos = None
            self._endPos = None

    def contextMenuEvent(self, evt):  # 连接菜单事件
        menu = QMenu(self)
        showfullscreen = QAction("全屏", menu)
        showfullscreen.triggered.connect(lambda: self.clickFullScreen())
        showdefault = QAction("默认显示", menu)
        showdefault.triggered.connect(lambda: self.clickDefultSize())
        showmax = QAction("最大化", menu)
        showmax.triggered.connect(lambda: self.clickMaximize())
        showmini = QAction("最小化", menu)
        showmini.triggered.connect(lambda: self.clickMinimize())
        exit_action = QAction("退出", menu)
        exit_action.triggered.connect(lambda: self.clickExit())
        menu.addAction(showfullscreen)
        menu.addAction(showdefault)
        menu.addAction(showmax)
        menu.addAction(showmini)
        menu.addSeparator()
        menu.addAction(exit_action)
        menu.exec_(evt.globalPos())

    def clickFullScreen(self):
        self.showFullScreen()

    def clickDefultSize(self):
        self.showNormal()

    def clickMaximize(self):
        self.showMaximized()

    def clickMinimize(self):
        self.showMinimized()

    def clickExit(self):
        self.close()


def main():
    app = QApplication([])
    global mainwindow
    global startwindow
    global drawing
    drawing = Drawing()
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
