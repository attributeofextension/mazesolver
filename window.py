from tkinter import Tk, BOTH, Canvas
from geometry import Point, Line

class Window:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.canvas = Canvas(self.__root)
        self.canvas.pack()
        self.running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def draw_line(self, line: Line, fill_color: str = "black"):
        self.canvas.create_line(*line.reduce_to_coordinates(), fill=fill_color, width=2)

    def draw_point(self, point: Point, fill_color: str = "green"):
        self.canvas.create_oval(*point.reduce_to_coordinates(), fill=fill_color, width=2)


    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.running = True
        while self.running:
            self.redraw()

    def close(self):
        self.running = False