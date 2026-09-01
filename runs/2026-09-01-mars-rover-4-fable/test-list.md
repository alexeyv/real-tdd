# Test list

Behaviors the finished rover should have, in the task's words. Checked
off as each becomes a test.

## Classic

- [x] A rover created with a position and heading reports that position and heading.
- [x] `F` moves one square forward in the current heading (north increases `y`, east increases `x`).
- [x] `F` moves one square forward when heading E (test written); S and W below.
- [x] `F` moves one square forward when heading S (test written); W below.
- [x] `F` moves one square forward when heading W.
- [x] `B` moves one square backward when heading N (test written).
- [x] `B` moves one square backward when heading E, S, or W. (satisfied by d58031d, not driven: B negates the same step table F uses)
- [x] `L` turns left ninety degrees from N to W (test written).
- [x] `L` turns left ninety degrees from W (W -> S).
- [x] `L` turns left ninety degrees from S and E (S -> E -> N).
- [x] `R` turns right ninety degrees from N (N -> E) (test written).
- [x] `R` turns right ninety degrees from E, S, and W (E -> S -> W -> N).
- [x] The commands in a string are executed in order.
- [x] Moving east off the last column lands on column 0.
- [x] Moving west off column 0 lands on the last column (regression test; passed on first run, satisfied by 5c3e121, not driven).
- [x] If a move would land on an obstacle, the rover does not move (test written).
- [x] If a move would land on an obstacle, the rover abandons the rest of the command string.
- [x] If a move would land on an obstacle, the rover reports where the obstacle is.
- [x] Turning never hits anything, even when an obstacle is adjacent. (regression test; passed on first run, committed in fb63c54, not driven).
- [x] After a command string that hit nothing, the rover reports that it did not stop because of an obstacle.
- [x] A command string that hits nothing clears the report of an earlier obstacle stop.

## Twist 1: the poles are real

- [x] Moving north from the north pole row keeps the rover on the north pole row, at longitude `(x + width / 2) mod width`, heading south.
- [x] Moving south from the south pole row keeps the rover on the south pole row, at longitude `(x + width / 2) mod width`, heading north.
- [x] A backward move across the north pole flips the heading and the longitude the same way a forward crossing does: on the north pole row heading S, `B` ends on the north pole row at the far longitude heading N (test written).
- [x] A backward move across the south pole does the same, mirrored (regression test; passed on first run, satisfied by a9b6465, not driven).
- [x] An obstacle on the far side of a pole stops a pole crossing like any other obstacle. (regression test; passed on first run, committed in fb63c54, not driven).

## Twist 2: the rover learns

- [x] A new rover reports no discovered obstacles.
- [x] An obstacle the rover bumps into is remembered and reported.
- [x] Discovered obstacles are reported in the order they were discovered. (regression test; passed on first run, committed in fb63c54, not driven).
- [x] Bumping into the same obstacle again does not record it twice.
- [x] A command string that would run into a known obstacle is refused as a whole: the rover does not move at all.
- [x] A refused command string reports which known obstacle it would have hit.
- [x] A refused command string does not change the rover's heading either. (regression test; passed on first run, committed in fb63c54, not driven).
- [x] `refused_by` is `None` after a command string that was not refused. (regression test; passed on first run, committed in fb63c54, not driven).
- [x] Turning next to a known obstacle is not refused. (regression test; passed on first run, committed in fb63c54, not driven).
- [x] A command string that would bump an unknown obstacle is not refused; the rover moves up to it and stops there. (regression test; passed on first run, committed in fb63c54, not driven).
