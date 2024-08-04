from uuid import uuid4
class Range:
    def __init__(self, start, end):
        if start > end:
            self.start = end
            self.end = start
        else:
            self.start = start
            self.end = end

    def is_trivial(self):
        return self.start == self.end

class Domain:
    def __init__(self, start, end):
        if start > end:
            self.start = end
            self.end = start
        else:
            self.start = start
            self.end = end

    def is_trivial(self):
        return self.start == self.end

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_range(self, other):
        return Range(self.y, other.y)

    def get_domain(self, other):
        return Domain(self.x, other.x)

    def reduce_to_coordinates(self):
        return self.x, self.y


class Line:
    def get_y(self, y=None):
        pass

    def get_x(self, x=None):
        pass

    def get_intersection(self, other: 'Line') -> Point | None:
        pass

    def get_vector_from_range(self, range: Range):
        pass

    def get_vector_from_domain(self, domain: Domain):
        pass

class VerticalLine(Line):
    def __init__(self, x):
        self.x = x

    def get_y(self,x=None):
        return None

    def get_x(self, y=None):
        return self.x

    def get_intersection(self, other: 'Line') -> Point | None:
        if isinstance(other, VerticalLine):
            return None
        if isinstance(other, HorizontalLine):
            return Point(self.x, other.y)
        if isinstance(other, Slope):
            return Point(self.x, other.m * self.x + other.b)
        return None

    def get_vector_from_range(self, range: Range):
        if range.is_trivial():
            return None
        p1 = Point(self.x, range.start)
        p2 = Point(self.x, range.end)
        return Vector(p1, p2)

    def get_vector_from_domain(self, domain: Domain):
        raise Exception("Cannot get vector from domain of a vertical line")


class HorizontalLine(Line):
    def __init__(self, y):
        self.y = y

    def get_y(self, y=None):
        return self.y

    def get_x(self, x=None):
        return None

    def get_intersection(self, other: 'HorizontalLine') -> Point | None:
        if isinstance(other, HorizontalLine):
            return None
        if isinstance(other, VerticalLine):
            return Point(other.x, self.y)
        if isinstance(other, Slope):
           return Point((self.y - other.b)/other.m, self.y)

    def get_vector_from_range(self, range: Range):
        raise Exception("Cannot get vector from range of a horizontal line")

    def get_vector_from_domain(self, domain: Domain):
        if domain.is_trivial():
            return None
        p1 = Point(domain.start, self.y)
        p2 = Point(domain.end, self.y)
        return Vector(p1, p2)

class Slope(Line):
    def __init__(self, m, b):
        if m == 0:
            raise Exception("m cannot be zero - try HorizontalLine class")
        self.m = m
        self.b = b

    def get_y(self, x=None):
        if x is None:
            raise Exception("x cannot be None")
        return self.m * x + self.b

    def get_x(self, y=None):
        if y is None:
            raise Exception("y cannot be None")
        return (y - self.b)/self.m

    def get_intersection(self, other: 'Vector') -> Point | None:
        if self.m == other.m:
            return None
        if isinstance(other, HorizontalLine) or isinstance(other, VerticalLine):
            return other.get_intersection(self)
        if isinstance(other, Slope):
            return Point((other.b - self.b)/(self.m - other.m), (self.m * (other.b - self.b)/(self.m - other.m)) + self.b)
        return None

    def get_vector_from_range(self, range: Range):
        if range.is_trivial():
            return None
        p1 = Point(self.get_x(range.start), range.start)
        p2 = Point(self.get_x(range.end), range.end)
        return Vector(p1, p2)

    def get_vector_from_domain(self, domain: Domain):
        if domain.is_trivial():
            return None
        p1 = Point(domain.start, self.get_y(domain.start))
        p2 = Point(domain.end, self.get_y(domain.end))
        return Vector(p1, p2)


class Vector:
    def __init__(self, p1: Point, p2: Point):
        self.p1: Point = p1
        self.p2: Point = p2

    def reduce_to_coordinates(self):
        return self.p1.reduce_to_coordinates() + self.p2.reduce_to_coordinates()


class Vertex(Point):
    def __init__(self, x, y, point):
        super().__init__(x, y)
        self.point = point
        self.x = x
        self.y = y
        self.id = f"{self.x},{self.y}"


class MazeVertex(Vertex):
    def __init__(self, x, y, point, is_boundary=False):
        super().__init__(x, y, point)
        self.is_boundary = is_boundary

    def get_drawing_coordinates(self):
        return self.point.x, self.point.y


class Edge:
    def __init__(self, coordinates, fill_color='black'):
        self.coordinates = coordinates
        self.fill_color = fill_color

class Wall(Edge):
    def __init__(self, coordinates, fill_color='black'):
        super().__init__(coordinates, fill_color)

class Boundary(Edge):
    def __init__(self, coordinates, fill_color='green'):
        super().__init__(coordinates, fill_color)

class Path(Edge):
    def __init__(self, coordinates, fill_color='red'):
        super().__init__(coordinates, fill_color)


class Graph:
    def __init__(self):
        self.graph = {}
    def add_edge(self, u, v):
        if u not in self.graph:
            self.graph[u] = set()
        if v not in self.graph:
            self.graph[v] = set()
        self.graph[u].add(v)
        self.graph[v].add(u)

    def edge_exists(self, u, v):
        if u in self.graph and v in self.graph:
            return (v in self.graph[u]) and (u in self.graph[v])
        return False

    def list_edges(self):
        edges = set()
        for u in self.graph:
            if self.graph[u]:
                for v in self.graph[u]:
                    edges.add((u, v))

        return sorted(list(edges))
class Lattice:
    def __init__(self, width, height, step):
        self.width = width
        self.height = height
        self.step = step
        self.horizontal_lines = []
        self.vertical_lines = []
        self.hash_table = {}
        self.path_hash_table = {}
        self.grid = Graph()
        self.paths = Graph()

        maximum_length = width if width < height else height

        print(maximum_length)

        for x in range(self.step, maximum_length - self.step, self.step):
            self.horizontal_lines.append(VerticalLine(x))
            self.vertical_lines.append(HorizontalLine(x))

        if len(self.horizontal_lines) % 2 == 0:
            self.horizontal_lines = self.horizontal_lines[0:-1]

        if len(self.vertical_lines) % 2 == 0:
            self.vertical_lines = list(self.vertical_lines[0:-1])

        print(len(self.horizontal_lines))
        print(len(self.vertical_lines))

        for i in range(0, len(self.horizontal_lines), 2):
            for j in range(0, len(self.vertical_lines), 2):
                if (i < len(self.horizontal_lines)) and (j < len(self.vertical_lines)):
                    point = self.horizontal_lines[i].get_intersection(self.vertical_lines[j])
                    is_boundary = i == 0 or j == 0 or i == len(self.horizontal_lines) - 1 or j == len(self.vertical_lines) - 1
                    maze_vertex = MazeVertex(i, j, point, is_boundary)
                    self.hash_table[maze_vertex.id] = maze_vertex
                    if f"{i - 2},{j}" in self.hash_table:
                        self.grid.add_edge(maze_vertex.id, self.hash_table[f"{i - 2},{j}"].id)
                    if f"{i},{j - 2}" in self.hash_table:
                        self.grid.add_edge(maze_vertex.id, self.hash_table[f"{i},{j - 2}"].id)
        for i in range(0, len(self.horizontal_lines)):
            for j in range(0, len(self.vertical_lines)):
                if f"{i},{j}" in self.hash_table:
                    continue
                point = self.horizontal_lines[i].get_intersection(self.vertical_lines[j])
                is_boundary = i == 0 or j == 0 or i == len(self.horizontal_lines) - 1 or j == len(self.vertical_lines) - 1
                path_vertex = MazeVertex(i, j, point, is_boundary)
                self.path_hash_table[path_vertex.id] = path_vertex
                if f"{i - 1},{j}" in self.path_hash_table:
                    self.paths.add_edge(path_vertex.id, self.path_hash_table[f"{i - 1},{j}"].id)
                if f"{i},{j - 1}" in self.path_hash_table:
                    self.paths.add_edge(path_vertex.id, self.path_hash_table[f"{i},{j - 1}"].id)


    def get_grid_drawing_coordinates(self):
        edges = self.grid.list_edges()

        coordinates = list()
        for edge in edges:
            if self.hash_table[edge[0]].is_boundary and self.hash_table[edge[1]].is_boundary:
                coordinates.append(Boundary(self.hash_table[edge[0]].get_drawing_coordinates() + self.hash_table[edge[1]].get_drawing_coordinates()))
            else:
                coordinates.append(Wall(self.hash_table[edge[0]].get_drawing_coordinates() + self.hash_table[edge[1]].get_drawing_coordinates()))

        return coordinates

    def get_path_drawing_coordinates(self):
        edges = self.paths.list_edges()

        coordinates = list()
        for edge in edges:
            coordinates.append(Path(self.path_hash_table[edge[0]].get_drawing_coordinates() + self.path_hash_table[edge[1]].get_drawing_coordinates()))

        return coordinates