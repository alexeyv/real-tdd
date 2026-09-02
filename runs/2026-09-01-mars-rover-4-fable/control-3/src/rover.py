"""Rover that executes command strings and learns obstacles by bumping."""

from __future__ import annotations

from collections.abc import Collection
from dataclasses import dataclass
from enum import Enum

from .planet import Heading, Planet, Position

_COMMANDS = frozenset("FBLR")


class Outcome(Enum):
    COMPLETED = "completed"
    BLOCKED = "blocked"
    REFUSED = "refused"


@dataclass(frozen=True)
class Report:
    """Outcome of one command string.

    ``obstacle`` is the obstacle hit for BLOCKED, the known obstacle that would
    have been hit for REFUSED, and None for COMPLETED. On REFUSED, ``position``
    and ``heading`` are unchanged from before the command.
    """

    position: Position
    heading: Heading
    outcome: Outcome
    obstacle: Position | None = None


@dataclass(frozen=True)
class _Simulation:
    position: Position
    heading: Heading
    obstacle: Position | None


class Rover:
    def __init__(self, planet: Planet, position: Position, heading: Heading) -> None:
        if not planet.contains(position):
            raise ValueError(f"start position {position} is outside the grid")
        if position in planet.obstacles:
            raise ValueError(f"start position {position} is on an obstacle")
        self._planet = planet
        self._position = position
        self._heading = heading
        self._discovered: list[Position] = []

    @property
    def position(self) -> Position:
        return self._position

    @property
    def heading(self) -> Heading:
        return self._heading

    @property
    def discovered_obstacles(self) -> tuple[Position, ...]:
        return tuple(self._discovered)

    def execute(self, commands: str) -> Report:
        unknown = [c for c in commands if c not in _COMMANDS]
        if unknown:
            raise ValueError(f"unknown command(s): {''.join(unknown)!r}")

        # Prediction: only what the rover has learned so far.
        predicted = self._simulate(commands, self._discovered)
        if predicted.obstacle is not None:
            return Report(self._position, self._heading, Outcome.REFUSED, predicted.obstacle)

        # Execution: against the real planet.
        actual = self._simulate(commands, self._planet.obstacles)
        self._position = actual.position
        self._heading = actual.heading
        if actual.obstacle is None:
            return Report(self._position, self._heading, Outcome.COMPLETED)
        if actual.obstacle not in self._discovered:
            self._discovered.append(actual.obstacle)
        return Report(self._position, self._heading, Outcome.BLOCKED, actual.obstacle)

    def _simulate(self, commands: str, obstacles: Collection[Position]) -> _Simulation:
        """Run ``commands`` from the current state, stopping at the first
        move whose target is in ``obstacles``. Does not mutate the rover."""
        position, heading = self._position, self._heading
        for command in commands:
            if command == "L":
                heading = heading.turn_left()
            elif command == "R":
                heading = heading.turn_right()
            else:
                move_heading = heading if command == "F" else heading.opposite
                new_position, new_heading = self._planet.step(position, move_heading)
                if new_position in obstacles:
                    return _Simulation(position, heading, new_position)
                position = new_position
                # Un-flip for B so heading changes only when a pole was crossed.
                heading = new_heading if command == "F" else new_heading.opposite
        return _Simulation(position, heading, None)
