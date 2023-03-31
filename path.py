import math

class Path:
    __slots__ = "__angle", "__start_pos", "__end_pos", "__pivot", "__radius", "__start_theta"
    def __init__(self, start_pos, end_pos, angle):
        # Angle is in radians. negative is counterclockwise.
        self.__angle = angle
        self.__start_pos = start_pos
        self.__end_pos = end_pos
        if angle != 0:
            # If angle is 0 the path is a line
            self.__calculate_arc_details()
    
    def dist_to_point(self, dist):
        """Gets the point on the path that is the given distance from the start."""
        if self.__angle == 0:
            (a_x, a_y) = self.__start_pos
            (b_x, b_y) = self.__end_pos
            c_x = a_x + dist * (b_x - a_x)
            c_y = a_y + dist * (b_y - a_y)
            return (c_x, c_y)
        else:
            (p_x, p_y) = self.__pivot
            # theta = arc_length * 2 * pi / circumference = arc_length / radius
            theta = dist / self.__radius
            return (p_x + math.cos(theta), p_y + math.sin(theta))
    def point_to_dist(self, point):
        """Gets how far the point is along the direction of the path."""
        (a_x, a_y) = self.__start_pos
        (b_x, b_y) = self.__end_pos
        (c_x, c_y) = point
        if self.__angle == 0:
            if a_y == b_y:
                return (c_x, a_y)
            elif a_x == b_x:
                return (a_x, c_y)
            else:
                x = (((a_x - b_x) / (b_y - a_y) * c_x - c_y + (a_y - b_y) / (b_x - a_x) * a_x + a_y)
                    / ((a_x - b_x) / (b_y - a_y) + (a_y - b_y) / (b_x - a_x)))
                y = (b_y - a_y) / (b_x - a_x) * x + (a_y - b_y) / (b_x - b_y) * a_x + a_y
                return (x, y)
        else:
            return ((math.atan2(c_y - self.__pivot[1], a_x - self.__pivot[0]) - self.__start_theta)
                * self.__radius)
    def get_angle(self):
        return self.__angle
    def get_radius(self):
        return self.__radius
    
    def __calculate_arc_details(self):
        """Calculates the center and radius of the arc segment that is the path."""
        (a_x, a_y) = self.__end_pos
        (b_x, b_y) = self.__start_pos
        # let d be the distance between a and b
        d = math.sqrt((a_x - b_x) ** 2 + (a_y - b_y) ** 2)
        # let l be the distance between c and p
        l = d / (2 * math.tan(self.__angle / 2))
        # let c be the midpoint of segment ab
        c_x = (a_x + b_x) / 2
        c_y = (a_y + b_y) / 2
        # Selector determines which pivot (there are two possible) to pick
        selector = 1 if self.__angle > 0 else -1
        if b_y == a_y:
            # Special case, calculating m_cp would divide by zero
            p_x = c_x
            p_y = c_y + selector * l
        else:
            # let m_cp be the slope of segment cp
            m_cp = (a_x - b_x) / (b_y - a_y)
            # let p be the pivot
            p_x = c_x + selector * math.sqrt(l ** 2 / (1 + m_cp ** 2))
            p_y = m_cp * (p_x - c_x) + c_y
        
        self.__pivot = (p_x, p_y)
        self.__radius = d / (2 * math.sin(self.__angle / 2))
        self.__start_theta = math.atan2(a_y - p_y, a_x - p_x)
