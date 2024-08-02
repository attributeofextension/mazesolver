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


class LatticeNode(Point):
    def __init__(self, x, y, point):
        super().__init__(x, y)
        self.point = point
        self.north = None
        self.east = None
        self.south = None
        self.west = None


class Lattice:
    def __init__(self, width, height, step):
        self.width = width
        self.height = height
        self.step = step
        self.horizontal_lines = []
        self.vertical_lines = []
        self.north_west_node = None
        self.south_west_node = None
        self.north_east_node = None
        self.south_east_node = None

        maximum_length = width if width > height else height

        count = 0
        previous_x_node = None
        previous_y_node = None
        previous_slope_node = None
        for x in range(self.step, maximum_length - self.step, self.step):
            self.horizontal_lines.append(VerticalLine(x))
            self.vertical_lines.append(HorizontalLine(x))
            if x == self.step:
                node = LatticeNode(count, count, self.horizontal_lines[count].get_intersection(self.vertical_lines[count]))
                self.north_west_node = node
                previous_x_node = node
                previous_y_node = node
                previous_slope_node = node
                count += 1
                continue
            x_node = LatticeNode(0, count, self.horizontal_lines[count].get_intersection(self.vertical_lines[0]))
            previous_x_node.east = x_node
            x_node.west = previous_x_node
            previous_x_node = x_node

            y_node = LatticeNode(count, 0, self.horizontal_lines[0].get_intersection(self.vertical_lines[count]))
            previous_y_node.south = y_node








