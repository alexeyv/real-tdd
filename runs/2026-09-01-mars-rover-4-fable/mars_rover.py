STEP = {"N": (0, 1), "E": (1, 0), "S": (0, -1), "W": (-1, 0)}
LEFT = {"N": "W", "W": "S", "S": "E", "E": "N"}
RIGHT = {after: before for before, after in LEFT.items()}
OPPOSITE = {"N": "S", "S": "N"}
DIRECTION = {"F": 1, "B": -1}


class Rover:
    def __init__(self, width, height, x, y, heading, obstacles=()):
        self.width = width
        self.height = height
        self.obstacles = set(obstacles)
        self.position = (x, y)
        self.heading = heading
        self.blocked_by = None
        self.discovered_obstacles = []

    def execute(self, commands):
        self.blocked_by = None
        _, _, self.refused_by = self._walk(commands, self.discovered_obstacles)
        if self.refused_by is not None:
            return
        self.position, self.heading, self.blocked_by = self._walk(
            commands, self.obstacles
        )
        if self.blocked_by is not None and self.blocked_by not in self.discovered_obstacles:
            self.discovered_obstacles.append(self.blocked_by)

    def _walk(self, commands, obstacles):
        """Run the commands from the rover's current state against a map of
        obstacles. Returns the end position, heading, and the obstacle that
        stopped the walk, or None."""
        position, heading = self.position, self.heading
        for command in commands:
            if command == "L":
                heading = LEFT[heading]
            elif command == "R":
                heading = RIGHT[heading]
            else:
                target, new_heading = self._step(position, heading, DIRECTION[command])
                if target in obstacles:
                    return position, heading, target
                position, heading = target, new_heading
        return position, heading, None

    def _step(self, position, heading, direction):
        x, y = position
        dx, dy = STEP[heading]
        x, y = (x + direction * dx) % self.width, y + direction * dy
        if not 0 <= y < self.height:
            # Crossed a pole: stay on the pole row, come out on the far side.
            y -= direction * dy
            x = (x + self.width // 2) % self.width
            heading = OPPOSITE[heading]
        return (x, y), heading
