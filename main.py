from window import Window
from geometry import Lattice, Point, Line
from time import sleep

if __name__ == '__main__':
    win = Window(1000, 1000)

    lattice = Lattice(800, 600, 10)
    grid_draw_coordinates = lattice.get_grid_drawing_coordinates()
    for coordinate in grid_draw_coordinates:
        win.draw_line(coordinate)

    win.wait_for_close()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
