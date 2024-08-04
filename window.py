from tkinter import Tk, BOTH, Canvas
from geometry import Point, Line
from time import sleep

class Window:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.__root.geometry("%dx%d" % (width, height))
        self.canvas = Canvas(self.__root, width=width, height=height)

        self.canvas.pack()
        self.running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def draw_line(self, coordinates, fill_color: str = "black"):
        self.canvas.create_line(*coordinates, fill=fill_color, width=2)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.running = True
        while self.running:
            self.redraw()

    def close(self):
        self.running = False