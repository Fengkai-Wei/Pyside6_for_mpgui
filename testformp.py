import meep as mp
from meep.materials import Al
a = mp.GeometricObject()
b= mp.Cylinder(radius = 0.5,height=0.5)
print(vars(a))
print(vars(b))