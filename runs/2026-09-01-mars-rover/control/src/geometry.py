"""Grid geometry: headings, positions, and the planet the rover drives on.

The planet is the surface of a sphere drawn as a rectangle. Longitude wraps;
latitude does not -- leaving a pole row crosses the pole.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from enum import Enum
from typing import NamedTuple


class Position(NamedTuple):
    """A square on the grid. ``x`` is longitude (east), ``y`` latitude (north)."""

    x: int
    y: int


class Heading(Enum):
    """One of the four compass directions."""

    NORTH = "N"
    EAST = "E"
    SOUTH = "S"
    WEST = "W"

    @classmethod
    def parse(cls, value: str) -> Heading:
        """Build a heading from its letter, case-insensitively."""
        try:
            return cls(value.strip().upper())
        except ValueError:
            raise ValueError(f"unknown heading: {value!r}") from None

    def left(self) -> Heading:
        """The heading ninety degrees counter-clockwise."""
        return _CLOCKWISE[(_CLOCKWISE.index(self) - 1) % 4]

    def right(self) -> Heading:
        """The heading ninety degrees clockwise."""
        return _CLOCKWISE[(_CLOCKWISE.index(self) + 1) % 4]

    def opposite(self) -> Heading:
        """The heading one hundred eighty degrees around."""
        return _CLOCKWISE[(_CLOCKWISE.index(self) + 2) % 4]


_CLOCKWISE = (Heading.NORTH, Heading.EAST, Heading.SOUTH, Heading.WEST)


@dataclass(frozen=True)
class Planet:
    """A rectangular map of a sphere, with obstacles at fixed squares.

    ``width`` must be even so that a pole crossing lands on a real column.
    """

    width: int
    height: int
    obstacles: frozenset[Position] = frozenset()

    def __init__(
        self,
        width: int,
        height: int,
        obstacles: Iterable[tuple[int, int]] = (),
    ) -> None:
        """Build a planet. ``obstacles`` is any iterable of ``(x, y)`` pairs;
        it is drained once and kept as a ``frozenset`` of :class:`Position`.
        """
        if width <= 0 or height <= 0:
            raise ValueError(f"grid must be positive, got {width}x{height}")
        if width % 2 != 0:
            raise ValueError(f"width must be even, got {width}")
        squares = frozenset(Position(*square) for square in obstacles)
        object.__setattr__(self, "width", width)
        object.__setattr__(self, "height", height)
        object.__setattr__(self, "obstacles", squares)
        for square in squares:
            if not self.contains(square):
                raise ValueError(f"obstacle off the grid: {tuple(square)}")

    def contains(self, position: Position) -> bool:
        """Whether ``position`` names a square of this grid."""
        return 0 <= position.x < self.width and 0 <= position.y < self.height

    def has_obstacle(self, position: Position) -> bool:
        """Whether ``position`` holds an obstacle."""
        return position in self.obstacles

    def step(
        self,
        position: Position,
        heading: Heading,
        forward: bool = True,
    ) -> tuple[Position, Heading]:
        """The square and heading after one move from ``position``.

        Obstacles are not consulted -- this is pure geometry. A move that
        leaves a pole row crosses the pole: same row, antipodal longitude,
        and the heading flips north <-> south.
        """
        direction = heading if forward else heading.opposite()

        if direction is Heading.EAST:
            return Position((position.x + 1) % self.width, position.y), heading
        if direction is Heading.WEST:
            return Position((position.x - 1) % self.width, position.y), heading

        at_pole = (direction is Heading.NORTH and position.y == self.height - 1) or (
            direction is Heading.SOUTH and position.y == 0
        )
        if at_pole:
            crossed = Position((position.x + self.width // 2) % self.width, position.y)
            return crossed, heading.opposite()

        offset = 1 if direction is Heading.NORTH else -1
        return Position(position.x, position.y + offset), heading
