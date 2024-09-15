# %%
from build123d import *
from ocp_vscode import *


ca = import_svg("crop_a.svg")
cb = import_svg("crop_b.svg")
cc = import_svg("crop_c.svg")

sc = 3

fa = ca.wires()
fa = make_face(fa).scale(sc)

fb = cb.wires()
fb = make_face(fb).scale(sc)

fc = cc.wires()
fc = make_face(fc).scale(sc)

pb = fa-fb+fc


ps = offset(fa, 2) - offset(fa, -0.5)
ps = extrude(ps, amount=-30)

pb = extrude(pb, amount=-2)
pb += Pos(63, 63, -3) * Box(82+3, 82+3, 2, align=(Align.CENTER, Align.CENTER, Align.MAX))
# Ramecek pro krabicku
pb -= Pos(63, 63, -3-1) * Box(82.2, 82.2, 1, align=(Align.CENTER, Align.CENTER, Align.MAX))
# Ramecek pro plexi
pb -= Pos(63, 63, -3) * Box(70.2, 70.2, 2, align=(Align.CENTER, Align.CENTER, Align.MAX))

pb += ps
pb += Pos(160-2, 65, -1)*Box(4, 80, 10, align=(Align.CENTER, Align.MIN, Align.MAX))

light = Pos(28+35, 28+35, 0) * Box(70, 70, 2+2, align=(Align.CENTER, Align.CENTER, Align.MAX))
light -= pb
light.label = "pruzor"
light.color = "white"


cover = Box(82, 82, 18, align=(Align.CENTER, Align.CENTER, Align.MIN))
cover += Pos(0, 0, 18-1)*Box(83, 83, 2, align=(Align.CENTER, Align.CENTER, Align.MIN))
cover -= Pos(0, 0, 2) * Box(80-2, 80-2, 18, align=(Align.CENTER, Align.CENTER, Align.MIN))
cover = Pos(28+35, 28+35, -20) * cover
cover.name = "cover"
cover.color = "gray"

printer = Box(160, 160, 100, align=(Align.MIN, Align.MIN, Align.CENTER))


printa = pb.intersect(Pos(-2, -3, 0)*printer)
printa.color = "black"
printa.label = "Bolidozor_case_part_a"

printb = pb.intersect(Pos(160-2, 50, 0)*printer)
printb.color = "black"
printb.label = "Bolidozor_case_part_b"

show(printa, printb, light, cover, reset_camera=Camera.KEEP)

# %%
export_stl(printa, "outer_model_a.stl")
export_stl(printb, "outer_model_b.stl")
export_stl(light, "light_model.stl")
export_stl(cover, "cover_model.stl")