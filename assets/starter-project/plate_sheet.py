"""Create a model-derived engineering PDF with nominal dimensions only."""
from cad.eng_drawing import Sheet, eng_drawing

from plate import HOLE_DIAMETER, HOLE_PITCH, THICKNESS, plate


@eng_drawing(out="output/plate.pdf")
def plate_sheet():
    sheet = Sheet("A4", title="TWO-HOLE PLATE", projection="FIRST ANGLE", revision="A")
    part = plate().shape
    top, front, right = sheet.three_views(part)
    sheet.view(part, "iso", at=(245, 135), label="ISO 1:2", scale=0.5)
    top.overall()
    top.hole((-HOLE_PITCH / 2, 0, THICKNESS / 2), HOLE_DIAMETER, thru=True, count=2)
    front.overall()
    return sheet


if __name__ == "__main__":
    plate_sheet()
