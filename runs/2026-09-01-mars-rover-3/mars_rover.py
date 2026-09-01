class Rover:
    # The headings in clockwise order, each with the step a forward move
    # takes. Turning walks this order, so it is not free to be rearranged.
    _FORWARD_STEP = {"N": (0, 1), "E": (1, 0), "S": (0, -1), "W": (-1, 0)}
    _CLOCKWISE = tuple(_FORWARD_STEP)
    _SQUARES_FORWARD = {"F": 1, "B": -1}
    _QUARTER_TURNS_CLOCKWISE = {"L": -1, "R": 1}

    def __init__(self, width, height, x, y, heading, obstacles=()):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.heading = heading
        self.obstacles = obstacles
        self.discovered_obstacles = ()
        self.blocked_by = None

    def execute(self, commands):
        *_, stopped_by = self._walk(commands, self.discovered_obstacles)
        if stopped_by is None:
            self.x, self.y, self.heading, stopped_by = self._walk(
                commands, self.obstacles
            )
            if stopped_by is not None:
                self._discover(stopped_by)
        self.blocked_by = stopped_by

    def _walk(self, commands, obstacles):
        """Where the commands take the rover, and the obstacle that stopped it."""
        x, y, heading = self.x, self.y, self.heading
        for command in commands:
            if command in self._QUARTER_TURNS_CLOCKWISE:
                heading = self._turned(heading, self._QUARTER_TURNS_CLOCKWISE[command])
            elif command in self._SQUARES_FORWARD:
                moved_x, moved_y, moved_heading = self._destination(
                    x, y, heading, self._SQUARES_FORWARD[command]
                )
                if (moved_x, moved_y) in obstacles:
                    return x, y, heading, (moved_x, moved_y)
                x, y, heading = moved_x, moved_y, moved_heading
        return x, y, heading, None

    def _destination(self, x, y, heading, squares_forward):
        step_x, step_y = self._FORWARD_STEP[heading]
        new_x = (x + squares_forward * step_x) % self.width
        new_y = y + squares_forward * step_y
        if not 0 <= new_y < self.height:
            new_x = (new_x + self.width // 2) % self.width
            new_y = y
            heading = self._turned(heading, 2)
        return new_x, new_y, heading

    def _discover(self, obstacle):
        if obstacle not in self.discovered_obstacles:
            self.discovered_obstacles += (obstacle,)

    @classmethod
    def _turned(cls, heading, quarter_turns_clockwise):
        cycle = cls._CLOCKWISE
        position = cycle.index(heading) + quarter_turns_clockwise
        return cycle[position % len(cycle)]
