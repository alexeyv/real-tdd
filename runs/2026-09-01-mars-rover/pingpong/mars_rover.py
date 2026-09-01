COMPASS = ("N", "E", "S", "W")
TURNS = {"L": -1, "R": 1}
STEPS = {"N": (0, 1), "E": (1, 0), "S": (0, -1), "W": (-1, 0)}
SENSES = {"F": 1, "B": -1}
ABOUT_FACE = 2


class Rover:
    def __init__(self, width, height, x, y, heading, obstacles=()):
        self.width = width
        self.height = height
        self.position = (x, y)
        self.heading = heading
        self.terrain = frozenset(obstacles)
        self.stopped_by = None
        self.discovered_obstacles = ()

    def execute(self, commands):
        self.stopped_by = None
        known = self._known_obstacle_ahead(commands)
        if known is not None:
            self.stopped_by = known
            return
        for command in commands:
            if self._execute_one(command):
                break

    def _execute_one(self, command):
        if command in TURNS:
            self.heading = self._turned(self.heading, TURNS[command])
            return False
        position, heading = self._destination(self.position, self.heading, SENSES[command])
        if position in self.terrain:
            self.stopped_by = position
            self._discover(position)
            return True
        self.position = position
        self.heading = heading
        return False

    def _known_obstacle_ahead(self, commands):
        position, heading = self.position, self.heading
        for command in commands:
            if command in TURNS:
                heading = self._turned(heading, TURNS[command])
                continue
            position, heading = self._destination(position, heading, SENSES[command])
            if position in self.terrain:
                return position if position in self.discovered_obstacles else None
        return None

    def _discover(self, position):
        if position not in self.discovered_obstacles:
            self.discovered_obstacles += (position,)

    def _turned(self, heading, step):
        return COMPASS[(COMPASS.index(heading) + step) % len(COMPASS)]

    def _destination(self, position, heading, sense):
        dx, dy = STEPS[heading]
        x, y = position
        x = (x + dx * sense) % self.width
        y = y + dy * sense
        if not 0 <= y < self.height:
            y = min(max(y, 0), self.height - 1)
            x = self._antipode(x)
            heading = self._turned(heading, ABOUT_FACE)
        return (x, y), heading

    def _antipode(self, x):
        return (x + self.width // 2) % self.width
