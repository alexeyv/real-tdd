# Test list

Behaviors the finished code should have, in the words of `task.md`.
Checked off when a test exists for them.

## The classic part

- [x] The rover is created with a planet `width` columns by `height` rows,
      a position, and a heading, and can report its position and heading.
- [x] `F` moves one square forward in the current heading.
- [x] `B` moves one square backward.
- [x] `L` turns left ninety degrees.
- [x] `R` turns right ninety degrees.
- [x] Turning left four times returns the rover to its original heading;
      likewise turning right.
- [x] A string of commands is executed in order.
- [x] An empty command string leaves the rover where it was.
- [x] `y` runs north: moving north raises `y`, moving south lowers it.
- [x] `x` runs east: moving east raises `x`, moving west lowers it.
- [x] Longitude wraps: moving east off the last column lands on column 0.
- [x] Longitude wraps in reverse: moving west off column 0 lands on the
      last column.
- [x] A move that would land on an obstacle leaves the rover where it was.
- [x] A move blocked by an obstacle abandons the rest of the command string.
- [x] After a blocked command string the rover reports that it stopped
      because of an obstacle, and which one.
- [x] After a command string that was not blocked the rover reports that it
      did not stop because of an obstacle.
- [x] A rover that was blocked, and then runs a command string that is not
      blocked, no longer reports an obstacle.
- [x] Turning never hits anything, even facing an obstacle.

## Twist 1: the poles are real

- [x] Moving north from the north pole row does not wrap to the south pole
      row: the rover stays on the north pole row.
- [x] Crossing the north pole puts the rover at longitude `x + width / 2`
      modulo `width`.
- [x] Crossing the north pole leaves the rover heading south.
- [x] Moving south from the south pole row crosses the south pole,
      mirrored: same row, longitude on the far side, now heading north.
- [x] A backward move off the north pole row crosses the pole the same way
      a forward move in the opposite heading would.
- [x] A backward move off the south pole row crosses the pole the same way
      a forward move in the opposite heading would.
- [x] An obstacle on the far side of the pole blocks a pole crossing.

## Twist 2: the rover learns

- [x] A new rover has discovered no obstacles.
- [x] An obstacle the rover bumps into is remembered as discovered.
- [x] The rover reports discovered obstacles in the order it discovered them.
- [x] Bumping into the same obstacle again does not record it twice.
- [x] A command string that would bump into an obstacle the rover already
      knows about is refused as a whole: the rover does not move at all.
- [x] After refusing a command string the rover reports which known
      obstacle it would have hit.
- [x] A command string is refused for a known obstacle it would hit part
      way through, not only on the first move.
- [x] A command string whose known-obstacle collision is avoided by a turn
      or a wrap is not refused.
- [x] A command string of only turns is never refused, even next to a
      known obstacle.
- [x] After a refusal the discovered obstacles are unchanged.
- [x] A known obstacle reached only by wrapping round the planet is seen in
      advance, like any other. (added turn 27)
