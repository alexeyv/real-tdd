"""The rover: executes command strings and learns obstacles by bumping."""

from __future__ import annotations

from dataclasses import dataclass

from mars_rover.planet import HEADINGS, Planet, Position, turned

COMMANDS = frozenset("FBLR")


@dataclass(frozen=True)
class Report:
    """Outcome of one ``Rover.execute`` call.

    ``blocked_by`` is the obstacle that ended the run, or None when every
    command ran. ``refused`` is True when the rover predicted a bump into an
    obstacle it already knew and therefore did not move at all; otherwise
    the rover moved up to ``blocked_by`` and stopped there.

    ``stopped_by_obstacle`` is True in both cases: a refusal counts as
    stopping because of an obstacle. Check ``refused`` to tell them apart.
    """

    position: Position
    heading: str
    blocked_by: Position | None = None
    refused: bool = False

    @property
    def stopped_by_obstacle(self) -> bool:
        return self.blocked_by is not None


class Rover:
    def __init__(self, planet: Planet, x: int, y: int, heading: str) -> None:
        if heading not in HEADINGS:
            raise ValueError(f"heading must be one of {HEADINGS}, got {heading!r}")
        if not planet.contains((x, y)):
            raise ValueError(f"({x}, {y}) is outside the {planet.width}x{planet.height} planet")
        self._planet = planet
        self._position: Position = (x, y)
        self._heading = heading
        self._discovered: list[Position] = []

    @property
    def position(self) -> Position:
        return self._position

    @property
    def heading(self) -> str:
        return self._heading

    def __repr__(self) -> str:
        return (
            f"Rover(position={self._position}, heading={self._heading!r}, "
            f"discovered_obstacles={self._discovered})"
        )

    def discovered_obstacles(self) -> list[Position]:
        """Obstacles bumped into so far, in discovery order, each once."""
        return list(self._discovered)

    def execute(self, commands: str) -> Report:
        """Run ``commands`` in order and report where the rover ended up.

        Commands are exactly the characters ``F``, ``B``, ``L`` and ``R``;
        anything else, including lowercase letters and whitespace, raises
        ValueError before the rover moves.
        """
        unknown = sorted(set(commands) - COMMANDS)
        if unknown:
            raise ValueError(f"unknown command(s) {unknown}; use only F, B, L, R")

        known_hit = self._predict_known_bump(commands)
        if known_hit is not None:
            return Report(self._position, self._heading, blocked_by=known_hit, refused=True)

        for command in commands:
            if command in "LR":
                self._heading = turned(self._heading, 1 if command == "R" else -1)
                continue
            target, heading_after = self._planet.step(self._position, self._heading, forward=command == "F")
            if self._planet.has_obstacle(target):
                # A known obstacle on the path is refused above, so this is
                # always a new discovery; the check only guards the invariant.
                if target not in self._discovered:
                    self._discovered.append(target)
                return Report(self._position, self._heading, blocked_by=target)
            self._position, self._heading = target, heading_after

        return Report(self._position, self._heading)

    def _predict_known_bump(self, commands: str) -> Position | None:
        """Walk the commands against the rover's own map; first known obstacle hit, or None."""
        position, heading = self._position, self._heading
        for command in commands:
            if command in "LR":
                heading = turned(heading, 1 if command == "R" else -1)
                continue
            target, heading = self._planet.step(position, heading, forward=command == "F")
            if target in self._discovered:
                return target
            position = target
        return None
