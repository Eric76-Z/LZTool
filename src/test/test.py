import tkinter
from PIL import ImageGrab, ImageTk

root = tkinter.Tk()
screenW = root.winfo_screenwidth()
screenH = root.winfo_screenheight()
root.geometry(str(screenW) + 'x' + str(screenH) + '+0+0')
root.overrideredirect(True)  # 不显示标题栏
root.resizable(False, False)

canvas = tkinter.Canvas(root, bg='white', width=screenW, height=screenH)  # 创建白色画布
image = ImageTk.PhotoImage(ImageGrab.grab())  # 全屏抓取
canvas.create_image(screenW // 2, screenH // 2, image=image)


def onMouseRightClick(event):
    root.destroy()


canvas.bind('<Button-3>', onMouseRightClick)

radius = 20


def onMouseMove(event):
    global lastIm, subIm
    try:
        canvas.delete(lastIm)
    except:
        pass
    x = event.x
    y = event.y
    subIm = ImageGrab.grab((x - radius, y - radius, x + radius, y + radius))  # 创建显示的下一图像
    subIm = subIm.resize((radius * 5, radius * 5))  # 放大该图像
    subIm = ImageTk.PhotoImage(subIm)
    lastIm = canvas.create_image(x - 70, y - 70, image=subIm)


canvas.bind('<Motion>', onMouseMove)

canvas.pack(fill=tkinter.BOTH, expand=tkinter.YES)  # 画布放置至窗体
root.mainloop()
