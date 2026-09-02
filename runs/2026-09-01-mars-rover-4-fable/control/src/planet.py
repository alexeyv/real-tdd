"""The planet: a rectangular map of a sphere with fixed obstacles.

Coordinates are zero-based. ``x`` is longitude and runs east; ``y`` is
latitude and runs north, so row 0 is the south pole row and row
``height - 1`` is the north pole row. Longitude wraps. Latitude does not:
a move off a pole row crosses the pole instead (see ``Planet.step``).
"""

from __future__ import annotations

from dataclasses import dataclass

Position = tuple[int, int]

# Clockwise order, so turning right is +1 and turning left is -1.
HEADINGS = ("N", "E", "S", "W")

_VECTORS = {"N": (0, 1), "E": (1, 0), "S": (0, -1), "W": (-1, 0)}


def opposite(heading: str) -> str:
    return HEADINGS[(HEADINGS.index(heading) + 2) % 4]


def turned(heading: str, quarter_turns: int) -> str:
    return HEADINGS[(HEADINGS.index(heading) + quarter_turns) % 4]


@dataclass(frozen=True)
class Planet:
    width: int
    height: int
    obstacles: frozenset[Position] = frozenset()

    def __post_init__(self) -> None:
        if self.width <= 0 or self.height <= 0:
            raise ValueError(f"planet must have positive size, got {self.width}x{self.height}")
        if self.width % 2 != 0:
            raise ValueError(f"width must be even so the far side of a pole exists, got {self.width}")
        obstacles: list[Position] = []
        for obstacle in self.obstacles:
            if len(obstacle) != 2:
                raise ValueError(f"obstacle {obstacle!r} must be an (x, y) pair")
            position = (obstacle[0], obstacle[1])
            if not self._contains(self.width, self.height, position):
                raise ValueError(f"obstacle {position} is outside the {self.width}x{self.height} planet")
            obstacles.append(position)
        # Accept any iterable of pairs at construction and normalise to a frozenset.
        object.__setattr__(self, "obstacles", frozenset(obstacles))

    @staticmethod
    def _contains(width: int, height: int, position: Position) -> bool:
        x, y = position
        return 0 <= x < width and 0 <= y < height

    def contains(self, position: Position) -> bool:
        return self._contains(self.width, self.height, position)

    def has_obstacle(self, position: Position) -> bool:
        return position in self.obstacles

    def step(self, position: Position, heading: str, forward: bool = True) -> tuple[Position, str]:
        """Where one square of travel lands, and the heading afterwards.

        Pure geometry: obstacles are not consulted. Travel direction is
        ``heading`` when ``forward`` is true and its opposite otherwise, as
        a backward move crosses a pole the way a forward move in the
        opposite heading would. Crossing a pole keeps the rover on the pole
        row, shifts it half the width in longitude, and turns it to face
        away from the pole, which is the opposite of the travel direction.
        """
        travel = heading if forward else opposite(heading)
        dx, dy = _VECTORS[travel]
        x, y = position
        north_pole_row = self.height - 1
        if (dy > 0 and y == north_pole_row) or (dy < 0 and y == 0):
            return ((x + self.width // 2) % self.width, y), opposite(travel)
        return ((x + dx) % self.width, y + dy), heading
