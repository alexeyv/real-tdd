"""Planet geometry: a rectangular grid mapping a sphere with real poles."""

from __future__ import annotations

from collections.abc import Iterable
from enum import Enum

Position = tuple[int, int]


class Heading(Enum):
    N = "N"
    E = "E"
    S = "S"
    W = "W"

    def turn_left(self) -> Heading:
        return _ORDER[(_ORDER.index(self) - 1) % 4]

    def turn_right(self) -> Heading:
        return _ORDER[(_ORDER.index(self) + 1) % 4]

    @property
    def opposite(self) -> Heading:
        return _ORDER[(_ORDER.index(self) + 2) % 4]

    @property
    def delta(self) -> tuple[int, int]:
        return _DELTAS[self]


_ORDER = (Heading.N, Heading.E, Heading.S, Heading.W)
_DELTAS = {
    Heading.N: (0, 1),
    Heading.E: (1, 0),
    Heading.S: (0, -1),
    Heading.W: (-1, 0),
}


class Planet:
    """Grid geometry plus the fixed set of obstacle squares.

    ``x`` is longitude and wraps modulo ``width``. ``y`` is latitude; row 0 is
    the south pole row and row ``height - 1`` the north pole row. Latitude
    never wraps: stepping off a pole row crosses the pole instead.
    """

    def __init__(self, width: int, height: int, obstacles: Iterable[Position] = ()) -> None:
        if width <= 0 or height <= 0:
            raise ValueError("width and height must be positive")
        if width % 2 != 0:
            raise ValueError("width must be even")
        self.width = width
        self.height = height
        self.obstacles: frozenset[Position] = frozenset(obstacles)
        for obstacle in self.obstacles:
            if not self.contains(obstacle):
                raise ValueError(f"obstacle {obstacle} is outside the grid")

    def contains(self, position: Position) -> bool:
        x, y = position
        return 0 <= x < self.width and 0 <= y < self.height

    def step(self, position: Position, heading: Heading) -> tuple[Position, Heading]:
        """Return the position and heading after one step in ``heading``.

        Crossing a pole keeps the rover on the same pole row, shifts longitude
        by half the width, and flips the heading.
        """
        x, y = position
        dx, dy = heading.delta
        new_y = y + dy
        if 0 <= new_y < self.height:
            return ((x + dx) % self.width, new_y), heading
        return ((x + self.width // 2) % self.width, y), heading.opposite
