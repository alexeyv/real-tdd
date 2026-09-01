# Mars Rover, with two twists

Implement a Mars rover in Python 3 with pytest. Single package, no
dependencies beyond the standard library and pytest.

## The classic part

- The planet is a rectangular grid, `width` columns by `height` rows,
  given when the rover is created. Positions are zero-based. `x` is
  longitude and runs east; `y` is latitude and runs north, so row 0 is the
  south pole row and row `height - 1` is the north pole row.
- The rover has a position and a heading, one of N, E, S, W. Both are
  given at creation.
- The rover accepts a string of commands and executes them in order:
  `F` moves one square forward in the current heading, `B` one square
  backward, `L` turns left ninety degrees, `R` turns right ninety degrees.
- Longitude wraps: moving east off the last column lands on column 0, and
  the reverse.
- The planet has obstacles at fixed squares. If a move would land on an
  obstacle, the rover does not move, abandons the rest of the command
  string, and reports where the obstacle is. Turning never hits anything.
- After any command string the rover can report its position and heading,
  and whether it stopped because of an obstacle and which one.

## Twist 1: the poles are real

The grid is a map of a sphere, not a torus. Moving north from the north
pole row does not wrap to the south pole row. The rover crosses the pole:
it is still on the north pole row afterwards, at the longitude on the far
side of the pole (`x + width / 2`, modulo `width`), and it is now heading
south. The same happens at the south pole row, mirrored. Backward moves
cross the pole the same way a forward move in the opposite heading would.
Assume `width` is even.

## Twist 2: the rover learns

The rover is not told where the obstacles are. It starts with no map and
discovers obstacles by bumping into them. Every obstacle it bumps into is
remembered, and the rover can be asked at any time for the obstacles it
has discovered, in the order it discovered them. Bumping into the same
obstacle again does not record it twice.

Known and unknown obstacles behave differently. An unknown obstacle is
discovered the classic way: the rover moves up to it, bumps, stops, and
learns. A command string that the rover can tell in advance would bump
into an obstacle it already knows about is refused as a whole: the rover
does not move at all, and it reports which known obstacle it would have
hit. Turning is fine either way.

## Done

The run is over when the test list is empty and the human has read the
journal. Interface, module layout, and report formats are yours to decide
through the tests. The task statement is deliberately silent on them.

## Answer from the human, turn 22

A rover that has not run a command string yet reports no obstacle, the
same as one whose last command string hit nothing. Every report the
rover makes is readable at any time, including before the first command.
Option (a).
