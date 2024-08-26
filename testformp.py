import meep as mp
import numpy as np
a = mp.Vector3(3,4,5)
b = mp.Vector3(1,1,0)
c = np.array(a)*np.array([[1,1,0],
                        [0,1,1],
                        [1,0,1]])
d = [None]*5
print(d)