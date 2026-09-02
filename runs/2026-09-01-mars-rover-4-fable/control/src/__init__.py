"""Mars rover on a spherical grid that learns obstacles by bumping into them.

See TASK.md for the rules. Public API:

- ``Planet(width, height, obstacles)`` -- the grid and its fixed obstacles.
- ``Rover(planet, x, y, heading)`` -- executes command strings, remembers bumps.
- ``Report`` -- the result of one ``Rover.execute`` call.

Example::

    planet = Planet(width=10, height=10, obstacles=[(0, 2)])
    rover = Rover(planet, x=0, y=0, heading="N")
    report = rover.execute("FFF")      # bumps the unknown obstacle at (0, 2)
    report.position, report.blocked_by  # ((0, 1), (0, 2))
    rover.execute("FF").refused         # True: (0, 2) is known now
    rover.discovered_obstacles()        # [(0, 2)]
"""

from mars_rover.planet import HEADINGS, Planet, Position
from mars_rover.rover import Report, Rover

__all__ = ["HEADINGS", "Planet", "Position", "Report", "Rover"]
