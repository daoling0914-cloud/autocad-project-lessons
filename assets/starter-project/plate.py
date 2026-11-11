"""Independent sample: a parameterized plate with two through holes, in mm."""
import math

import build123d as bd
from cad import model

WIDTH = 60.0
DEPTH = 40.0
THICKNESS = 6.0
HOLE_DIAMETER = 6.0
HOLE_PITCH = 30.0


@model
def plate():
    body = bd.Box(WIDTH, DEPTH, THICKNESS)
    for x in (-HOLE_PITCH / 2, HOLE_PITCH / 2):
        body = body - bd.Pos(x, 0, 0) * bd.Cylinder(HOLE_DIAMETER / 2, THICKNESS + 2)
    bounds = body.bounding_box().size
    assert body.is_valid and len(body.solids()) == 1
    assert all(abs(actual - expected) < 1e-6 for actual, expected in
               zip((bounds.X, bounds.Y, bounds.Z), (WIDTH, DEPTH, THICKNESS)))
    expected_volume = WIDTH * DEPTH * THICKNESS - 2 * math.pi * (HOLE_DIAMETER / 2) ** 2 * THICKNESS
    assert abs(body.volume - expected_volume) < 1e-5
    body.label = "two_hole_plate"
    return body


if __name__ == "__main__":
    plate()
