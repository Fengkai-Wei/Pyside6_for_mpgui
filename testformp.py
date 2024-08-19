import meep as mp
from meep.materials import Al
a = {'1':1,'2':2,'3':3}
new = a['2']
a.update({'4':new})
print(a)
a['2'] = -1
print(a)