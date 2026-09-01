FORWARD_STEP = {"N": (0, 1), "S": (0, -1), "E": (1, 0), "W": (-1, 0)}
LEFT_OF = {"N": "W", "W": "S", "S": "E", "E": "N"}
RIGHT_OF = {left: heading for heading, left in LEFT_OF.items()}
MOVE_SIGN = {"F": 1, "B": -1}
BEHIND = {"N": "S", "S": "N"}


class Rover:
    def __init__(self, width, height, x, y, heading, obstacles=()):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.heading = heading
        self.obstacles = obstacles
        self.blocked_by = None
        self.discovered = []

    def execute(self, commands):
        self.blocked_by = self._first_obstacle_on(commands, self.discovered)
        if self.blocked_by is not None:
            return
        for command in commands:
            x, y, heading = self._after(self.x, self.y, self.heading, command)
            if (x, y) in self.obstacles:
                self.blocked_by = (x, y)
                if (x, y) not in self.discovered:
                    self.discovered.append((x, y))
                return
            self.x, self.y, self.heading = x, y, heading

    def _first_obstacle_on(self, commands, obstacles):
        x, y, heading = self.x, self.y, self.heading
        for command in commands:
            x, y, heading = self._after(x, y, heading, command)
            if (x, y) in obstacles:
                return (x, y)
        return None

    def _after(self, x, y, heading, command):
        if command == "L":
            return x, y, LEFT_OF[heading]
        if command == "R":
            return x, y, RIGHT_OF[heading]
        step_x, step_y = FORWARD_STEP[heading]
        sign = MOVE_SIGN[command]
        next_x = x + sign * step_x
        next_y = y + sign * step_y
        if not 0 <= next_y < self.height:
            return (next_x + self.width // 2) % self.width, y, BEHIND[heading]
        return next_x % self.width, next_y, heading
