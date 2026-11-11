"""Explicitly write the sample's STEP and cutting DXF."""
from pathlib import Path

from cad import export

from plate import plate
from plate_profile import plate_profile


if __name__ == "__main__":
    output = Path(__file__).resolve().parent / "output"
    output.mkdir(exist_ok=True)
    export(plate(), output / "plate.step")
    export(plate_profile(), output / "plate_profile.dxf")
