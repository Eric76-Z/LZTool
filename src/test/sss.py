import sys, math
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class Drawing(QWidget):
    def __init__(self, parent=None):
        super(Drawing, self).__init__(parent)
        self.resize(600, 400)
        self.setWindowTitle('拖拽绘制矩形')
        self.rect = None
        self.move = False
        self.bigger = False
        self.x = 0
        self.y = 0
        self.singleOffset = QPoint(0, 0)
        self.isLeftPressed = bool(False)

    # 重写绘制函数
    def paintEvent(self, event):
        # 初始化绘图工具
        qp = QPainter()
        # 开始在窗口绘制
        qp.begin(self)
        # 自定义画点方法
        if self.rect:
            self.drawRect(qp)
        # 结束在窗口的绘制
        qp.end()

    def drawRect(self, qp):
        # 创建红色，宽度为4像素的画笔
        pen_line = QPen(Qt.red, 2)
        pen_ellipse = QPen(Qt.black, 1)

        brush_ellipse = QBrush(QColor(0, 78, 152))

        if self.rect[0] < self.x:
            qp.setPen(pen_line)
            # qp.drawLine(self.rect[0] + 4, self.rect[1] + 8, self.rect[0] + 4, self.y)  # 横向
            qp.drawLine(self.rect[0] + 8, self.rect[1] + 4, self.x, self.rect[1] + 4)  # 竖直
            # qp.drawLine(self.rect[0] + 8, self.y + 4, self.x, self.y + 4)
            # qp.drawLine(self.x + 4, self.rect[1] + 8, self.x + 4, self.y)

            qp.setPen(pen_ellipse)
            qp.setBrush(brush_ellipse)
            qp.drawEllipse(self.rect[0], self.rect[1], 8, 8)  # (startx, starty, w, h) 左上
            qp.drawEllipse(self.rect[0], self.y, 8, 8)  # (startx, starty, w, h) 左上
            qp.drawEllipse(self.x, self.rect[1], 8, 8)  # (startx, starty, w, h) 右上
            qp.drawEllipse(self.x, self.y, 8, 8)  # (startx, starty, w, h) 右下

            # qp.drawEllipse(self.rect[0] + self.rect[2] / 2, self.rect[1], 8, 8)  # (startx, starty, w, h) 上中
            # qp.drawEllipse(self.x - self.rect[2] / 2, self.y, 8, 8)  # (startx, starty, w, h) 下中
            qp.drawEllipse(self.rect[0], self.rect[1] + self.rect[3] / 2, 8, 8)  # (startx, starty, w, h) 左中
            qp.drawEllipse(self.x, self.rect[1] + self.rect[3] / 2, 8, 8)  # (startx, starty, w, h) 右中
        # else:
        #     qp.drawLine(self.rect[0] + 4, self.rect[1], self.rect[0] + 4, self.y + 8)  # 竖直
        #     qp.drawLine(self.rect[0], self.rect[1] + 4, self.x + 8, self.rect[1] + 4)  # 横向
        #     qp.drawLine(self.rect[0], self.y + 4, self.x + 8, self.y + 4)
        #     qp.drawLine(self.x + 4, self.rect[1], self.x + 4, self.y + 8)
        #
        #     qp.drawEllipse(self.rect[0], self.rect[1], 8, 8)  # (startx, starty, w, h) 左上
        #     qp.drawEllipse(self.rect[0], self.y, 8, 8)  # (startx, starty, w, h) 左上
        #     qp.drawEllipse(self.x, self.rect[1], 8, 8)  # (startx, starty, w, h) 右上
        #     qp.drawEllipse(self.x, self.y, 8, 8)  # (startx, starty, w, h) 右下
        #
        #     qp.drawEllipse(self.rect[0] + self.rect[2] / 2, self.rect[1], 8, 8)  # (startx, starty, w, h) 右上
        #     qp.drawEllipse(self.x - self.rect[2] / 2, self.y, 8, 8)  # (startx, starty, w, h) 右下
        # qp.drawRect(*self.rect)

    # 重写三个时间处理
    def mousePressEvent(self, event):
        print("mouse press")

        if event.buttons() == Qt.LeftButton:  # 左键按下
            # 左键按下(图片被点住),置Ture
            self.isLeftPressed = bool(True)
            print(event.pos(), " ", self.x, " ", self.y)

            if self.rect and (
                    event.pos().x() >= self.x and event.pos().x() <= self.x + 8 and (event.pos().y() >= self.rect[1]
                                                                                     and event.pos().y() <= self.rect[
                                                                                         1] + 8) or (
                            event.pos().y() >= self.rect[1] + self.rect[3] / 2
                            and event.pos().y() <= self.rect[1] + self.rect[3] / 2 + 8)
                    or (event.pos().y() >= self.y and event.pos().y() <= self.y + 8)):
                print("Big")
                self.bigger = True


            elif self.rect and (event.pos().x() <= self.x and event.pos().x() >= self.rect[0]
                                and event.pos().y() <= self.y and event.pos().y() >= self.rect[1]):
                print("MOVE!")
                self.move = True
                self.preMousePosition = event.pos()

            else:
                self.move = False
                self.bigger = False
                self.rect = (event.pos().x(), event.pos().y(), 0, 0)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:  # 左键释放
            self.isLeftPressed = False  # 左键释放(图片被点住),置False
            self.bigger = False
            self.move = False
            print("mouse release")

    def mouseMoveEvent(self, event):
        start_x, start_y = self.rect[0:2]
        if self.isLeftPressed:

            if self.bigger:
                print("bigger")
                if event.pos().x() > self.rect[0]:
                    print(event.pos().x() - self.rect[0])
                    self.x, self.y = event.pos().x(), self.y

            elif self.move:
                differ = event.pos() - self.preMousePosition
                self.x, self.y = self.x + differ.x(), self.y + differ.y()
                start_x, start_y = start_x + differ.x(), start_y + differ.y()
                self.preMousePosition = event.pos()

            else:
                self.x = event.pos().x()
                self.y = event.pos().y()

            self.rect = (start_x, start_y, self.x - start_x, self.y - start_y)
            self.repaint()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Drawing()
    demo.show()
    sys.exit(app.exec_())
