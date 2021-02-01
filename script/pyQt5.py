from PyQt5.QtWidgets import QApplication,QWidget
import sys
if __name__ == '__main__':
    # 创建实例
    app = QApplication(sys.argv)
    # 创建窗口
    w = QWidget()
    # 创建窗口的尺寸
    w.resize(500,150)
    # 移动窗口
    w.move(300,300)
    # 创建标题
    w.setWindowTitle('桌面应用')
    # 显示窗口
    w.show()
    #进入程序的主循环，并通过exit函数确保主循环安全结束
    sys.exit(app.exec_())