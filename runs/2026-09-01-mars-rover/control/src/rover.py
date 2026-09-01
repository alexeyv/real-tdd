"""The rover: position, heading, and the obstacles it has found the hard way."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .geometry import Heading, Planet, Position


class Outcome(Enum):
    """How a command string ended."""

    COMPLETED = "completed"
    BLOCKED = "blocked"
    REFUSED = "refused"


@dataclass(frozen=True)
class Report:
    """What the rover reports after a command string.

    ``obstacle`` is the square that stopped it, or ``None`` when the whole
    string ran.
    """

    outcome: Outcome
    position: Position
    heading: Heading
    obstacle: Position | None = None

    @property
    def stopped(self) -> bool:
        """Whether an obstacle stood in the way -- bumped or foreseen.

        True for both a string cut short partway and one refused before it
        began, so it says nothing about how much of the string ran.
        """
        return self.outcome is not Outcome.COMPLETED


_TURNS = {"L": Heading.left, "R": Heading.right}
_MOVES = {"F": True, "B": False}


class Rover:
    """A rover driving a :class:`Planet` it has no map of."""

    def __init__(
        self,
        planet: Planet,
        position: tuple[int, int],
        heading: Heading | str,
    ) -> None:
        start = Position(*position)
        if not planet.contains(start):
            raise ValueError(f"start position off the grid: {tuple(start)}")
        self._planet = planet
        self._position = start
        self._heading = heading if isinstance(heading, Heading) else Heading.parse(heading)
        self._discovered: list[Position] = []

    @property
    def position(self) -> Position:
        """The square the rover is on."""
        return self._position

    @property
    def heading(self) -> Heading:
        """The direction the rover faces."""
        return self._heading

    @property
    def discovered_obstacles(self) -> tuple[Position, ...]:
        """Obstacles bumped into so far, in discovery order, without repeats."""
        return tuple(self._discovered)

    def execute(self, commands: str) -> Report:
        """Run a command string and report the result.

        The string is first replayed against the obstacles already known. If
        that replay bumps into one, nothing runs at all and the outcome is
        ``REFUSED``. Otherwise the string runs for real, where an obstacle the
        rover has never met can still stop it partway -- and teach it.
        """
        parsed = self._parse(commands)

        foreseen = self._simulate(parsed)
        if foreseen is not None:
            return Report(Outcome.REFUSED, self._position, self._heading, foreseen)

        for command in parsed:
            turn = _TURNS.get(command)
            if turn is not None:
                self._heading = turn(self._heading)
                continue

            target, heading = self._planet.step(
                self._position, self._heading, forward=_MOVES[command]
            )
            if self._planet.has_obstacle(target):
                self._learn(target)
                return Report(Outcome.BLOCKED, self._position, self._heading, target)
            self._position, self._heading = target, heading

        return Report(Outcome.COMPLETED, self._position, self._heading)

    def _parse(self, commands: str) -> list[str]:
        """Normalise a command string, rejecting anything that is not FBLR.

        Each character is judged on its own: uppercasing the string first
        would let a ligature such as ``'ﬀ'`` expand into two commands the
        caller never wrote. The error names the character as typed.
        """
        parsed = []
        for index, command in enumerate(commands):
            upper = command.upper()
            if len(upper) != 1 or (upper not in _TURNS and upper not in _MOVES):
                raise ValueError(f"unknown command {command!r} at index {index}")
            parsed.append(upper)
        return parsed

    def _simulate(self, commands: list[str]) -> Position | None:
        """The first known obstacle the string would hit, or ``None``."""
        position, heading = self._position, self._heading
        known = set(self._discovered)

        for command in commands:
            turn = _TURNS.get(command)
            if turn is not None:
                heading = turn(heading)
                continue

            target, heading_after = self._planet.step(
                position, heading, forward=_MOVES[command]
            )
            if target in known:
                return target
            position, heading = target, heading_after

        return None

    def _learn(self, obstacle: Position) -> None:
        """Remember an obstacle, once."""
        if obstacle not in self._discovered:
            self._discovered.append(obstacle)
