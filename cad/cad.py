# %%
from build123d import *
from ocp_vscode import *
import copy


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

pbc = fa-fb+fc


ps = offset(fa, 2) - offset(fa, -0.5)
ps = extrude(ps, amount=-30)

pb = extrude(pbc, amount=-2)
pb += Pos(63, 63, -1) * Box(82+3, 82+3, 4, align=(Align.CENTER, Align.CENTER, Align.MAX))
# Ramecek pro krabicku
pb -= Pos(63, 63, -3-1) * Box(82.2, 82.2, 1, align=(Align.CENTER, Align.CENTER, Align.MAX))
# Ramecek pro plexi
pb -= Pos(63, 63, -1) * Box(70.2, 70.2, 5, align=(Align.CENTER, Align.CENTER, Align.MAX))

pb += ps
pb += Pos(160-2, 65, -1)*Box(4, 80, 10, align=(Align.CENTER, Align.MIN, Align.MAX))


# Pripevneni RP-PICO modulu do krabicky
rp_col = Cylinder(radius=3.8/2, height=10, align=(Align.CENTER, Align.CENTER, Align.MAX))
rp_col += Cylinder(radius=2.5,height=8, align=(Align.CENTER, Align.CENTER, Align.MAX))
rp_col -= Cylinder(radius=2/2, height=10, align=(Align.CENTER, Align.CENTER, Align.MAX))

col_set = Pos(11.4/2, 48.26/2, 0) * rp_col
col_set += Pos(-11.4/2, -48.26/2, 0) * rp_col
col_set += Pos(11.4/2, -48.26/2, 0) * rp_col
col_set += Pos(-11.4/2, 48.26/2, 0) * rp_col

col_set = Pos(100, 125, 0) * Rotation((0, 0, 90)) * col_set
pb += col_set


light = Pos(28+35, 28+35, 0) * Box(70, 70, 2, align=(Align.CENTER, Align.CENTER, Align.MAX))
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

bc = fa
bca = offset(bc, -0.5)
bca = extrude(bca, amount=4)

bcb = offset(bc, 1)
bcb = extrude(bcb, amount=-1)

bcc = offset(bc, -5)
bcc = extrude(bcc, amount=-10)

bcd = offset(bc, -6)
bcd = extrude(bcd, amount=9, both=True)

bc = (bca + bcb + bcc) - bcd
bc += Pos(160-2, 110, -5) * Box(4, 73, 5, align=(Align.CENTER, Align.CENTER, Align.MAX))
bc = Pos(0, 0, -30) * bc
bc.color = "white"
bc.label = "Back cover"


printba = bc.intersect(Pos(-2, -3, 0)*printer)
printba.color = "white"
printba.label = "Bolidozor_back_part_a"

printbb = bc.intersect(Pos(160-2, 50, 0)*printer)
printbb.color = "white"
printbb.label = "Bolidozor_back_part_b"

show(printa, printb, light, cover, printba, printbb, reset_camera=Camera.KEEP)

# %%
export_stl(printa, "outer_model_a.stl")
export_stl(printb, "outer_model_b.stl")
export_stl(light, "light_model.stl")
export_stl(cover, "cover_model.stl")

export_stl(printba, "back_model_a.stl")
export_stl(printbb, "back_model_b.stl")


# %% 

text = import_svg("logo_text.svg")
charactes = []
legs = []

l = Pos(70, -20, -15) * Cylinder(radius=2.5, height=35, align=(Align.CENTER, Align.CENTER, Align.MIN), rotation=(-90, 0, 0))
l.color = "silver"
l.label = "leg - b"
legs.append(l)

for i, f in enumerate(text.faces()):
    f.wires()
    f = Pos((0, -25)) * f.scale(sc*1.9)
    f = extrude(f, amount=-15)
    bb = f.bounding_box()
    
    x_shift = 0
    if i == 9: x_shift = -8
    f -= Pos(bb.center().X+x_shift, bb.min.Y, -7.5) * Cylinder(radius=2.6, height=10, align=(Align.CENTER, Align.CENTER, Align.MIN), rotation=(-90, 0, 0))
    print(bb)
    f.label = f"text - {i}"
    f.color = "darkgray"

    charactes.append(f)

    l = Pos((bb.center().X+x_shift, -20, -7.5)) * Cylinder(radius=2.5, height=35, align=(Align.CENTER, Align.CENTER, Align.MIN), rotation=(-90, 0, 0))
    l.color = "silver"
    l.label = f"leg - {i}"
    legs.append(l)

    export_stl(f, f"Bolidozor_{i}.stl")


slap = Pos((-40, -20, -10)) * Box(700, 20, 100, align=(Align.MIN, Align.CENTER, Align.CENTER))
slap = chamfer(slap.edges().group_by(Axis.Y)[-1], 7)
slap.color = "brown"
slap.label = "slap"

show(slap, printa, printb, light, cover, printba, printbb, *charactes, *legs, reset_camera=Camera.KEEP)