from window import Window
from geometry import Point, Line

if __name__ == '__main__':
    win = Window(800, 600)
    test_point = Point(100, 100)
    win.draw_point(test_point)
    win.wait_for_close()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
