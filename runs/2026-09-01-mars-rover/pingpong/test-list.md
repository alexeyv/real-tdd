# Test list — Mars Rover

Behaviors the finished rover should exhibit, in the problem's words.
Either session may add items at any time. Check items off when their
test exists.

## Creation and reporting
- [x] A new rover reports the position and heading it was created with
- [x] After a command string with no obstacle, the rover reports that it did not stop for an obstacle

## Turning
- [x] `L` from N heads W
- [x] `L` from W heads S
- [x] `L` from S heads E, from E heads N (regression; the compass cycle answered it; passed on arrival)
- [x] `R` from N heads E
- [x] `R` from E heads S, from S heads W, from W heads N (regression; same cycle; passed on arrival)
- [x] Turning does not change position (regression; passed on arrival)

## Moving
- [x] `F` heading N increases y by one
- [x] `F` heading E increases x by one
- [x] `F` heading S decreases y by one
- [x] `F` heading W decreases x by one
- [x] `B` moves one square opposite to the heading, heading unchanged
- [x] A command string executes in order: `FFRFF` from (0,0) N ends at (2,2) E

## Longitude wraps
- [x] `F` heading E from the last column lands on column 0
- [x] `F` heading W from column 0 lands on the last column (regression; the modulo answered it; passed on arrival)
- [x] `B` wraps the same way (regression; passed on arrival)

## The poles are real (twist 1)
- [x] `F` heading N from the north pole row stays on that row, x becomes (x + width/2) mod width, heading becomes S
- [x] `F` heading S from the south pole row stays on row 0, x becomes (x + width/2) mod width, heading becomes N
- [x] `B` heading S from the north pole row crosses the north pole the way `F` heading N would: same row, far-side longitude, and heading flipped to N (regression; the crossing is computed from the destination; passed on arrival)
- [x] `B` heading N from the south pole row crosses the south pole (regression; passed on arrival)
- [x] Crossing the pole twice returns to the original longitude (regression; passed on arrival)
- [x] Longitude wrap and pole crossing compose: crossing at x near the wrap edge lands at the right modulo (regression; passed on arrival)

## Obstacles, unknown (classic behavior)
- [x] Moving `F` into an unknown obstacle: rover stays put
- [x] Moving `F` into an unknown obstacle: rover reports it was stopped by that obstacle
- [x] Moving `B` into an unknown obstacle behaves the same (regression; passed on arrival)
- [x] After bumping, the rest of the command string is abandoned
- [x] Commands before the bump are executed (position reflects them) (regression; passed on arrival)
- [x] An obstacle on the far side of a pole crossing is hit at the crossed-to square (regression; passed on arrival)
- [x] An obstacle across the longitude wrap is hit at the wrapped-to square (regression; passed on arrival)
- [x] Turning next to an obstacle never bumps (regression; passed on arrival)

## The rover learns (twist 2)
- [x] A new rover has discovered no obstacles
- [x] After bumping, the rover lists that obstacle as discovered
- [x] Discovered obstacles are listed in discovery order (regression; passed on arrival)
- [x] Bumping the same obstacle twice lists it once
- [x] A command string that would bump a known obstacle is refused whole: position unchanged
- [x] A refused command string leaves the heading unchanged too, turns included (regression; passed on arrival)
- [x] A refused command string reports which known obstacle it would have hit
- [x] Refusal looks ahead past turns and wraps and pole crossings (the known obstacle is several commands in) (regression; passed on arrival)
- [x] A command string that would hit an unknown obstacle before reaching a known one is not refused; it bumps the unknown one
- [x] A command string that is only turns is never refused, even next to a known obstacle (regression; passed on arrival)
- [x] Refusal does not add anything to the discovered list (regression; passed on arrival)

## Odds and ends
- [x] An empty command string leaves the rover where it was (regression; passed on arrival)
- [x] Reports after a second command string reflect only that string's stop (a previous bump is not still reported)
