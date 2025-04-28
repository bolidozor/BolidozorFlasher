# %%
from build123d import *
from ocp_vscode import *
import copy


multimaterial = True

bac_cap_screw_positions = [(55, 15, 0), (55, 120, 0), (180, 95, 0), (180, 145, 0)]


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

pbc = fa+fc


ps = offset(fa, 2) - offset(fa, -0.5)
ps = extrude(ps, amount=-30)

pb = extrude(pbc, amount=-2)
pb -= extrude(fb, amount=-2)
if multimaterial:
    pb += extrude(fb, amount=-0.6)
pb += extrude(fc, amount=-2)

pb += Pos(63, 63, -1) * Box(82+3, 82+3, 5, align=(Align.CENTER, Align.CENTER, Align.MAX))
for y in (-82/3, +82/3):
    for x in ((82+12)/2-3, -(82+12)/2+3):
        pb += Pos((x+63, y+63, 0)) * Cylinder(radius=5, height=19.5, align=(Align.CENTER, Align.CENTER, Align.MAX))
        pb -= Pos((x+63, y+63, -3)) * Cylinder(radius=2/2, height=20, align=(Align.CENTER, Align.CENTER, Align.MAX))

# Ramecek pro krabicku
pb -= Pos(63, 63, -3-1) * Box(82.2, 82.2, 20, align=(Align.CENTER, Align.CENTER, Align.MAX))
# Ramecek pro plexi
pb -= Pos(63, 63, -1) * Box(70.2, 70.2, 20, align=(Align.CENTER, Align.CENTER, Align.MAX))

pb += ps

# Vyztuzovaci pricka
pb += Pos(160-2, 65, -1)*Box(4, 80, 6, align=(Align.CENTER, Align.MIN, Align.MAX))
pb += Pos(160-2, 65+35, -1)*Box(80, 4, 6, align=(Align.CENTER, Align.MIN, Align.MAX))


# Pripevneni RP-PICO modulu do krabicky
rp_col = Cylinder(radius=3.8/2, height=10, align=(Align.CENTER, Align.CENTER, Align.MAX))
rp_col += Cylinder(radius=2.5,height=8, align=(Align.CENTER, Align.CENTER, Align.MAX))
rp_col -= Cylinder(radius=2/2, height=10, align=(Align.CENTER, Align.CENTER, Align.MAX))

col_set = Pos(11.4/2, 47/2, 0) * rp_col
col_set += Pos(-11.4/2, -47/2, 0) * rp_col
col_set += Pos(11.4/2, -47/2, 0) * rp_col
col_set += Pos(-11.4/2, 47/2, 0) * rp_col

col_set = Pos(100, 125, 0) * Rotation((0, 0, 90)) * col_set
pb += col_set


for loc in bac_cap_screw_positions:
    c = Cylinder(radius = 10/2, height=30, align=(Align.CENTER, Align.CENTER, Align.MAX))
    c -= Cylinder(radius = 3.3/2, height=30, align=(Align.CENTER, Align.CENTER, Align.MAX))
    c -= Pos(0,0,-(30-9))*Cylinder(radius = 4.1/2, height=30, align=(Align.CENTER, Align.CENTER, Align.MAX))

    pb += Pos(*loc) * c



light_thickness = 2

light = Pos(28+35, 28+35, 0) * Box(70, 70, light_thickness, align=(Align.CENTER, Align.CENTER, Align.MAX))
light -= scale(pb, (1,1,2 if multimaterial else 1))
light.label = "pruzor"
light.color = "white"


cover = Box(82, 82, 18, align=(Align.CENTER, Align.CENTER, Align.MIN))
cover -= Pos(0, 0, 2) * Box(80-2, 80-2, 18, align=(Align.CENTER, Align.CENTER, Align.MIN))

for y in (-82/3, +82/3):
    cover += Pos((0, y, 0)) * Box(83+12, 6, 2, align=(Align.CENTER, Align.CENTER, Align.MIN))
    for x in (-(82+12)/2+3, (82+12)/2-3):
        cover -= Pos((x, y, 0)) * Cylinder(radius=3/2, height=4, align=(Align.CENTER, Align.CENTER, Align.MIN))

# Otvory pro pripevneni LED svetel
for x in [-49/2, 49/2]:
    for y in [-51/2, 0, 51/2]:
        cover += Pos(x, y, 0) * Cylinder(radius=2.5, height=6, align=(Align.CENTER, Align.CENTER, Align.MIN))
        if y != 0:
            cover -= Pos(x, y, 0) * Cylinder(radius=1, height=20, align=(Align.CENTER, Align.CENTER, Align.MIN))

cover -= Cylinder(radius=2.5, height=2, align=(Align.CENTER, Align.CENTER, Align.MIN))
cover = Pos(28+35, 28+35, -20-2) * cover
cover.name = "cover"
cover.color = "gray"

printer = Box(160, 160, 100, align=(Align.MIN, Align.MIN, Align.CENTER))



printa = pb.intersect(Pos(-2, -3, 0)*printer)
printa.color = "black"
printa.label = "Bolidozor_case_part_a"

printb = pb.intersect(Pos(160-2, 50, 0)*printer)
printb.color = "black"
printb.label = "Bolidozor_case_part_b"

#show(cover, reset_camera=Camera.KEEP)
#show(printa, printb, light, cover, reset_camera=Camera.KEEP)

#print(pb)
show(pb, light, cover, reset_camera=Camera.KEEP)


# %% 

bc = fa
bca = offset(bc, -1)
bca = extrude(bca, amount=4)

bcb = offset(bc, 1)
bcb = extrude(bcb, amount=-1)

bcc = offset(bc, -5)
bcc = extrude(bcc, amount=-10)

bcd = offset(bc, -6)
bcd = extrude(bcd, amount=9, both=True)

bc = (bca + bcb + bcc) - bcd

for loc in bac_cap_screw_positions:
    bc += Pos((0, 0, -10)) * Pos(*loc) * Cylinder(radius = 11/2, height=10, align=(Align.CENTER, Align.CENTER, Align.MIN))
    bc -= Pos((0, 0, -10)) * Pos(*loc) * Cylinder(radius = 9/2, height=9, align=(Align.CENTER, Align.CENTER, Align.MIN))
    bc -= Pos((0, 0, -10)) * Pos(*loc) * Cylinder(radius = 3.3/2, height=10, align=(Align.CENTER, Align.CENTER, Align.MIN))

bc += Pos(160-2, 110, -5) * Box(4, 73, 5, align=(Align.CENTER, Align.CENTER, Align.MAX))
bc += Pos(110, 110, -5) * Box(150, 4, 5, align=(Align.CENTER, Align.CENTER, Align.MAX))
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

if not multimaterial:
    export_stl(printa, "outer_model_a.stl")
    export_stl(printb, "outer_model_b.stl")
    export_stl(light, "light_model.stl")
else:
    export_stl(pb, "multimaterial_outer_model.stl")
    export_stl(light, "multimaterial_light_model.stl")
export_stl(cover, "cover_model.stl")

if not multimaterial:
    export_stl(printba, "back_model_a.stl")
    export_stl(printbb, "back_model_b.stl")
else:
    export_stl(bc, "multimaterial_back_model.stl")


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