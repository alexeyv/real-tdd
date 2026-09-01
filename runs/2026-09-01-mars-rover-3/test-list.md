# Test list

Behaviors the finished code should have, in the task's words. Checked off
as they become tests. Add to this list whenever a new behavior comes to
mind; nothing may be built that is not on it.

## The classic part

- [x] The rover is created with a rectangular grid `width` columns by `height` rows
- [x] The rover is created with a position and a heading, one of N, E, S, W
- [x] The rover reports its position and heading
- [x] `F` moves one square forward in the current heading
- [x] `B` moves one square backward
- [x] `F` while heading south moves one square south
- [x] `F` while heading west moves one square west
- [x] `L` turns left ninety degrees
- [x] `R` turns right ninety degrees
- [x] Moving north increases latitude (row 0 is the south pole row, row `height - 1` the north pole row)
- [x] Moving east increases longitude
- [x] A command string is executed in order, one command after another
- [x] Longitude wraps: moving east off the last column lands on column 0
- [x] Longitude wraps the other way: moving west off column 0 lands on the last column — satisfied by 1222798, not driven
- [x] A move that would land on an obstacle does not happen: the rover does not move
- [x] A move that would land on an obstacle abandons the rest of the command string
- [x] After hitting an obstacle the rover reports that it stopped because of an obstacle, and which one
- [x] After a command string with no obstacle the rover reports that it did not stop because of an obstacle
- [x] Turning never hits anything

## Twist 1: the poles are real

- [x] Moving north off the north pole row does not wrap to the south pole row
- [x] Moving north off the north pole row leaves the rover on the north pole row, at longitude `x + width / 2` modulo `width`, heading south
- [x] Moving south off the south pole row leaves the rover on the south pole row, at longitude `x + width / 2` modulo `width`, heading north
- [x] A backward move crosses the pole the way a forward move in the opposite heading would
- [x] An obstacle on the far side of the pole stops the pole crossing like any other obstacle

## Twist 2: the rover learns

- [x] A rover that has not run a command string yet reports no obstacle (added turn 16; ruled in scope by the human at turn 22)
- [x] The rover starts with no map: asked for discovered obstacles before it moves, it has none
- [x] An obstacle the rover has not discovered is discovered the classic way: the rover moves up to it, bumps, stops, and learns it
- [x] The rover can be asked at any time for the obstacles it has discovered — demonstrated before the first move and after a bump, by the tests of turns 17 and 18
- [x] Discovered obstacles come back in the order they were discovered
- [x] Bumping into the same obstacle again does not record it twice
- [x] A command string that would bump into an obstacle the rover already knows about is refused as a whole: the rover does not move at all
- [x] A refused command string reports which known obstacle the rover would have hit
- [x] Turning is fine either way: a command string of turns alone is never refused
