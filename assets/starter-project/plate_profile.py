"""Derive the cutting profile from the same plate geometry."""
from cad import flatten, model

from plate import THICKNESS, plate


@model
def plate_profile():
    return flatten.flat_pattern(plate().shape, coordinate=THICKNESS / 2)


if __name__ == "__main__":
    plate_profile()
